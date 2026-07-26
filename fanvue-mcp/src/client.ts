/**
 * Minimal, dependency-free HTTP client for the Fanvue REST API.
 *
 * Implements the cross-cutting conventions documented at
 * https://api.fanvue.com/docs :
 *   - Bearer access-token auth
 *   - the required `X-Fanvue-API-Version` header
 *   - error-body normalisation across the API's several shapes
 *   - 429 rate-limit handling (honours Retry-After) and 502/503 retry with backoff
 *
 * Pagination is intentionally NOT abstracted away: list endpoints return the
 * raw `data` array alongside `nextCursor` (cursor style) or `pagination`
 * (page style), so the agent decides how far to page.
 */

import type { TokenProvider } from "./auth.js";

export interface FanvueClientConfig {
  /** Supplies (and refreshes) the OAuth 2.0 access token. */
  tokenProvider: TokenProvider;
  /** Date-string API version, e.g. "2025-06-26". */
  apiVersion: string;
  /** Base URL. Defaults to https://api.fanvue.com. */
  baseUrl?: string;
  /** Max automatic retries for 429/502/503. Defaults to 3. */
  maxRetries?: number;
}

export type QueryValue = string | number | boolean | undefined | null;
export type Query = Record<string, QueryValue>;

export interface RequestOptions {
  query?: Query;
  body?: unknown;
  /** Extra headers merged over the defaults (e.g. Idempotency-Key). */
  headers?: Record<string, string>;
}

/** Error thrown for any non-2xx Fanvue response, with the status + best-effort message. */
export class FanvueApiError extends Error {
  readonly status: number;
  readonly body: unknown;
  readonly nextVersion?: string;

  constructor(status: number, message: string, body: unknown, nextVersion?: string) {
    super(message);
    this.name = "FanvueApiError";
    this.status = status;
    this.body = body;
    this.nextVersion = nextVersion;
  }
}

const DEFAULT_BASE_URL = "https://api.fanvue.com";
const RETRYABLE_STATUS = new Set([429, 502, 503]);

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function buildQueryString(query?: Query): string {
  if (!query) return "";
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null || value === "") continue;
    params.append(key, String(value));
  }
  const s = params.toString();
  return s ? `?${s}` : "";
}

/**
 * Turn the API's several error body shapes into one readable message.
 * The docs describe: `{ error }`, `{ message }`, `{ errors: [...] }`,
 * and the 410 `{ error, message, nextVersion }`.
 */
function extractError(status: number, body: unknown): { message: string; nextVersion?: string } {
  if (body && typeof body === "object") {
    const b = body as Record<string, unknown>;
    if (Array.isArray(b.errors) && b.errors.length > 0) {
      return { message: `Validation failed: ${b.errors.map(String).join("; ")}` };
    }
    const parts: string[] = [];
    if (typeof b.error === "string") parts.push(b.error);
    if (typeof b.message === "string" && b.message !== b.error) parts.push(b.message);
    const nextVersion = typeof b.nextVersion === "string" ? b.nextVersion : undefined;
    if (parts.length > 0) return { message: parts.join(" — "), nextVersion };
  }
  if (typeof body === "string" && body.trim()) {
    return { message: body.trim() };
  }
  return { message: `Fanvue API request failed with HTTP ${status}.` };
}

/** Map a status code to an actionable hint appended to the thrown error message. */
function statusHint(status: number, nextVersion?: string): string {
  switch (status) {
    case 400:
      return "Check the request parameters and the X-Fanvue-API-Version header.";
    case 401:
      return "The access token is missing, invalid or expired — refresh it via the OAuth flow.";
    case 403:
      return "The token lacks the scope for this resource (e.g. write:media). Re-authorise with the needed scope.";
    case 404:
      return "The resource or a referenced UUID does not exist.";
    case 409:
      return "A uniquely named resource already exists — choose a different name.";
    case 410:
      return nextVersion
        ? `This API version has been sunset. Set FANVUE_API_VERSION to "${nextVersion}".`
        : "This API version has been sunset — upgrade to a newer version.";
    case 429:
      return "Rate limit exceeded (100 req / 60 s). Back off before retrying.";
    default:
      return "";
  }
}

export class FanvueClient {
  private readonly tokenProvider: TokenProvider;
  private readonly apiVersion: string;
  private readonly baseUrl: string;
  private readonly maxRetries: number;

  constructor(config: FanvueClientConfig) {
    if (!config.tokenProvider) throw new Error("FanvueClient requires a tokenProvider.");
    if (!config.apiVersion) throw new Error("FanvueClient requires an apiVersion.");
    this.tokenProvider = config.tokenProvider;
    this.apiVersion = config.apiVersion;
    this.baseUrl = (config.baseUrl ?? DEFAULT_BASE_URL).replace(/\/+$/, "");
    this.maxRetries = config.maxRetries ?? 3;
  }

  async request<T = unknown>(
    method: string,
    path: string,
    options: RequestOptions = {},
  ): Promise<T> {
    const normalizedPath = path.startsWith("/") ? path : `/${path}`;
    const url = `${this.baseUrl}${normalizedPath}${buildQueryString(options.query)}`;

    let payload: string | undefined;
    if (options.body !== undefined && method !== "GET" && method !== "HEAD") {
      payload = JSON.stringify(options.body);
    }

    let attempt = 0;
    let refreshedAfter401 = false;
    // Retry loop for 429/502/503 (and a single refresh-and-retry on 401).
    // Other errors throw immediately.
    // eslint-disable-next-line no-constant-condition
    while (true) {
      const token = await this.tokenProvider.getToken();
      const headers: Record<string, string> = {
        Authorization: `Bearer ${token}`,
        "X-Fanvue-API-Version": this.apiVersion,
        Accept: "application/json",
        ...(payload !== undefined ? { "Content-Type": "application/json" } : {}),
        ...options.headers,
      };

      const response = await fetch(url, { method, headers, body: payload });

      if (response.ok) {
        if (response.status === 204) return undefined as T;
        const text = await response.text();
        if (!text) return undefined as T;
        try {
          return JSON.parse(text) as T;
        } catch {
          return text as unknown as T;
        }
      }

      // Parse error body (JSON if possible, else raw text).
      const raw = await response.text();
      let parsed: unknown = raw;
      try {
        parsed = raw ? JSON.parse(raw) : undefined;
      } catch {
        /* keep raw string */
      }

      // On 401, try a single token refresh (if the provider can) then retry once.
      if (response.status === 401 && this.tokenProvider.canRefresh && !refreshedAfter401) {
        refreshedAfter401 = true;
        this.tokenProvider.invalidate();
        continue;
      }

      if (RETRYABLE_STATUS.has(response.status) && attempt < this.maxRetries) {
        attempt += 1;
        const retryAfter = Number(response.headers.get("Retry-After"));
        const waitMs = Number.isFinite(retryAfter) && retryAfter > 0
          ? retryAfter * 1000
          : Math.min(1000 * 2 ** (attempt - 1), 8000); // 1s, 2s, 4s, capped 8s
        await sleep(waitMs);
        continue;
      }

      const { message, nextVersion } = extractError(response.status, parsed);
      const hint = statusHint(response.status, nextVersion);
      throw new FanvueApiError(
        response.status,
        hint ? `${message} (${hint})` : message,
        parsed,
        nextVersion,
      );
    }
  }

  get<T = unknown>(path: string, query?: Query): Promise<T> {
    return this.request<T>("GET", path, { query });
  }

  post<T = unknown>(path: string, body?: unknown, headers?: Record<string, string>): Promise<T> {
    return this.request<T>("POST", path, { body, headers });
  }
}

#!/usr/bin/env node
/**
 * Fanvue MCP server (single-creator).
 *
 * Exposes the Fanvue REST API to MCP clients over stdio. Configure via env:
 *   FANVUE_ACCESS_TOKEN   (required)  OAuth 2.0 access token
 *   FANVUE_API_VERSION    (optional)  defaults to 2025-06-26
 *   FANVUE_BASE_URL       (optional)  defaults to https://api.fanvue.com
 *
 * Tools cover the documented single-creator surfaces (insights, chats, media
 * grant) plus a generic `fanvue_request` escape hatch so every endpoint in the
 * OpenAPI spec is reachable. Swap in typed tools per endpoint once the full
 * spec at /openapi.json is available.
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { FanvueClient, FanvueApiError } from "./client.js";
import { RefreshTokenProvider, StaticTokenProvider, type TokenProvider } from "./auth.js";

const DEFAULT_API_VERSION = "2025-06-26";
const DEFAULT_ISSUER = "https://auth.fanvue.com";

let cachedClient: FanvueClient | undefined;

/**
 * Build a token provider from the environment. Prefers OAuth auto-refresh
 * (client id/secret + refresh token) and falls back to a static access token.
 */
function buildTokenProvider(): TokenProvider {
  const clientId = process.env.FANVUE_OAUTH_CLIENT_ID;
  const clientSecret = process.env.FANVUE_OAUTH_CLIENT_SECRET;
  const refreshToken = process.env.FANVUE_OAUTH_REFRESH_TOKEN;
  if (clientId && clientSecret && refreshToken) {
    return new RefreshTokenProvider({
      issuerBaseUrl: process.env.FANVUE_OAUTH_ISSUER_BASE_URL || DEFAULT_ISSUER,
      clientId,
      clientSecret,
      refreshToken,
    });
  }

  const staticToken = process.env.FANVUE_ACCESS_TOKEN;
  if (staticToken) {
    return new StaticTokenProvider(staticToken);
  }

  throw new Error(
    "No Fanvue credentials found. Set FANVUE_OAUTH_CLIENT_ID, FANVUE_OAUTH_CLIENT_SECRET and " +
      "FANVUE_OAUTH_REFRESH_TOKEN for automatic token refresh (recommended), or FANVUE_ACCESS_TOKEN " +
      "for a static access token. See the README for how to obtain these.",
  );
}

function getClient(): FanvueClient {
  if (cachedClient) return cachedClient;
  cachedClient = new FanvueClient({
    tokenProvider: buildTokenProvider(),
    apiVersion: process.env.FANVUE_API_VERSION || DEFAULT_API_VERSION,
    baseUrl: process.env.FANVUE_BASE_URL || undefined,
  });
  return cachedClient;
}

type ToolResult = {
  content: { type: "text"; text: string }[];
  structuredContent?: Record<string, unknown>;
  isError?: boolean;
};

/** Run an API call and wrap the result (or a clean error) in an MCP tool result. */
async function run(fn: (client: FanvueClient) => Promise<unknown>): Promise<ToolResult> {
  try {
    const data = await fn(getClient());
    const structured =
      data && typeof data === "object" && !Array.isArray(data)
        ? (data as Record<string, unknown>)
        : { result: data };
    return {
      content: [{ type: "text", text: JSON.stringify(data, null, 2) }],
      structuredContent: structured,
    };
  } catch (err) {
    let message: string;
    if (err instanceof FanvueApiError) {
      message = `Fanvue API error (HTTP ${err.status}): ${err.message}`;
    } else if (err instanceof Error) {
      message = err.message;
    } else {
      message = String(err);
    }
    return { content: [{ type: "text", text: message }], isError: true };
  }
}

const server = new McpServer({ name: "fanvue-mcp", version: "0.1.0" });

// Shared query fields.
const cursorSize = {
  size: z
    .number()
    .int()
    .min(1)
    .max(50)
    .optional()
    .describe("Items per page, 1-50 (default varies by endpoint, often 20)."),
  cursor: z
    .string()
    .optional()
    .describe("Opaque cursor from the previous response's `nextCursor`. Omit for the first page."),
  startDate: z
    .string()
    .optional()
    .describe("ISO 8601 datetime lower bound (UTC), e.g. 2025-05-01T00:00:00Z."),
  endDate: z
    .string()
    .optional()
    .describe("ISO 8601 datetime upper bound (UTC)."),
};

// ── Insights (cursor pagination) ────────────────────────────────────────────
server.registerTool(
  "fanvue_get_insights_earnings",
  {
    title: "Get earnings insights",
    description:
      "List earnings rows (subscriptions, tips, etc.) for the authenticated creator. " +
      "Cursor-paginated: read `data`, then pass `nextCursor` as `cursor` until it is null. " +
      "Amounts are in minor currency units (e.g. cents).",
    inputSchema: cursorSize,
    annotations: { readOnlyHint: true, openWorldHint: true },
  },
  async ({ size, cursor, startDate, endDate }) =>
    run((c) => c.get("/insights/earnings", { size, cursor, startDate, endDate })),
);

server.registerTool(
  "fanvue_get_insights_spending",
  {
    title: "Get spending insights",
    description:
      "List spending rows for the authenticated creator. Cursor-paginated: read `data`, " +
      "then pass `nextCursor` as `cursor` until it is null.",
    inputSchema: cursorSize,
    annotations: { readOnlyHint: true, openWorldHint: true },
  },
  async ({ size, cursor, startDate, endDate }) =>
    run((c) => c.get("/insights/spending", { size, cursor, startDate, endDate })),
);

server.registerTool(
  "fanvue_get_insights_subscribers",
  {
    title: "Get subscriber insights",
    description:
      "List subscriber insight rows for the authenticated creator. Cursor-paginated: read " +
      "`data`, then pass `nextCursor` as `cursor` until it is null.",
    inputSchema: cursorSize,
    annotations: { readOnlyHint: true, openWorldHint: true },
  },
  async ({ size, cursor, startDate, endDate }) =>
    run((c) => c.get("/insights/subscribers", { size, cursor, startDate, endDate })),
);

// ── Chats (page pagination) ─────────────────────────────────────────────────
server.registerTool(
  "fanvue_list_chats",
  {
    title: "List chats",
    description:
      "List the creator's chats. Page-paginated: pass `page` (1-based) and `size`; the response " +
      "includes a `pagination` object with `hasMore`. Keep incrementing `page` while `hasMore` is true.",
    inputSchema: {
      page: z.number().int().min(1).optional().describe("1-based page number (default 1)."),
      size: z.number().int().min(1).max(50).optional().describe("Items per page, 1-50 (default 15)."),
    },
    annotations: { readOnlyHint: true, openWorldHint: true },
  },
  async ({ page, size }) => run((c) => c.get("/chats", { page, size })),
);

// ── Media grant (idempotent write) ──────────────────────────────────────────
server.registerTool(
  "fanvue_grant_media",
  {
    title: "Grant media access",
    description:
      "Grant a consumer access to a media item. Idempotent on (source, sourceRef): repeated calls " +
      "return the existing entitlement instead of creating a duplicate. Requires the write:media scope.",
    inputSchema: {
      uuid: z.string().describe("UUID of the media item to grant."),
      consumerId: z.string().describe("UUID of the consumer to grant access to."),
      source: z
        .string()
        .regex(/^[a-z0-9_]+$/, "Lowercase letters, digits and underscores only.")
        .max(100)
        .describe("Granting application/reason, e.g. spin_the_wheel_reward."),
      sourceRef: z
        .string()
        .max(255)
        .describe("Unique reference within `source` — the idempotency key (e.g. an attempt UUID)."),
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: true },
  },
  async ({ uuid, consumerId, source, sourceRef }) =>
    run((c) => c.post(`/media/${encodeURIComponent(uuid)}/grant`, { consumerId, source, sourceRef })),
);

// ── Generic escape hatch (full API coverage) ────────────────────────────────
server.registerTool(
  "fanvue_request",
  {
    title: "Call any Fanvue endpoint",
    description:
      "Low-level access to any Fanvue endpoint not covered by a dedicated tool (lists, mass messages, " +
      "tracking links, media, users, agency endpoints, etc.). Auth and the version header are added " +
      "automatically. Use a dedicated tool when one exists. Only use non-GET methods when you intend to " +
      "modify data.",
    inputSchema: {
      method: z
        .enum(["GET", "POST", "PATCH", "PUT", "DELETE"])
        .describe("HTTP method. Non-GET methods modify data — use deliberately."),
      path: z
        .string()
        .describe("Path beginning with '/', e.g. /lists or /media/{uuid}/grant. Do not include the host."),
      query: z
        .record(z.string(), z.union([z.string(), z.number(), z.boolean()]))
        .optional()
        .describe("Query parameters as key/value pairs."),
      body: z.any().optional().describe("JSON request body for non-GET methods."),
    },
    annotations: { openWorldHint: true },
  },
  async ({ method, path, query, body }) =>
    run((c) => c.request(method, path, { query, body })),
);

async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  // Log to stderr so we don't corrupt the stdio JSON-RPC stream on stdout.
  process.stderr.write("fanvue-mcp server running on stdio\n");
}

main().catch((err) => {
  process.stderr.write(`Fatal: ${err instanceof Error ? err.stack ?? err.message : String(err)}\n`);
  process.exit(1);
});

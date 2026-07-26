/**
 * Token providers for the Fanvue MCP server.
 *
 * Two modes:
 *   - StaticTokenProvider: you supply a ready access token (it will expire).
 *   - RefreshTokenProvider: you supply OAuth client credentials + a refresh
 *     token; the provider discovers the issuer's token endpoint via OIDC
 *     (.well-known/openid-configuration) and mints/refreshes access tokens
 *     automatically, caching until shortly before expiry.
 *
 * Fanvue's OAuth issuer is https://auth.fanvue.com and the `offline_access`
 * scope yields the refresh token used here.
 */

export interface TokenProvider {
  /** Return a currently-valid access token, refreshing if necessary. */
  getToken(): Promise<string>;
  /** Drop any cached token so the next getToken() re-fetches (call after a 401). */
  invalidate(): void;
  /** Whether this provider can obtain a new token on its own (i.e. supports refresh). */
  readonly canRefresh: boolean;
}

export class StaticTokenProvider implements TokenProvider {
  readonly canRefresh = false;
  constructor(private readonly token: string) {}
  async getToken(): Promise<string> {
    return this.token;
  }
  invalidate(): void {
    /* nothing to invalidate for a static token */
  }
}

export interface OAuthConfig {
  /** e.g. https://auth.fanvue.com */
  issuerBaseUrl: string;
  clientId: string;
  clientSecret: string;
  refreshToken: string;
}

interface TokenResponse {
  access_token?: string;
  expires_in?: number;
  refresh_token?: string;
}

const EXPIRY_SKEW_MS = 60_000; // refresh a minute before the token actually expires

export class RefreshTokenProvider implements TokenProvider {
  readonly canRefresh = true;
  private accessToken?: string;
  private expiresAt = 0;
  private tokenEndpoint?: string;
  private refreshToken: string;

  constructor(private readonly cfg: OAuthConfig) {
    if (!cfg.issuerBaseUrl) throw new Error("OAuth issuerBaseUrl is required.");
    if (!cfg.clientId || !cfg.clientSecret) throw new Error("OAuth clientId and clientSecret are required.");
    if (!cfg.refreshToken) throw new Error("OAuth refreshToken is required.");
    this.refreshToken = cfg.refreshToken;
  }

  invalidate(): void {
    this.accessToken = undefined;
    this.expiresAt = 0;
  }

  private async discoverTokenEndpoint(): Promise<string> {
    if (this.tokenEndpoint) return this.tokenEndpoint;
    const base = this.cfg.issuerBaseUrl.replace(/\/+$/, "");
    const url = `${base}/.well-known/openid-configuration`;
    const res = await fetch(url, { headers: { Accept: "application/json" } });
    if (!res.ok) {
      throw new Error(`OIDC discovery failed (HTTP ${res.status}) at ${url}.`);
    }
    const doc = (await res.json()) as { token_endpoint?: string };
    if (!doc.token_endpoint) {
      throw new Error(`OIDC discovery at ${url} did not include a token_endpoint.`);
    }
    this.tokenEndpoint = doc.token_endpoint;
    return this.tokenEndpoint;
  }

  async getToken(): Promise<string> {
    const now = Date.now();
    if (this.accessToken && now < this.expiresAt - EXPIRY_SKEW_MS) {
      return this.accessToken;
    }

    const tokenEndpoint = await this.discoverTokenEndpoint();
    const body = new URLSearchParams({
      grant_type: "refresh_token",
      refresh_token: this.refreshToken,
      client_id: this.cfg.clientId,
      client_secret: this.cfg.clientSecret,
    });

    const res = await fetch(tokenEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Accept: "application/json",
      },
      body,
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(
        `OAuth token refresh failed (HTTP ${res.status}) at ${tokenEndpoint}: ${text.slice(0, 300)}. ` +
          "Check FANVUE_OAUTH_CLIENT_ID/SECRET and that the refresh token is still valid.",
      );
    }

    const tok = (await res.json()) as TokenResponse;
    if (!tok.access_token) {
      throw new Error("OAuth token response did not include an access_token.");
    }
    this.accessToken = tok.access_token;
    this.expiresAt = now + (tok.expires_in ? tok.expires_in * 1000 : 3_600_000);
    // Some issuers rotate the refresh token on each use; adopt the new one if present.
    if (tok.refresh_token) this.refreshToken = tok.refresh_token;
    return this.accessToken;
  }
}

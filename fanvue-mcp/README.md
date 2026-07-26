# Fanvue MCP server

A [Model Context Protocol](https://modelcontextprotocol.io) server that wraps the
[Fanvue REST API](https://api.fanvue.com/docs) so an MCP client (Claude, etc.) can read
insights, browse chats, and grant media access for a **single creator** account.

It implements the API's shared conventions for you: Bearer auth, the required
`X-Fanvue-API-Version` header, both pagination styles, normalised error messages, and
automatic retry on rate limits (`429`, honouring `Retry-After`) and transient `502/503`.

> **Why a self-hosted server?** Fanvue isn't a prebuilt Zapier or Claude connector, and its
> API requires an OAuth 2.0 token that must be authorised in a browser. This server is the
> bridge: you run it where it has network access to `api.fanvue.com`, complete the OAuth step
> once, and point your MCP client at it.

## Tools

| Tool | Method | Notes |
| --- | --- | --- |
| `fanvue_get_insights_earnings` | GET `/insights/earnings` | Cursor-paginated. Amounts in minor units. |
| `fanvue_get_insights_spending` | GET `/insights/spending` | Cursor-paginated. |
| `fanvue_get_insights_subscribers` | GET `/insights/subscribers` | Cursor-paginated. |
| `fanvue_list_chats` | GET `/chats` | Page-paginated (`page`/`size`, `hasMore`). |
| `fanvue_grant_media` | POST `/media/{uuid}/grant` | Idempotent on `(source, sourceRef)`. Needs `write:media`. |
| `fanvue_request` | any | Escape hatch — call **any** endpoint (lists, mass messages, tracking links, media, users…). |

The dedicated tools cover the documented single-creator surfaces; `fanvue_request` reaches
everything else. Once you feed the full spec at `https://api.fanvue.com/openapi.json` into a
generator (or back to Claude), each endpoint can get its own typed tool.

## Prerequisites

- Node.js ≥ 18 (uses the built-in `fetch`).
- A Fanvue account with API access, and an OAuth application (below).

## 1. Get OAuth credentials (one-time, in your browser)

The API uses OAuth 2.0 (issuer `https://auth.fanvue.com`) — there is no static API key. You
need a **creator account with KYC completed** to access the Developer area.

1. In the Fanvue Developer area, **register an app** to get a **client ID**, **client secret**,
   and set a **redirect URI** you control.
2. Select the **scopes** you need: read scopes for insights/chats, `write:media` for
   `fanvue_grant_media`, and **`offline_access`** so you receive a **refresh token**.
3. Complete the authorization-code flow once to obtain a **refresh token**. The quickest way is
   the official [Fanvue App Starter](https://github.com/fanvue/fanvue-app-starter) (Next.js) —
   run its "Login with Fanvue" flow, then read the refresh token from the session. Any OAuth
   client you trust works.

This server supports two auth modes:

- **Auto-refresh (recommended):** give it `FANVUE_OAUTH_CLIENT_ID`, `FANVUE_OAUTH_CLIENT_SECRET`
  and `FANVUE_OAUTH_REFRESH_TOKEN`. It discovers the token endpoint via OIDC and mints fresh
  access tokens automatically, including a one-shot refresh-and-retry on `401`.
- **Static token:** give it `FANVUE_ACCESS_TOKEN`. Simpler, but it expires and you must update
  it by hand.

> Keep all secrets out of version control (`.env` is gitignored).

## 2. Install and build

```bash
cd fanvue-mcp
npm install
npm run build
```

## 3. Configure

```bash
cp .env.example .env
# then edit .env and set FANVUE_ACCESS_TOKEN
```

Provide **either** the OAuth trio (recommended) **or** a static token:

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `FANVUE_OAUTH_CLIENT_ID` | OAuth mode | — | App client ID. |
| `FANVUE_OAUTH_CLIENT_SECRET` | OAuth mode | — | App client secret. |
| `FANVUE_OAUTH_REFRESH_TOKEN` | OAuth mode | — | Refresh token (needs `offline_access`). |
| `FANVUE_OAUTH_ISSUER_BASE_URL` | | `https://auth.fanvue.com` | OAuth issuer for OIDC discovery. |
| `FANVUE_ACCESS_TOKEN` | static mode | — | Static access token (used only if the OAuth trio isn't set). |
| `FANVUE_API_VERSION` | | `2025-06-26` | Pin the API version. A `410` error tells you the next version. |
| `FANVUE_BASE_URL` | | `https://api.fanvue.com` | Override the base URL. |

## 4. Run / register with an MCP client

The server speaks MCP over **stdio**. Register it in your client's MCP config, for example:

```jsonc
{
  "mcpServers": {
    "fanvue": {
      "command": "node",
      "args": ["/absolute/path/to/fanvue-mcp/dist/index.js"],
      "env": {
        "FANVUE_OAUTH_CLIENT_ID": "your-client-id",
        "FANVUE_OAUTH_CLIENT_SECRET": "your-client-secret",
        "FANVUE_OAUTH_REFRESH_TOKEN": "your-refresh-token",
        "FANVUE_API_VERSION": "2025-06-26"
      }
    }
  }
}
```

To try it interactively without a client:

```bash
FANVUE_ACCESS_TOKEN=your-token npx @modelcontextprotocol/inspector node dist/index.js
```

## Notes & limitations

- **Single-creator scope.** Agency `/agencies/*` endpoints aren't wired as dedicated tools;
  reach them through `fanvue_request` if your token is agency-scoped.
- **Pagination is explicit.** List tools return the raw `data` plus `nextCursor` / `pagination`
  so the agent controls how far to page.
- **Amounts** are integer minor units (e.g. cents); divide by 100 for display.
- **Rate limit** is 100 requests / 60 s; the client backs off and retries automatically.
- Built from Fanvue's published API conventions. Endpoint paths beyond those in the table
  above should be confirmed against `https://api.fanvue.com/openapi.json`.

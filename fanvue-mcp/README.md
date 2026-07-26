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

## 1. Get an access token (one-time, in your browser)

The API uses OAuth 2.0 — there is no static API key. Follow the
[Authentication guide](https://api.fanvue.com/docs/authentication/overview):

1. Register an OAuth application in your Fanvue developer settings. Note the **client ID**,
   **client secret**, and set a **redirect URI** you control.
2. Request the scopes you need. For the tools above: read scopes for insights/chats, and
   `write:media` for `fanvue_grant_media`.
3. Complete the authorization-code flow to obtain an **access token** (and refresh token).
   A token from any OAuth client you trust works — the server only needs the access token.

> Keep tokens secret. Never commit them. Access tokens expire — refresh and update the env
> var when they do (a `401` from any tool means the token needs refreshing).

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

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `FANVUE_ACCESS_TOKEN` | ✅ | — | OAuth 2.0 access token. |
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
        "FANVUE_ACCESS_TOKEN": "your-access-token",
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

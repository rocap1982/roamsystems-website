---
name: deploy-app
description: >
  Deploy, manage, and troubleshoot the Roam Systems website on Railway. Use when deploying code,
  checking deployment status, viewing logs, managing environment variables, configuring domains,
  or troubleshooting production issues. Also use when the user mentions Railway, deployment,
  production, hosting, or domain setup. The Railway MCP server is available with CLI tools.
---

# Deploy App (Railway)

## Infrastructure overview

- **Platform**: Railway (Pro plan, us-east4 region)
- **Project**: "Roam systems website" — 1 service: `roamsystems-website`
- **Source**: GitHub `rocap1982/roamsystems-website`, branch `main` (auto-deploy on push)
- **Build**: Railpack (Node provider) — detects Astro, builds static, serves via Caddy
- **Domain**: `roamsystems.co.uk` (custom domain via Cloudflare)
- **DNS**: Cloudflare (proxied) — CNAME to `ltrgyo93.up.railway.app`

## Railway MCP tools

Use the Railway MCP for all operations. The workspace path is always the repo root.

### Common operations

**Check status:**
```
mcp__Railway__check-railway-status
mcp__Railway__list-services (workspacePath)
mcp__Railway__list-deployments (workspacePath, limit, json: true)
```

**Deploy:**
```
mcp__Railway__deploy (workspacePath)
```
Note: Pushes to `main` auto-deploy. Manual deploy only needed for local changes.

**View logs:**
```
mcp__Railway__get-logs (workspacePath, logType: "build" | "deploy")
mcp__Railway__get-logs (workspacePath, logType: "deploy", filter: "@level:error")
```

**Environment variables:**
```
mcp__Railway__list-variables (workspacePath)
mcp__Railway__set-variables (workspacePath, variables: ["KEY=value"])
```

**Service linking (if CLI loses context):**
```
mcp__Railway__link-service (workspacePath, serviceName: "roamsystems-website")
mcp__Railway__link-environment (workspacePath, environmentName: "production")
```

### What Railway MCP cannot do

These require the browser (Cloudflare dashboard or Railway UI):
- Adding/removing **custom domains** on Railway
- Managing **Cloudflare DNS records**
- Changing **SSL/TLS settings** in Cloudflare
- Deleting services (use Railway dashboard)

## Deployment workflow

1. Confirm target (this project only has `production`)
2. Run build locally to catch errors: `npm run build`
3. Commit and push to `main` — Railway auto-deploys
4. Monitor with `get-logs` (logType: "build") until build succeeds
5. Verify with `get-logs` (logType: "deploy") — check for runtime errors
6. Test the live site at `roamsystems.co.uk`

## Domain & DNS setup (reference)

### Cloudflare DNS records for Railway

| Type | Name | Value | Proxy |
|------|------|-------|-------|
| CNAME | @ | ltrgyo93.up.railway.app | Proxied |
| CNAME | www | ltrgyo93.up.railway.app | Proxied |
| TXT | _railway-verify | railway-verify=1c5841765c21d67bbd58d0226299a68c9093a7e6dae49ddeb89fcf1c465d9d7b | DNS only |

### Email records (do not touch)

| Type | Name | Value |
|------|------|-------|
| A | mail | 92.205.12.83 |
| MX | @ | mail.roamsystems.co.uk (priority 0) |
| TXT | @ | v=spf1 include:secureserv... |

### Cloudflare settings

- SSL/TLS: **Full (Strict)** — Railway provides valid SSL certs

## Troubleshooting

**Build fails:** Check `get-logs` with logType `build`. Common causes: missing deps, Node version mismatch (requires >=22.12.0).

**Site down but deployment succeeded:** Check deploy logs for runtime errors. Verify Cloudflare DNS is still pointing to Railway. Check if Cloudflare SSL mode is correct (must be Full or Full Strict).

**Domain not resolving:** Verify `_railway-verify` TXT record exists. Check Railway custom domain status in the UI — it should say "Active" not "Waiting for DNS".

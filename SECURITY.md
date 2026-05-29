# Security Policy

## Reporting

Report security issues privately via
[GitHub Security Advisories](https://github.com/therudywolf/Furry-Translater/security/advisories/new).
Please do not open public issues for vulnerabilities.

## Secrets

- The LLM API key lives only in `.env` (copied from `.env.example`) and is
  injected into upstream requests **server-side** by the nginx proxy. It must
  never be committed and never ships in the browser bundle.
- `Web/config.js` (local API settings) is gitignored. Only `config.js.example`
  is committed.
- Do not commit the Python GUI's `settings.json` / `history.json`.
- Secret scanning runs in CI (gitleaks) and as a pre-commit hook; see
  [`.gitleaks.toml`](.gitleaks.toml) and [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

## Deployment notes

- Prefer the reverse-proxy deployment (`docker compose up`) so the API key
  stays out of client code. Direct-from-browser mode (`config.js` with
  `API_KEY`) exposes the key to every visitor — use it for local testing only.
- AGPL-3.0-or-later applies: if you run a modified version as a network
  service, publish your changes.

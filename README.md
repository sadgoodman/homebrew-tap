# homebrew-tap

Homebrew formulae for [sadgoodman](https://github.com/sadgoodman)'s tools.

## Install

```sh
brew install sadgoodman/tap/cli-proxy
```

## Formulae

| Formula | Description |
|---|---|
| [`cli-proxy`](Formula/cli-proxy.rb) | Lightweight HTTP/HTTPS intercepting proxy with a terminal UI |

## How the formulae stay current

Each formula is generated from the corresponding upstream release by
[`scripts/update_formula.py`](scripts/update_formula.py), which reads the
release's `checksums.txt` and rewrites the URLs and SHA-256 values. The
[Update formulae](.github/workflows/update.yml) workflow runs it hourly, and can
be started by hand from the Actions tab when you do not want to wait.

Nothing is shared between this repository and the upstream ones — no personal
access token, nothing that can expire.

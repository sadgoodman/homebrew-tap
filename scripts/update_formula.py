#!/usr/bin/env python3
"""Regenerate Formula/cli-proxy.rb from the latest upstream release.

Reads the release metadata and checksums.txt from the GitHub API, then rewrites
the formula in place. Exits 0 either way: the caller decides whether anything
changed by looking at git.
"""

import json
import os
import re
import sys
import urllib.request

UPSTREAM = os.environ.get("UPSTREAM_REPO", "sadgoodman/cli-proxy")
OUTPUT = sys.argv[1] if len(sys.argv) > 1 else "Formula/cli-proxy.rb"
API = f"https://api.github.com/repos/{UPSTREAM}"

# (goos, goarch) -> the section of the formula it belongs to.
TARGETS = {
    ("darwin", "amd64"): ("macos", "intel"),
    ("darwin", "arm64"): ("macos", "arm"),
    ("linux", "amd64"): ("linux", "intel"),
    ("linux", "arm64"): ("linux", "arm"),
}


def get(url):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "homebrew-tap-updater",
            **(
                {"Authorization": f"Bearer {os.environ['GH_TOKEN']}"}
                if os.environ.get("GH_TOKEN")
                else {}
            ),
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def latest_release():
    release = json.loads(get(f"{API}/releases/latest"))
    if release.get("draft") or release.get("prerelease"):
        raise SystemExit("the latest release is a draft or prerelease; nothing to do")
    return release


def checksums(release):
    asset = next(
        (a for a in release["assets"] if a["name"] == "checksums.txt"), None
    )
    if asset is None:
        raise SystemExit("checksums.txt is missing from the release")
    text = get(asset["browser_download_url"]).decode()
    sums = {}
    for line in text.splitlines():
        match = re.match(r"^([0-9a-f]{64})\s+\*?(.+)$", line.strip())
        if match:
            sums[match.group(2)] = match.group(1)
    return sums


def render(release, sums):
    version = release["tag_name"].lstrip("v")
    assets = {a["name"]: a["browser_download_url"] for a in release["assets"]}

    blocks = {}
    for (goos, goarch), (os_name, cpu) in TARGETS.items():
        name = f"cli-proxy_{version}_{goos}_{goarch}.tar.gz"
        if name not in assets:
            raise SystemExit(f"the release is missing {name}")
        blocks.setdefault(os_name, []).append(
            (cpu, assets[name], sums.get(name, ""))
        )

    lines = [
        "class CliProxy < Formula",
        '  desc "Lightweight HTTP/HTTPS intercepting proxy with a terminal UI"',
        f'  homepage "https://github.com/{UPSTREAM}"',
        '  license "MIT"',
        "",
    ]
    for os_name in ("macos", "linux"):
        lines.append(f"  on_{os_name} do")
        for cpu, url, sha in blocks[os_name]:
            lines.append(f"    if Hardware::CPU.{cpu}?")
            lines.append(f'      url "{url}"')
            lines.append(f'      sha256 "{sha}"')
            lines.append("    end")
        lines.append("  end")
        lines.append("")
    lines += [
        "  def install",
        '    bin.install "cli-proxy"',
        "  end",
        "",
        "  test do",
        '    assert_match "cli-proxy", shell_output("#{bin}/cli-proxy -version")',
        "  end",
        "end",
        "",
    ]
    return "\n".join(lines)


def main():
    release = latest_release()
    formula = render(release, checksums(release))
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    previous = open(OUTPUT).read() if os.path.exists(OUTPUT) else ""
    if previous == formula:
        print(f"{OUTPUT} is already up to date for {release['tag_name']}")
        return
    with open(OUTPUT, "w") as handle:
        handle.write(formula)
    print(f"{OUTPUT} updated for {release['tag_name']}")


if __name__ == "__main__":
    main()

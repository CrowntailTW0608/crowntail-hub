#!/usr/bin/env python3
"""
掃描 GitHub API，找出所有啟用 GitHub Pages 的 repo，
確認 URL 可連線後產生 index.html。
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone

GITHUB_USER = "CrowntailTW0608"
API_URL = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "index.html")


def fetch_repos() -> "list[dict]":
    req = urllib.request.Request(
        API_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "crowntail-hub/generate.py",
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def check_url(url: str) -> bool:
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", "crowntail-hub/generate.py")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def pages_url(repo: dict) -> str:
    name = repo["name"]
    if name.lower() == f"{GITHUB_USER.lower()}.github.io":
        return f"https://{GITHUB_USER.lower()}.github.io/"
    return f"https://{GITHUB_USER.lower()}.github.io/{name}/"


def build_html(sites: "list[dict]", updated_at: str) -> str:
    cards = ""
    for site in sites:
        name = site["name"]
        url = site["url"]
        desc = site.get("description") or ""
        desc_html = f'<p class="desc">{desc}</p>' if desc else ""
        cards += f"""
        <a class="card" href="{url}" target="_blank" rel="noopener">
          <h2>{name}</h2>
          {desc_html}
          <span class="url">{url}</span>
        </a>"""

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Crowntail Pages Hub</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #0d1117;
      color: #c9d1d9;
      min-height: 100vh;
      padding: 2rem 1rem;
    }}
    header {{
      text-align: center;
      margin-bottom: 2.5rem;
    }}
    header h1 {{
      font-size: 2rem;
      color: #f0f6fc;
      margin-bottom: .4rem;
    }}
    header p {{
      color: #8b949e;
      font-size: .9rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1.2rem;
      max-width: 960px;
      margin: 0 auto;
    }}
    .card {{
      display: block;
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 1.2rem 1.4rem;
      text-decoration: none;
      color: inherit;
      transition: border-color .2s, box-shadow .2s;
    }}
    .card:hover {{
      border-color: #58a6ff;
      box-shadow: 0 0 0 3px rgba(88,166,255,.15);
    }}
    .card h2 {{
      font-size: 1rem;
      color: #58a6ff;
      margin-bottom: .35rem;
      word-break: break-all;
    }}
    .card .desc {{
      font-size: .85rem;
      color: #8b949e;
      margin-bottom: .5rem;
      line-height: 1.5;
    }}
    .card .url {{
      font-size: .75rem;
      color: #3fb950;
      word-break: break-all;
    }}
    footer {{
      text-align: center;
      margin-top: 3rem;
      color: #8b949e;
      font-size: .8rem;
    }}
    .empty {{
      text-align: center;
      color: #8b949e;
      margin-top: 4rem;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Crowntail Pages Hub</h1>
    <p>@{GITHUB_USER} 的所有 GitHub Pages 站台</p>
  </header>
  {"<div class='grid'>" + cards + "</div>" if sites else "<p class='empty'>目前沒有可連線的 GitHub Pages 站台。</p>"}
  <footer>
    <p>最後更新：{updated_at}</p>
  </footer>
</body>
</html>
"""


def main():
    print("抓取 GitHub repo 清單...")
    repos = fetch_repos()
    pages_repos = [r for r in repos if r.get("has_pages")]
    print(f"找到 {len(pages_repos)} 個啟用 Pages 的 repo")

    sites = []
    for repo in pages_repos:
        url = pages_url(repo)
        print(f"  確認 {url} ...", end=" ", flush=True)
        ok = check_url(url)
        print("OK" if ok else "FAIL")
        if ok:
            sites.append({
                "name": repo["name"],
                "url": url,
                "description": repo.get("description"),
            })

    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html = build_html(sites, updated_at)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n產生完成：{OUTPUT_FILE}（{len(sites)} 個站台）")


if __name__ == "__main__":
    main()

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
THIS_REPO = "crowntail-hub"
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
      background-image: radial-gradient(
        circle 1200px at var(--cx, -9999px) var(--cy, -9999px),
        rgba(88, 166, 255, 0.07),
        transparent 70%
      );
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
    .gh-link {{
      display: inline-flex;
      align-items: center;
      gap: .35rem;
      color: #8b949e;
      text-decoration: none;
      transition: color .2s;
    }}
    .gh-link:hover {{
      color: #f0f6fc;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Crowntail Pages Hub</h1>
    <p>
      <a href="https://github.com/{GITHUB_USER}" target="_blank" rel="noopener" class="gh-link">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="18" height="18" aria-label="GitHub" fill="currentColor">
          <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.68 7.68 0 0 1 2-.27c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
        </svg>
        @{GITHUB_USER}
      </a> 的所有 GitHub Pages 站台
    </p>
  </header>
  {"<div class='grid'>" + cards + "</div>" if sites else "<p class='empty'>目前沒有可連線的 GitHub Pages 站台。</p>"}
  <footer>
    <p>最後更新：{updated_at}</p>
  </footer>
  <script>
    document.addEventListener('mousemove', (e) => {{
      document.body.style.setProperty('--cx', e.clientX + 'px');
      document.body.style.setProperty('--cy', e.clientY + 'px');
    }});
    document.addEventListener('mouseleave', () => {{
      document.body.style.setProperty('--cx', '-9999px');
      document.body.style.setProperty('--cy', '-9999px');
    }});
  </script>
</body>
</html>
"""


def main():
    print("抓取 GitHub repo 清單...")
    repos = fetch_repos()
    pages_repos = [r for r in repos if r.get("has_pages") and r["name"] != THIS_REPO]
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

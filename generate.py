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
    .refresh-btn {{
      display: inline-flex;
      align-items: center;
      gap: .4rem;
      margin-top: 1rem;
      padding: .45rem 1rem;
      background: #21262d;
      border: 1px solid #30363d;
      border-radius: 6px;
      color: #c9d1d9;
      font-size: .85rem;
      cursor: pointer;
      transition: border-color .2s, background .2s;
    }}
    .refresh-btn:hover {{ background: #30363d; border-color: #8b949e; }}
    .refresh-btn:disabled {{ opacity: .5; cursor: not-allowed; }}
    .modal-overlay {{
      display: none;
      position: fixed; inset: 0;
      background: rgba(0,0,0,.6);
      align-items: center; justify-content: center;
      z-index: 100;
    }}
    .modal-overlay.open {{ display: flex; }}
    .modal {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 10px;
      padding: 1.5rem;
      width: min(360px, 90vw);
    }}
    .modal h3 {{ color: #f0f6fc; margin-bottom: .5rem; font-size: 1rem; }}
    .modal p {{ color: #8b949e; font-size: .82rem; margin-bottom: 1rem; line-height: 1.5; }}
    .modal input {{
      width: 100%; padding: .5rem .7rem;
      background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
      color: #c9d1d9; font-size: .85rem; margin-bottom: .8rem;
    }}
    .modal input:focus {{ outline: none; border-color: #58a6ff; }}
    .modal-actions {{ display: flex; gap: .6rem; justify-content: flex-end; }}
    .btn-cancel {{
      padding: .4rem .9rem; background: transparent;
      border: 1px solid #30363d; border-radius: 6px;
      color: #8b949e; font-size: .85rem; cursor: pointer;
    }}
    .btn-cancel:hover {{ border-color: #8b949e; color: #c9d1d9; }}
    .btn-trigger {{
      padding: .4rem .9rem; background: #238636;
      border: 1px solid #2ea043; border-radius: 6px;
      color: #fff; font-size: .85rem; cursor: pointer;
    }}
    .btn-trigger:hover {{ background: #2ea043; }}
    .toast {{
      position: fixed; bottom: 1.5rem; left: 50%; transform: translateX(-50%);
      background: #161b22; border: 1px solid #30363d; border-radius: 8px;
      padding: .6rem 1.2rem; font-size: .85rem; color: #c9d1d9;
      opacity: 0; transition: opacity .3s; pointer-events: none; white-space: nowrap;
    }}
    .toast.show {{ opacity: 1; }}
    .toast.success {{ border-color: #2ea043; color: #3fb950; }}
    .toast.error {{ border-color: #f85149; color: #f85149; }}
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
    <button class="refresh-btn" onclick="openModal()">
      <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
        <path d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
        <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
      </svg>
      立即更新
    </button>
  </footer>

  <div class="modal-overlay" id="modalOverlay" onclick="closeOnOverlay(event)">
    <div class="modal">
      <h3>觸發 GitHub Actions</h3>
      <p>請輸入具有 <code>workflow</code> 權限的 GitHub PAT。Token 僅在瀏覽器端使用，不會傳送至任何第三方。</p>
      <input type="password" id="tokenInput" placeholder="ghp_xxxxxxxxxxxx" />
      <div class="modal-actions">
        <button class="btn-cancel" onclick="closeModal()">取消</button>
        <button class="btn-trigger" onclick="triggerWorkflow()">觸發</button>
      </div>
    </div>
  </div>

  <div class="toast" id="toast"></div>

  <script>
    const OWNER = '{GITHUB_USER}';
    const REPO = '{THIS_REPO}';
    const WORKFLOW = 'update-pages.yml';

    function openModal() {{ document.getElementById('modalOverlay').classList.add('open'); document.getElementById('tokenInput').focus(); }}
    function closeModal() {{ document.getElementById('modalOverlay').classList.remove('open'); document.getElementById('tokenInput').value = ''; }}
    function closeOnOverlay(e) {{ if (e.target === document.getElementById('modalOverlay')) closeModal(); }}

    function showToast(msg, type) {{
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.className = 'toast show ' + type;
      setTimeout(() => {{ t.className = 'toast'; }}, 3500);
    }}

    async function triggerWorkflow() {{
      const token = document.getElementById('tokenInput').value.trim();
      if (!token) {{ showToast('請輸入 Token', 'error'); return; }}
      const btn = document.querySelector('.btn-trigger');
      btn.disabled = true; btn.textContent = '觸發中…';
      try {{
        const res = await fetch(
          `https://api.github.com/repos/${{OWNER}}/${{REPO}}/actions/workflows/${{WORKFLOW}}/dispatches`,
          {{
            method: 'POST',
            headers: {{
              'Authorization': `Bearer ${{token}}`,
              'Accept': 'application/vnd.github+json',
              'Content-Type': 'application/json',
            }},
            body: JSON.stringify({{ ref: 'main' }}),
          }}
        );
        if (res.status === 204) {{
          showToast('Workflow 已觸發！約 1 分鐘後頁面更新', 'success');
          closeModal();
        }} else {{
          const err = await res.json().catch(() => ({{}}));
          showToast('失敗：' + (err.message || res.status), 'error');
        }}
      }} catch (e) {{
        showToast('網路錯誤：' + e.message, 'error');
      }} finally {{
        btn.disabled = false; btn.textContent = '觸發';
      }}
    }}

    document.getElementById('tokenInput').addEventListener('keydown', e => {{
      if (e.key === 'Enter') triggerWorkflow();
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

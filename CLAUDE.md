# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案說明

GitHub Pages 統一入口站，對應 repo：`CrowntailTW0608/crowntail-hub`

部署後網址：`https://crowntailtw0608.github.io/crowntail-hub`

入口頁面列出帳號下所有已部署的 GitHub Pages 網站，並透過 GitHub Actions 自動更新。

## 本機執行

需要 Python 3.12+，無額外套件依賴（僅用標準函式庫）。

```bash
# 直接執行（不帶 token，API rate limit 較低）
python generate.py

# 帶 token 執行（提高 rate limit，建議使用）
GITHUB_TOKEN=<your_token> python generate.py
```

執行後會在當前目錄產生 / 覆蓋 `index.html`。

## 架構

```
crowntail-hub/
├── index.html                      # 入口頁面（由 generate.py 自動產生，勿手動編輯）
├── generate.py                     # 掃描 GitHub API 並產生 index.html
└── .github/workflows/
    └── update-pages.yml            # GitHub Actions：每週一 UTC 02:00 自動執行
```

## 運作流程

1. `generate.py` 呼叫 GitHub API（`/users/CrowntailTW0608/repos`）
2. 篩選 `has_pages: true` 且非本 repo 的項目
3. 對每個 Pages URL 發 HTTP GET，確認回 200
4. 產生 `index.html`，寫入最後更新時間（UTC）
5. GitHub Actions 若偵測到 `index.html` 有變動才 commit，避免空 commit

## GitHub Actions 觸發方式

- **自動**：每週一 UTC 02:00
- **手動**：在 Actions 頁面點選 `workflow_dispatch` 觸發

## 注意事項

- `index.html` 完全由 `generate.py` 產生，直接修改會在下次執行時被覆蓋
- HTML 樣式（深色主題）內嵌於 `generate.py` 的 `build_html()` 函式，如需調整請修改該函式

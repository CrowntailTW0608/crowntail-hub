# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案說明

GitHub Pages 統一入口站，對應 repo：`CrowntailTW0608/crowntail-hub`

部署後網址：`https://crowntailtw0608.github.io/crowntail-hub`

入口頁面列出帳號下所有已部署的 GitHub Pages 網站，並透過 GitHub Actions 自動更新。

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
2. 篩選 `has_pages: true` 的 repo
3. 對每個 repo 的 Pages URL 發 HTTP GET，確認回 200
4. 產生 `index.html`，寫入最後更新時間
5. GitHub Actions 若偵測到 `index.html` 有變動才 commit，避免空 commit

## GitHub Actions 觸發方式

每週一 UTC 02:00 自動執行。

## 新增 Pages 站後的更新方式

不需手動修改任何檔案，等下次 Actions 自動執行即可。

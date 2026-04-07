# Crowntail Pages Hub

> 一個自動整理、自動更新的 GitHub Pages 入口站。

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-2ea043?logo=github)](https://crowntailtw0608.github.io/crowntail-hub)
[![Update Pages](https://github.com/CrowntailTW0608/crowntail-hub/actions/workflows/update-pages.yml/badge.svg)](https://github.com/CrowntailTW0608/crowntail-hub/actions/workflows/update-pages.yml)

把 [@CrowntailTW0608](https://github.com/CrowntailTW0608) 所有已部署的 GitHub Pages 站台，自動整合成一個乾淨的導覽頁面——不需手動維護，新站上線後自動出現。

---

## 它如何運作？

```
GitHub API  →  篩選啟用 Pages 的 repo
           →  逐一確認 URL 可連線（HTTP 200）
           →  產生 index.html
           →  GitHub Actions 自動 commit 並部署
```

整個流程由 `generate.py` 驅動，透過 GitHub Actions 每週自動執行，無需人工介入。

---

> `index.html` 由程式自動產生，請勿手動編輯。

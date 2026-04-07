# Crowntail Pages Hub

[@CrowntailTW0608](https://github.com/CrowntailTW0608) 帳號下所有 GitHub Pages 站台的統一入口。

**部署網址：** https://crowntailtw0608.github.io/crowntail-hub

## 運作方式

`generate.py` 呼叫 GitHub API，篩選出 `has_pages: true` 的 repo，對每個 Pages URL 確認可連線（HTTP 200），產生 `index.html`。

GitHub Actions 每週一 UTC 02:00 自動執行，或可手動觸發：

> Actions → **Update Pages Index** → **Run workflow**

## 本機執行

```bash
python generate.py
```

可選擇設定環境變數 `GITHUB_TOKEN` 以提高 API rate limit：

```bash
GITHUB_TOKEN=ghp_xxx python generate.py
```

> `index.html` 由 `generate.py` 自動產生，請勿手動編輯。

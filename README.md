# Docker 微服務編排示範專案

本專案展示如何透過 Docker Compose 建立一個具備 **Sidecar 架構** 的自動化環境，由 **n8n** 進行工作流編排，並調用 **Python 爬蟲服務** 執行數據處理任務。

## 架構說明

- **n8n (指揮官)**：負責流程編排、接收外部 Webhook 觸發，並透過內部網路調用 Sidecar。
- **Python Sidecar (專業 Worker)**：運行 Flask 服務，內建 `requests` 與 `BeautifulSoup`，負責執行實際的網頁抓取邏輯。
- **內部通訊**：使用 Docker 網路 `demo-net`，n8n 可透過 `http://sidecar:5000` 直接存取 Python 服務。

## 目錄結構

```text
docker-demo/
├── docker-compose.yml       # 容器服務定義
├── workflow.json            # n8n 匯入用的工作流定義
├── scraper_workflow.json    # 爬蟲專用工作流定義
└── sidecar/
    ├── Dockerfile           # Python 執行環境建置檔
    └── app.py               # Flask API 服務程式碼
```

## 快速啟動

1. **啟動服務**：
   ```bash
   docker compose up -d --build
   ```
2. **服務存取**：
   - n8n: `http://localhost:5679`
   - Python Sidecar API: `http://localhost:5000`

## n8n 工作流測試
若要透過 n8n 調用功能，請確保已在 n8n 中匯入 `scraper_workflow_sync.json` 與 `analyzer_workflow.json` 並啟用。

### 1. 測試網頁爬蟲工作流
```bash
curl -s "http://localhost:5679/webhook/scrape-trigger?url=https://dashboard.ngrok.com"
```

### 2. 測試字數分析工作流
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"text": "Hello world from OpenClaw and n8n"}' \
     "http://localhost:5679/webhook/analyze-trigger"
```


## 功能模組與路由分流
- 透過 Flask Blueprints 將應用程式模組化 (Sidecar/routes/)，實現路由分流：
  - `/api/scraper/scrape`: 執行網頁爬蟲任務。
  - `/api/analyzer/analyze`: 執行文字數據統計任務。
- 新增 `analyzer_workflow.json` 以支援字數統計工作流的同步呼叫。

### API 測試指南
您可以透過以下指令進行功能模組驗證：

#### 1. 爬蟲模組 (GET 請求)
需在 URL 參數中傳入 `url`：
```bash
curl -s "http://localhost:5000/api/scraper/scrape?url=https://www.google.com"
```

#### 2. 分析模組 (POST 請求)
需在 Request Payload 中傳入 JSON 格式的 `text`：
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"text": "這是一段測試文字，用來測試分析功能"}' \
     "http://localhost:5000/api/analyzer/analyze"
```





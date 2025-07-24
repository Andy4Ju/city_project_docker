# 🚢 Titanic Dockerized Project

本專案使用 Docker Compose 建立一個可協作的多容器環境，其中為處理 Titanic 數據匯入、儲存與網頁呈現，建立以下三個容器：

1. MySQL 資料庫容器
2. Python 應用程式容器（匯入 titanic.csv）
3. Web 容器（Flask 顯示資料）

請見下方啟動方式與任務分工。

## ⚙️ 環境需求

- Docker & Docker Compose
- git

## 🚀 啟動方式

```bash
git clone https://github.com/Andy4Ju/titanic_project_docker
cd titanic_project_docker
cp .env.example .env
docker compose up -d --build # 在背景執行
```

## ✅ 專案結構簡介

|目錄 | 用途 |
|---------------|------|
| init/         | 初始 SQL 建表檔 |
| csv/          | Titanic 資料來源 |
| python_app/   | 匯入程式與 Dockerfile |
| web/          | Flask 顯示資料介面 |

## .gitignore

.env

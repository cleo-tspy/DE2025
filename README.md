# DE2025 — Data Engineering Projects

> 目標：端到端資料平台（ETL → Streaming → OLAP/Graph → Ontology/Knowledge Graph → Federation → Governance/Observability），並以企業級實務標準產出程式碼、文件與監控

---

## Roadmap

```mermaid
flowchart TB
  subgraph P1[Phase 1 基礎與容器化]
    A1[7 個 pandas 資料處理腳本] --> A2[容器化服務 + Logging]
    A2 --> A3[Containerized ETL: 抓 API/CSV/爬蟲 → DQ → PostgreSQL]
    A3 --> A4[CI/CD: GitHub Actions + 單元/整合測試]
    A3 --> A5[監控基本版: Healthcheck + Alert]
  end

  subgraph P2[Phase 2 資料平台架構]
    B1["Kafka Ingest(Clickstream 模擬)"] --> B2[Spark Streaming/Structured Streaming]
    B2 --> B3[(PostgreSQL-OLTP)]
    B2 --> B4[(ClickHouse-OLAP)]
    B3 --> B5[Grafana 即時儀表板]
    B4 --> B5
    B6[Terraform IaC + 雲端託管] --> B7[Auto-scaling & 成本優化]
  end

  subgraph P3[Phase 3 本體與知識圖譜]
    C1["Ontology 設計 (RDF/OWL)"] --> C2[SPARQL Query 範本]
    C1 --> C3[Neo4j Property Graph 實作]
    C1 --> C4[Jena/RDF Store 與 Endpoint]
    C5[NLP/IE: spaCy + LLM 實體/關係抽取] --> C6[自動充填 Ontology + 信心分數 + 人在回圈]
  end

  subgraph P4[Phase 4 進階整合與聯邦]
    D1[Metadata: DataHub/Atlas] --> D2[血緣/影響分析]
    D3[FastAPI/GraphQL API] --> D4["AuthN/AuthZ (OAuth2/JWT)"]
    D5[Trino/Presto 聯邦查詢] --> D6[Delta/Parquet/Arrow 儲存層]
  end

  subgraph P5[Phase 5 企業級上線]
    E1[安全治理: Ranger/Policy/遮罩] --> E2[稽核/備援/備份]
    E3[Observability: OpenTelemetry + Prometheus + Grafana] --> E4[分散式追蹤/告警/Runbook]
    E5[壓測與效能優化] --> E6[文件與使用者訓練]
  end

  %% 關聯
  A5 --> B1
  B5 --> C5
  C4 --> D5
  C3 --> D3
  D5 --> E5
  D2 --> E1
```


## About this repo

- **產出**：`artifacts/`（每週 demo 的輸出，例：`/artifacts/w1/`）
- **已完成的文檔**：`docs/progress/W{週}.md`


## Quick Start
```bash
# 安裝依賴與虛擬環境（uv 可改為 pip）
uv venv && uv sync

# 基本任務（Makefile）
make fmt      # ruff format
make lint     # ruff check
make type     # mypy
make test     # pytest
make demo     # 本週 demo；輸出固定在 artifacts/
```

## Portfolio
- README 保持**一頁總覽**與快速啟動；詳情請見 Notion 主頁與 `docs/progress/` 歸檔
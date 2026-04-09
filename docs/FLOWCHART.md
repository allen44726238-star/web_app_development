# 線上算命系統 - 流程圖與對照表

本文件根據專案的 PRD 與架構設計，繪製了使用者的操作流程圖（User Flow），以及核心功能的系統序列圖（Sequence Diagram），最後附上各功能與預計路由的路徑對照表。

## 1. 使用者流程圖（User Flow）

描述使用者從進入系統到操作各項主要功能的完整路徑。

```mermaid
flowchart LR
    A([使用者開啟網站]) --> B(首頁 - 顯示基本介紹與每日運勢)
    
    B --> C{是否已登入?}
    C -->|否| D[點擊登入/註冊]
    D --> E[填寫帳號密碼]
    E --> F{驗證成功?}
    F -->|否| D
    F -->|是| B
    
    C -->|是| G{選擇操作?}
    
    G -->|開始抽籤| H[進入抽籤/儀式頁面]
    H --> I[搖籤筒動畫/點擊抽籤]
    I --> J[顯示求得的籤號]
    J --> K[進入解籤詳情頁面]
    K --> L[檢視籤詩與事業/感情解析]
    L --> M([系統自動儲存結果])
    
    G -->|查看紀錄| N[進入歷史紀錄頁面]
    N --> O[瀏覽過去抽籤紀錄與解析]
    
    G -->|捐香油錢| P[進入香油錢贊助頁面]
    P --> Q[查看匯款資訊/送出贊助表單]
    
    G -->|登出| R([結束使用並登出])
    R --> B
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖描述核心功能：「使用者點擊抽籤」一直到「獲得詳細解籤並儲存在資料庫」的完整資料流。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask (Controller)
    participant Model as Model (Fortune/History)
    participant DB as SQLite
    
    User->>Browser: 在抽籤頁面點擊「開始抽籤」
    Browser->>Flask: POST /fortune/draw
    
    Flask->>Model: 呼叫抽籤邏輯 (FortuneModel.draw_random())
    Model->>DB: 查詢所有籤詩 (SELECT random one)
    DB-->>Model: 回傳抽中的籤詩資料
    Model-->>Flask: 取得籤號與解析資料
    
    opt 使用者已登入
        Flask->>Model: 呼叫儲存邏輯 (HistoryModel.save(user_id, fortune_id))
        Model->>DB: 寫入歷史紀錄 (INSERT INTO history)
        DB-->>Model: 成功
        Model-->>Flask: 儲存完畢
    end
    
    Flask->>Browser: 重導向 (Redirect) 至解籤結果頁面 /fortune/result/<id>
    Browser->>Flask: GET /fortune/result/<id>
    Flask->>Browser: 透過 Jinja2 渲染含有籤詩解析的 HTML
    Browser-->>User: 畫面顯示籤詩與白話文解析結果
```

## 3. 功能清單對照表

根據 PRD 提出的功能，對應預計實作的 URL 路徑與發送的 HTTP 方法：

| 功能需求 | 對應介面 / 操作 | HTTP 方法 | URL 路徑 (預計) |
| -------- | --------------- | --------- | --------------- |
| 1. 首頁/每日運勢 | 顯示系統首頁與當日簡易運勢 | GET | `/` |
| 2. 會員註冊 | 進入註冊頁面 | GET | `/auth/register` |
| | 送出註冊資料 | POST | `/auth/register` |
| 3. 會員登入 | 進入登入頁面 | GET | `/auth/login` |
| | 送出登入資料 | POST | `/auth/login` |
| 4. 會員登出 | 執行登出操作 | GET | `/auth/logout` |
| 5. 算命抽籤 | 進入抽籤儀式頁面 | GET | `/fortune` |
| | 執行隨機抽籤操作 | POST | `/fortune/draw` |
| 6. 靈籤解析 | 顯示單一籤詩的詳細解析結果 | GET | `/fortune/result/<fortune_id>` |
| 7. 儲存/查詢紀錄 | 查看自己的歷史抽籤結果列表 | GET | `/history` |
| 8. 捐香油錢 | 顯示贊助資訊與表單 | GET | `/donate` |

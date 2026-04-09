# 系統流程圖與功能對照表

本文件依據 PRD 與系統架構規劃，定義使用者的操作動線以及系統內部的資料流程。

## 1. 使用者流程圖（User Flow）

描述使用者從進入系統到執行主要功能（註冊登入、搜尋、CRUD 等）的完整操作路徑。

```mermaid
flowchart LR
    A([使用者造訪首頁]) --> B{是否已登入？}
    B -->|否| C[註冊 / 登入頁]
    C -->|成功| D[首頁 / 儀表板]
    B -->|是| D
    
    D --> E{選擇操作}
    
    E -->|一般搜尋| F[輸入關鍵字]
    F --> G[食譜列表頁]
    
    E -->|食材組合搜尋| H[輸入多種食材]
    H --> G
    
    E -->|瀏覽| G
    
    G -->|點擊食譜| I[食譜詳細資訊頁]
    
    E -->|新增食譜| J[填寫新增表單]
    J -->|儲存| I
    
    I -->|編輯| K[修改食譜表單]
    K -->|儲存| I
    
    I -->|刪除| L[確認刪除]
    L --> G
    
    E -->|管理權限| M[後台管理畫面]
    M -->|檢視使用者/強制下架| N[管理員操作]
```

## 2. 系統序列圖（Sequence Diagram）

以下描述「使用者填寫新食譜並送出」到「資料存入資料庫」的完整流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite DB
    
    User->>Browser: 填寫新增食譜表單並點擊「儲存」
    Browser->>Route: POST /recipes/new (帶有表單資料)
    Route->>Route: 驗證使用者身分與資料格式
    Route->>Model: 呼叫 create_recipe(data)
    
    Model->>DB: INSERT INTO recipes (名稱, 步驟...)
    DB-->>Model: 回傳食譜 ID
    Note over Model, DB: 透過關聯表處理多對多食材資料
    Model->>DB: INSERT INTO recipe_ingredients (食譜ID, 食材ID)
    DB-->>Model: 寫入成功
    Model-->>Route: 回傳處理成功狀態
    
    Route-->>Browser: HTTP 302 Redirect 
    Browser->>User: 重新導向至該篇「食譜詳細資訊頁」
```

## 3. 功能清單與路由對照表

以下整理系統主要功能、預期的網址路徑 (URL) 以及對應的 HTTP 請求方法。

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :---: | :--- |
| **首頁 / 列表** | `/` 或 `/recipes` | GET | 顯示食譜列表，支援一般關鍵字搜尋與食材組合搜尋。 |
| **註冊帳號** | `/auth/register` | GET, POST | 顯示註冊表單，處理註冊邏輯並存入使用者資料。 |
| **登入系統** | `/auth/login` | GET, POST | 顯示登入表單，驗證帳號密碼並建立 session。 |
| **登出系統** | `/auth/logout` | GET (或 POST) | 清除 session，並重導向回首頁或登入頁。 |
| **新增食譜** | `/recipes/new` | GET, POST | GET 顯示表單；POST 處理並寫入新食譜與食材資料。 |
| **食譜詳細資訊** | `/recipes/<id>` | GET | 檢視該筆食譜的所有內容、步驟與所需食材。 |
| **編輯食譜** | `/recipes/<id>/edit` | GET, POST | GET 顯示帶有原資料的表單；POST 更新內容至資料庫。 |
| **刪除食譜** | `/recipes/<id>/delete`| POST | 將該筆食譜自資料庫中移除（僅限原作者或管理員）。 |
| **後台：管理面板**| `/admin` | GET | 顯示全站資訊概覽（僅限管理員）。 |
| **後台：用戶清單**| `/admin/users` | GET | 檢視所有註冊用戶清單。 |

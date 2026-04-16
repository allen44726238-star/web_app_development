# 路由設計文件 (ROUTES.md)

本文件根據 PRD、架構圖與資料庫設計，規劃 Flask 的路由與頁面對應關係。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| ---- | --------- | -------- | -------- | ---- |
| 首頁 / 每日運勢 | GET | `/` | `index.html` | 顯示首頁內容與登入者的簡易運勢 |
| 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 建立新使用者，成功後重導向登入頁 |
| 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | — | 驗證帳號密碼，成功後寫入 Session 並重導向首頁 |
| 登出 | GET | `/auth/logout` | — | 清除 Session 並重導向首頁 |
| 抽籤頁面 | GET | `/fortune` | `fortune/index.html` | 顯示求籤儀式畫面 |
| 執行抽籤 | POST | `/fortune/draw` | — | 隨機抽出籤詩，紀錄至歷史，重導向至結果頁 |
| 解析結果頁 | GET | `/fortune/result/<id>` | `fortune/result.html` | 顯示單一籤詩的詳細解析 |
| 歷史紀錄清單 | GET | `/history` | `history/index.html` | 顯示當前使用者的過往抽籤紀錄 |
| 捐香油錢頁面 | GET | `/donate` | `donate/index.html` | 顯示募款說明及相關資訊 |

## 2. 每個路由的詳細說明

### `main` Blueprint (一般功能, 無 prefix)

- **GET `/` (首頁)**
  - 輸入：無
  - 處理邏輯：檢查使用者是否登入，登入則可隨機產生一句每日運勢。
  - 輸出：渲染 `index.html`。
  
- **GET `/fortune` (抽籤頁面)**
  - 輸入：無
  - 處理邏輯：檢查使用者登入狀態。
  - 輸出：渲染 `fortune/index.html`。

- **POST `/fortune/draw` (執行抽籤)**
  - 輸入：無
  - 處理邏輯：呼叫 `Fortune.draw_random()`。若使用者已登入，將抽中結果寫入 `History`。
  - 輸出：重導向至 `/fortune/result/<fortune_id>`。
  - 錯誤處理：若無籤詩可抽，回傳 500 或顯示錯誤訊息。

- **GET `/fortune/result/<id>` (解析結果頁)**
  - 輸入：`id` (URL 參數，對應 Fortune ID)
  - 處理邏輯：呼叫 `Fortune.get_by_id(id)` 取得籤詩資料。
  - 輸出：渲染 `fortune/result.html` 並帶入籤詩資料。
  - 錯誤處理：若 `id` 不存在，導向 404 頁面。

- **GET `/history` (歷史紀錄)**
  - 輸入：使用者 Session
  - 處理邏輯：若未登入，重導向至登入頁。若已登入，呼叫 `History.get_by_user_id()` 取得紀錄（並 Join 籤詩表取得標題）。
  - 輸出：渲染 `history/index.html` 列表。

- **GET `/donate` (捐香油錢)**
  - 輸入：無
  - 處理邏輯：無特定邏輯。
  - 輸出：渲染 `donate/index.html`。

### `auth` Blueprint (認證相關, url_prefix='/auth')

- **GET `/auth/register`**
  - 處理邏輯：如果已經登入則重導向至首頁。
  - 輸出：渲染 `auth/register.html`。

- **POST `/auth/register`**
  - 輸入：`username`, `password` (表單)
  - 處理邏輯：驗證帳號是否已存在。若無，對密碼加密後寫入 `User`。
  - 輸出：成功重導向 `/auth/login`，失敗回傳錯誤訊息並重新渲染 `auth/register.html`。

- **GET `/auth/login`**
  - 處理邏輯：如果已經登入則重導向首頁。
  - 輸出：渲染 `auth/login.html`。

- **POST `/auth/login`**
  - 輸入：`username`, `password` (表單)
  - 處理邏輯：驗證帳號密碼。成功則在 Session 中紀錄 `user_id`。
  - 輸出：成功重導向 `/`，失敗則重新渲染 `auth/login.html` 並帶入錯誤提示。

- **GET `/auth/logout`**
  - 處理邏輯：清除 Session 中的會員資訊。
  - 輸出：重導向至 `/`。

## 3. Jinja2 模板清單

- `templates/base.html` (全站共用母版，含導覽列與首尾)
- `templates/index.html` (首頁)
- `templates/auth/login.html` (登入頁)
- `templates/auth/register.html` (註冊頁)
- `templates/fortune/index.html` (求籤儀式頁)
- `templates/fortune/result.html` (解籤結果頁)
- `templates/history/index.html` (歷史紀錄列表頁)
- `templates/donate/index.html` (香油錢贊助頁)

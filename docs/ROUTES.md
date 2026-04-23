# 個人記帳簿 — 路由設計文件

> **版本**：v1.0  
> **建立日期**：2026-04-23  
> **對應文件**：docs/PRD.md、docs/ARCHITECTURE.md、docs/DB_DESIGN.md  

---

## 1. 路由總覽表格

### 1.1 首頁 / 儀表板（main）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|---------|---------|------|
| 首頁儀表板 | GET | `/` | `templates/index.html` | 顯示餘額、收支摘要、預算警示、固定支出提醒、近期交易 |

### 1.2 使用者驗證（auth）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|---------|---------|------|
| 註冊頁面 | GET | `/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 註冊送出 | POST | `/register` | — | 驗證表單、建立帳號、重導向到登入頁 |
| 登入頁面 | GET | `/login` | `templates/auth/login.html` | 顯示登入表單 |
| 登入送出 | POST | `/login` | — | 驗證帳密、建立 Session、重導向到首頁 |
| 登出 | GET | `/logout` | — | 清除 Session、重導向到登入頁 |

### 1.3 交易紀錄（transaction）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|---------|---------|------|
| 新增帳目頁面 | GET | `/transaction/new` | `templates/transaction/create.html` | 顯示記帳表單 |
| 新增帳目送出 | POST | `/transaction/new` | — | 驗證表單、存入 DB、重導向到首頁 |
| 歷史帳目列表 | GET | `/transactions` | `templates/transaction/list.html` | 帳目列表、搜尋篩選、分頁 |
| 編輯帳目頁面 | GET | `/transaction/<id>/edit` | `templates/transaction/edit.html` | 顯示編輯表單（帶入既有資料） |
| 編輯帳目送出 | POST | `/transaction/<id>/edit` | — | 驗證表單、更新 DB、重導向到列表 |
| 刪除帳目 | POST | `/transaction/<id>/delete` | — | 刪除帳目、重導向到列表 |

### 1.4 統計分析（statistics）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|---------|---------|------|
| 統計頁面 | GET | `/statistics` | `templates/statistics/overview.html` | 圓餅圖 + 分類統計表格 |
| 統計資料 API | GET | `/statistics/data` | — (JSON) | 回傳指定月份的分類統計 JSON |

### 1.5 預算管理（budget）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|---------|---------|------|
| 預算設定頁面 | GET | `/budget` | `templates/budget/settings.html` | 顯示目前預算設定 |
| 預算設定送出 | POST | `/budget` | — | 儲存預算設定、重導向回預算頁 |

### 1.6 週期性固定支出（recurring）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|---------|---------|------|
| 固定支出管理頁 | GET | `/recurring` | `templates/recurring/manage.html` | 顯示所有固定支出項目 |
| 新增固定支出 | POST | `/recurring/new` | — | 新增項目、重導向回管理頁 |
| 編輯固定支出 | POST | `/recurring/<id>/edit` | — | 更新項目、重導向回管理頁 |
| 刪除固定支出 | POST | `/recurring/<id>/delete` | — | 刪除項目、重導向回管理頁 |
| 暫停/恢復提醒 | POST | `/recurring/<id>/toggle` | — | 切換啟用狀態、重導向回管理頁 |
| 一鍵記帳 | POST | `/recurring/<id>/record` | — | 轉為實際帳目、重導向到首頁 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁儀表板

#### `GET /`

- **輸入**：無（從 Session 取得 `current_user`）
- **處理邏輯**：
  1. 呼叫 `Transaction.get_total_balance(user_id)` → 取得總餘額
  2. 呼叫 `Transaction.get_monthly_summary(user_id, year, month)` → 取得本月收支
  3. 呼叫 `Transaction.get_recent(user_id, limit=10)` → 取得近期交易
  4. 呼叫 `Budget.get_all(user_id, year, month)` → 取得本月預算
  5. 計算預算使用率，判斷警示等級（< 80% 正常 / 80-100% 黃色 / > 100% 紅色）
  6. 呼叫 `Recurring.get_due_today(user_id)` → 取得今日到期的固定支出
- **輸出**：渲染 `index.html`，傳入餘額、收支摘要、預算警示、提醒、近期交易
- **錯誤處理**：未登入 → 重導向到 `/login`

---

### 2.2 使用者驗證

#### `GET /register`

- **輸入**：無
- **處理邏輯**：建立空白註冊表單
- **輸出**：渲染 `auth/register.html`
- **錯誤處理**：已登入 → 重導向到 `/`

#### `POST /register`

- **輸入**：表單欄位 `username`、`password`、`confirm_password`
- **處理邏輯**：
  1. Flask-WTF 驗證表單
  2. 檢查 `password == confirm_password`
  3. 呼叫 `User.get_by_username(username)` 確認帳號不重複
  4. 呼叫 `User.create(username, password)` 建立帳號
- **輸出**：成功 → 重導向到 `/login` 並顯示 flash 成功訊息
- **錯誤處理**：帳號重複 → 渲染表單 + 錯誤訊息；驗證失敗 → 渲染表單 + 錯誤

#### `GET /login`

- **輸入**：無
- **處理邏輯**：建立空白登入表單
- **輸出**：渲染 `auth/login.html`
- **錯誤處理**：已登入 → 重導向到 `/`

#### `POST /login`

- **輸入**：表單欄位 `username`、`password`
- **處理邏輯**：
  1. 呼叫 `User.get_by_username(username)` 查詢使用者
  2. 呼叫 `user.check_password(password)` 驗證密碼
  3. 呼叫 `login_user(user)` 建立 Session
- **輸出**：成功 → 重導向到 `/`
- **錯誤處理**：帳密錯誤 → 渲染登入頁 + 錯誤訊息

#### `GET /logout`

- **輸入**：無
- **處理邏輯**：呼叫 `logout_user()` 清除 Session
- **輸出**：重導向到 `/login`

---

### 2.3 交易紀錄

#### `GET /transaction/new`

- **輸入**：無
- **處理邏輯**：建立空白記帳表單，帶入預設分類清單
- **輸出**：渲染 `transaction/create.html`
- **錯誤處理**：未登入 → 重導向到 `/login`

#### `POST /transaction/new`

- **輸入**：表單欄位 `type`、`category`、`amount`、`date`、`note`
- **處理邏輯**：
  1. Flask-WTF 驗證表單
  2. 呼叫 `Transaction.create(user_id, type, category, amount, date, note)`
- **輸出**：成功 → 重導向到 `/` 並顯示 flash 成功訊息
- **錯誤處理**：驗證失敗 → 渲染表單 + 錯誤訊息

#### `GET /transactions`

- **輸入**：URL 參數 `page`、`date_from`、`date_to`、`category`、`keyword`
- **處理邏輯**：
  1. 解析篩選條件
  2. 呼叫 `Transaction.get_paginated(user_id, page, per_page, ...)` 分頁查詢
- **輸出**：渲染 `transaction/list.html`，傳入分頁結果與篩選條件
- **錯誤處理**：未登入 → 重導向到 `/login`

#### `GET /transaction/<id>/edit`

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 呼叫 `Transaction.get_by_id(id)` 取得帳目
  2. 檢查帳目是否屬於 `current_user`
  3. 將資料帶入編輯表單
- **輸出**：渲染 `transaction/edit.html`
- **錯誤處理**：帳目不存在 → 404；不是自己的 → 403

#### `POST /transaction/<id>/edit`

- **輸入**：URL 參數 `id`、表單欄位 `type`、`category`、`amount`、`date`、`note`
- **處理邏輯**：
  1. 取得帳目並驗證權限
  2. Flask-WTF 驗證表單
  3. 呼叫 `txn.update(type=..., category=..., amount=..., date=..., note=...)`
- **輸出**：成功 → 重導向到 `/transactions` 並顯示 flash 成功訊息
- **錯誤處理**：帳目不存在 → 404；驗證失敗 → 渲染表單 + 錯誤

#### `POST /transaction/<id>/delete`

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 取得帳目並驗證權限
  2. 呼叫 `txn.delete()`
- **輸出**：重導向到 `/transactions` 並顯示 flash 刪除成功訊息
- **錯誤處理**：帳目不存在 → 404；不是自己的 → 403

---

### 2.4 統計分析

#### `GET /statistics`

- **輸入**：URL 參數 `year`、`month`（選填，預設為當月）
- **處理邏輯**：
  1. 呼叫 `Transaction.get_category_summary(user_id, year, month)` → 分類統計
  2. 呼叫 `Transaction.get_monthly_summary(user_id, year, month)` → 月收支摘要
- **輸出**：渲染 `statistics/overview.html`，傳入統計資料
- **錯誤處理**：未登入 → 重導向到 `/login`

#### `GET /statistics/data`

- **輸入**：URL 參數 `year`、`month`
- **處理邏輯**：
  1. 呼叫 `Transaction.get_category_summary(user_id, year, month)`
- **輸出**：JSON 格式的分類統計資料（供 Chart.js 前端呼叫）
- **錯誤處理**：參數缺失 → 回傳 400 JSON 錯誤

---

### 2.5 預算管理

#### `GET /budget`

- **輸入**：URL 參數 `year`、`month`（選填，預設為當月）
- **處理邏輯**：
  1. 呼叫 `Budget.get_all(user_id, year, month)` → 取得所有預算
  2. 呼叫 `Transaction.get_monthly_summary(user_id, year, month)` → 取得本月支出
  3. 呼叫 `Transaction.get_category_summary(user_id, year, month)` → 各分類支出
  4. 計算各預算的使用率
- **輸出**：渲染 `budget/settings.html`，傳入預算設定與使用情況
- **錯誤處理**：未登入 → 重導向到 `/login`

#### `POST /budget`

- **輸入**：表單欄位 `total_amount`、多組 `category_name[]` + `category_amount[]`、`year`、`month`
- **處理邏輯**：
  1. Flask-WTF 驗證表單
  2. 呼叫 `Budget.set_budget(user_id, total_amount, year, month)` → 設定總預算
  3. 迴圈呼叫 `Budget.set_budget(user_id, amount, year, month, category)` → 設定各分類預算
- **輸出**：重導向到 `/budget` 並顯示 flash 成功訊息
- **錯誤處理**：驗證失敗 → 渲染頁面 + 錯誤訊息

---

### 2.6 週期性固定支出

#### `GET /recurring`

- **輸入**：無
- **處理邏輯**：呼叫 `Recurring.get_all(user_id)` → 取得所有固定支出
- **輸出**：渲染 `recurring/manage.html`
- **錯誤處理**：未登入 → 重導向到 `/login`

#### `POST /recurring/new`

- **輸入**：表單欄位 `name`、`category`、`amount`、`due_day`
- **處理邏輯**：
  1. 驗證表單
  2. 呼叫 `Recurring.create(user_id, name, category, amount, due_day)`
- **輸出**：重導向到 `/recurring` 並顯示 flash 成功訊息
- **錯誤處理**：驗證失敗 → 重導向回 `/recurring` + flash 錯誤

#### `POST /recurring/<id>/edit`

- **輸入**：URL 參數 `id`、表單欄位 `name`、`category`、`amount`、`due_day`
- **處理邏輯**：
  1. 取得項目並驗證權限
  2. 呼叫 `recurring.update(name=..., category=..., amount=..., due_day=...)`
- **輸出**：重導向到 `/recurring`
- **錯誤處理**：項目不存在 → 404

#### `POST /recurring/<id>/delete`

- **輸入**：URL 參數 `id`
- **處理邏輯**：取得項目 → 驗證權限 → 呼叫 `recurring.delete()`
- **輸出**：重導向到 `/recurring`
- **錯誤處理**：項目不存在 → 404

#### `POST /recurring/<id>/toggle`

- **輸入**：URL 參數 `id`
- **處理邏輯**：取得項目 → 驗證權限 → 呼叫 `recurring.toggle_active()`
- **輸出**：重導向到 `/recurring`
- **錯誤處理**：項目不存在 → 404

#### `POST /recurring/<id>/record`

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 取得項目並驗證權限
  2. 呼叫 `recurring.to_transaction_data()` 取得交易資料
  3. 呼叫 `Transaction.create(user_id, **data)` 建立實際帳目
- **輸出**：重導向到 `/` 並顯示 flash 成功訊息
- **錯誤處理**：項目不存在 → 404

---

## 3. Jinja2 模板清單

所有模板皆繼承 `base.html` 基礎模板。

| 模板檔案 | 繼承自 | 用途 | 對應路由 |
|---------|--------|------|---------|
| `templates/base.html` | — | 基礎版面（導覽列、頁尾、CSS/JS） | — |
| `templates/index.html` | `base.html` | 首頁儀表板 | `GET /` |
| `templates/auth/login.html` | `base.html` | 登入表單 | `GET /login` |
| `templates/auth/register.html` | `base.html` | 註冊表單 | `GET /register` |
| `templates/transaction/create.html` | `base.html` | 新增帳目表單 | `GET /transaction/new` |
| `templates/transaction/edit.html` | `base.html` | 編輯帳目表單 | `GET /transaction/<id>/edit` |
| `templates/transaction/list.html` | `base.html` | 歷史帳目列表（含搜尋篩選） | `GET /transactions` |
| `templates/statistics/overview.html` | `base.html` | 圓餅圖統計分析 | `GET /statistics` |
| `templates/budget/settings.html` | `base.html` | 預算設定頁面 | `GET /budget` |
| `templates/recurring/manage.html` | `base.html` | 固定支出管理 | `GET /recurring` |

---

## 4. 錯誤頁面

| HTTP 狀態碼 | 模板 | 說明 |
|------------|------|------|
| 404 | `templates/errors/404.html` | 頁面不存在 |
| 403 | `templates/errors/403.html` | 無權限存取 |
| 500 | `templates/errors/500.html` | 伺服器內部錯誤 |

---

> 📌 **下一步**：路由設計確認後，進入 **實作（Implementation）** 階段。

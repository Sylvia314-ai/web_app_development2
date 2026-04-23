# 個人記帳簿 — 流程圖文件

> **版本**：v1.0  
> **建立日期**：2026-04-23  
> **對應文件**：docs/PRD.md、docs/ARCHITECTURE.md  

---

## 1. 使用者流程圖（User Flow）

### 1.1 整體操作流程

使用者從進入網站到完成各項功能的操作路徑：

```mermaid
flowchart LR
    START(["🌐 使用者開啟網站"]) --> CHECK{"已登入？"}

    CHECK -->|"否"| AUTH_CHOICE{"選擇操作"}
    AUTH_CHOICE -->|"註冊"| REGISTER["📝 填寫註冊表單"]
    AUTH_CHOICE -->|"登入"| LOGIN["🔑 輸入帳密登入"]
    REGISTER --> LOGIN
    LOGIN --> DASHBOARD

    CHECK -->|"是"| DASHBOARD["🏠 首頁儀表板"]

    DASHBOARD --> NAV{"要執行什麼操作？"}

    NAV -->|"快速記帳"| ADD_TXN["💰 新增帳目"]
    NAV -->|"查看歷史"| HISTORY["📋 歷史帳目"]
    NAV -->|"統計分析"| STATS["📊 圓餅圖統計"]
    NAV -->|"預算設定"| BUDGET["⚙️ 預算管理"]
    NAV -->|"固定支出"| RECURRING["🔁 週期性支出"]
    NAV -->|"登出"| LOGOUT["🚪 登出"]

    ADD_TXN --> DASHBOARD
    HISTORY --> DASHBOARD
    STATS --> DASHBOARD
    BUDGET --> DASHBOARD
    RECURRING --> DASHBOARD
    LOGOUT --> LOGIN
```

---

### 1.2 快速記帳流程

```mermaid
flowchart LR
    A["🏠 首頁儀表板"] --> B["點擊「新增帳目」"]
    B --> C["📝 記帳表單頁面"]
    C --> D{"選擇類型"}
    D -->|"收入"| E["選擇收入分類"]
    D -->|"支出"| F["選擇支出分類"]
    E --> G["輸入金額"]
    F --> G
    G --> H["選擇日期\n（預設今天）"]
    H --> I["輸入備註\n（選填）"]
    I --> J{"送出表單"}
    J -->|"驗證失敗"| K["❌ 顯示錯誤訊息"]
    K --> C
    J -->|"驗證成功"| L["✅ 儲存成功"]
    L --> M["🏠 返回儀表板\n餘額已更新"]
```

---

### 1.3 歷史帳目搜尋與編輯流程

```mermaid
flowchart LR
    A["🏠 首頁儀表板"] --> B["點擊「歷史帳目」"]
    B --> C["📋 帳目列表頁"]
    C --> D{"操作選擇"}

    D -->|"搜尋篩選"| E["設定篩選條件"]
    E --> E1["日期範圍"]
    E --> E2["分類篩選"]
    E --> E3["關鍵字搜尋"]
    E1 --> F["顯示篩選結果"]
    E2 --> F
    E3 --> F
    F --> D

    D -->|"編輯帳目"| G["點擊編輯按鈕"]
    G --> H["📝 編輯表單"]
    H --> I{"儲存修改"}
    I -->|"成功"| J["✅ 更新完成"]
    J --> C
    I -->|"失敗"| H

    D -->|"刪除帳目"| K["點擊刪除按鈕"]
    K --> L{"確認刪除？"}
    L -->|"取消"| C
    L -->|"確認"| M["🗑️ 刪除完成"]
    M --> C

    D -->|"切換分頁"| N["前往下一頁"]
    N --> C
```

---

### 1.4 預算設定與警示流程

```mermaid
flowchart LR
    A["🏠 首頁儀表板"] --> B["點擊「預算設定」"]
    B --> C["⚙️ 預算管理頁"]
    C --> D{"操作選擇"}

    D -->|"設定總預算"| E["輸入每月總預算金額"]
    E --> F{"儲存"}
    F -->|"成功"| G["✅ 設定完成"]
    G --> C

    D -->|"設定分類預算"| H["選擇分類"]
    H --> I["輸入該分類預算金額"]
    I --> F

    D -->|"返回首頁"| J["🏠 儀表板"]
    J --> K{"預算狀態檢查"}
    K -->|"< 80%"| L["✅ 正常（綠色）"]
    K -->|"80% ~ 100%"| M["⚠️ 警告（黃色）"]
    K -->|"> 100%"| N["🚨 超支（紅色）"]
```

---

### 1.5 統計分析流程

```mermaid
flowchart LR
    A["🏠 首頁儀表板"] --> B["點擊「統計分析」"]
    B --> C["📊 統計頁面"]
    C --> D["顯示本月圓餅圖\n+ 分類統計表格"]
    D --> E{"切換月份？"}
    E -->|"是"| F["選擇其他月份"]
    F --> D
    E -->|"否"| G{"查看詳情？"}
    G -->|"是"| H["滑鼠懸停\n顯示金額與佔比"]
    H --> D
    G -->|"否"| I["🏠 返回儀表板"]
```

---

### 1.6 週期性固定支出流程

```mermaid
flowchart LR
    A["🏠 首頁儀表板"] --> B{"有到期提醒？"}
    B -->|"是"| C["🔔 顯示提醒通知"]
    C --> D{"一鍵記帳？"}
    D -->|"是"| E["✅ 自動新增帳目"]
    E --> A
    D -->|"否"| F["稍後處理"]
    F --> A

    B -->|"否"| G["點擊「固定支出」"]
    G --> H["🔁 固定支出管理頁"]
    H --> I{"操作選擇"}
    I -->|"新增"| J["填寫固定支出\n名稱/金額/分類/到期日"]
    J --> K{"儲存"}
    K -->|"成功"| L["✅ 新增完成"]
    L --> H
    I -->|"編輯"| M["修改固定支出"]
    M --> K
    I -->|"暫停/恢復"| N["切換提醒狀態"]
    N --> H
    I -->|"刪除"| O{"確認刪除？"}
    O -->|"確認"| P["🗑️ 刪除完成"]
    P --> H
    O -->|"取消"| H
```

---

### 1.7 使用者註冊與登入流程

```mermaid
flowchart LR
    A(["🌐 開啟網站"]) --> B{"已有帳號？"}

    B -->|"否"| C["點擊「註冊」"]
    C --> D["📝 填寫註冊表單\n帳號/密碼/確認密碼"]
    D --> E{"驗證通過？"}
    E -->|"帳號重複"| F["❌ 帳號已存在"]
    F --> D
    E -->|"密碼不符"| G["❌ 密碼不一致"]
    G --> D
    E -->|"通過"| H["✅ 註冊成功"]
    H --> I["🔑 前往登入頁"]

    B -->|"是"| I
    I --> J["輸入帳號密碼"]
    J --> K{"登入驗證"}
    K -->|"失敗"| L["❌ 帳密錯誤"]
    L --> I
    K -->|"成功"| M["🏠 進入儀表板"]
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 快速記帳序列圖

描述使用者新增一筆帳目的完整資料流：

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as 🎮 Flask Route
    participant Model as 📦 Model
    participant DB as 🗄️ SQLite

    User->>Browser: 點擊「新增帳目」
    Browser->>Flask: GET /transaction/new
    Flask-->>Browser: 渲染記帳表單 (create.html)

    User->>Browser: 填寫表單並送出
    Browser->>Flask: POST /transaction/new
    Flask->>Flask: 驗證表單資料 (Flask-WTF)

    alt 驗證失敗
        Flask-->>Browser: 渲染表單 + 錯誤訊息
    else 驗證成功
        Flask->>Model: 建立 Transaction 物件
        Model->>DB: INSERT INTO transactions
        DB-->>Model: 寫入成功
        Model-->>Flask: 回傳新紀錄
        Flask-->>Browser: 302 重導向到首頁
        Browser->>Flask: GET /
        Flask->>Model: 查詢餘額與近期交易
        Model->>DB: SELECT 統計查詢
        DB-->>Model: 回傳結果
        Model-->>Flask: 回傳資料
        Flask-->>Browser: 渲染儀表板 (index.html)
    end
```

---

### 2.2 歷史帳目搜尋序列圖

描述使用者搜尋並編輯帳目的資料流：

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as 🎮 Flask Route
    participant Model as 📦 Model
    participant DB as 🗄️ SQLite

    User->>Browser: 點擊「歷史帳目」
    Browser->>Flask: GET /transactions
    Flask->>Model: 查詢所有帳目（分頁）
    Model->>DB: SELECT * FROM transactions LIMIT/OFFSET
    DB-->>Model: 回傳帳目清單
    Model-->>Flask: 回傳分頁資料
    Flask-->>Browser: 渲染帳目列表 (list.html)

    User->>Browser: 輸入篩選條件並搜尋
    Browser->>Flask: GET /transactions?date_from=...&category=...&keyword=...
    Flask->>Model: 依條件篩選查詢
    Model->>DB: SELECT ... WHERE 條件
    DB-->>Model: 回傳篩選結果
    Model-->>Flask: 回傳資料
    Flask-->>Browser: 渲染篩選結果

    User->>Browser: 點擊某筆帳目的「編輯」
    Browser->>Flask: GET /transaction/42/edit
    Flask->>Model: 查詢 id=42 的帳目
    Model->>DB: SELECT * FROM transactions WHERE id=42
    DB-->>Model: 回傳帳目
    Model-->>Flask: 回傳資料
    Flask-->>Browser: 渲染編輯表單 (edit.html)

    User->>Browser: 修改內容並儲存
    Browser->>Flask: POST /transaction/42/edit
    Flask->>Flask: 驗證表單資料
    Flask->>Model: 更新 Transaction
    Model->>DB: UPDATE transactions SET ... WHERE id=42
    DB-->>Model: 更新成功
    Flask-->>Browser: 302 重導向到帳目列表
```

---

### 2.3 預算警示檢查序列圖

描述首頁儀表板載入時，系統如何檢查預算狀態：

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as 🎮 Flask Route
    participant Model as 📦 Model
    participant DB as 🗄️ SQLite

    User->>Browser: 進入首頁
    Browser->>Flask: GET /

    Flask->>Model: 查詢本月收支統計
    Model->>DB: SELECT SUM 收入/支出
    DB-->>Model: 回傳統計數據

    Flask->>Model: 查詢使用者預算設定
    Model->>DB: SELECT * FROM budgets
    DB-->>Model: 回傳預算設定

    Flask->>Flask: 比較支出 vs 預算
    Note over Flask: 支出 < 80% → 正常<br/>80%~100% → 黃色警示<br/>> 100% → 紅色警示

    Flask->>Model: 查詢今日到期的固定支出
    Model->>DB: SELECT * FROM recurring WHERE due_day = today
    DB-->>Model: 回傳到期項目

    Flask->>Model: 查詢近期交易
    Model->>DB: SELECT * FROM transactions ORDER BY date DESC LIMIT 10
    DB-->>Model: 回傳交易清單

    Flask-->>Browser: 渲染儀表板 + 警示 + 提醒 (index.html)
```

---

### 2.4 使用者註冊與登入序列圖

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as 🎮 Flask Route
    participant Model as 📦 Model
    participant DB as 🗄️ SQLite

    Note over User, DB: === 註冊流程 ===
    User->>Browser: 點擊「註冊」
    Browser->>Flask: GET /register
    Flask-->>Browser: 渲染註冊表單

    User->>Browser: 填寫帳號密碼並送出
    Browser->>Flask: POST /register
    Flask->>Model: 檢查帳號是否存在
    Model->>DB: SELECT * FROM users WHERE username=?
    DB-->>Model: 查詢結果

    alt 帳號已存在
        Flask-->>Browser: 渲染表單 + 錯誤訊息
    else 帳號可用
        Flask->>Flask: 密碼雜湊處理
        Flask->>Model: 建立 User 物件
        Model->>DB: INSERT INTO users
        DB-->>Model: 寫入成功
        Flask-->>Browser: 302 重導向到登入頁
    end

    Note over User, DB: === 登入流程 ===
    User->>Browser: 輸入帳密並送出
    Browser->>Flask: POST /login
    Flask->>Model: 查詢使用者
    Model->>DB: SELECT * FROM users WHERE username=?
    DB-->>Model: 回傳使用者資料
    Flask->>Flask: 驗證密碼雜湊

    alt 驗證失敗
        Flask-->>Browser: 渲染登入頁 + 錯誤訊息
    else 驗證成功
        Flask->>Flask: 建立 Session (Flask-Login)
        Flask-->>Browser: 302 重導向到首頁
    end
```

---

## 3. 功能清單對照表

| # | 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
|---|---------|---------|-----------|------|
| 1 | 首頁儀表板 | `/` | GET | 顯示餘額、本月收支、近期交易、預算警示、固定支出提醒 |
| 2 | 新增帳目（表單） | `/transaction/new` | GET | 顯示記帳表單 |
| 3 | 新增帳目（送出） | `/transaction/new` | POST | 處理表單送出，新增交易紀錄 |
| 4 | 歷史帳目列表 | `/transactions` | GET | 顯示所有帳目，支援篩選搜尋與分頁 |
| 5 | 編輯帳目（表單） | `/transaction/<id>/edit` | GET | 顯示編輯表單，帶入既有資料 |
| 6 | 編輯帳目（送出） | `/transaction/<id>/edit` | POST | 處理表單送出，更新交易紀錄 |
| 7 | 刪除帳目 | `/transaction/<id>/delete` | POST | 刪除指定帳目（需確認） |
| 8 | 統計分析 | `/statistics` | GET | 顯示圓餅圖與分類統計表格 |
| 9 | 統計資料 API | `/statistics/data` | GET | 回傳指定月份的分類統計 JSON（供 Chart.js 使用） |
| 10 | 預算設定頁面 | `/budget` | GET | 顯示目前預算設定 |
| 11 | 更新預算 | `/budget` | POST | 儲存預算設定 |
| 12 | 固定支出管理 | `/recurring` | GET | 顯示所有週期性支出項目 |
| 13 | 新增固定支出 | `/recurring/new` | POST | 新增週期性支出項目 |
| 14 | 編輯固定支出 | `/recurring/<id>/edit` | POST | 修改固定支出項目 |
| 15 | 刪除固定支出 | `/recurring/<id>/delete` | POST | 刪除固定支出項目 |
| 16 | 暫停/恢復提醒 | `/recurring/<id>/toggle` | POST | 切換固定支出的提醒狀態 |
| 17 | 一鍵記帳 | `/recurring/<id>/record` | POST | 將到期的固定支出轉為實際帳目 |
| 18 | 使用者註冊（表單） | `/register` | GET | 顯示註冊表單 |
| 19 | 使用者註冊（送出） | `/register` | POST | 處理註冊，建立帳號 |
| 20 | 使用者登入（表單） | `/login` | GET | 顯示登入表單 |
| 21 | 使用者登入（送出） | `/login` | POST | 驗證帳密，建立 Session |
| 22 | 使用者登出 | `/logout` | GET | 清除 Session，重導向到登入頁 |

---

> 📌 **下一步**：本文件確認後，進入 **資料庫設計（DB Schema）** 階段。

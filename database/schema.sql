-- ============================================
-- 個人記帳簿 — SQLite 資料庫建表語法
-- 版本：v1.0
-- 建立日期：2026-04-23
-- ============================================

-- 啟用外鍵約束
PRAGMA foreign_keys = ON;

-- --------------------------------------------
-- 1. 使用者資料表 (users)
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
    username        TEXT        NOT NULL UNIQUE,
    password_hash   TEXT        NOT NULL,
    created_at      DATETIME    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- --------------------------------------------
-- 2. 交易紀錄資料表 (transactions)
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER     NOT NULL,
    type            TEXT        NOT NULL CHECK (type IN ('income', 'expense')),
    category        TEXT        NOT NULL,
    amount          REAL        NOT NULL CHECK (amount > 0),
    date            DATE        NOT NULL,
    note            TEXT        DEFAULT '',
    created_at      DATETIME    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at      DATETIME    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- --------------------------------------------
-- 3. 預算設定資料表 (budgets)
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS budgets (
    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER     NOT NULL,
    category        TEXT        DEFAULT NULL,
    amount          REAL        NOT NULL CHECK (amount > 0),
    year            INTEGER     NOT NULL,
    month           INTEGER     NOT NULL CHECK (month BETWEEN 1 AND 12),
    created_at      DATETIME    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at      DATETIME    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (user_id, category, year, month)
);

-- --------------------------------------------
-- 4. 週期性固定支出資料表 (recurring)
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS recurring (
    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER     NOT NULL,
    name            TEXT        NOT NULL,
    category        TEXT        NOT NULL,
    amount          REAL        NOT NULL CHECK (amount > 0),
    due_day         INTEGER     NOT NULL CHECK (due_day BETWEEN 1 AND 31),
    is_active       INTEGER     NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at      DATETIME    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at      DATETIME    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- 索引設計
-- ============================================

-- transactions 索引
CREATE INDEX IF NOT EXISTS idx_transactions_user_id   ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date      ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_category  ON transactions(category);
CREATE INDEX IF NOT EXISTS idx_transactions_type      ON transactions(type);

-- budgets 索引
CREATE INDEX IF NOT EXISTS idx_budgets_user_month     ON budgets(user_id, year, month);

-- recurring 索引
CREATE INDEX IF NOT EXISTS idx_recurring_user_id      ON recurring(user_id);

"""
個人記帳簿 — Transaction Model（交易紀錄模型）

資料表：transactions
用途：儲存每一筆收入或支出的帳目紀錄
"""

from datetime import datetime, date
from app.models import db


# 預設分類清單
INCOME_CATEGORIES = ['薪資', '打工', '獎學金', '投資', '其他收入']
EXPENSE_CATEGORIES = ['餐飲', '交通', '娛樂', '購物', '居住', '醫療', '教育', '其他支出']
ALL_CATEGORIES = INCOME_CATEGORIES + EXPENSE_CATEGORIES


class Transaction(db.Model):
    """交易紀錄資料模型"""

    __tablename__ = 'transactions'

    # ---- 欄位定義 ----
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.Text, nullable=False)          # 'income' 或 'expense'
    category = db.Column(db.Text, nullable=False)       # 分類名稱
    amount = db.Column(db.Float, nullable=False)         # 金額（正數）
    date = db.Column(db.Date, nullable=False)            # 交易日期
    note = db.Column(db.Text, default='')                # 備註
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # ---- CRUD 方法 ----
    @staticmethod
    def create(user_id, type, category, amount, date, note=''):
        """新增一筆交易紀錄

        Args:
            user_id: 使用者 ID
            type: 交易類型 ('income' / 'expense')
            category: 分類名稱
            amount: 金額
            date: 交易日期
            note: 備註（選填）

        Returns:
            Transaction: 新建立的交易紀錄
        """
        txn = Transaction(
            user_id=user_id,
            type=type,
            category=category,
            amount=amount,
            date=date,
            note=note
        )
        db.session.add(txn)
        db.session.commit()
        return txn

    @staticmethod
    def get_all(user_id):
        """取得指定使用者的所有交易紀錄（依日期倒序）"""
        return Transaction.query.filter_by(user_id=user_id) \
            .order_by(Transaction.date.desc(), Transaction.id.desc()).all()

    @staticmethod
    def get_by_id(txn_id):
        """依 ID 取得交易紀錄"""
        return Transaction.query.get(txn_id)

    @staticmethod
    def get_paginated(user_id, page=1, per_page=10, date_from=None, date_to=None,
                      category=None, keyword=None):
        """分頁查詢交易紀錄（支援篩選）

        Args:
            user_id: 使用者 ID
            page: 頁碼（從 1 開始）
            per_page: 每頁筆數
            date_from: 起始日期篩選
            date_to: 結束日期篩選
            category: 分類篩選
            keyword: 備註關鍵字搜尋

        Returns:
            Pagination: SQLAlchemy 分頁物件
        """
        query = Transaction.query.filter_by(user_id=user_id)

        if date_from:
            query = query.filter(Transaction.date >= date_from)
        if date_to:
            query = query.filter(Transaction.date <= date_to)
        if category:
            query = query.filter(Transaction.category == category)
        if keyword:
            query = query.filter(Transaction.note.ilike(f'%{keyword}%'))

        return query.order_by(Transaction.date.desc(), Transaction.id.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_monthly_summary(user_id, year, month):
        """取得指定月份的收支摘要

        Args:
            user_id: 使用者 ID
            year: 年份
            month: 月份

        Returns:
            dict: {'income': 總收入, 'expense': 總支出, 'balance': 餘額}
        """
        from sqlalchemy import func, extract

        income = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)) \
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == 'income',
                extract('year', Transaction.date) == year,
                extract('month', Transaction.date) == month
            ).scalar()

        expense = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)) \
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                extract('year', Transaction.date) == year,
                extract('month', Transaction.date) == month
            ).scalar()

        return {
            'income': float(income),
            'expense': float(expense),
            'balance': float(income) - float(expense)
        }

    @staticmethod
    def get_total_balance(user_id):
        """取得使用者的總餘額（所有時間的總收入 - 總支出）"""
        from sqlalchemy import func

        income = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)) \
            .filter(Transaction.user_id == user_id, Transaction.type == 'income').scalar()

        expense = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)) \
            .filter(Transaction.user_id == user_id, Transaction.type == 'expense').scalar()

        return float(income) - float(expense)

    @staticmethod
    def get_category_summary(user_id, year, month):
        """取得指定月份各分類的支出統計

        Args:
            user_id: 使用者 ID
            year: 年份
            month: 月份

        Returns:
            list[dict]: [{'category': '餐飲', 'total': 3000.0}, ...]
        """
        from sqlalchemy import func, extract

        results = db.session.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            extract('year', Transaction.date) == year,
            extract('month', Transaction.date) == month
        ).group_by(Transaction.category).all()

        return [{'category': r.category, 'total': float(r.total)} for r in results]

    @staticmethod
    def get_recent(user_id, limit=10):
        """取得最近的交易紀錄

        Args:
            user_id: 使用者 ID
            limit: 筆數上限

        Returns:
            list[Transaction]: 交易紀錄列表
        """
        return Transaction.query.filter_by(user_id=user_id) \
            .order_by(Transaction.date.desc(), Transaction.id.desc()) \
            .limit(limit).all()

    def update(self, **kwargs):
        """更新交易紀錄

        Args:
            **kwargs: 要更新的欄位與值
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        """刪除交易紀錄"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Transaction {self.type} {self.category} {self.amount}>'

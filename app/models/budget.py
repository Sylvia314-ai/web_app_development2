"""
個人記帳簿 — Budget Model（預算模型）

資料表：budgets
用途：儲存使用者每月的總預算與各分類預算設定
"""

from datetime import datetime
from app.models import db


class Budget(db.Model):
    """預算設定資料模型"""

    __tablename__ = 'budgets'

    # ---- 欄位定義 ----
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.Text, default=None)          # NULL 表示「每月總預算」
    amount = db.Column(db.Float, nullable=False)           # 預算金額
    year = db.Column(db.Integer, nullable=False)           # 年份
    month = db.Column(db.Integer, nullable=False)          # 月份（1-12）
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # ---- 唯一約束 ----
    __table_args__ = (
        db.UniqueConstraint('user_id', 'category', 'year', 'month', name='uq_budget_user_cat_month'),
    )

    # ---- CRUD 方法 ----
    @staticmethod
    def create(user_id, amount, year, month, category=None):
        """建立預算設定

        Args:
            user_id: 使用者 ID
            amount: 預算金額
            year: 年份
            month: 月份
            category: 分類名稱（None 表示總預算）

        Returns:
            Budget: 新建立的預算
        """
        budget = Budget(
            user_id=user_id,
            category=category,
            amount=amount,
            year=year,
            month=month
        )
        db.session.add(budget)
        db.session.commit()
        return budget

    @staticmethod
    def get_all(user_id, year=None, month=None):
        """取得使用者的所有預算設定

        Args:
            user_id: 使用者 ID
            year: 篩選年份（選填）
            month: 篩選月份（選填）

        Returns:
            list[Budget]: 預算列表
        """
        query = Budget.query.filter_by(user_id=user_id)
        if year:
            query = query.filter_by(year=year)
        if month:
            query = query.filter_by(month=month)
        return query.all()

    @staticmethod
    def get_by_id(budget_id):
        """依 ID 取得預算"""
        return Budget.query.get(budget_id)

    @staticmethod
    def get_monthly_total(user_id, year, month):
        """取得指定月份的總預算

        Args:
            user_id: 使用者 ID
            year: 年份
            month: 月份

        Returns:
            Budget or None: 總預算物件
        """
        return Budget.query.filter_by(
            user_id=user_id,
            category=None,
            year=year,
            month=month
        ).first()

    @staticmethod
    def get_category_budget(user_id, year, month, category):
        """取得指定月份特定分類的預算

        Args:
            user_id: 使用者 ID
            year: 年份
            month: 月份
            category: 分類名稱

        Returns:
            Budget or None: 分類預算物件
        """
        return Budget.query.filter_by(
            user_id=user_id,
            category=category,
            year=year,
            month=month
        ).first()

    @staticmethod
    def set_budget(user_id, amount, year, month, category=None):
        """設定預算（若已存在則更新，否則新增）

        Args:
            user_id: 使用者 ID
            amount: 預算金額
            year: 年份
            month: 月份
            category: 分類名稱（None 表示總預算）

        Returns:
            Budget: 預算物件
        """
        budget = Budget.query.filter_by(
            user_id=user_id,
            category=category,
            year=year,
            month=month
        ).first()

        if budget:
            budget.amount = amount
            budget.updated_at = datetime.now()
        else:
            budget = Budget(
                user_id=user_id,
                category=category,
                amount=amount,
                year=year,
                month=month
            )
            db.session.add(budget)

        db.session.commit()
        return budget

    def update(self, **kwargs):
        """更新預算設定

        Args:
            **kwargs: 要更新的欄位與值
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        """刪除預算設定"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        cat = self.category or '總預算'
        return f'<Budget {cat} {self.amount} ({self.year}/{self.month})>'

"""
個人記帳簿 — Recurring Model（週期性固定支出模型）

資料表：recurring
用途：儲存使用者設定的每月固定支出項目，到期日自動提醒
"""

from datetime import datetime, date
from app.models import db


class Recurring(db.Model):
    """週期性固定支出資料模型"""

    __tablename__ = 'recurring'

    # ---- 欄位定義 ----
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)              # 項目名稱
    category = db.Column(db.Text, nullable=False)           # 分類
    amount = db.Column(db.Float, nullable=False)             # 金額
    due_day = db.Column(db.Integer, nullable=False)          # 每月到期日（1-31）
    is_active = db.Column(db.Integer, nullable=False, default=1)  # 是否啟用（1=啟用, 0=暫停）
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # ---- CRUD 方法 ----
    @staticmethod
    def create(user_id, name, category, amount, due_day):
        """新增週期性固定支出

        Args:
            user_id: 使用者 ID
            name: 項目名稱（例如：房租）
            category: 分類名稱
            amount: 金額
            due_day: 每月到期日（1-31）

        Returns:
            Recurring: 新建立的固定支出項目
        """
        recurring = Recurring(
            user_id=user_id,
            name=name,
            category=category,
            amount=amount,
            due_day=due_day
        )
        db.session.add(recurring)
        db.session.commit()
        return recurring

    @staticmethod
    def get_all(user_id):
        """取得使用者的所有固定支出項目"""
        return Recurring.query.filter_by(user_id=user_id) \
            .order_by(Recurring.due_day).all()

    @staticmethod
    def get_by_id(recurring_id):
        """依 ID 取得固定支出項目"""
        return Recurring.query.get(recurring_id)

    @staticmethod
    def get_due_today(user_id):
        """取得今日到期的固定支出項目（僅啟用中的）

        Args:
            user_id: 使用者 ID

        Returns:
            list[Recurring]: 今日到期的固定支出列表
        """
        today = date.today().day
        return Recurring.query.filter_by(
            user_id=user_id,
            due_day=today,
            is_active=1
        ).all()

    @staticmethod
    def get_active(user_id):
        """取得使用者所有啟用中的固定支出項目"""
        return Recurring.query.filter_by(
            user_id=user_id,
            is_active=1
        ).order_by(Recurring.due_day).all()

    def toggle_active(self):
        """切換啟用 / 暫停狀態"""
        self.is_active = 0 if self.is_active else 1
        self.updated_at = datetime.now()
        db.session.commit()

    def update(self, **kwargs):
        """更新固定支出項目

        Args:
            **kwargs: 要更新的欄位與值
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        """刪除固定支出項目"""
        db.session.delete(self)
        db.session.commit()

    def to_transaction_data(self):
        """將固定支出轉為交易紀錄資料（一鍵記帳用）

        Returns:
            dict: 可直接傳入 Transaction.create() 的參數
        """
        return {
            'type': 'expense',
            'category': self.category,
            'amount': self.amount,
            'date': date.today(),
            'note': f'固定支出：{self.name}'
        }

    def __repr__(self):
        status = '啟用' if self.is_active else '暫停'
        return f'<Recurring {self.name} {self.amount} 每月{self.due_day}日 [{status}]>'

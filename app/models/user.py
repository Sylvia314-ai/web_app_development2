"""
個人記帳簿 — User Model（使用者模型）

資料表：users
用途：儲存使用者帳號與驗證資訊
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db


class User(UserMixin, db.Model):
    """使用者資料模型"""

    __tablename__ = 'users'

    # ---- 欄位定義 ----
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # ---- 關聯定義 ----
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')
    budgets = db.relationship('Budget', backref='user', lazy=True, cascade='all, delete-orphan')
    recurring_items = db.relationship('Recurring', backref='user', lazy=True, cascade='all, delete-orphan')

    # ---- 密碼處理 ----
    def set_password(self, password):
        """將明文密碼轉為雜湊值儲存"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """驗證密碼是否正確"""
        return check_password_hash(self.password_hash, password)

    # ---- CRUD 方法 ----
    @staticmethod
    def create(username, password):
        """建立新使用者

        Args:
            username: 帳號
            password: 明文密碼

        Returns:
            User: 新建立的使用者物件
        """
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all():
        """取得所有使用者"""
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        """依 ID 取得使用者"""
        return User.query.get(user_id)

    @staticmethod
    def get_by_username(username):
        """依帳號取得使用者"""
        return User.query.filter_by(username=username).first()

    def update(self, **kwargs):
        """更新使用者資料

        Args:
            **kwargs: 要更新的欄位與值
        """
        if 'password' in kwargs:
            self.set_password(kwargs.pop('password'))
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """刪除使用者"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'

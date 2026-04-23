"""
個人記帳簿 — 資料模型初始化

匯出所有 SQLAlchemy Model，並提供資料庫初始化功能。
"""

from flask_sqlalchemy import SQLAlchemy

# 建立 SQLAlchemy 實例（在 create_app 中初始化）
db = SQLAlchemy()

# 匯出所有 Model
from app.models.user import User
from app.models.transaction import Transaction
from app.models.budget import Budget
from app.models.recurring import Recurring

__all__ = ['db', 'User', 'Transaction', 'Budget', 'Recurring']

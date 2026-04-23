"""
個人記帳簿 — Flask 應用程式工廠

使用 Application Factory 模式建立 Flask App。
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


def create_app(config_name='default'):
    """建立並設定 Flask 應用程式

    Args:
        config_name: 組態名稱（'development' / 'production' / 'default'）

    Returns:
        Flask: 已設定好的 Flask 應用程式實例
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # ---- 初始化擴充套件 ----
    from app.models import db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_form'
    login_manager.login_message = '請先登入才能使用此功能。'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.get_by_id(int(user_id))

    # ---- 註冊 Blueprint ----
    from app.routes import register_blueprints
    register_blueprints(app)

    # ---- 建立資料庫表格 ----
    with app.app_context():
        db.create_all()

    return app

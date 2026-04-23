"""
個人記帳簿 — 組態設定

區分開發環境與生產環境的組態。
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基礎組態"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 分頁設定
    ITEMS_PER_PAGE = 10

    # 預算警示門檻
    BUDGET_WARNING_THRESHOLD = 0.8   # 80% 黃色警示
    BUDGET_DANGER_THRESHOLD = 1.0    # 100% 紅色警示


class DevelopmentConfig(Config):
    """開發環境"""
    DEBUG = True


class ProductionConfig(Config):
    """生產環境"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

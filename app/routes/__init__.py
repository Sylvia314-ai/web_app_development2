"""
個人記帳簿 — 路由初始化

註冊所有 Blueprint 到 Flask App。
"""


def register_blueprints(app):
    """註冊所有 Blueprint

    Args:
        app: Flask 應用程式實例
    """
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.transaction import bp as transaction_bp
    from app.routes.statistics import bp as statistics_bp
    from app.routes.budget import bp as budget_bp
    from app.routes.recurring import bp as recurring_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(recurring_bp)

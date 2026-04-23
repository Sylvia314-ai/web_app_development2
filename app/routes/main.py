"""
個人記帳簿 — 首頁 / 儀表板路由

Blueprint: main
URL Prefix: /
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    """首頁儀表板

    顯示：
    - 目前總餘額
    - 本月收入合計、支出合計
    - 預算警示（黃色 80% / 紅色 100%）
    - 今日到期的固定支出提醒
    - 最近 10 筆交易紀錄

    處理邏輯：
    1. Transaction.get_total_balance(user_id) → 總餘額
    2. Transaction.get_monthly_summary(user_id, year, month) → 本月收支
    3. Transaction.get_recent(user_id, limit=10) → 近期交易
    4. Budget.get_all(user_id, year, month) → 本月預算設定
    5. 計算預算使用率與警示等級
    6. Recurring.get_due_today(user_id) → 今日到期固定支出

    輸出：渲染 index.html
    """
    pass

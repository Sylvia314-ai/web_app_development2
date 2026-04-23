"""
個人記帳簿 — 預算管理路由

Blueprint: budget
URL Prefix: /
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

bp = Blueprint('budget', __name__)


@bp.route('/budget', methods=['GET'])
@login_required
def settings():
    """預算設定頁面

    輸入：URL 參數 year, month（選填，預設為當月）
    處理邏輯：
    1. Budget.get_all(user_id, year, month) → 取得所有預算設定
    2. Transaction.get_monthly_summary(user_id, year, month) → 取得本月支出
    3. Transaction.get_category_summary(user_id, year, month) → 各分類支出
    4. 計算各預算的使用率
    輸出：渲染 budget/settings.html，傳入預算設定與使用情況
    """
    pass


@bp.route('/budget', methods=['POST'])
@login_required
def settings_submit():
    """處理預算設定表單送出

    輸入：表單欄位 total_amount, category_name[], category_amount[], year, month
    處理邏輯：
    1. Flask-WTF 驗證表單
    2. Budget.set_budget(user_id, total_amount, year, month) → 設定總預算
    3. 迴圈呼叫 Budget.set_budget(user_id, amount, year, month, category) → 各分類預算
    輸出：重導向到 /budget + flash 成功訊息
    錯誤處理：驗證失敗 → 渲染頁面 + 錯誤訊息
    """
    pass

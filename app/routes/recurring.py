"""
個人記帳簿 — 週期性固定支出路由

Blueprint: recurring
URL Prefix: /
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

bp = Blueprint('recurring', __name__)


@bp.route('/recurring')
@login_required
def manage():
    """固定支出管理頁面

    輸入：無
    處理邏輯：Recurring.get_all(user_id) → 取得所有固定支出項目
    輸出：渲染 recurring/manage.html
    """
    pass


@bp.route('/recurring/new', methods=['POST'])
@login_required
def create():
    """新增固定支出

    輸入：表單欄位 name, category, amount, due_day
    處理邏輯：
    1. 驗證表單
    2. Recurring.create(user_id, name, category, amount, due_day)
    輸出：重導向到 /recurring + flash 成功訊息
    錯誤處理：驗證失敗 → 重導向回 /recurring + flash 錯誤
    """
    pass


@bp.route('/recurring/<int:id>/edit', methods=['POST'])
@login_required
def edit(id):
    """編輯固定支出

    輸入：URL 參數 id、表單欄位 name, category, amount, due_day
    處理邏輯：
    1. Recurring.get_by_id(id) 取得項目
    2. 檢查項目是否屬於 current_user
    3. recurring.update(name=..., category=..., amount=..., due_day=...)
    輸出：重導向到 /recurring
    錯誤處理：項目不存在 → 404
    """
    pass


@bp.route('/recurring/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """刪除固定支出

    輸入：URL 參數 id
    處理邏輯：
    1. Recurring.get_by_id(id) 取得項目
    2. 檢查項目是否屬於 current_user
    3. recurring.delete()
    輸出：重導向到 /recurring
    錯誤處理：項目不存在 → 404
    """
    pass


@bp.route('/recurring/<int:id>/toggle', methods=['POST'])
@login_required
def toggle(id):
    """暫停 / 恢復固定支出提醒

    輸入：URL 參數 id
    處理邏輯：
    1. Recurring.get_by_id(id) 取得項目
    2. 檢查項目是否屬於 current_user
    3. recurring.toggle_active()
    輸出：重導向到 /recurring
    錯誤處理：項目不存在 → 404
    """
    pass


@bp.route('/recurring/<int:id>/record', methods=['POST'])
@login_required
def record(id):
    """一鍵記帳（將固定支出轉為實際帳目）

    輸入：URL 參數 id
    處理邏輯：
    1. Recurring.get_by_id(id) 取得項目
    2. 檢查項目是否屬於 current_user
    3. recurring.to_transaction_data() 取得交易資料
    4. Transaction.create(user_id, **data) 建立實際帳目
    輸出：重導向到 / + flash 成功訊息
    錯誤處理：項目不存在 → 404
    """
    pass

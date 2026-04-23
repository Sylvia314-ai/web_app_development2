"""
個人記帳簿 — 交易紀錄路由

Blueprint: transaction
URL Prefix: /
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

bp = Blueprint('transaction', __name__)


@bp.route('/transaction/new', methods=['GET'])
@login_required
def create_form():
    """顯示新增帳目表單

    輸入：無
    處理邏輯：建立空白記帳表單，帶入預設分類清單
    輸出：渲染 transaction/create.html
    """
    pass


@bp.route('/transaction/new', methods=['POST'])
@login_required
def create_submit():
    """處理新增帳目表單送出

    輸入：表單欄位 type, category, amount, date, note
    處理邏輯：
    1. Flask-WTF 驗證表單
    2. Transaction.create(user_id, type, category, amount, date, note)
    輸出：成功 → 重導向到 / + flash 成功訊息
    錯誤處理：驗證失敗 → 渲染表單 + 錯誤訊息
    """
    pass


@bp.route('/transactions')
@login_required
def list_transactions():
    """歷史帳目列表（含搜尋篩選與分頁）

    輸入：URL 參數 page, date_from, date_to, category, keyword
    處理邏輯：
    1. 解析篩選條件
    2. Transaction.get_paginated(user_id, page, per_page, date_from, date_to, category, keyword)
    輸出：渲染 transaction/list.html，傳入分頁結果與篩選條件
    """
    pass


@bp.route('/transaction/<int:id>/edit', methods=['GET'])
@login_required
def edit_form(id):
    """顯示編輯帳目表單

    輸入：URL 參數 id
    處理邏輯：
    1. Transaction.get_by_id(id) 取得帳目
    2. 檢查帳目是否屬於 current_user
    3. 將資料帶入編輯表單
    輸出：渲染 transaction/edit.html
    錯誤處理：帳目不存在 → 404；不是自己的 → 403
    """
    pass


@bp.route('/transaction/<int:id>/edit', methods=['POST'])
@login_required
def edit_submit(id):
    """處理編輯帳目表單送出

    輸入：URL 參數 id、表單欄位 type, category, amount, date, note
    處理邏輯：
    1. 取得帳目並驗證權限
    2. Flask-WTF 驗證表單
    3. txn.update(type=..., category=..., amount=..., date=..., note=...)
    輸出：成功 → 重導向到 /transactions + flash 成功訊息
    錯誤處理：帳目不存在 → 404；驗證失敗 → 渲染表單 + 錯誤
    """
    pass


@bp.route('/transaction/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """刪除帳目

    輸入：URL 參數 id
    處理邏輯：
    1. Transaction.get_by_id(id) 取得帳目
    2. 檢查帳目是否屬於 current_user
    3. txn.delete()
    輸出：重導向到 /transactions + flash 刪除成功訊息
    錯誤處理：帳目不存在 → 404；不是自己的 → 403
    """
    pass

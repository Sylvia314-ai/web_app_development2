"""
個人記帳簿 — 使用者驗證路由

Blueprint: auth
URL Prefix: /
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET'])
def register_form():
    """顯示註冊表單

    輸入：無
    處理邏輯：建立空白註冊表單
    輸出：渲染 auth/register.html
    錯誤處理：已登入 → 重導向到 /
    """
    pass


@bp.route('/register', methods=['POST'])
def register_submit():
    """處理註冊表單送出

    輸入：表單欄位 username, password, confirm_password
    處理邏輯：
    1. Flask-WTF 驗證表單
    2. 檢查 password == confirm_password
    3. User.get_by_username(username) 確認帳號不重複
    4. User.create(username, password) 建立帳號
    輸出：成功 → 重導向到 /login + flash 成功訊息
    錯誤處理：帳號重複 → 渲染表單 + 錯誤；驗證失敗 → 渲染表單 + 錯誤
    """
    pass


@bp.route('/login', methods=['GET'])
def login_form():
    """顯示登入表單

    輸入：無
    處理邏輯：建立空白登入表單
    輸出：渲染 auth/login.html
    錯誤處理：已登入 → 重導向到 /
    """
    pass


@bp.route('/login', methods=['POST'])
def login_submit():
    """處理登入表單送出

    輸入：表單欄位 username, password
    處理邏輯：
    1. User.get_by_username(username) 查詢使用者
    2. user.check_password(password) 驗證密碼
    3. login_user(user) 建立 Session
    輸出：成功 → 重導向到 /
    錯誤處理：帳密錯誤 → 渲染登入頁 + 錯誤訊息
    """
    pass


@bp.route('/logout')
@login_required
def logout():
    """使用者登出

    輸入：無
    處理邏輯：logout_user() 清除 Session
    輸出：重導向到 /login
    """
    pass

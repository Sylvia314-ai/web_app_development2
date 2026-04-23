"""
個人記帳簿 — 使用者驗證路由

Blueprint: auth
URL Prefix: /
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth_forms import RegisterForm, LoginForm
from app.models.user import User

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET'])
def register_form():
    """顯示註冊表單"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    return render_template('auth/register.html', form=form)


@bp.route('/register', methods=['POST'])
def register_submit():
    """處理註冊表單送出"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        # User.create creates the user and hashes the password
        User.create(username=form.username.data, password=form.password.data)
        flash('註冊成功！請登入。', 'success')
        return redirect(url_for('auth.login_form'))
        
    # 驗證失敗的錯誤訊息（也可在前端模板直接印出 form.errors）
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'danger')
            
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET'])
def login_form():
    """顯示登入表單"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@bp.route('/login', methods=['POST'])
def login_submit():
    """處理登入表單送出"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('登入成功！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('帳號或密碼錯誤。', 'danger')
            
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    """使用者登出"""
    logout_user()
    flash('您已成功登出。', 'success')
    return redirect(url_for('auth.login_form'))

"""
個人記帳簿 — 統計分析路由

Blueprint: statistics
URL Prefix: /
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

bp = Blueprint('statistics', __name__)


@bp.route('/statistics')
@login_required
def overview():
    """統計分析頁面

    輸入：URL 參數 year, month（選填，預設為當月）
    處理邏輯：
    1. Transaction.get_category_summary(user_id, year, month) → 分類統計
    2. Transaction.get_monthly_summary(user_id, year, month) → 月收支摘要
    輸出：渲染 statistics/overview.html，傳入統計資料
    """
    pass


@bp.route('/statistics/data')
@login_required
def data():
    """統計資料 API（JSON）

    輸入：URL 參數 year, month
    處理邏輯：
    1. Transaction.get_category_summary(user_id, year, month)
    輸出：JSON 格式的分類統計資料，供 Chart.js 前端使用
    格式：{
        "labels": ["餐飲", "交通", ...],
        "data": [3000, 1500, ...],
        "total": 8500
    }
    錯誤處理：參數缺失 → 回傳 400 JSON 錯誤
    """
    pass

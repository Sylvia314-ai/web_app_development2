"""
個人記帳簿 — 工具函式

提供日期處理、金額格式化等輔助功能。
"""

from datetime import datetime, date


def format_currency(amount):
    """格式化金額為千分位格式

    Args:
        amount: 金額數值

    Returns:
        str: 格式化後的金額字串，例如 '1,234'
    """
    return '{:,.0f}'.format(amount)


def get_current_year_month():
    """取得當前年份與月份

    Returns:
        tuple: (year, month)
    """
    today = date.today()
    return today.year, today.month


def parse_date(date_str):
    """解析日期字串為 date 物件

    Args:
        date_str: 日期字串，格式為 'YYYY-MM-DD'

    Returns:
        date: 日期物件，解析失敗回傳 None
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None

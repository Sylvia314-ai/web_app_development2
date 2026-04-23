from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.transaction import Transaction
from app.models.budget import Budget
from app.models.recurring import Recurring
from datetime import date

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    today = date.today()
    balance = Transaction.get_total_balance(current_user.id)
    monthly = Transaction.get_monthly_summary(current_user.id, today.year, today.month)
    recent = Transaction.get_recent(current_user.id, limit=5)
    budget = Budget.get_monthly_total(current_user.id, today.year, today.month)
    due_today = Recurring.get_due_today(current_user.id)
    
    return render_template('index.html', 
        balance=balance, 
        monthly=monthly, 
        recent=recent, 
        budget=budget, 
        due_today=due_today)

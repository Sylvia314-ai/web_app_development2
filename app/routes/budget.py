from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.budget import Budget
from app.forms.budget_forms import BudgetForm
from datetime import date

bp = Blueprint('budget', __name__, url_prefix='/budget')

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = BudgetForm()
    today = date.today()
    current_budget = Budget.get_monthly_total(current_user.id, today.year, today.month)
    
    if form.validate_on_submit():
        Budget.set_budget(
            user_id=current_user.id,
            amount=form.amount.data,
            year=form.year.data,
            month=form.month.data
        )
        flash('預算設定成功！', 'success')
        return redirect(url_for('budget.settings'))
        
    if request.method == 'GET':
        form.year.data = today.year
        form.month.data = today.month
        if current_budget:
            form.amount.data = current_budget.amount
            
    return render_template('budget/settings.html', form=form, current_budget=current_budget)

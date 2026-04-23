from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.recurring import Recurring
from app.forms.recurring_forms import RecurringForm

bp = Blueprint('recurring', __name__, url_prefix='/recurring')

@bp.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    form = RecurringForm()
    if form.validate_on_submit():
        Recurring.create(
            user_id=current_user.id,
            name=form.name.data,
            category=form.category.data,
            amount=form.amount.data,
            due_day=form.due_day.data
        )
        flash('固定支出設定成功！', 'success')
        return redirect(url_for('recurring.manage'))
        
    items = Recurring.get_all(current_user.id)
    return render_template('recurring/manage.html', form=form, items=items)

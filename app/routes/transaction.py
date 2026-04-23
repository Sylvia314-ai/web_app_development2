from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.transaction import Transaction
from app.forms.transaction_forms import TransactionForm
from datetime import date

bp = Blueprint('transaction', __name__, url_prefix='/transaction')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TransactionForm()
    if request.method == 'GET':
        form.date.data = date.today()
        
    if form.validate_on_submit():
        Transaction.create(
            user_id=current_user.id,
            type=form.type.data,
            category=form.category.data,
            amount=form.amount.data,
            date=form.date.data,
            note=form.note.data
        )
        flash('記帳成功！', 'success')
        return redirect(url_for('transaction.list_all'))
    return render_template('transaction/create.html', form=form)

@bp.route('/list')
@login_required
def list_all():
    transactions = Transaction.get_all(current_user.id)
    return render_template('transaction/list.html', transactions=transactions)

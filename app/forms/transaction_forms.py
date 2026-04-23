from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired
from app.models.transaction import INCOME_CATEGORIES, EXPENSE_CATEGORIES

class TransactionForm(FlaskForm):
    type = SelectField('類型', choices=[('expense', '支出'), ('income', '收入')], validators=[DataRequired()])
    category = SelectField('分類', choices=[], validators=[DataRequired()])
    amount = FloatField('金額', validators=[DataRequired()])
    date = DateField('日期', validators=[DataRequired()])
    note = StringField('備註')
    submit = SubmitField('儲存')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(c, c) for c in INCOME_CATEGORIES + EXPENSE_CATEGORIES]

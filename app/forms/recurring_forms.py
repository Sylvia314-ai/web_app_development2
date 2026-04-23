from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models.transaction import EXPENSE_CATEGORIES

class RecurringForm(FlaskForm):
    name = StringField('項目名稱', validators=[DataRequired()])
    category = SelectField('分類', choices=[(c, c) for c in EXPENSE_CATEGORIES], validators=[DataRequired()])
    amount = FloatField('金額', validators=[DataRequired()])
    due_day = IntegerField('每月到期日 (1-31)', validators=[DataRequired()])
    submit = SubmitField('新增固定支出')

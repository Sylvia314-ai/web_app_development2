from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class BudgetForm(FlaskForm):
    year = IntegerField('年份', validators=[DataRequired()])
    month = IntegerField('月份 (1-12)', validators=[DataRequired()])
    amount = FloatField('總預算金額', validators=[DataRequired()])
    submit = SubmitField('設定預算')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models.user import User

class RegisterForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('密碼', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('確認密碼', validators=[DataRequired(), EqualTo('password', message='密碼不一致')])
    submit = SubmitField('註冊')

    def validate_username(self, field):
        if User.get_by_username(field.data):
            raise ValidationError('此帳號已被使用，請選擇另一個帳號')

class LoginForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    submit = SubmitField('登入')

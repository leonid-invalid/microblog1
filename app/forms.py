from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить это устройство')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Данный логин уже есть в системе.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Данный адрес уже зарегестрирован.')

class EditProfileForm(FlaskForm):
    username = StringField('Новое имя:', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне:', validators=[Length(min=0, max=140)])
    submit = SubmitField('Сохранить')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Данный логин уже есть в системе.')

class PostForm(FlaskForm):
    post = TextAreaField('Новый пост:', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Отправить')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Запросить сброс пароля')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Обновить пароль')
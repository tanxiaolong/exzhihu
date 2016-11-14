# coding=utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Email, EqualTo, Required, Length, Regexp
from ..models import User


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1,64), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegistrationForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField(u'用户名（不少于8位）', validators=[Required(), Length(8, 64)])
    password = PasswordField(u'密码（不少于8位）', validators=[Required(), Length(8, 64),
                                                       EqualTo('password2', message=u'两次密码不相同')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册,请换一个试试')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被注册,请换一个试试')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'当前密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message=u'密码必须相同')])
    password2 = PasswordField(u'确认新密码', validators=[Required()])
    submit = SubmitField(u'更新密码')


class ResetPasswordRequestForm(Form):
    email = StringField(u'注册邮箱', validators=[Required(), Email()])
    submit = SubmitField(u'找回密码')


class ResetPasswordForm(Form):
    email = StringField(u'注册邮箱', validators=[Required(), Email()])
    password = PasswordField(u'新密码', validators=[Required(), EqualTo('password2', message=u'两次密码不相同')])
    password2 = PasswordField(u'确认新密码', validators=[Required()])
    submit = SubmitField(u'修改密码')


class ChangeEmailForm(Form):
    email = StringField(u'新邮箱', validators=[Required(), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'修改邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册,请换一个试试')
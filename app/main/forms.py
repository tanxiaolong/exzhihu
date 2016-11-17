# coding=utf-8
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, StringField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User, Role


class EditProfileForm(Form):
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'所在地', validators=[Length(0, 64)])
    about_me = TextAreaField(u'简介')
    submit = SubmitField(u'修改资料')


class EditProfileAdminForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp(u'^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名只能是字母或数字的组合')])
    confirmed = BooleanField(u'已确认')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'所在地', validators=[Length(0, 64)])
    about_me = TextAreaField(u'简介')
    submit = SubmitField(u'修改资料')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.rolename)
                             for role in Role.query.order_by(Role.rolename).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册,请重新输入')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已存在,请重新输入')


class PostQuestionForm(Form):
    title = StringField(u'写下你的问题', validators=[Required(), Length(0, 64)])
    body = TextAreaField(u'问题背景、条件等详细信息（可选）')
    submit = SubmitField(u'发布问题')


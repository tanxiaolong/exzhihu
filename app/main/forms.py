# coding=utf-8
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required

class SearchForm(Form):
    search_text = TextAreaField(u'搜索你感兴趣的内容…')
    submit = SubmitField(u'搜索')
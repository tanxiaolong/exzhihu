# coding=utf-8

from datetime import datetime

from flask import render_template, session, redirect, url_for

from . import main
from .forms import SearchForm
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        session['search_text'] = form.search_text.data
        return redirect(url_for('.index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, search_text=session.get('search_text'))



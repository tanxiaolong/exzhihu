# coding=utf-8

from datetime import datetime

from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user, current_app
from . import main
from ..decorators import admin_required
from ..models import User, Role, Permission, Question, Answer
from .forms import EditProfileForm, EditProfileAdminForm, PostQuestionForm, AnswerForm
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostQuestionForm()
    if current_user.can(Permission.POST) and \
            form.validate_on_submit():
        question = Question(title=form.title.data,
                            body=form.body.data,
                            asker=current_user._get_current_object())
        db.session.add(question)
        return redirect(url_for('.index'))
    # questions = Question.query.order_by(Question.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.timestamp.desc()).paginate(
        page, per_page=current_app.config.get('FLASKY_POSTS_PER_PAGE', 10), error_out=False)
    questions = pagination.items
    return render_template('index.html', form=form, questions=questions, pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    questions = user.questions.order_by(Question.timestamp.desc()).all()
    return render_template('user.html', user=user, questions=questions)


@main.route('/edit-profile', methods=['GET', 'HOST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me
        db.session.add(current_user)
        flash(u'你的资料已修改')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash(u'资料已更新')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    question = Question.query.get_or_404(id)
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(question=question,
                        body=form.body.data,
                        author=current_user._get_current_object())
        db.session.add(answer)
        flash(u'你的回答已发布')
        return redirect(url_for('.question', id=question.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (question.answers.count() -1)/current_app.config.get('FLASKY_POSTS_PER_PAGE', 10) + 1
    pagination = question.answers.order_by(Answer.timestamp.asc()).paginate(
        page, per_page=current_app.config.get('FLASKY_POSTS_PER_PAGE', 10), error_out=False)
    answers = pagination.items
    return render_template('question.html', question=question, questions=[question], answers=answers, pagination=pagination, form=form)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    question = Question.query.get_or_404(id)
    if current_user != question.asker and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostQuestionForm()
    if form.validate_on_submit():
        question.title = form.title.data
        question.body = form.body.data
        db.session.add(question)
        flash(u'问题已更新')
        return redirect(url_for('question', id=question.id))
    form.title.data = question.title
    form.body.data = question.body
    return render_template('edit_question.html', form=form)
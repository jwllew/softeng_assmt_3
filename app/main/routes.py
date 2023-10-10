from datetime import datetime
from flask import url_for, render_template, flash, redirect, request, jsonify
import random, re
# from app.forms import LoginForm, RegistrationForm, CommentForm, ProjectForm, UserEditor, DeleteProjectForm, DeleteCommentForm
# from flask_login import current_user, login_user, logout_user, login_required

# from werkzeug import NotFound, Unauthorized
from werkzeug.wrappers.request import Request
from werkzeug.exceptions import HTTPException, NotFound, Unauthorized
from werkzeug.urls import url_parse
from app.models import User, QuestionOne, Module
from app.main import bp


@bp.route("/", methods=['GET', 'POST'])
# defaults the URL to home
def urltohome():
    return redirect(url_for('main.home'))

@bp.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('index.html', title='Dashboard')

@bp.route("/assessments", methods=['GET', 'POST'])
def assessments():
    return render_template('assessments.html', title='Assessments')

@bp.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Log in')

@bp.route("/register", methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    return render_template('register.html', title='Register')

# will not work until user db is populated, current_user imported into routes
# @bp.route("/user/<username>", methods=['GET', 'POST'])
# @login_required
# def user(username):
#     return render_template('user.html', title='Userpage', user=user)


@bp.route("/modules", methods=['GET', 'POST'])
def modules():
    return render_template('modules.html', title='Modules')

@bp.route("/question_one/create")
def question_one_create():
    question_id = ''
    function = 'createQuestion()'
    return render_template('questions/create_question_one.html', question_id=question_id, func=function)

@bp.route("/question_one/<int:id>")
def question_one(id):
    return render_template('questions/question_one.html', question_id=id)

@bp.route("/question_one/edit/<int:id>")
def question_one_edit(id):
    function = 'saveEdit(' + str(id) + ')'
    return render_template('questions/create_question_one.html', func=function, question_id=id)

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
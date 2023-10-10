from app.api import bp
from app import db
from flask import jsonify, request, url_for, abort
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import QuestionOne, Module

@bp.route('/question_one/<int:id>', methods=['GET'])
def get_question_one(id):
    return jsonify(QuestionOne.query.get_or_404(id).to_dict())

@bp.route('/question_one', methods=['GET'])
#@token_auth.login_required
def get_question_ones():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = QuestionOne.to_collection_dict(QuestionOne.query, page, per_page, 'api.get_question_ones')
    return jsonify(data)

@bp.route('/question_one/module/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_question_one_module(id):
    questions = QuestionOne.query.filter_by(module_id=id)
    data = {
        'items': [item.to_dict() for item in questions],
    }
    return jsonify(data)

@bp.route('/question_one/author/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_question_one_author(id):
    questions = QuestionOne.query.filter_by(author_id=id)
    data = {
        'items': [item.to_dict() for item in questions],
    }
    return jsonify(data)

@bp.route('/question_one/<int:id>/mark', methods=['POST'])
def mark_question_one(id):
    data = request.get_json() or {}
    question = QuestionOne.query.get_or_404(id).to_dict()
    marks = {
        'question_mark':{}
    }

    marks['answer'] = question['answers']
    marks['num_blanks'] = question['num_blanks']
    marks['total_marks'] = question['total_marks']

    mark = 0
    correct = 0

    for key in data['answers']:
        if data['answers'][key].lower() == question['answers'][key][0].lower():
            marks['question_mark'][key] = question['answers'][key][1]
            mark += int(question['answers'][key][1])
            correct += 1
        else:
            marks['question_mark'][key] = 0

    marks['mark'] = mark
    marks['correct'] = correct

    return jsonify(marks)

@bp.route('/question_one', methods=['POST'])
#@token_auth.login_required
def create_question_one():
    data = request.get_json() or {}
    question = QuestionOne()
    question.from_dict(data)
    db.session.add(question)
    db.session.commit()
    response = jsonify(question.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_question_one', id=question.id)
    return response

@bp.route('/question_one/<int:id>', methods=['PUT'])
def update_question_one(id):
    data = request.get_json() or {}
    question = QuestionOne.query.get_or_404(id)

    #if question.author_id != token_auth.current_user().id:
    #    abort(403)

    question.from_dict(data)
    db.session.commit()
    response = jsonify(question.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_question_one', id=question.id)
    return response

@bp.route('/question_one/<int:id>', methods=['DELETE'])
def delete_question_one(id):
    question = QuestionOne.query.get_or_404(id)

    #if question.author_id != token_auth.current_user().id:
    #    abort(403)

    db.session.delete(question)
    db.session.commit()
    
    data = {
        'message':'Successfully deleted question type one'
    }

    return jsonify(data)

#HTTP Method	Resource URL	Notes
#GET	/api//question_one/<int:id>	Return a question.
#GET	/api/question_one	Return the collection of all questions.
#GET	/api/question_one/<int:id>/mark	Return weather the question is marked right.
#GET	/api/users/<id>/followed	Return the users this user is following.
#POST	/api/question_one	Register a new user question.
#PUT	/api/question_one/<int:id>	Modify a question.
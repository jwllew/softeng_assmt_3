from app.api import bp
from app import db
from flask import jsonify, request, url_for
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User

@bp.route('/users/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
#@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

@bp.route('/users/teacher', methods=['GET'])
#@token_auth.login_required
def get_users_teacher():
    teacher = User.query.filter_by(is_teacher='True')
    data = {
        'items': [{'id': item.to_dict()['id'], 'name': item.to_dict()['username']} for item in teacher],
    }
    return jsonify(data)
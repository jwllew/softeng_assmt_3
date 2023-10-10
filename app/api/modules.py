from app.api import bp
from app import db
from flask import jsonify, request, url_for
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Module

@bp.route('/module/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_subject(id):
    return jsonify(Module.query.get_or_404(id).to_dict())


@bp.route('/modules', methods=['GET'])
#@token_auth.login_required
def get_subjects():
    modules = Module.query
    data = {
        'items': [item.to_dict() for item in modules],
    }
    return jsonify(data)

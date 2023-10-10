from app.api import bp

@bp.route('/question_two/<int:id>', methods=['GET'])
def get_question_two(id):
    pass

@bp.route('/question_two', methods=['GET'])
def get_questions_two():
    pass

@bp.route('/question_two/<int:id>/mark', methods=['GET'])
def mark_question_two(id):
    pass

@bp.route('/question_two', methods=['POST'])
def create_question_two():
    pass

@bp.route('/question_two/<int:id>', methods=['PUT'])
def update_question_two(id):
    pass
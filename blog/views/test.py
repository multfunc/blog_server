from flask import Blueprint, request, jsonify, json
from blog.models.base import db
from flask_cors import CORS

test_bp = Blueprint('test', __name__, url_prefix='/test')
CORS(test_bp)

@test_bp.route('/1', methods=['GET'])
# @cross_origin()  # 置于route后
def test_1():
    """

    :return:
    """
    return "<body>hh</body>"

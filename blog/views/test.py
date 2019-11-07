from flask import Blueprint, request, jsonify, json
from blog.models.base import db
from flask_cors import CORS

test_bp = Blueprint('test', __name__, url_prefix='/test')
CORS(test_bp)

@test_bp.route('/token', methods=['POST'])
def token():
    """

    :return:
    """
    response_body = {
        "status": False,
        "data": None
    }
    request_body = json.loads(request.data)
    #request_body = request.get_json()
    try:
        token=request.headers["Authorization"]
        print("token->",token)
        response_body['status'] = True
        response_body['data'] = None
    except Exception as e:
        print(e)
    return jsonify(response_body)

@test_bp.route('/1', methods=['GET'])
# @cross_origin()  # 置于route后
def test_1():
    """

    :return:
    """
    return "<body>hh</body>"


@test_bp.route('/2', methods=['POST'])
def test_2():
    """

    :return:
    """
    response_body = {
        "status": False,
        "data": None
    }
    request_body = json.loads(request.data)
    # request_body = request.get_json()
    try:
        with open(file="电视剧详情页链接.json", mode="w", encoding="utf8") as f:
            json.dump(request_body, f)
        response_body['status'] = True
    except Exception as e:
        print(e)
    return jsonify(response_body)

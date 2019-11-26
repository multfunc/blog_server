from flask import Blueprint, request, jsonify, json
from blog.models.base import db
from flask_cors import CORS
import base64
from time import sleep

from blog.utils.rsa_utils import rsa_utils

test_bp = Blueprint('test', __name__, url_prefix='/test')
CORS(test_bp)

@test_bp.route('/js', methods=['POST','GET'])
def js():
    """

    :return:
    """
    response_body = {
        "status": False,
        "data": None
    }
    # request_body = json.loads(request.data)
    try:

        response_body['status'] = True
        response_body['data'] = None
    except Exception as e:
        print(e)
    sleep(2)
    return jsonify(response_body)

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
        token=base64.b64decode(bytes(token.encode("utf8")))
        print("token->",token)

        de_token=rsa_utils.decrypt_by_PKS1_OAEP(token)
        print("decrypt->",de_token)
        print(b'admin'==de_token)

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

from flask import Blueprint, request, jsonify, json, url_for, app
from blog.models.base import db
from flask_cors import CORS
import base64
from time import sleep
from datetime import datetime
import os, sys, random, string

from blog.utils.rsa_utils import rsa_utils
# from blog.GQL.dimension_note_reading import dimension_note_reading_schema as schema
from blog.GQL_schema.schema import GQL_schema as schema

test_bp = Blueprint('test', __name__, url_prefix='/test')
CORS(test_bp)

# upload image
basedir = os.path.abspath((os.path.dirname(__file__)))  # 定义一个根目录 用于保存图片用
basedir = 'F:\\workspace-python-flask\\blog_server\\blog'  # 定义一个根目录 用于保存图片用


@test_bp.route('/upload', methods=['POST', 'GET'])
def upload():
    """
    upload image
    :return:
    """
    try:
        # 生成随机字符串，防止图片名字重复
        ran_str = ''.join((random.sample(string.ascii_letters + string.digits, 16)))
        # 获取图片文件夹 name = upload
        tmp = request
        img = request.files.get('file')
        # 定义一个图片存放的位置 存放在static下面
        path = basedir + "/static/img/"
        # 图片名称 给图片重命名 为了图片名称的唯一性
        imgName = ran_str + img.filename
        # 图片path和名称组成图片的保存路径
        file_path = path + imgName
        # 保存图片
        img.save(file_path)
        # 这个是图片的访问路径，需返回前端（可有可无）
        url = 'http://127.0.0.1:5000/static/img/' + imgName
        return jsonify({
            "name": imgName,
            "status": "done",
            "url": url,
            "thumbUrl": url
        })
    except Exception as e:
        print(e)


@test_bp.route('/cbbpa', methods=['POST'])
def cbbpa():
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
        teleplay_data = request_body.get('teleplay_data', None)
        response_body['status'] = True
        response_body['data'] = teleplay_data
        tmp = str(datetime.now()).replace(' ', '_').replace('.', '_').replace(':', '_')
        with open(f'C:/Users/hejun/Desktop/剧目资料单{tmp}.txt', mode='w', encoding='utf8') as file:
            file.write(str(teleplay_data))
    except Exception as e:
        print(e)
    return jsonify(response_body)


@test_bp.route('/graph_ql', methods=['get'])
def graph_ql():
    """

    :return:
    """
    response_body = {
        "status": False,
        "data": None
    }
    # request_body = json.loads(request.data)
    # request_body = request.get_json()
    try:

        query = """
            query{
                dimensionNoteReadings(limit:10,offset:20){
                    note,
                    create
                }
            }
        """
        result = schema.execute(query, context_value={'session': db.session})
        print(result.errors)
        result = result.data

        response_body['status'] = True
        response_body['data'] = result
        print(result)
    except Exception as e:
        print(e)
    return jsonify(response_body)


@test_bp.route('/js', methods=['POST', 'GET'])
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
        response_body['data'] = {
            "current": datetime.now()
        }
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
    # request_body = request.get_json()
    try:
        my_request = request
        token = request.headers["Authorization"]
        token = base64.b64decode(bytes(token.encode("utf8")))
        print("token->", token)

        de_token = rsa_utils.decrypt_by_PKS1_OAEP(token)
        print("decrypt->", de_token)
        print(b'admin' == de_token)

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

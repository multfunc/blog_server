from flask import request, json, jsonify, Blueprint,app,current_app
from flask_cors import *
from sqlalchemy import func

import base64
from datetime import datetime

from blog.utils.rsa_utils import rsa_utils
from blog.models.base import db
from blog.models.dimension_note_reading import DimensionNoteReading

# graph_ql schema
from blog.GQL_schema.schema import GQL_schema

notification_your_bp = Blueprint('notification_your', __name__, url_prefix='/blog/notification_your')

@notification_your_bp.before_request
def authority_verify():
    tmp=request

    print('authority verify2')
    print(request.remote_addr)
    print(request.remote_user)
    print("=================")


@notification_your_bp.route('/gql', methods=['POST'])
@cross_origin()  # 置于route后
def gql():
    """
    
    :return: 
    """
    response_body = {
        "status": False,
        "gql": None
    }
    request_body = json.loads(request.data)
    # request_body = request.get_json()
    try:
        GQL_query = request_body.get("query", None)
        GQL_result = GQL_schema.execute(GQL_query, context={'session': db.session})
        print(GQL_result.errors)
        GQL_result = GQL_result.data
        print(GQL_result)
        response_body['status'] = True
        response_body['gql'] = GQL_result
    except Exception as e:
        print(e)
    return jsonify(response_body)


@notification_your_bp.route('/note_reading_query', methods=['POST'])
@cross_origin()  # 置于route后
def note_reading_query():
    """
    
    :return: 
    """
    response_body = {
        "status": False,
        "data": {
            "data": None,
            "message": None
        }
    }
    request_body = json.loads(request.data)
    # request_body = request.get_json()
    try:
        page_size = request_body.get('page_size', 10)
        page_index = request_body.get('page_index', 1)
        results = db.session.query(DimensionNoteReading).order_by(DimensionNoteReading.create.desc()).limit(
            page_size).offset((page_index - 1) * page_size)
        tmp = []
        for result in results:
            tmp.append({
                "id": result.id,
                "origin_name_book": result.origin_name_book,
                "origin_author_book": result.origin_author_book,
                'origin_page_book': result.origin_page_book,
                'note': result.note,
                'category': result.category,
                'modified': result.modified
            })
        response_body['status'] = True
        response_body['data']['data'] = tmp
    except Exception as e:
        print(e)
    return jsonify(response_body)


@notification_your_bp.route('/tool_tip_category_and_author', methods=['POST'])
@cross_origin()  # 置于route后
def tool_tip_category_and_author():
    """
    根据书名获取详细信息
    :return:
    """
    response_body = {
        "status": False,
        "data": {
            "detail": None
        }
    }
    request_body = json.loads(request.data)
    # request_body = request.get_json()
    try:
        token = request.headers['Authorization']
        token = base64.b64decode(bytes(token.encode('utf8')))
        print("save-token: ", token)
        de_token = rsa_utils.decrypt_by_PKS1_OAEP(token)
        print("save-detoken ", de_token)
        if b'admin' != de_token:
            response_body['status'] = False
            response_body['data']['message'] = '非法请求'
            return jsonify(response_body)
        origin_name_book = request_body.get('origin_name_book', None)
        dimension_note_reading = db.session.query(DimensionNoteReading).filter(
            DimensionNoteReading.origin_name_book == origin_name_book).all()

        # for item in dimension_note_reading:
        #     print(item.category)
        # print(dimension_note_reading[0].origin_name_book)
        response_body['status'] = True
        response_body['data']['detail'] = {
            'origin_name_book': dimension_note_reading[0].origin_name_book,
            'origin_author_book': dimension_note_reading[0].origin_author_book,
            'category': dimension_note_reading[0].category
        }
    except Exception as e:
        print(e)
    return jsonify(response_body)


@notification_your_bp.route('/tool_tip_input', methods=['POST'])
@cross_origin()  # 置于route后
def tool_tip_input():
    """
    获取数目类别
    :return:
    """
    response_body = {
        "status": False,
        "data": {
            "message": None
        }
    }
    request_body = json.loads(request.data)
    # request_body = request.get_json()
    try:
        token = request.headers['Authorization']
        token = base64.b64decode(bytes(token.encode('utf8')))
        print("save-token: ", token)
        de_token = rsa_utils.decrypt_by_PKS1_OAEP(token)
        print("save-detoken ", de_token)
        if b'admin' != de_token:
            response_body['status'] = False
            response_body['data']['message'] = '非法请求'
            return jsonify(response_body)

        exist_list_origin_author_book = db.session.query(DimensionNoteReading.origin_name_book).distinct().all()
        print(exist_list_origin_author_book)
        response_body['status'] = True
        response_body['data']['data'] = exist_list_origin_author_book
        response_body['data']['message'] = "Ok!"

    except Exception as e:
        print(e)
    return jsonify(response_body)


@notification_your_bp.route('/note_reading_save', methods=['POST'])
@cross_origin()  # 置于route后
def note_reading_save():
    """

    :return:
    """
    response_body = {
        "status": False,
        "data": {
            'message': ''
        }
    }
    request_body = json.loads(request.data)
    # request_body = request.get_json()
    try:
        token = request.headers['Authorization']
        token = base64.b64decode(bytes(token.encode('utf8')))
        print('save token->', token)
        de_token = rsa_utils.decrypt_by_PKS1_OAEP(token)
        print('save decrypt->', de_token)
        print(b'admin' == de_token)
        if b'admin' != de_token:
            response_body['status'] = False
            response_body['data']['message'] = '非法请求'
            return jsonify(response_body)

        origin_name_book = request_body.get('origin_name_book', '###')
        category = request_body.get('category', '###')
        origin_author_book = request_body.get('origin_author_book', '###')
        origin_page_book = request_body.get('origin_page_book', '###')
        note = request_body.get('note', '###')
        dimension_note_reading = DimensionNoteReading(origin_name_book=origin_name_book,
                                                      category=category,
                                                      origin_page_book=origin_page_book,
                                                      origin_author_book=origin_author_book, note=note,
                                                      modified=datetime.now(), create=datetime.now())
        db.session.add(dimension_note_reading)
        db.session.commit()
        response_body['status'] = True
        response_body['data']['message'] = f"ok!--{datetime.now()}"
    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify(response_body)

#!/usr/bin/env python
# encoding: utf-8
import json

from flask import request, Blueprint, jsonify
from flask_jwt import jwt_required, current_identity

import application.models as Models
from application.utils.validator import user_schema
from application.utils.generator import generator_user_id
from application.utils.response import normal_resp


user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('/user_info', methods=['POST'])
@jwt_required()
def user_info():
    return normal_resp(current_identity.to_json())


@user_bp.route('/register', methods=['POST'])
def register_user():
    data = json.loads(request.data)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    user = user_schema({'username': username,
                        'password': password,
                        'email': email})

    email_user = Models.User.objects.filter(
        email=user.get('email')).first()
    name_user = Models.User.objects.filter(
        username=user.get('username')).first()
    if email_user or name_user:
        resp = {
            'data': {},
            'msg': 'user exists',
            'code': 1001,
            'extra': {}
        }
    else:
        id = generator_user_id()
        user = Models.User(
            email=user.get('email'),
            id=id, username=user.get('username'),
            password=user.get('password'), role=1)
        status = user.is_valid()
        if status:
            user.save()
            resp = {
                'data': user.to_json(),
                'msg': 'register success',
                'code': 1000,
                'extra': {}
            }
        else:
            resp = {
                'data': {},
                'msg': user.errors,
                'code': 1001,
                'extra': {}
            }

    return jsonify(**resp)

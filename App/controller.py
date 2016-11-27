#!/usr/bin/python
#coding: utf-8

from flask import request, abort, url_for
from flask.ext.restful import Resource, reqparse
from App import client
from flask.ext.security import auth_token_required, roles_required, login_user
from .models import User
from App import auth
from App import app


class Protected(Resource):
    pass
    # @auth.login_required
    # # @auth_token_required
    # def get(self):
    #     return {"msg": "这是需要Token的GET方法"}, 200
	#
    # @auth.login_required
    # # @auth_token_required
    # # @roles_required('admin')  # 不满足则跳转至SECURITY_UNAUTHORIZED_VIEW
    # def post(self):
    #     return {"msg": "这是需要Token和admin权限的POST方法"}, 201


class Login(Resource):  # 自定义登录函数
    # def post(self):
    #     args = reqparse.RequestParser() \
    #         .add_argument('username', type=str, location='json', required=True, help="用户名不能为空") \
    #         .add_argument("password", type=str, location='json', required=True, help="密码不能为空") \
    #         .parse_args()
    #     user = User.authenticate(args['username'], args['password'])
    #     if user:
    #         login_user(user=user)
    #         return {"message": "登录成功", "token": user.get_auth_token()}, 200
    #     else:
    #         return {"message": "用户名或密码错误"}, 401
    pass


class Test(Resource):  # 自定义登录函数
    @auth.login_required
    def get(self):
        return {'message:': 'hello'}


class Register(Resource):
    def post(self):
        # username = request.json.get('username')
        # password = request.json.get('password')
        db = client.maindb
        coll = db['userinfo']
        username = request.form.get('username')
        passwordhash = request.form.get('passwordhash')
        if username is None or passwordhash is None:
            # abort(400)  # missing arguments
            return {'错误：': '用户名或密码有误！'}
        if coll.find_one({'username': username}) is not None:
            return {'错误：': '用户已存在！'}
        # if User.query.filter_by(username=username).first() is not None:
        #     abort(400)  # existing user

        user = User(username=username)
        user.hash_passwordhash(passwordhash)
        user.token = user.generate_auth_token(app.config['SECURITY_TOKEN_MAX_AGE'])
        adduser={'username': user.username, 'userpassword': user.hash_thepasswordhash, 'token': user.token}
        # try:
        user.id = coll.insert(adduser)
        # except

        # return (jsonify({'username': user.username}), 201,
        #         {'Location': url_for('get_userinfo', username=user.username, _external=True)})
        return ({'username': user.username, 'userpasswordhash': user.hash_thepasswordhash, 'token': user.token,
                 'userid': str(user.id)})

#!/usr/bin/python
# coding: utf-8

from flask import request, abort, url_for
from flask.ext.restful import Resource, reqparse
from passlib.apps import custom_app_context as pwd_context
from App import client
from flask.ext.security import auth_token_required, roles_required, login_user
from .models import User
from App import auth
from App import app
import datetime

# def verify_user(token, username):
# 	verifyusername = User.verify_auth_token(token)
# 	if cmp(username, verifyusername.get('username')):
# 		pass


def verify_account(token, username):
	user = User.verify_auth_token(token)
	if user.get['username'] == username :
		return True
	else:
		return False


class Protected(Resource):
	pass

'''
登录验证，读取用户POST过来的BasicAuth中的用户名和hash过的密码
与从数据库中读取的用户密码通过pwd_context.verify校验，如果正确则生成token并返回
'''


class Login(Resource):
	def post(self):
		db = client.maindb
		coll = db['userinfo']
		loginuser = request.authorization.get('username')
		loginhashpassword = request.authorization.get('password')
		if loginuser is None or loginhashpassword is None:
			return {'错误：': '用户名或密码有误！'}
		getuser = coll.find_one({'username': loginuser})
		if getuser is None:
			return {'错误：': '用户不存在！'}
		if pwd_context.verify(loginhashpassword, getuser.get('userpassword')) is not True:
			return {'错误：': '密码错误'}
		user = User(username=loginuser)
		user.usertoken = user.generate_auth_token(app.config['SECURITY_TOKEN_MAX_AGE'])
		return {'username:': loginuser, 'token:': user.usertoken}


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
		email = request.form.get('email')

		if username is None or passwordhash is None:
			# abort(400)  # missing arguments
			return {'错误：': '用户名或密码有误！'}
		if coll.find_one({'username': username}) is not None:
			return {'错误：': '用户已存在！'}
		user = User(username=username)
		user.hash_passwordhash(passwordhash)
		user.token = user.generate_auth_token(app.config['SECURITY_TOKEN_MAX_AGE'])
		adduser = {
			'username': user.username, 'userpassword': user.hash_thepasswordhash, 'token': user.token, 'email': email,
			'regdate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		}
		user.id = coll.insert(adduser)
		# useruri = 'http://192.168.2.8/v1/%s' % user.username
		sendmessage = {
			'username': user.username, 'userpasswordhash': user.hash_thepasswordhash, 'token': user.token,
			'useruri': user.useruri
		}

		# return ({'username': user.username, 'userpasswordhash': user.hash_thepasswordhash, 'token': user.token,
		# 		 'userid': str(user.id)})
		return {'state': 'ok', 'data': sendmessage}


class AddAddresser(Resource):
	def post(self):
		pass


class Reward(Resource):
	def get(self):
		pass


class UpdateUserInfo(Resource):
	@auth.login_required
	def post(self):
		pass


class Forget(Resource):
	def get(self):
		pass


class GetUserInfo(Resource):
	def post(self):
		pass


class GetItemList(Resource):
	def get(self):
		pass


class GetItem(Resource):
	def get(self):
		pass


class AddItem(Resource):
	def post(self):
		pass


class AddCart(Resource):
	def post(self):
		pass


class PlacedOrder(Resource):
	def post(self):
		pass

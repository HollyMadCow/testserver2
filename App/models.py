from flask import Flask, abort, request, jsonify, g, url_for
from App import client
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from App import auth
from App import app


class User:
    # username = ''
    # passwordhash = ''
    hash_thepasswordhash = ''
    id = ''

    def __init__(self, username, passwordhash):
        self.username = username
        self.passwordhash = passwordhash
        self.db = client.maindb

    # __tablename__ = 'users'
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(32), index=True)
    # password_hash = db.Column(db.String(64))

    def hash_passwordhash(self, passwordhash):
        self.hash_thepasswordhash = pwd_context.encrypt(passwordhash)

    def verify_passwordhash(self, passwordhash):
        return pwd_context.verify(passwordhash, self.hash_thepasswordhash)

    def generate_auth_token(self, appkey, expiration=app.config['SECURITY_TOKEN_MAX_AGE']):
        s = Serializer(appkey, expires_in=expiration)
        return s.dumps({'id': self.id, 'username': self.username})

    @staticmethod
    def verify_auth_token(appkey, token):
        s = Serializer(appkey)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


@auth.verify_password
def verify_password(username_or_token, passwordhash):
    # first try to authenticate by token
    user = User.verify_auth_token(app.config['SECRET_KEY'], username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_passwordhash(passwordhash):
            return False
    g.user = user
    return True

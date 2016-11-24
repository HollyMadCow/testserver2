from App import app
from flask.ext.restful import Api
from App.controller import Protected, Login, Register, Test

api = Api(app, default_mediatype="application/json")
api.add_resource(Login, '/login')
api.add_resource(Protected, '/protected')
api.add_resource(Register, '/reg')
api.add_resource(Test, '/test')
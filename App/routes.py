from App import app
from flask.ext.restful import Api
from App.controller import Protected, Login, Register, Test, AddAddresser, Reward, UpdateUserInfo, Forget, GetUserInfo, \
	GetItemList, GetItem, AddItem, AddCart, PlacedOrder

api = Api(app, default_mediatype="application/json")
api.add_resource(Login, '/v1/login')
api.add_resource(Protected, '/v1/protected')
api.add_resource(Register, '/v1/reg')
api.add_resource(Test, '/v1/test')
api.add_resource(AddAddresser, '/v1/addaddress')
api.add_resource(Reward, '/v1/reward')
api.add_resource(UpdateUserInfo,'/v1/updateinfo')
api.add_resource(Forget, '/v1/forget')
api.add_resource(GetUserInfo, '/v1/user/<username>')
api.add_resource(GetItemList, '/v1/itemlist')
api.add_resource(GetItem, '/v1/item/<item>')
api.add_resource(AddItem, '/v1/additem')
api.add_resource(AddCart, '/v1/addcart')
api.add_resource(PlacedOrder, '/v1/placedorder')

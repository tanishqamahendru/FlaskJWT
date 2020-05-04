#import necessary library
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from security import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity

#configuring your application
app = Flask(__name__)
app.secret_key = 'secretKeyShouldBeSecret' #This key should be hidden in real projects

#Creating our Api
api = Api(app)


jwt = JWT(app, authenticate, identity)
#jwt creates a new endpoint-- /auth 
#we send username and pswd and jwt calls authenticate method and matches the pswd, if matches return user (returns jwt token) we can send this token to the next request we make.
#then, if a request has a token with it, jwt calls the identity function , then get the userid and gets correct user that jwt token represents.

#initializing an empty list
items = []

#api works with resources and a resource must be a class and inherits from the class Resource
class Item(Resource):
	#creating a parser for taking in the price argument
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type = float,
		#no request can come through without price
		required = True,
		#this is the message displayed
		help = "This field cannot be left blank!"
	)

	#we have to authenticate before calling get method. @jwt_required() is a decorator
	@jwt_required()
	#Creating a get method to get an item after authenticating with jwt token
	def get(self, name):
		#The filter() method constructs an iterator from elements of an iterable for which a function returns true.Syntax -- filter(function, iterable)
		#next() returns the first item found/matched by the filter(). next() can give error if there is no item matched, so we write None as default.
		item = next(filter(lambda x: x['name'] == name,items), None)
		return {'item': item}, 200 if item else 404
		#if there is item then 200 else 404 status code

	def post(self, name):
		#if we found an item that is not none, so we don't need to return that item.
		if next(filter(lambda x: x['name'] == name, items), None):
			return {'message': "An item with name '{}' already exists.".format(name)},400
		#taking in the input price argument from the parser
		data = Item.parser.parse_args()
		item = {'name': name, 'price':data['price']}
		items.append(item)
		#we will return item just to show the client that the item is appended.
		return item, 201
		#http status cod 201 means created 

#Adding the resource to out api
api.add_resource(Item, '/item/<string:name>')

#The below code will run our app.
app.run(port=5000, debug=True)
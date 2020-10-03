from flask import Flask, request 
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Stores, StoreList
from db import db

app = Flask(__name__)
app.secret_key = "pythonflaskjwt"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'      
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Stores, "/store/<string:name>")
api.add_resource(StoreList, "/stores")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
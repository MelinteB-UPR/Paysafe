from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import os
from datetime import timedelta
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///data.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app
app.config["JWT_AUTH_URL_RULE"] = '/login'
# config JWT to expire within half on hour
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
app.secret_key = 'bogdan'
api = Api(app)



jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item')
# api.add_resource(Item, '/item/<string:checkCode>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True

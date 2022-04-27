from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    user_name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    type_user = db.Column(db.Integer)

class Shop(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    id_user = db.Column(db.Integer)
    address = db.Column(db.String(200))
    img = db.Column(db.String(150))

class Furniture(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    id_shop = db.Column(db.Integer)
    img = db.Column(db.String(150))
    price = db.Column(db.Integer)
    describe = db.Column(db.String(5000))
    status = db.Column(db.String(50))

# class Cart(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     id_furniture = db.Column(db.Integer)
#     id_user = db.Column(db.Integer) 
#     id_shop = db.Column(db.Integer) 
#     quantity = db.Column(db.Integer)
#     p_name = db.Column(db.String(5000))
#     p_phone = db.Column(db.String(5000))
#     p_address = db.Column(db.String(5000))

class Order(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_furniture = db.Column(db.Integer)
    id_user = db.Column(db.Integer) 
    id_shop = db.Column(db.Integer) 
    quantity = db.Column(db.Integer)
    p_name = db.Column(db.String(5000))
    p_phone = db.Column(db.String(5000))
    p_address = db.Column(db.String(5000))
    status = db.Column(db.Integer) #0:đang giao, 1:đã giao, 2:hủy

class FurInCart(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    id_shop = db.Column(db.Integer) #id_furniture
    img = db.Column(db.String(150))
    price = db.Column(db.Integer)
    describe = db.Column(db.String(5000))
    id_cart = db.Column(db.Integer) #id_user
    id_order = db.Column(db.Integer) #id_shop
    quantity = db.Column(db.Integer)

class Comment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    id_user = db.Column(db.Integer)
    id_furniture = db.Column(db.Integer)

class Image(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_furniture = db.Column(db.Integer)
    name = db.Column(db.String(500))
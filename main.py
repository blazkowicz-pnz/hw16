import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from utils import load_data_from_json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hw16.db"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    customer = relationship("User", foreign_keys=[customer_id])
    executor = relationship("User", foreign_keys=[executor_id])
    offers = relationship("Offer")
#
#
class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    order = relationship("Order",  overlaps="offers")
    executor = relationship("User")
#
db.drop_all()
db.create_all()

users_data = load_data_from_json("users.json")
for user_data in users_data:
    user = User(id=user_data["id"], first_name=user_data["first_name"], last_name=user_data["last_name"], age=user_data["age"], email=user_data["email"], role=user_data["role"], phone=user_data["phone"])
    db.session.add(user)
db.session.commit()


offers_data = load_data_from_json("offers.json")
for offer_data in offers_data:
    offer = Offer(id=offer_data["id"], order_id=offer_data["order_id"], executor_id=offer_data["executor_id"])
    db.session.add(offer)
db.session.commit()


orders_data = load_data_from_json("orders.json")

for order_data in orders_data:
    order = Order(id=order_data["id"], name=order_data["name"], description=order_data["description"], start_date=order_data["start_date"], end_date=order_data["end_date"], address=order_data["address"], price=order_data["price"], customer_id=order_data["customer_id"], executor_id=order_data["executor_id"])
    db.session.add(order)
db.session.commit()

# @app.route("/users")
# def get_users():
#     id_user = request.args.get(int("user_id"))
#     one_user = db.session.query(User).filter(User.id == id_user)
#     if id_user:
#         result = {
#             "id": one_user.id,
#             "first_name": one_user.first_name,
#             "last_name": one_user.last_name,
#             "age": one_user.age,
#             "email": one_user.email,
#             "role": one_user.role,
#             "phone": one_user.phone
#         }
#
#         return json.dumps(result)
#     else:
#         users_list = []
#         users = User.query.all()
#         for user in users:
#             users_list.append({
#             "id": user.id,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "age": user.age,
#             "email": user.email,
#             "role": user.role,
#             "phone": user.phone
#         })
#         return jsonify(users_list)


if __name__ == '__main__':
    app.run()

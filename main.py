from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////hw16.db"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user_id"))

    customer = relationship("User", foreign_keys=[customer_id])
    executor = relationship("User", foreign_keys=[executor_id])
    offers = relationship("Offer")


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    offer = relationship("Offer")
    executor = relationship("User")

if __name__ == '__main__':
    app.run(debug=True)

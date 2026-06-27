from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    orders = db.relationship('Order', backref='user', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    price = db.Column(db.Float, nullable=False)

    image_url = db.Column(db.String(400), default='')

    stock = db.Column(db.Integer, default=10)

    category = db.Column(
        db.String(80),
        default='lifestyle'
    )

    is_popular = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=True
    )

    razorpay_order_id = db.Column(db.String(200))

    razorpay_payment_id = db.Column(db.String(200))

    total = db.Column(db.Float)

    status = db.Column(
        db.String(50),
        default='pending'
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
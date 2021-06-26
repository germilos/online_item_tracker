import json
import mongoengine as me
import jwt
import datetime
from app import app
import flask_bcrypt


class Item:
    def __init__(self, url, name, price, available, additional_info):
        self.url = url
        self.name = name
        self.price = price
        self.available = available
        # Some sort of map - similar to object in JS
        self.additional_info = additional_info

    def __repr__(self):
        return f"Name: ({self.name!r}, Price: {self.price!r}, Available: {self.available!r})"

    def __str__(self):
        return f"Name: {self.name}, Price: {self.price}, Available: {self.available}"

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)


class Price(me.EmbeddedDocument):
    amount = me.DecimalField(required=True)
    currency = me.StringField(required=True)

    def __repr__(self):
        return f"{self.price!r} {self.currency!r})"

    def __str__(self):
        return f"{self.amount} {self.currency}"


class ItemToTrack(me.Document):
    url = me.StringField(required=True)
    price = me.EmbeddedDocumentField(Price)
    available = me.BooleanField(required=True)
    shopper_id = me.StringField()
    additional_info = me.DictField()

    def __repr__(self):
        return f"Price: {self.price!r}, Available: {self.available!r})"

    def __str__(self):
        return f"Price: {self.price}, Available: {self.available}"


class CurrentPrice:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"{self.price!r} {self.currency!r})"

    def __str__(self):
        return f"{self.amount} {self.currency}"


class OnlineShopper(me.Document):
    email = me.StringField(required=True)
    password = me.StringField(required=True)
    registered_on = me.DateTimeField()

    @classmethod
    def create_user(cls, email, password):
        user = cls(email=email, registered_on=datetime.datetime.now())
        user.set_password(password)
        return user

    def set_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        return self

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': str(user_id)
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms="HS256")
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return f"{self.email!r} {self.registered_on!r})"

    def __str__(self):
        return f"{self.email} {self.registered_on}"



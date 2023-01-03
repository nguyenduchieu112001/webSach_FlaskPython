from shop import db, app, login_manager
from flask_login import UserMixin
from datetime import datetime
import json

@login_manager.user_loader
def user_loader(user_id):
    return Customer.query.get(user_id)

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique=False)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(150), unique=False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

    def __repr__(self):
        return '<Customer> %r'% self.name

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return '<CustomerOrder %r>' % self.invoice

with app.app_context():
    db.create_all()

    
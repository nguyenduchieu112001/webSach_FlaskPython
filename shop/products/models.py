from shop import db, app
from datetime import datetime


class Addproduct(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,0), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)


    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category', backref=db.backref('categories', lazy=True))

    image = db.Column(db.String(150), nullable=False, default = 'image.jpg')

    def __repr__(self):
        return '<Addproduct %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False, unique=True)

with app.app_context():
    db.create_all()
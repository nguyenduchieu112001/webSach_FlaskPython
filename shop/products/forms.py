from flask_wtf.file import FileAllowed, FileField
from wtforms import Form, IntegerField, StringField, TextAreaField, validators, DecimalField

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    discription = TextAreaField('Discription', [validators.DataRequired()])

    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])


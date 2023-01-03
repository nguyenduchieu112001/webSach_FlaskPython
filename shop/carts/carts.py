from flask import redirect, render_template, session, url_for, flash, request, current_app
from shop import db, app
from shop.products.models import Addproduct, Category

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1+dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False 


@app.route('/addcart', methods=['POST'])
def addcart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Addproduct.query.filter_by(id=product_id).first()
        if request.method=="POST":
            DictItems = {product_id:{'name': product.name, 'price': float(product.price), 'discount': product.discount, 
            'quantity': quantity, 'image': product.image}}
            if 'ShoppingCart' in session:
                print(session['ShoppingCart'])
                if product_id in session['ShoppingCart']:
                    for key, item in session['ShoppingCart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['ShoppingCart'] = MagerDicts(session['ShoppingCart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['ShoppingCart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    if 'ShoppingCart' not in session or len(session['ShoppingCart']) <=0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['ShoppingCart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        grandtotal = float("%0.2f" % (subtotal)) 
    return render_template('products/carts.html', grandtotal=grandtotal, categories=categories)

@app.route('/updatecart/<int:id>', methods=['POST'])
def updatecart(id):
    if 'ShoppingCart' not in session or len(session['ShoppingCart']) <=0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['ShoppingCart'].items():
                if int(key) == id:
                    item['quantity'] = quantity
                    flash(f'Item is updated!', 'success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'ShoppingCart' not in session or len(session['ShoppingCart']) <=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['ShoppingCart'].items():
            if int(key) == id:
                session['ShoppingCart'].pop(key, None)
        return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/clearcart')
def clearcart():
    try:
        session.pop('ShoppingCart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)



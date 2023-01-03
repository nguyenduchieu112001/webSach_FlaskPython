from flask import redirect, render_template, session, url_for, flash, request, current_app
from shop import db, app, photos, search
from .models import Category, Addproduct
from .forms import Addproducts
import secrets, os

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=8)
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', products = products, categories=categories)

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name'], limit=5)
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/result.html', products=products, categories=categories)

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/single_page.html', product=product, categories=categories)


@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cate = Category.query.filter_by(id=id).first_or_404()
    get_category_product = Addproduct.query.filter_by(category = get_cate).paginate(page=page, per_page=8)
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', get_category_product = get_category_product, categories = categories, get_cate = get_cate)


@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if 'username' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method =="POST":
        getcategory = request.form.get('category')
        category = Category(name = getcategory)
        db.session.add(category)
        flash(f'The Category {getcategory} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/addcategory.html')

@app.route('/updatecategory/<int:id>', methods =['GET', 'POST'])
def updatecategory(id):
    if 'username' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method=="POST":
        updatecategory.name = category
        flash(f'Your Category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatecategory.html', title = "Update Category Page", updatecategory = updatecategory)

@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    product = db.session.query(Addproduct).filter(Addproduct.category_id==id).first()
    if request.method=="POST":
        if product is not None:
            flash(f'The category {category.name} already used', 'warning')
        else:
            db.session.delete(category)
            db.session.commit()
            flash(f'The category  {category.name} was deleted from your database', 'success')
        return redirect(url_for('categories'))
    flash(f'The category  {category.name} cannot be deleted', 'warning')
    return redirect(url_for('categories'))


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'username' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method=="POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        category = request.form.get('category')

        image = photos.save(request.files.get('image'), name=secrets.token_hex(10)+".")

        addpro = Addproduct(name = name, price=price, discount = discount, stock=stock, category_id = category, image = image)
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title='Add Product Page', form=form, categories =categories)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)

    category=request.form.get('category')
    form = Addproducts(request.form)
    if request.method=="POST":
        product.name=form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.category_id = category
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image))
                product.image = photos.save(request.files.get('image'), name=secrets.token_hex(10)+".")
            except:
                product.image = photos.save(request.files.get('image'), name=secrets.token_hex(10)+".")
        db.session.commit()
        flash(f'Your Product has been updated', 'success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    return render_template('products/updateproduct.html', form=form, categories=categories, product=product)

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method=="POST":
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image))
            except Exception as e:
                print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The Product {product.name} was deleted from ypur database', 'success')
        return redirect(url_for('admin'))
    flash(f'Cannot delete the Product {product.name} from ypur database', 'success')
    return redirect(url_for('admin'))
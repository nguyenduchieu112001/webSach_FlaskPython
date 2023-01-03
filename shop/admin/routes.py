from flask import render_template, session, redirect, request, url_for, flash

from shop import app, db, bcrypt
from shop.admin.models import Admin
from shop.products.models import Addproduct, Category
from .forms  import RegistrationForm, LoginForm
import os

@app.route('/admin')
def admin():
    if 'username' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title="Admin Page", products = products)

@app.route('/categories')
def categories():
    if 'username' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('/admin/category.html', title = "Category Page", categories = categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = Admin(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form, title="Registeration Page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = Admin.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['username'] = form.username.data
            flash(f'Welcome {form.username.data} You are logedin now', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password please try again', 'danger')
    return render_template('admin/login.html', form = form, title = "Login Page")
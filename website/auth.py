import os
from flask import Blueprint, render_template, request, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Shop, Furniture, Order, FurInCart, Comment, Image
from . import db
from . import create_app

auth = Blueprint('auth', __name__)
app = create_app()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'glb', 'gltf'])
def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')

        user = User.query.filter_by(user_name=user_name).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('User does not exist', category='error')        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        full_name = request.form.get('full_name')
        type_user = 1

        user = User.query.filter_by(user_name=user_name).first()
        if user:
            flash('User name already exists', category='error')
        elif password1 != password2:
            flash('Your password don' "'" 't match', category='error')
        else:
            new_user = User(user_name=user_name,
                            password=generate_password_hash(password1, method='sha256'),
                            full_name=full_name, 
                            type_user=type_user)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account created', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/create_shop/<int:id_user>', methods=['POST', 'GET'])
def create_shop(id_user):
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        id_user = current_user.id 

        img = request.files['img']
        if allowed_image(img.filename):
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            print("Image saved")

        new_shop = Shop(name=name,
                        address=address,
                        id_user=id_user,
                        img=secure_filename(img.filename))
        db.session.add(new_shop)

        db.session.commit()
        return redirect(url_for('views.my_shop', id_shop=new_shop.id))
    return render_template("create_shop.html", user=current_user)

@auth.route('/add_new_furniture/<int:id_shop>', methods=['POST', 'GET'])
def add_new_furniture(id_shop):
    if request.method == 'POST':
        name = request.form.get('name')
        id_shop = id_shop
        price = request.form.get('price')
        describe = request.form.get('describe')
        status = request.form.get('status')

        img = request.files['img']
        if allowed_image(img.filename):
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            print("Image saved")
        
        new_furniture = Furniture(name=name,
                                id_shop=id_shop,
                                img=secure_filename(img.filename),
                                price=price,
                                describe=describe,
                                status=status)
        db.session.add(new_furniture)
        db.session.commit()
        return redirect(url_for('views.my_shop'))
    return render_template('add_new_furniture.html', user=current_user)

@auth.route('/delete_fur/<int:id_fur>')
def delete_fur(id_fur):
    fur = Furniture.query.get_or_404(id_fur)
    db.session.delete(fur)
    db.session.commit()
    return redirect(url_for('views.my_shop'))

@auth.route('/edit_furniture/<int:id_fur>', methods=['POST', 'GET'])
def edit_furniture(id_fur):
    edit_fur = Furniture.query.get_or_404(id_fur)

    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        describe = request.form.get('describe')
        status = request.form.get('status')

        img = request.files['img']
        if allowed_image(img.filename):
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        r_img =  secure_filename(img.filename)
        
        
        edit_fur.name=name
        if r_img != "":
            edit_fur.img=r_img
        edit_fur.price=price
        edit_fur.describe=describe
        edit_fur.status=status
        
        db.session.commit()
        return redirect(url_for('views.my_shop'))
    return render_template('edit_furniture.html', user=current_user, furniture=edit_fur)

@auth.route('/delete_fic/<int:id_fic>')
def delete_fic(id_fic):
    fic = FurInCart.query.get_or_404(id_fic)
    db.session.delete(fic)
    db.session.commit()
    return redirect(url_for('views.view_cart'))

@auth.route('/edit_shop/<int:id_shop>', methods=['POST', 'GET'])
def edit_shop(id_shop):
    shop = Shop().query.get_or_404(id_shop)

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address') 

        img = request.files['img']
        if allowed_image(img.filename):
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        r_img = secure_filename(img.filename)

        shop.name=name
        shop.address=address
        if r_img != "":
            shop.img=r_img
        
        db.session.commit()
        return redirect(url_for('views.my_shop', id_shop=id_shop))
    return render_template("edit_shop.html", user=current_user, shop=shop)

@auth.route('/add_comment/<int:id_furniture>', methods=['POST', 'GET'])
def add_comment(id_furniture):
    if request.method == 'POST':
        title = request.form.get('title')
        cmt = Comment(title=title,
                    id_user=current_user.id,
                    id_furniture=id_furniture)
        db.session.add(cmt)
        db.session.commit()
    return redirect(url_for('views.detail_furniture', id_furniture=id_furniture))

@auth.route('/delete_comment/<int:id_cmt>')
def delete_comment(id_cmt):
    cmt = Comment().query.get_or_404(id_cmt)
    db.session.delete(cmt)
    db.session.commit()
    return redirect(url_for('views.detail_furniture', id_furniture=id_furniture))
    
@auth.route('add_3d_file/<int:id_furniture>', methods=['POST', 'GET'])
def add_3d_file(id_furniture):
    if request.method == 'POST':
        file3d = request.files['file3d']
        if allowed_image(file3d.filename):
            filename = secure_filename(file3d.filename)
            file3d.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            f3d = Image(id_furniture=id_furniture, name=secure_filename(file3d.filename))
            db.session.add(f3d)
            db.session.commit()

        return redirect(url_for('views.detail_furniture', id_furniture=id_furniture))  
    return render_template('add_3d_file.html', user=current_user) 

@auth.route('add_3d_img/<int:id_furniture>', methods=['POST', 'GET'])     
def add_3d_img(id_furniture):
    if request.method == 'POST':
        img1 = request.files['img1']
        if allowed_image(img1.filename):
            filename = secure_filename(img1.filename)
            img1.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            i1 = Image(id_furniture=id_furniture, name=secure_filename(img1.filename))

        img2 = request.files['img2']
        if allowed_image(img2.filename):
            filename = secure_filename(img2.filename)
            img2.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            i2 = Image(id_furniture=id_furniture, name=secure_filename(img2.filename))

        img3 = request.files['img3']
        if allowed_image(img3.filename):
            filename = secure_filename(img3.filename)
            img3.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            i3 = Image(id_furniture=id_furniture, name=secure_filename(img3.filename))

        img4 = request.files['img4']
        if allowed_image(img4.filename):
            filename = secure_filename(img4.filename)
            img4.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            i4 = Image(id_furniture=id_furniture, name=secure_filename(img4.filename))

        img5 = request.files['img5']
        if allowed_image(img5.filename):
            filename = secure_filename(img5.filename)
            img5.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            i5 = Image(id_furniture=id_furniture, name=secure_filename(img5.filename))

        img6 = request.files['img6']
        if allowed_image(img6.filename):
            filename = secure_filename(img6.filename)
            img6.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            i6 = Image(id_furniture=id_furniture, name=secure_filename(img6.filename))

        db.session.add(i1)
        db.session.add(i2)
        db.session.add(i3)
        db.session.add(i4)
        db.session.add(i5)
        db.session.add(i6)
        db.session.commit()

        return redirect(url_for('views.detail_furniture', id_furniture=id_furniture)) 
    return render_template('add_3d_img.html', user=current_user)

@auth.route('delete_3d/<int:id_furniture>')     
def delete_3d(id_furniture):
    list_img = Image().query.all()
    for li in list_img:
        if li.id_furniture == id_furniture:
            db.session.delete(li)
    db.session.commit()
    return redirect(url_for('views.detail_furniture', id_furniture=id_furniture))
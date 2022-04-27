from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc, asc
from .models import User, Shop, Furniture, Order, FurInCart, Comment, Image
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    list_shop = Shop.query.all()

    list_fic = FurInCart().query.all()
    total=0
    count=0
    if current_user.is_active != False:
        for i in list_fic:
            if i.id_cart == current_user.id:
                total+=i.price*i.quantity
                count+=1
    
    return render_template("home.html", user=current_user,
                                        list_shop=list_shop,
                                        total=total,
                                        count=count)

@views.route('/shop/<int:id_shop>', methods=['POST', 'GET'])
def shop(id_shop):
    shop = Shop.query.get_or_404(id_shop)
    list_furniture = Furniture.query.all()
    manager = User().query.get_or_404(shop.id_user)

    list_fic = FurInCart().query.all()
    total=0
    count=0
    for i in list_fic:
        if i.id_cart == current_user.id:
            total+=i.price*i.quantity
            count+=1

    return render_template("shop.html", user=current_user,
                                        shop=shop,
                                        list_fur=list_furniture,
                                        manager=manager,
                                        total=total,
                                        count=count)

@views.route('/my_shop', methods=['POST', 'GET'])
def my_shop():
    list_shop = Shop.query.all()
    list_furniture = Furniture.query.all()
    user=current_user
    shop = False
    for i in list_shop:
        if i.id_user == user.id:
            shop = i

    list_fic = FurInCart().query.all()
    total=0
    count=0
    for i in list_fic:
        if i.id_cart == current_user.id:
            total+=i.price*i.quantity
            count+=1

    return render_template("my_shop.html", user=current_user,
                                        shop=shop,
                                        list_fur=list_furniture,
                                        total=total,
                                        count=count)

@views.route('/detail_furniture/<int:id_furniture>', methods=['POST', 'GET'])
def detail_furniture(id_furniture):
    furniture = Furniture.query.get_or_404(id_furniture)
    shop = Shop.query.get_or_404(furniture.id_shop)
    list_cmt = Comment().query.order_by(desc(Comment.id)).all()
    list_user = User().query.all()
    manager = User().query.get_or_404(shop.id_user)

    list_fic = FurInCart().query.all()
    total=0
    count=0
    for i in list_fic:
        if i.id_cart == current_user.id:
            total+=i.price*i.quantity
            count+=1

    check_3d = 0
    list_img = Image().query.all()
    img_3d = []
    for i in list_img:
        if i.id_furniture == id_furniture:
            check_3d+=1
            img_3d.append(i)

    return render_template("detail_furniture.html", user=current_user,
                                                    furniture=furniture,
                                                    shop=shop,
                                                    list_cmt=list_cmt,
                                                    list_user=list_user,
                                                    manager=manager,
                                                    total=total,
                                                    count=count,
                                                    check_3d=check_3d,
                                                    img_3d=img_3d)
                                                    
@views.route('/add_to_cart/<int:id_furniture>', methods=['POST', 'GET'])
def add_to_cart(id_furniture):
    fur = Furniture.query.get_or_404(id_furniture)
    list_fic = FurInCart.query.all()
    check = 0
    for fic in list_fic:
        if fic.id_shop==fur.id and fic.id_cart==current_user.id and fic.id_order==fur.id_shop:
            check=1
            fic.quantity+=1
            db.session.commit()
    if check == 0:
        new_furincart = FurInCart(name=fur.name,
                            id_shop=fur.id,
                            img=fur.img,
                            price=fur.price,
                            describe=fur.describe,
                            id_cart=current_user.id,
                            id_order=fur.id_shop,
                            quantity=1)
        db.session.add(new_furincart)
        db.session.commit()

    shop = Shop.query.get_or_404(fur.id_shop)
    list_furniture = Furniture.query.all()
    print("add1furn")

    list_fic = FurInCart().query.all()
    total=0
    count=0
    for i in list_fic:
        if i.id_cart == current_user.id:
            total+=i.price*i.quantity
            count+=1

    return redirect(url_for('views.shop', id_shop=shop.id))
    
@views.route('/view_cart', methods=['POST', 'GET'])
def view_cart():
    list_fic = FurInCart().query.all()
    list_ficOfUser = []
    total=0
    for i in list_fic:
        if i.id_cart == current_user.id:
            total+=i.price*i.quantity
            list_ficOfUser.append(i)
    return render_template('cart.html', user=current_user,
                                        list_ficOfUser=list_ficOfUser,
                                        total=total)  

@views.route('/add_many_to_cart/<int:id_furniture>', methods=['POST', 'GET'])
def add_many_to_cart(id_furniture):
    fur = Furniture.query.get_or_404(id_furniture)
    if request.method == 'POST':
        tmp = request.form.get('data')
        print(tmp)
        list_fic = FurInCart.query.all()
        check = 0
        for fic in list_fic:
            if fic.id_shop==fur.id and fic.id_cart==current_user.id and fic.id_order==fur.id_shop:
                check=1
                fic.quantity+=int(tmp)
                db.session.commit()
        if check == 0:
            new_furincart = FurInCart(name=fur.name,
                            id_shop=fur.id,
                            img=fur.img,
                            price=fur.price,
                            describe=fur.describe,
                            id_cart=current_user.id,
                            id_order=fur.id_shop,
                            quantity=int(tmp) )
            db.session.add(new_furincart)
            db.session.commit()
    
    return redirect(url_for('views.detail_furniture', id_furniture=id_furniture))
    
@views.route('/check_out', methods=["POST", "GET"])
def check_out():
    if request.method == "POST":
        p_name = request.form.get('name')
        p_phone = request.form.get('phone')
        p_address = request.form.get('address')
        list_fic = FurInCart.query.all()
        for fic in list_fic:
            if fic.id_cart == current_user.id:
                new_order = Order(id_furniture=fic.id_shop,
                                id_user=current_user.id,
                                id_shop=fic.id_order,
                                quantity=fic.quantity,
                                p_name=p_name,
                                p_phone=p_phone,
                                p_address=p_address,
                                status=0)
                db.session.add(new_order)
                db.session.delete(fic)
                db.session.commit()
        return redirect(url_for('views.order_tracking'))
    return render_template("check_out.html", user=current_user)

@views.route('/order_tracking', methods=["POST", "GET"])
def order_tracking():
    list_order = Order.query.order_by(asc(Order.status)).all()
    list_furniture = Furniture().query.all()
    user_order = []
    for lo in list_order:
        if lo.id_user == current_user.id:
            user_order.append(lo)
    return render_template("order_tracking.html", user=current_user,
                                                user_order=user_order,
                                                list_furniture=list_furniture)

@views.route('/store_order/<int:id_shop>', methods=["POST", "GET"])
def store_order(id_shop):
    list_order = Order.query.order_by(asc(Order.status)).all()
    list_furniture = Furniture().query.all()
    list_user = User().query.all()
    store_order = []
    for lo in list_order:
        if lo.id_shop == id_shop:
            store_order.append(lo)
    return render_template("store_order.html", user=current_user,
                                                store_order=store_order,
                                                list_furniture=list_furniture,
                                                list_user=list_user)                                         

@views.route('/cancel_order/<int:id_order>')
def cancel_order(id_order):
    order = Order.query.get_or_404(id_order)
    order.status = 2
    db.session.commit()
    return redirect(url_for('views.order_tracking'))

@views.route('/complete_order/<int:id_order>')
def complete_order(id_order):
    order = Order.query.get_or_404(id_order)
    order.status = 1
    db.session.commit()
    return redirect(url_for('views.order_tracking'))
    
@views.route('/view_user/<int:id_user>')
def view_user(id_user):
    v_user = User.query.get_or_404(id_user)
    return render_template("view_user.html", user=current_user,
                                           v_user=v_user)


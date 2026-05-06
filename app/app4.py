from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SECRET_KEY'] = 'd24008856'

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    eco_impact = db.Column(db.Float, nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    comment = db.Column(db.Text, nullable = False)

@app.route('/')
def galleryPage():
    sort = request.args.get('sort', 'name')
    search = request.args.get('search', '')

    query = Product.query

    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    if sort == 'price':
        query = query.order_by(Product.price)
    elif sort == 'eco':
        query = query.order_by(Product.eco_impact)
    else:
        query = query.order_by(Product.name)

    products = query.all()

    return render_template('index.html', technologies=products, sort=sort, search=search)

@app.route('/tech/<int:techId>')
def singleProductPage(techId):
    product = Product.query.get_or_404(techId)
    reviews = Review.query.filter_by(product_id=techId).all()
    return render_template('SingleTech.html', technology=product, techId=techId, reviews=reviews)

@app.route('/review/<int:techId>', methods=['POST'])
def add_review(techId):
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    review = Review(product_id=techId, rating=int(rating), comment=comment)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('singleProductPage', techId=techId))

@app.route('/add_to_cart/<int:techId>', methods=['POST'])
def add_to_cart(techId):
    qty = int(request.form.get('quantity'))
    product = Product.query.get_or_404(techId)

    basket = session.get('basket', {})
    basket[str(techId)] = basket.get(str(techId), 0) + qty

    session['basket'] = basket
    return redirect(url_for('view_basket'))

@app.route('/basket')
def view_basket():
    basket = session.get('basket', {})
    items = []
    total = 0
    for product_id, qty in basket.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * qty
            total += subtotal
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return render_template('basket.html', items=items, total=total)

@app.route('/increase/<int:techId>')
def increase_item(techId):
    basket = session.get('basket', {})
    basket[str(techId)] = basket.get(str(techId), 0) + 1
    session['basket'] = basket
    return redirect(url_for('view_basket'))

@app.route('/decrease/<int:techId>')
def decrease_item(techId):
    basket = session.get('basket', {})
    if str(techId) in basket:
        basket[str(techId)] -= 1
        if basket[str(techId)] <= 0:
            basket.pop(str(techId))
    session['basket'] = basket
    return redirect(url_for('view_basket'))

@app.route('/remove_from_basket/<int:techId>')
def remove_from_basket(techId):
    basket = session.get('basket', {})
    basket.pop(str(techId), None)
    session['basket'] = basket
    return redirect(url_for('view_basket'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    errors = []
    if request.method == 'POST':
        name = request.form.get('name')
        card = request.form.get('card_number')
        expiry = request.form.get('expiry')
        cvv = request.form.get('cvv')

        if not card.isdigit() or len(card) != 16:
            errors.append('Card number must be exactly 16 digits.')

        if not cvv.isdigit() or len(cvv) != 3:
            errors.append('CVV must be exactly 3 digits.')

        import re
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', expiry):
            errors.append('Expiry must be in MM/YY format.')

        if not errors:
            session.pop('basket', None)
            return render_template('order_confirm.html', name=name)

    return render_template('checkout.html', errors=errors)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

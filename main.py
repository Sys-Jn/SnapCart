import os, hmac, hashlib, razorpay
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from models import db, User, Product, Order

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY']                     = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']        = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

razorpay_client = razorpay.Client(
    auth=(os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRET'))
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ── PRODUCTS DATA ───────────────────────────────────────────────────────
PRODUCTS = [
    {"name": "Minimal Leather Watch", "price": 2499, "description": "Genuine leather strap, sapphire glass",
     "image_url": "https://i.pinimg.com/736x/4c/c4/8f/4cc48f399abd5a96d1b8291fd32e90c5.jpg"},

    {"name": "Ceramic Coffee Set", "price": 1299, "description": "Handcrafted ceramic dripper & mug",
     "image_url": "https://i.pinimg.com/originals/02/9a/b0/029ab0ef346caa284f3fe132f5c3d147.jpg"},

    {"name": "Linen Tote Bag", "price": 799, "description": "Natural linen, reinforced handles",
     "image_url": "https://i.pinimg.com/1200x/ad/ef/03/adef0341b8783f013ecaa1fe60e778f4.jpg"},

    {"name": "Wireless Earbuds", "price": 3499, "description": "40hr battery, active noise cancellation",
     "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&q=80"},

    {"name": "Merino Wool Sweater", "price": 1999, "description": "100% merino, naturally breathable",
     "image_url": "https://i.pinimg.com/1200x/df/36/66/df3666dac77501c62681407212014ac1.jpg"},

    {"name": "Hardcover Notebook", "price": 499, "description": "A5, 200 pages, dotted grid",
     "image_url": "https://i.pinimg.com/1200x/fd/5e/d5/fd5ed549a5db368205c02206b039afce.jpg"},

    {"name": "Bamboo Desk Organiser", "price": 899, "description": "Sustainable bamboo, 6 compartments",
     "image_url": "https://images.unsplash.com/photo-1611269154421-4e27233ac5c7?w=600&q=80"},

    {"name": "Scented Soy Candle", "price": 649, "description": "Cedarwood & vanilla, 50hr burn",
     "image_url": "https://i.pinimg.com/736x/11/92/69/1192690c1f2fe0e23d9e9b9478a28175.jpg"},

    {"name": "Running Sneakers", "price": 2999, "description": "Lightweight mesh, cushioned sole",
     "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80"},

    {"name": "Stainless Steel Bottle", "price": 799, "description": "750ml, keeps cold 24hrs, hot 12hrs",
     "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&q=80"},  # FIXED duplicate

    {"name": "Wooden Sunglasses", "price": 1599, "description": "Walnut frame, polarised UV400 lens",
     "image_url": "https://i.pinimg.com/1200x/15/20/74/1520745b92fd43952251910fa70a0cb7.jpg"},

    {"name": "Cotton Pyjama Set", "price": 1199, "description": "100% organic cotton, relaxed fit",
     "image_url": "https://i.pinimg.com/736x/e5/9a/4f/e59a4f46865206356949a41bee48551f.jpg"},

    {"name": "Aroma Diffuser", "price": 1199, "description": "Ultrasonic mist, wooden cover",
     "image_url": "https://aromatherapynaturals.com/wp-content/uploads/2023/09/how-do-you-use-theultrasonic-aromatherapy-essential-oil-diffuser-100ml-cool-mist-humidifier_130.png"},
]

# ── SEED / UPDATE PRODUCTS ─────────────────────────────────────────────
def seed_products():
    for p in PRODUCTS:
        existing = Product.query.filter_by(name=p["name"]).first()

        if existing:
            # Update existing product (fix mismatch issue)
            existing.price = p["price"]
            existing.description = p["description"]
            existing.image_url = p["image_url"]
        else:
            db.session.add(
                Product(
                    name=p["name"],
                    price=p["price"],
                    description=p["description"],
                    image_url=p["image_url"],
                    category=p.get("category", "lifestyle"),
                    is_popular=p.get("is_popular", False)
                )
            )

    db.session.commit()
    print("✅ Products synced successfully")

with app.app_context():
    db.create_all()
    seed_products()

# ── AUTH ───────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.')
            return redirect(url_for('login'))

        user = User(
            name=request.form['name'],
            email=email,
            password=generate_password_hash(request.form['password'])
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Welcome to SnapCart, {user.name.split()[0]}!")
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            flash(f"Welcome back, {user.name.split()[0]}!")
            return redirect(url_for('index'))

        flash('Wrong email or password.')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('index'))

# ── SHOP ───────────────────────────────────────────────────────────────
@app.route('/')
def index():
    category = request.args.get('category')
    filter_type = request.args.get('filter')
    search = request.args.get('search')

    query = Product.query

    if category:
        query = query.filter_by(category=category)

    if filter_type == 'popular':
        query = query.filter_by(is_popular=True)

    if filter_type == 'new':
        query = query.order_by(Product.id.desc())

    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    products = query.all()

    return render_template(
        'index.html',
        products=products,
        selected_category=category,
        selected_filter=filter_type,
        search=search
    )

@app.route('/product/<int:product_id>')
def product_detail(product_id):

    product = Product.query.get_or_404(product_id)

    related = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(4).all()

    return render_template(
        'product.html',
        product=product,
        related=related
    )


@app.route('/cart/add/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart

    product = Product.query.get(product_id)
    flash(f"{product.name} added to cart!")
    return redirect(request.referrer or url_for('index'))


@app.route('/cart/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0

    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            subtotal = product.price * qty
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
            total += subtotal

    return render_template('cart.html', items=items, total=total)

# ── PAYMENTS ───────────────────────────────────────────────────────────
@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Cart is empty.')
        return redirect(url_for('cart'))

    total_paise = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            total_paise += int(product.price * 100) * qty

    rz_order = razorpay_client.order.create({
        'amount': total_paise,
        'currency': 'INR',
        'payment_capture': 1
    })

    order = Order(
        user_id=current_user.id,
        razorpay_order_id=rz_order['id'],
        total=total_paise / 100,
        status='pending'
    )
    db.session.add(order)
    db.session.commit()

    return render_template('checkout.html',
        razorpay_order_id=rz_order['id'],
        razorpay_key_id=os.getenv('RAZORPAY_KEY_ID'),
        total_paise=total_paise,
        user=current_user
    )


@app.route('/payment/verify', methods=['POST'])
def verify_payment():
    data = request.form
    rz_order_id = data.get('razorpay_order_id')
    rz_payment_id = data.get('razorpay_payment_id')
    rz_signature = data.get('razorpay_signature')

    key_secret = os.getenv('RAZORPAY_KEY_SECRET').encode()
    msg = f"{rz_order_id}|{rz_payment_id}".encode()

    generated_signature = hmac.new(key_secret, msg, hashlib.sha256).hexdigest()

    if generated_signature == rz_signature:
        order = Order.query.filter_by(razorpay_order_id=rz_order_id).first()
        if order:
            order.razorpay_payment_id = rz_payment_id
            order.status = 'paid'
            db.session.commit()

        session.pop('cart', None)
        return redirect(url_for('success'))
    else:
        flash('Payment verification failed.')
        return redirect(url_for('cart'))


@app.route('/success')
def success():
    return render_template('order_success.html')


if __name__ == '__main__':
    app.run(debug=True)

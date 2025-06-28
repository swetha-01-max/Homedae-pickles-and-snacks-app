from flask import Flask, render_template_string, redirect, url_for, session, request, flash
from functools import wraps
from werkzeug.exceptions import BadRequest
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Simple in-memory user storage
users = {}

# Store reviews and contacts in files
REVIEWS_FILE = 'reviews.txt'
CONTACTS_FILE = 'contacts.txt'

# Product List with Online Image URLs
products = [
    # Non-Veg Pickles
    {
        "id": 1,
        "name": "Spicy Chicken Pickle Boneless",
        "price": 320,
        "image": "https://www.picklesraja.com/wp-content/uploads/2024/11/boon-less-chicken.jpg",
        "description": "Authentic, Spicy, Meaty pickles with high quality and organic ingredients"
    },
    {
        "id": 2,
        "name": "Prawns Pickle",
        "price": 330,
        "image": "https://m.media-amazon.com/images/X/bxt1/M/ibxt1RrE3LsjWSq._SL640_QL75_FMwebp_.jpg",
        "description": "Packed with a generous quantity of prawns in every bottle"
    },
    {
        "id": 3,
        "name": "Korrameru Fish Pickle",
        "price": 400,
        "image": "https://5.imimg.com/data5/ANDROID/Default/2022/1/ZG/CF/RB/145196166/product-jpeg-500x500.jpg",
        "description": "Fresh fish and hygienic preparation"
    },
    {
        "id": 4,
        "name": "Mutton Pickle",
        "price": 330,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlP2WddI5Nd_xVz2UfUhxe32Xyglpw_cnM9w&s",
        "description": "Juicy mutton pieces"
    },

    # Veg Pickles
    {
        "id": 5,
        "name": "Special Mango Pickle",
        "price": 250,
        "image": "https://cinnamonsnail.com/wp-content/uploads/2023/07/Mango-pickle-02.jpg",
        "description": "Raw mangoes with traditional spices and mustard oil"
    },
    {
        "id": 6,
        "name": "Mixed Veg Pickle",
        "price": 280,
        "image": "https://s3-ap-south-1.amazonaws.com/betterbutterbucket-silver/divya-r20180620215346113.jpeg",
        "description": "Carrot, cauliflower, lime and mango combo"
    },
    {
        "id": 7,
        "name": "Spicy Garlic Pickle",
        "price": 270,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVNmOpJDzNs5MMuI21ELT76xZgtKqI5CR_Mg&s",
        "description": "Whole garlic cloves in spicy mustard oil"
    },
    {
        "id": 8,
        "name": "Gongura Pickle",
        "price": 290,
        "image": "https://vellankifoods.com/cdn/shop/products/gongura_pickle_2.jpg?v=1680180278",
        "description": "Tangy sorrel leaves with special spices"
    },

    # Snacks
    {
        "id": 9,
        "name": "Chekkalu and Chekkaralu",
        "price": 230,
        "image": "https://i.ytimg.com/vi/69jkEiK3XNs/sddefault.jpg",
        "description": "Roasted chekkalu and chekkaralu with delicious taste"
    },
    {
        "id": 10,
        "name": "Spicy Murkku",
        "price": 130,
        "image": "https://anandhaassweets.com/cdn/shop/files/MIniSpicyMurkku_2024-05-16T07_17_25.769Z.png?v=1715843854",
        "description": "Roasted murkku with delicious taste"
    },
    {
        "id": 11,
        "name": "Karam (GirijaPaati)",
        "price": 200,
        "image": "https://girijapaati.com/cdn/shop/collections/enh_classicribbon.jpg?v=1691556230",
        "description": "Tasty GirijaPaati style snack"
    },
    {
        "id": 12,
        "name": "Bombay Mixture",
        "price": 100,
        "image": "https://karaikaliyangars.com/cdn/shop/products/BombayMixture.jpg?v=1628014057",
        "description": "Crunchy Bombay Mixture"
    }
]

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with open(CONTACTS_FILE, 'a') as f:
            f.write(f"{name} ({email}): {message}\n")
        flash("Thank you for contacting us!", "success")
        return redirect(url_for('contact'))
    try:
        with open(CONTACTS_FILE, 'r') as f:
            contacts = f.readlines()
    except FileNotFoundError:
        contacts = []

    return render_template_string("""
    <h2>Contact Us</h2>
    <form method="POST">
        Name: <input type="text" name="name" required><br><br>
        Email: <input type="email" name="email" required><br><br>
        Message: <br><textarea name="message" rows="5" cols="40" required></textarea><br><br>
        <button type="submit">Send</button>
    </form>
    <ul>                              
     {% for line in contacts %}
    <li>{{ line }}</li>
    {% endfor %}
    </ul>

    <a href="{{ url_for('products_page') }}">⬅ Back to Products</a>
    """,contacts=contacts)

# Reviews Page
@app.route('/reviews', methods=['GET', 'POST'])
def product_reviews():
    if request.method == 'POST':
        user = session.get('username', 'Guest')
        review = request.form['review']
        with open(REVIEWS_FILE, 'a') as f:
            f.write(f"{user}: {review}\n")
        flash("Thanks for your review!", "success")
        return redirect(url_for('product_reviews'))
    try:
        with open(REVIEWS_FILE, 'r') as f:
            saved_reviews = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        saved_reviews = []

    return render_template_string("""
    <h2>Leave a Review</h2>
    <form method="POST">
        <textarea name="review" rows="4" cols="50" placeholder="Write your review here..." required></textarea><br><br>
        <button type="submit">Submit Review</button>
    </form>
    <h3>All Reviews</h3>
    <ul>
    {% for r in reviews %}
        <li> {{ r }}</li>
    {% endfor %}
    </ul>
    <a href="{{ url_for('products_page') }}">⬅ Back to Products</a>
    """, reviews=saved_reviews)
    
@app.route('/')
@login_required
def products_page():
    return render_template_string("""
    <h1>Welcome, {{ session['username'] }}!</h1>
    <a href="{{ url_for('logout') }}">Logout</a><br><br>
                                  
    <a href="{{ url_for('contact') }}">📬 Contact</a> |
    <a href="{{ url_for('product_reviews') }}">⭐ Reviews</a><br><br>

    <h2>Products</h2>
    <ul>
        {% for product in products %}
        <li>
            <img src="{{ product.image }}" width="100"><br>
            <b>{{ product.name }}</b><br>
            ₹{{ product.price }}<br>
            <a href="{{ url_for('add_to_cart', product_id=product.id) }}">Add to Cart</a>
        </li><br>
        {% endfor %}
    </ul>
    <a href="{{ url_for('cart') }}">Go to Cart</a>
    """, products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if username in users:
            flash("Username already exists.", "error")
        elif not username or not password:
            flash("Please enter both username and password.", "error")
        else:
            users[username] = password
            flash("Registered successfully. Please login.", "success")
            return redirect(url_for('login'))
    return render_template_string("""
    <h2>Register</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <button type="submit">Register</button>
    </form>
    <a href="{{ url_for('login') }}">Already registered? Login</a>
    """)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if users.get(username) == password:
            session['username'] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for('products_page'))
        else:
            flash("Invalid username or password.", "error")
    return render_template_string("""
    <h2>Login</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <button type="submit">Login</button>
    </form>
    <a href="{{ url_for('register') }}">Don't have an account? Register</a>
    """)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('products_page'))

    cart = session.get('cart', {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart
    session.modified = True
    flash(f'{product["name"]} added to cart', 'success')
    return redirect(url_for('products_page'))

@app.route('/update_cart/<int:product_id>/<int:change>')
@login_required
def update_cart(product_id, change):
    if change not in (-1, 1):
        raise BadRequest("Invalid quantity change")

    cart = session.get('cart', {})
    key = str(product_id)

    if key in cart:
        cart[key] += change
        if cart[key] <= 0:
            del cart[key]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    key = str(product_id)
    if key in cart:
        del cart[key]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
@login_required
def cart():
    cart_items = []
    subtotal = 0

    for product_id, quantity in session.get('cart', {}).items():
        product = next((p for p in products if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            cart_items.append({
                'id': product['id'],
                'name': product['name'],
                'quantity': quantity,
                'price': product['price'],
                'image': product['image'],
                'total': item_total
            })
            subtotal += item_total

    shipping = 50 if subtotal > 0 else 0
    total = subtotal + shipping

    return render_template_string("""
    <h1>Your Cart ({{ session['username'] }})</h1>
    <a href="{{ url_for('logout') }}">Logout</a><br><br>
    {% if cart_items %}
        <ul>
        {% for item in cart_items %}
            <li>
                <img src="{{ item.image }}" width="100"><br>
                {{ item.name }} (x{{ item.quantity }}) - ₹{{ item.total }}<br>
                <a href="{{ url_for('update_cart', product_id=item.id, change=1) }}">➕</a>
                <a href="{{ url_for('update_cart', product_id=item.id, change=-1) }}">➖</a>
                <a href="{{ url_for('remove_from_cart', product_id=item.id) }}">🗑 Remove</a>
            </li><br>
        {% endfor %}
        </ul>
        <p>Subtotal: ₹{{ subtotal }}</p>
        <p>Shipping: ₹{{ shipping }}</p>
        <p><strong>Total: ₹{{ total }}</strong></p>
        <br>
        <a href="{{ url_for('checkout') }}">🛒 Proceed to Checkout</a><br>
        <a href="{{ url_for('products_page') }}">⬅ Back to Products</a>
    {% else %}
        <p>Your cart is empty.</p>
        <a href="{{ url_for('products_page') }}">⬅ Browse Products</a>
    {% endif %}
    """, cart_items=cart_items, subtotal=subtotal, shipping=shipping, total=total)

@app.route('/checkout')
@login_required
def checkout():
    cart_items = []
    total = 0

    for product_id, quantity in session.get('cart', {}).items():
        product = next((p for p in products if p['id'] == int(product_id)), None)
        if product:
            cart_items.append({
                'name': product['name'],
                'quantity': quantity,
                'price': product['price']
            })
            total += product['price'] * quantity

    return render_template_string("""
    <h1>Checkout</h1>
    {% if cart_items %}
        <ul>
            {% for item in cart_items %}
                <li>{{ item.name }} × {{ item.quantity }} — ₹{{ item.quantity * item.price }}</li>
            {% endfor %}
        </ul>
        <p><strong>Total: ₹{{ total }}</strong></p>
        <form method="POST" action="{{ url_for('place_order') }}">
            <button type="submit">✅ Place Order</button>
        </form>
    {% else %}
        <p>Your cart is empty.</p>
    {% endif %}
    <a href="{{ url_for('cart') }}">← Back to Cart</a>
    """, cart_items=cart_items, total=total)

@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    session['cart'] = {}
    flash("🎉 Your order has been placed successfully!", "success")
    return redirect(url_for('order_success'))

@app.route('/success')
@login_required
def order_success():
    return render_template_string("""
    <h2>✅ Order Successful!</h2>
    <p>Thank you for your order, {{ session['username'] }}! 😊</p>
    <a href="{{ url_for('products_page') }}">← Back to Products</a><br>
    <a href="{{ url_for('logout') }}">🚪 Logout</a>
    """)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

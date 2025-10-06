from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP
from datetime import datetime

# ----------------------------------
# Flask + DB + SocketIO Setup
# ----------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///orders.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret_key"

socketio = SocketIO(app, cors_allowed_origins="*")


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


# ----------------------------------
# Database Models
# ----------------------------------
class Orders(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(250), nullable=False)
    product_name: Mapped[str] = mapped_column(String(250), nullable=False)
    status: Mapped[str] = mapped_column(String(250), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    customer_info: Mapped["CustomerInfo"] = relationship(back_populates="order", uselist=False)


class CustomerInfo(db.Model):
    __tablename__ = "customer_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    phone_no: Mapped[str] = mapped_column(String(15), nullable=False)
    order: Mapped["Orders"] = relationship(back_populates="customer_info")


# ----------------------------------
# Initialize Database with Sample Data
# ----------------------------------
with app.app_context():
    db.create_all()
    if Orders.query.count() == 0:
        order1 = Orders(customer_name='Mohammad Ali', product_name='S25 Ultra', status='pending')
        order2 = Orders(customer_name='Ali Ansari', product_name='PS5', status='shipped')
        customer1 = CustomerInfo(order=order1, email='toastedcheese146@gmail.com', phone_no='9869019221')
        customer2 = CustomerInfo(order=order2, email='ali.221204.co@mhssce.ac.in', phone_no='9930896262')
        db.session.add_all([order1, order2, customer1, customer2])
        db.session.commit()
        print(" Sample data inserted.")


# ----------------------------------
# Routes
# ----------------------------------

@app.route('/')
def home():
    return render_template('home.html')


# ----------- LOGIN (Customer Side) ------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Customer login via email"""
    if request.method == 'POST':
        email = request.form.get('email')
        user = CustomerInfo.query.filter_by(email=email).first()
        if user:
            session['email'] = email
            return redirect('/customer')
        else:
            return render_template('login.html', error="Email not found.")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')


# ----------- CUSTOMER DASHBOARD ------------
@app.route('/customer')
def customer_dashboard():
    """Show orders for logged-in customer"""
    if 'email' not in session:
        return redirect('/login')

    email = session['email']
    customer_orders = (
        db.session.query(Orders)
        .join(CustomerInfo)
        .filter(CustomerInfo.email == email)
        .all()
    )

    return render_template('customer.html', orders=customer_orders, email=email)


# ----------- ADMIN ADD ORDER ------------
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        product_name = request.form.get('product_name')
        status = request.form.get('status')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')

        new_order = Orders(customer_name=customer_name, product_name=product_name, status=status)
        db.session.add(new_order)
        db.session.commit()

        new_customer = CustomerInfo(order_id=new_order.id, email=email, phone_no=phone_no)
        db.session.add(new_customer)
        db.session.commit()

        socketio.emit('order_update', {'action': 'add'})
        return redirect('/edit')

    return render_template('add.html')


# ----------- ADMIN EDIT ORDERS ------------
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        customer_name = request.form.get('customer_name')
        product_name = request.form.get('product_name')
        status = request.form.get('status')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')

        order = Orders.query.get(order_id)
        if order:
            order.customer_name = customer_name
            order.product_name = product_name
            order.status = status
            order.updated_at = datetime.utcnow()

            if order.customer_info:
                order.customer_info.email = email
                order.customer_info.phone_no = phone_no

            db.session.commit()

            #  Notify ALL connected clients (including customer dashboards)
            socketio.emit('order_update', {
                'id': order.id,
                'customer_name': order.customer_name,
                'product_name': order.product_name,
                'status': order.status,
                'email': order.customer_info.email,
                'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return redirect('/edit')

    all_orders = Orders.query.all()
    return render_template('edit.html', orders=all_orders)


# ----------------------------------
# SocketIO Events
# ----------------------------------
@socketio.on('connect')
def handle_connect():
    print("⚡ A user connected!")


@socketio.on('disconnect')
def handle_disconnect():
    print(" A user disconnected.")


# ----------------------------------
# Run App
# ----------------------------------
if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

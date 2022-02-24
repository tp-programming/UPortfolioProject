from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    money = db.Column(db.Float, nullable=False, default=10000)

    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    def __init__(self, id, email, password, first_name, role, money):
        self.id = id
        self.email = email
        self.password = generate_password_hash(password, "sha256")
        self.first_name = first_name
        self.role = role
        self.money = money
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None

class Stock(db.Model):
    __tablename__ = 'stocks'

    stock_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    stock_name = db.Column(db.String(100), nullable=False)
    stock_symbol = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=False)
    bought_price = db.Column(db.Float, nullable=False, default=False)
    current_price = db.Column(db.Float, nullable=False, default=False)
    profit_loss = db.Column(db.Float, nullable=False, default=False)

    def __init__(self, id, stock_name, stock_symbol, amount, bought_price, current_price, profit_loss):
        self.id = id
        self.stock_name = stock_name
        self.stock_symbol = stock_symbol
        self.amount = amount
        self.bought_price = bought_price
        self.current_price = current_price
        self.profit_loss = profit_loss

# Database Initialisation Function
def init_db():
    db.drop_all()
    db.create_all()
    new_user = User(id=1, email='admin@email.com', password='testuserspassword', first_name="John", role="Admin", money=10000)
    db.session.add(new_user)
    db.session.commit()
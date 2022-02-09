from datetime import datetime
from app import db
from flask_login import UserMixin

# User Class - Theodore Palmer
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')

    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    def __init__(self, id, email, password, first_name, role):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None

# Database Initialisation Function
def init_db():
    db.drop_all()
    db.create_all()
    new_user = User(id=1, email='admin@email.com', password='testuserspassword', first_name="John", role="Admin")
    db.session.add(new_user)
    db.session.commit()
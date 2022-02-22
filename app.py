from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = 'BLANK'
app.config['SQLALCHEMY_DATABASE_URI'] = 'BLANK'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':

    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from users.views import users_blueprint
    from portfolio.views import portfolio_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(portfolio_blueprint)

    app.run()

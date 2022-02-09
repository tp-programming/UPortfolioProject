from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BLANK!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'BLANK!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':

    from users.views import users_blueprint
    app.register_blueprint(users_blueprint)

    app.run()

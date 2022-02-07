from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':

    from users.views import users_blueprint
    app.register_blueprint(users_blueprint)

    app.run()

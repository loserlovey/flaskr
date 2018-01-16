from flask import Flask, g
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

db = SQLAlchemy(app)

from . import views

# from contextlib import closing

# def connect_db():
#     return sqlite3.connect(app.config['DATABASE'])

# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('../schema.sql') as f:
#             db.cursor().executescript(f.read())
#         db.commit()


# @app.before_request
# def before_request():
#     g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
#     g.db.close()
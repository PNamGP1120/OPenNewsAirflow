from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = 'vcjgdvoiagvfdigahfj*^%$&$(&^hjgvsdcyws'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:0212@localhost/mysaleappdb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
app.app_context().push()
login = LoginManager(app =app)

cloudinary.config(
    cloud_name = 'dqpu49bbo',
    api_key = '743773348627895',
    api_secret = 'EF7elKsibuI8JEBqfMNZYYWUYvo',
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)
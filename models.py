"""Models for notes app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)


    @classmethod
    def register_user(cls, form):
        
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        #catch duplicate username

          
        return cls(username=form.username.data, password=hashed, email=form.email.data,  
                first_name=form.first_name.data,  last_name=form.last_name.data)

    @classmethod
    def authenticate_user(cls, username, password):
        
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        
        return False


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    owner = db.Column(db.String(20), db.ForeignKey('users.username'))

    user = db.relationship('User', backref="notes")

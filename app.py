"""Flask app for Notes"""

from flask import Flask, request, redirect, render_template, jsonify, flash, session
from models import db, connect_db, User
from forms import AddUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'youllneverguess'

connect_db(app)
db.create_all()

"""data = {
        "id" : self.id,
        "flavor" : self.flavor,
        "size" : self.size,
        "rating" : self.rating,
        "image" : self.image
        } """

@app.route("/")
def index():
    """ Loads Home Page """
   
    return redirect('/register')

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    """ Loads Home Page """
    form = AddUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            if User.query.filter_by(username=username).all():
                flash("Username already taken")
                return redirect('/register')
            user = User.register_user(form)
            db.session.add(user)
            db.session.commit()
            session["cur_user"] = user.username
            return redirect('/secret')
    return render_template("user_form.html", form=form)


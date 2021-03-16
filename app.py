"""Flask app for Notes"""

from flask import Flask, request, redirect, render_template, jsonify, flash, session
from models import db, connect_db, User
from forms import AddUserForm, LogInForm
from sqlalchemy.exc import IntegrityError

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

            # Is this the best way to check for duplicate user?
            try:
                user = User.register_user(form)
                db.session.add(user)
                db.session.commit()
                session["cur_user"] = user.username
            
                return redirect('/secret')

            except IntegrityError:
                flash("Username/email already taken")
                return redirect('/register')

    return render_template("user_form.html", form=form)


@app.route('/login', methods = ["GET", "POST"])
def log_in():
    """Displays log in page"""
    form = LogInForm()

    if request.method == "POST":
        if form.validate_on_submit():
            
            user = User.authenticate_user(form.username.data, form.password.data)
            if user:
                session["cur_user"] = user.username

            return redirect(f'/users/{user.username}') 

    return render_template("log_in_form.html", form=form)


@app.route('/logout', methods = ["POST"])
def log_out():
    session.pop("cur_user", None)
    flash("You are logged out!")
    return redirect('/')


@app.route('/users/<username>')
def secret_page(username):
    """Secret page for only logged in users"""

    if "cur_user" not in session:
         flash("Please log in to access this page!")
         return redirect('/login')
    
    user = User.query.get_or_404(username)

    return render_template("user_page.html", user=user)

@app.route('/users/<username>/delete', methods = ["POST"])
def delete_user(username):
    """Deletes user and their notes"""

    user = User.query.get_or_404(username)
    for note in user.notes:
        db.session.delete(note)
    db.session.delete(user)
    db.session.commit()

    session.pop("cur_user", None)
    flash("User deleted!")

    return redirect('/')


@app.route('/users/<username>/notes/add', methods = ["GET", "POST"])
def add_new_note():
    """Shows/processes form for adding new note"""
    form = LogInForm()

    if request.method == "POST":
        if form.validate_on_submit():
            
            user = User.authenticate_user(form.username.data, form.password.data)
            if user:
                session["cur_user"] = user.username

            return redirect(f'/users/{user.username}') 

    return render_template("log_in_form.html", form=form)
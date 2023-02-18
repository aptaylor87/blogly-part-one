from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "catzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    # render the homepage
    return redirect('/users')

@app.route('/users')
def list_users():
    """Show list of all users in db"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user():
    """Show a form to add a new user"""
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """post info from new user form to db"""
    first_name = request.form['first_name'] 
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')    
def edit_user(user_id):
    """Show a form for editing a user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])    
def submit_edit(user_id):
    "submit changes in form to db"
    edited_user = User.query.get_or_404(user_id)

    edited_user.first_name = request.form['first_name'] 
    edited_user.last_name = request.form['last_name']
    edited_user.image_url = request.form['image_url']

    db.session.add(edited_user)
    db.session.commit()
    return render_template('details.html', user=edited_user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    deleted_user = User.query.get_or_404(user_id)

    db.session.delete(deleted_user)
    db.session.commit()
    return redirect('/users')

"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hushhush'

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def all_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def new_users():
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def display_user(user_id):
    id = User.query.get(user_id)
    return render_template('users.html', user=id)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    id = User.query.get(user_id)
    return render_template('edit_user.html', user=id)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_user(user_id):
    id = User.query.get(user_id)
    id.first_name = request.form['first_name']
    id.last_name = request.form['last_name']
    id.image_url = request.form['image_url']
    db.session.add(id)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    id = User.query.get(user_id)
    db.session.delete(id)
    db.session.commit()
    
    return redirect ('/users')
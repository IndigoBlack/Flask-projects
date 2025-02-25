# app.py
from flask import Flask, render_template, request, redirect
from models import db, User, Post, Likes, Comment 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app) #Initialize the database with the app.

# Create the database tables if they don't exist.
with app.app_context():
    db.create_all()

# Routes and views go here...

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Post, Likes, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app) #Initialize the database with the app.

login_manager = LoginManager()
login_manager.init_app(app)

# Create the database tables if they don't exist.
#with app.app_context():
 #   db.create_all()

# Routes and views go here...
#Main routes: Login route, register route, index route, profile route
@app.route('/')
def index():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = 'Guest'
    posts = Post.query.all()
    comments = Comment.query.all()
    return render_template('index.html', username=username, posts=posts, comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #get username
        #get password
        #verify if the user exist. if they do redirect them to the index page if not tell them to register
        pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #get username: check if a user with the same username exist
        #get email: check if a user with the same email exist
        #get password and confirm password
        #if the passwords match create user else message-passwords must match
        #after creating the user redirect them to the login page
        pass

@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.get_or_404(user_id)
    if user == current_user:
        is_own_profile = True
    else:
        is_own_profile = False
    return render_template('profile.html', user=user, posts=posts, is_own_profile=is_own_profile)

if __name__ == '__main__':

    db.create_all()

    app.run(debug=True)
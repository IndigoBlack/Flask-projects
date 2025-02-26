from flask import Flask, render_template, request, redirect, flash, url_for
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        # Get form inputs
        username = request.form.get('username')
        password = request.form.get('password')

        # Check user exists. logged them in if they do if they don't return them a message
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message="User not found. Are you registered?")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form inputs
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirmation = request.form.get('confirm-password')
        
        # Check if username exists
        check_username = User.query.filter_by(username=username).first()
        if check_username is not None:
            return render_template('register.html', message="Username already exists")
        
        # Check if email exists
        check_email = User.query.filter_by(email=email).first()
        if check_email is not None:
            return render_template('register.html', message="User with same email already exists")

        # Check if password and the password confirmation match
        if password == password_confirmation:
            return render_template('register.html', message="Passwords must match")
        
        # Create user and redirect to login page
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')

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
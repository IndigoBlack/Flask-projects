from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
from models import db, User, Post, Likes, Comment, Follow

app = Flask(__name__)
app.config.from_object(Config) 
db.init_app(app) #Initialize the database with the app.
app.secret_key = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

# Create the database tables if they don't exist.
with app.app_context():
   db.create_all()

# Routes and views go here...

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    #username = current_user.username
    user = current_user
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    comments = Comment.query.all()
    return render_template('index.html', user=user, posts=posts, comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form inputs
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user exists. logged them in if they do, if they don't return them a message
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("User not found. Are you registered?")
            return render_template('login.html')
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

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
            flash("Username already exists")
            return render_template('register.html')
        
        # Check if email exists
        check_email = User.query.filter_by(email=email).first()
        if check_email is not None:
            flash("User with same email already exists")
            return render_template('register.html')

        # Check if password and the password confirmation match
        if password != password_confirmation:
            flash("Passwords must match")
            return render_template('register.html')
        
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

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == "POST":
        content = request.form.get('content')
        user = current_user
        if content:
            create_post = Post(content=content, user_id=user.id)
            db.session.add(create_post)
            db.session.commit()
            flash('Post submitted succesfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Post must not be empty', 'danger')

    return render_template('new_post.html')

@app.route('/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id):
    if request.method == "POST":
        comment_content = request.form.get('comment-content')
        user = current_user
        if comment_content:
            create_comment = Comment(content=comment_content, user_id=user.id, post_id=post_id)
            db.session.add(create_comment)
            db.session.commit()
            flash('Comment successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Comment must not be empty', 'danger')
            return redirect(url_for('index'))
    return render_template('comment.html')

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    user = current_user
    post = Post.query.get_or_404(post_id, user=user)

    try:
        db.session.delete(post)
        db.session.commit() 
        flash('Post has been deleted!', 'success')
    except Exception as e:
        db.session.rollback()  # In case of error, rollback the transaction
        flash('There was an issue deleting the post.', 'danger')
    
    return redirect(url_for('index'))

app.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user_to_follow = User.query.get_or_404(user_id)
    try:
        follow_ = Follow(follower_id=current_user.id , followed_id=user_to_follow)
        db.session.add(follow_)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('There was an issue with following the user', 'danger')
    return redirect(url_for('index'))

@app.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    try:
        follow_record = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
        
        if follow_record:
            db.session.delete(follow_record)
            db.session.commit()
            
        else:
            flash('You are not following this user')
    except Exception as e:
        flash('The was a problem unfollowing the user')
    return redirect(url_for('profile', user_id=user_id))

#Like and unlike route. PS It can be the same route
@app.route('/like/<int:post_id>')
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    like_ = Likes.query.filter_by(post_id=post.id, user_id=current_user.id).first()
    if like_:
        db.session.delete(like_)
        db.session.commit()
    else:
        like_ = Likes(post_id=post.id, user_id=current_user.id)
        db.session.add(like_)
        db.session.commit()
    return redirect(url_for('new_post'))

if __name__ == '__main__':

    app.run(debug=True)
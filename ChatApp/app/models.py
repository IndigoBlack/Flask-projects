from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    #profile_picture = db.Column(db.String(120), nullable=True)
    post = db.relationship('Post', back_populates='user', cascade='all, delete')
    likes = db.relationship('Likes', backref='User', cascade='all, delete')

    def set_password(self, password):
        """Hashes the password before saving it to the database."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='posts', cascade='all, delete')
    likes = db.relationship('Likes', backref='Post', cascade='all, delete')

    def __repr__(self):
        return '<Post %r>' % self.content

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', nullable=False))

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='_user_post_uc'),)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user = db.relationship('User', backref='comments')
    post = db.relationship('Post', backref='comments')
    parent_comment = db.relationship('Comment', remote_side=[id], backref='replies')

    def __repr__(self):
        return f'<Comment {self.id}>'
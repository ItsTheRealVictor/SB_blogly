from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

    
    
    
    
    
    
class User(db.Model):
    '''A model of blog users'''
    
        
    PLACEHOLDER = 'https://www.clipartmax.com/png/middle/340-3400182_special-school-nurse-placeholder-person.png'
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    
    image_url = db.Column(db.String(50), nullable=False, unique=False, default=PLACEHOLDER)
    
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'User #{self.id}: Full name is {self.first_name} {self.last_name}'
    
    def greet(self):
        return f'Greetings to you, {self.first_name} {self.last_name}'
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class Post(db.Model):
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    title = db.Column(db.Text, nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.Text, nullable=False, default=datetime.datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='posts')
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    

class PostTag(db.Model):
    __tablename__ = 'posts_tags'
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, autoincrement=True)
    name = db.Column(db.Text, db.ForeignKey('tags.name'), nullable=False, unique=True)

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')


class TestUser(db.Model):
    __tablename__ = 'testDB'
    __bind_key__ = 'testDB'
    
    PLACEHOLDER = 'https://www.clipartmax.com/png/middle/340-3400182_special-school-nurse-placeholder-person.png'

    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    
    # no idea how to do this, stackoverflow isn't showing anything compelling. I need to ask a tutor
    # In the meantime, this is a placeholder
    image_url = db.Column(db.String(50), nullable=False, unique=False, default=PLACEHOLDER)
    
    def __repr__(self):
        return f'User #{self.id}: Full name is {self.first_name} {self.last_name}'
    
    def greet(self):
        return f'Greetings to you, {self.first_name} {self.last_name}'
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
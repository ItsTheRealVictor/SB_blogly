from flask import Flask, request, render_template, redirect
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogly.db'
app.config['SQLALCHEMY_BINDS'] = {'testDB' : 'sqlite:///test_blogly.db'}



db = SQLAlchemy(app)
app.app_context().push()

migrate = Migrate(app, db)

class User(db.Model):
    '''A model of blog users'''
    
        
    PLACEHOLDER = 'https://www.clipartmax.com/png/middle/340-3400182_special-school-nurse-placeholder-person.png'
    
    __tablename__ = 'users'
    
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


class Post(db.Model):
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    title = db.Column(db.Text, nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.Text, nullable=False, default=dt.utcnow)
    
    user_id = db.Column(db.Text, db.ForeignKey('users.id'), nullable=False)












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
    


@app.route('/')
def home():
    
    users = User.query.all()
    
    return render_template('home.html', users=users)

@app.route('/add_user')
def add_form():
    
    return render_template('add_user.html')

@app.route('/', methods=['POST'])
def add_user():
    
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')
    if not image_url:
        image_url = User.PLACEHOLDER
    
    user_to_add = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(user_to_add)
    db.session.commit()
    
    return redirect('/')

@app.route('/edit_user<int:user_id>')
def edit_form(user_id):
    user=User.get_by_id(user_id)
    
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.image_url = request.form.get('image_url')
    
    return render_template('edit_user.html', user=user)

@app.route('/edit', methods=['POST'])
def edit_user():
    # pass
    # new_first_name = User.query.filter_by(first_name=request.form.get('first_name')).first()
    # new_first_name.first_name = 'test'
    
    # last_name = request.form.get('last_name')
    # image_url = request.form.get('image_url')
    
    # user_to_add = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    # db.session.add(user_to_add)
    # db.session.commit()
    
    return 'test'
    
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect('/')

@app.route('/<int:user_id>')
def show_user_details(user_id):
    
    user = User.query.get(user_id)
    return render_template('user_details.html', user=user)


@app.route('/<int:user_id>/posts/new')
def posts(user_id):
    posts = Post.query.all()
    user = User.query.get_or_404(user_id)
    
    return render_template('posts/new.html', user=user, posts=posts)

@app.route('/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    
    user = User.query.get_or_404(user_id)
    post_title = request.form.get('post_title')
    post_content = request.form.get('post_content')
    
    
    post_to_add = Post(title=post_title, content=post_content, user_id=user_id)
    
    db.session.add(post_to_add)
    db.session.commit()
    
    return redirect(f'/{user.id}')

@app.route('/<int:post_id>/posts')
def show_posts(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)
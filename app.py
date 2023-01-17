from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from models import db, connect_db, User, Post, PostTag, Tag, TestUser

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/blogly'
app.config['SQLALCHEMY_BINDS'] = {'testDB': 'sqlite:///test_blogly.db'}

app.debug = False
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
    

# USER-RELATED ROUTES
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

@app.route('/edit_user/<int:user_id>')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    print(user)
    return render_template('edit_user.html', user=user)

@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user_form(user_id):
    user=User.query.get_or_404(user_id)
    
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    if not user.image_url:
        user.image_url = User.PLACEHOLDER
    
    db.session.add(user)
    db.session.commit()
    
    return redirect(f'/')
    
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

# POST RELATED ROUTES
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

@app.route('/posts/show_all')
def show_all_posts():
    posts = Post.query.all()
    users = User.query.all()

    return render_template('/posts/show_all.html', posts=posts, users=users)


@app.route('/<int:post_id>/posts')
def show_posts(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/post_id_<int:post_id>')
def show_user_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    return render_template('/posts/show.html', post=post)

@app.route('/posts/edit_post_<int:post_id>')
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/edit_post_<int:post_id>', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    post.tag = request.form.get('tag_name')
    
    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/posts/post_id_{post_id}')
    
@app.route('/delete_post_<int:post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/{user_id}')


# TAG RELATED ROUTES

@app.route('/tags')
def show_tag_info():
    tags = Tag.query.all()
    return render_template('/tags/tags.html', tags=tags)

@app.route('/tags/new')
def new_tag_form():
    posts = Post.query.all()
    return render_template('/tags/new_tags.html', posts=posts)

@app.route('/tags/new', methods=['GET', 'POST'])
def create_new_tag():
        
    new_tag_name = request.form.get('tag_name')
    tag_to_add = Tag(name=new_tag_name)
    
    db.session.add(tag_to_add)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tags(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/show_tags.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    
    return render_template('/tags/edit_tag.html', tag=tag, posts=posts)



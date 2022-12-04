from flask import Flask, request, render_template, redirect
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogly.db'

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
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
# from models import full_names
# db.session.add_all(full_names)
# db.session.commit()

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
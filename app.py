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
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    
    # no idea how to do this, stackoverflow isn't showing anything compelling. I need to ask a tutor
    # In the meantime, this is a placeholder
    PLACEHOLDER = 'https://www.clipartmax.com/png/middle/340-3400182_special-school-nurse-placeholder-person.png'
    image_url = db.Column(db.String(50), nullable=True, unique=False, default=PLACEHOLDER)
    
    def __repr__(self):
        return f'User #{self.id}: Full name is {self.first_name} {self.last_name}'
    
# test = User(id=1, first_name='Vic', last_name='Del', image_name='img')
# db.session.add(test)
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
    
    user_to_add = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user_to_add)
    db.session.commit()
    return redirect('/')
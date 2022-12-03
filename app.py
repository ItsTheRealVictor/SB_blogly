from flask import Flask, request, render_template
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
    image_name = db.Column(db.String(50), nullable=True, unique=False, default='Cool Image!')
    
    def __repr__(self):
        return f'User #{self.id}: Full name is {self.first_name} {self.last_name}'
    
# test = User(id=1, first_name='Vic', last_name='Del', image_name='img')
# db.session.add(test)
# db.session.commit()

@app.route('/')
def home():
    return render_template('home.html')
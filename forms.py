from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField



class AddTagForm(FlaskForm):
    
    name = StringField()
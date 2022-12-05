from unittest import TestCase
from app import app, db, TestUser
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



class BloglyTestCase(TestCase):
    
    def setUp(self):
        TestUser.query.delete()
        
    def tearDown(self):
        db.session.rollback()
    
    
    def test_home_page(self):
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('Welcome to the Victor Blogly!', html)
            

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
    
            
    def test_greet(self):
        test_example = TestUser(first_name='testFirst', last_name='testLast', image_url='testURL')
        self.assertEqual(test_example.greet(), 'Greetings to you, testFirst testLast')
        
        
    def test_home_page(self):
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('Welcome to the Victor Blogly!', html)
            
    def test_get_by_id(self):
        example = TestUser(first_name='example1', last_name='example2', image_url='example3')
        db.session.add(example)
        db.session.commit()
        
        test_example = TestUser.get_by_id(1)
        self.assertEquals(test_example, example)

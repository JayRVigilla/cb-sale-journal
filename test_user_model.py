""" User Model Tests
  to run:
    python -m unittest test_user_model.py
"""

import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User

# environmental variable for test database

os.environ['DATABASE_URL'] = "postgresql:///sales-journal-test"

from app import app
db.create_all()


class UserModelTestCase(TestCase):
    """ Test views for sales_reports """

    def setUp(self):
        """ Create test client, add sample data."""

        User.query.delete()

        u1 = User(
            username='test1',
            first_name='Test1',
            last_name='User',
            passsword='password1'
        )

        db.session.add(u1)

        u2 = User(
            username='test2',
            first_name='Test2',
            last_name='User',
            passsword='password2')

        db.session.add(u2)

        self.client = app.test_client()

    def tearDown(self):
        """ Clean slate each time """

        db.session.rollback()

    def test_user_register_valid(self):
        """ Valid sign up scenario """

        u_valid = User.register(
            'testUser',
            'validpassword',
            'Test',
            'Name',
            'about:blank',
            'candidate')
        u_valid.id = 99999
        db.session.commit()

        valid_test = User.query(99999)

        self.assertEqual(valid_test.username, 'testUser')
        self.assertNotEqual(
            valid_test.password, 'testUser')  # password gets hashed
        self.assertTrue(valid_test.password.startswith("$2b$"))
        self.assertEqual(valid_test.first_name, 'Test')
        self.assertEqual(valid_test.last_name, 'Name')
        self.assertEqual(valid_test.username, 'testUser')
        self.assertEqual(valid_test.img_url, 'about:blank')
        self.assertEqual(valid_test.status, 'candidate')

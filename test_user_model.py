""" User Model Tests
  to run:
    python -m unittest test_user_model.py
"""

import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, SalesReport

# environmental variable for test database

os.environ['DATABASE_URL'] = "postgresql:///sales-journal-test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """ Test views for sales_reports """

    def setUp(self):
		""" Create test client, add sample data."""

    User.query.delete()
    SalesReport.query.delete()

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
		passsword='password2'
	)

	db.session.add(u1)

	self.client = app.test_client()

	def tearDown(self):
		""" Clean slate each time """

		db.session.rollback()

	def test_user_model(self):

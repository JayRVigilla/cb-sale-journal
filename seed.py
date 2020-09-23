"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import app
from models import User, SalesReport, db

db.drop_all()
db.create_all()

# with open('generator/users.csv') as users:
#     db.session.bulk_insert_mappings(User, DictReader(users))
with open('generator/salesReport.csv') as users:
    db.session.bulk_insert_mappings(SalesReport, DictReader(sales-reports))
db.session.commit()

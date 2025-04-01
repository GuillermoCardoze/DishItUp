#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db

if __name__ == '__main__':
    with app.app_context():
        print("Start Seeding")


        db.drop_all()
        db.create_all()
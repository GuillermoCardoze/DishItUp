#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Dish, Recipe, Message

# if __name__ == '__main__':
#     with app.app_context():
#         print("Start Seeding")


#         db.drop_all()
#         db.create_all()

def seed_data():
    with app.app_context():
        # Clear existing data
        db.session.commit()
        db.drop_all()
        db.create_all()

        # Create Users
        user1 = User(username='chefjohn', email='chefjohn@example.com')
        user1.password = 'password123'
        
        user2 = User(username='foodie92', email='foodie92@example.com')
        user2.password = 'securepass'

        db.session.add_all([user1, user2])
        db.session.commit()

        # Create Dishes
        dish1 = Dish(name='Spaghetti Carbonara', cuisine='Italian')
        dish2 = Dish(name='Sushi Roll', cuisine='Japanese')

        db.session.add_all([dish1, dish2])
        db.session.commit()

        # Create Recipes
        recipe1 = Recipe(
            title='Classic Carbonara',
            ingredients='Pasta, Eggs, Cheese, Pancetta, Pepper',
            instructions='Cook pasta. Mix eggs and cheese. Fry pancetta. Combine all.',
            user_id=user1.id,
            dish_id=dish1.id
        )

        recipe2 = Recipe(
            title='Homemade Sushi',
            ingredients='Rice, Nori, Fish, Soy Sauce',
            instructions='Prepare rice. Roll with fish and nori. Serve with soy sauce.',
            user_id=user2.id,
            dish_id=dish2.id
        )

        db.session.add_all([recipe1, recipe2])
        db.session.commit()

        # Create Messages
        message1 = Message(sender_id=user1.id, receiver_id=user2.id, content='Hey, love your sushi recipe!')
        message2 = Message(sender_id=user2.id, receiver_id=user1.id, content='Thanks! Your carbonara looks amazing.')

        db.session.add_all([message1, message2])
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()

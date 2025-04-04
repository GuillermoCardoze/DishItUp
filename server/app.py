#!/usr/bin/env python3

# Remote library imports
from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db, api
# Import models
from models import User, Recipe, Message, Dish

# Views go here!
class Dishes(Resource):
    def get(self):
        if session.get('user_id'):
            dishes = Dish.query.filter_by(user_id=session['user_id']).all()
            return [dish.to_dict() for dish in dishes], 200
        return {'error': '401 Unauthorized'}, 401
    
    def post(self):
        user_id = session.get('user_id')
        if user_id:
            request_json = request.get_json()

            name = request_json['name']
            cuisine = request_json['cuisine']

            try:
                dish = Dish(
                    name=name, 
                    cuisine=cuisine,
                    user_id=user_id
                    )

                db.session.add(dish)
                db.session.commit()
                return dish.to_dict(),201
            
            except IntegrityError:

                return {'error': "422 Unprocessable Entity"},422
        return {'error': '401 Unauthorized'}, 401

api.add_resource(Dishes, '/dishes')

class Signup(Resource):
    def post(self):
        form_json = request.get_json()

        new_user = User(
            username=form_json["username"],
            email=form_json["email"]
        )
        new_user.password = form_json["password"]  # Use setter to hash password

        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return new_user.to_dict(), 201
    
api.add_resource(Signup, '/signup')


class SignIn(Resource):
    def post(self):
        form_json = request.get_json()
        username = form_json["username"]
        password = form_json["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):  # Ensuring proper authentication
            session["user_id"] = user.id
            return user.to_dict(), 200
        else:
            return {"error": "Invalid Credentials"}, 401  # Use JSON response

api.add_resource(SignIn, '/signin')


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")  # Prevent KeyError

        if user_id:
            user = User.query.get(user_id)  # More efficient than filter().first()
            if user:
                return user.to_dict(), 200
        return {}, 401
    
api.add_resource(CheckSession, '/check_session')


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)  # Remove session key
        return {}, 204
    
api.add_resource(Logout, '/logout')


# @app.before_request
# def check_session():
#     if "user_id" not in session:
#         session["user_id"] = None
#     else:
#         print("User is logged in:", session["user_id"])  # Debugging info


if __name__ == '__main__':
    app.run(port=5555, debug=True)

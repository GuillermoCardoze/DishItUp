from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime, timezone
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, flask_bcrypt

# Models go here!
# Association table for users and favorite recipes (many-to-many)
user_favorite_recipes = db.Table(
    'user_favorite_recipes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column("password_hash", db.String)    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    recipes = db.relationship('Recipe', backref='user', lazy=True)
    favorite_recipes = db.relationship('Recipe', secondary=user_favorite_recipes, backref='favorited_by')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)

    #Serialize Rules
    serialize_rules = ('-_password_hash', '-recipes.user', '-sent_messages.sender', '-received_messages.receiver')

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError('Invalid email address')
        return email

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return username
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password(self, password):
        password_hash = flask_bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password.encode("utf-8"))


class Dish(db.Model, SerializerMixin):
    __tablename__ = 'dishes'
    serialize_rules = ('-recipes.dish',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    recipes = db.relationship('Recipe', backref='dish', lazy=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Dish name cannot be empty')
        return name


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    serialize_rules = ('-user.recipes', '-dish.recipes')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)

    @validates('title')
    def validate_title(self, key, title):
        if len(title) < 3:
            raise ValueError('Recipe title must be at least 3 characters long')
        return title

    @validates('ingredients', 'instructions')
    def validate_text_fields(self, key, value):
        if not value.strip():
            raise ValueError(f'{key} cannot be empty')
        return value


class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
    serialize_rules = ('-sender.sent_messages', '-receiver.received_messages')

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    read_status = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)
    thread_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.receiver_id}>'

    @validates('content')
    def validate_content(self, key, content):
        if not content.strip():
            raise ValueError('Message content cannot be empty')
        return content

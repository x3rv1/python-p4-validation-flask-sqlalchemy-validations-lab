from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Author must have a non-empty name.")
        
        # Check for uniqueness
        if Author.query.filter_by(name=value).first():
            raise ValueError("Name must be unique")
            
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if value is None:
            return value
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Post must have a non-empty title.")
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("Title must contain one of: 'Won't Believe', 'Secret', 'Top', or 'Guess'.")
        return value

    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError("Summary must not exceed 250 characters.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        allowed_categories = ["Fiction", "Non-Fiction"]
        if value not in allowed_categories:
            raise ValueError(f"Category must be one of {allowed_categories}.")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db
from datetime import datetime


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    # User types
    USER_TYPES = ['university', 'company', 'investor']
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), default='')
    last_name = db.Column(db.String(255), default='')
    user_type = db.Column(db.String(20), nullable=False, default='university')
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ttoprofile = db.relationship('TTOProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def __str__(self):
        return self.email
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def display_name(self):
        """Return full name or email"""
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.email
    
    @property
    def is_university(self):
        return self.user_type == 'university'
    
    @property
    def is_company(self):
        return self.user_type == 'company'
    
    @property
    def is_investor(self):
        return self.user_type == 'investor'


class TTOProfile(db.Model):
    """Technology Transfer Office profile for university users"""
    __tablename__ = 'tto_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    institution_name = db.Column(db.String(255), default='')
    office_name = db.Column(db.String(255), default='')
    country = db.Column(db.String(100), default='')
    therapeutic_focus_tags = db.Column(db.JSON, default=list)  # Stored as JSON array
    trl_range_interest_min = db.Column(db.Integer, nullable=True)
    trl_range_interest_max = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TTOProfile {self.user.email}>'
    
    def __str__(self):
        return f"TTO Profile for {self.user.display_name}"

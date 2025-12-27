"""
User Data Models - Doctor/Admin data models
Handles user authentication and role-based access
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class UserRole(Enum):
    """User role enumeration"""
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    RECEPTIONIST = "receptionist"


class UserException(Exception):
    """Custom exception for user-related errors"""
    pass


@dataclass
class User:
    """User data model for hospital staff"""
    user_id: str
    username: str
    password: str
    role: UserRole
    full_name: str
    email: str
    phone: Optional[str] = None
    specialization: Optional[str] = None  # For doctors
    is_active: bool = True
    
    def __post_init__(self):
        """Validate user data after initialization"""
        if not self.username or len(self.username) < 3:
            raise UserException("Username must be at least 3 characters long")
        
        if not self.password or len(self.password) < 6:
            raise UserException("Password must be at least 6 characters long")
        
        if not self.full_name:
            raise UserException("Full name is required")
        
        if isinstance(self.role, str):
            self.role = UserRole(self.role)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'role': self.role.value,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'specialization': self.specialization,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create user object from dictionary"""
        return cls(
            user_id=data['user_id'],
            username=data['username'],
            password=data['password'],
            role=UserRole(data['role']),
            full_name=data['full_name'],
            email=data['email'],
            phone=data.get('phone'),
            specialization=data.get('specialization'),
            is_active=data.get('is_active', True)
        )
    
    def verify_password(self, password: str) -> bool:
        """Verify user password"""
        return self.password == password

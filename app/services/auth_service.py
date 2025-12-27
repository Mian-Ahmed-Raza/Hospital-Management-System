"""
Authentication Service - Authentication logic
Handles user login, logout, and session management
"""

from typing import Optional, Dict
from app.models.user import User, UserRole, UserException
from app.utils.db_connector import DatabaseConnector


class AuthenticationException(Exception):
    """Custom exception for authentication errors"""
    pass


class AuthService:
    """Authentication service for user management"""
    
    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize authentication service
        
        Args:
            db_connector: Database connector instance
        """
        self.db = db_connector
        self.current_user: Optional[User] = None
    
    def login(self, username: str, password: str) -> User:
        """
        Authenticate user and create session
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Authenticated user object
            
        Raises:
            AuthenticationException: If authentication fails
        """
        if not username or not password:
            raise AuthenticationException("Username and password are required")
        
        # Fetch user from database
        users = self.db.read('users', {'username': username})
        
        if not users:
            raise AuthenticationException("Invalid username or password")
        
        user_data = users[0]
        
        # Check if user is active
        if not user_data.get('is_active', True):
            raise AuthenticationException("User account is inactive")
        
        # Verify password
        if user_data['password'] != password:
            raise AuthenticationException("Invalid username or password")
        
        # Create user object
        try:
            self.current_user = User.from_dict(user_data)
            return self.current_user
        except Exception as e:
            raise AuthenticationException(f"Failed to load user data: {str(e)}")
    
    def logout(self):
        """Clear current session"""
        self.current_user = None
    
    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated
        
        Returns:
            True if user is logged in
        """
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[User]:
        """
        Get currently authenticated user
        
        Returns:
            Current user or None
        """
        return self.current_user
    
    def require_authentication(self):
        """
        Require user to be authenticated
        
        Raises:
            AuthenticationException: If user is not authenticated
        """
        if not self.is_authenticated():
            raise AuthenticationException("Authentication required")
    
    def require_role(self, required_role: UserRole):
        """
        Require user to have specific role
        
        Args:
            required_role: Required user role
            
        Raises:
            AuthenticationException: If user doesn't have required role
        """
        self.require_authentication()
        
        if self.current_user.role != required_role:
            raise AuthenticationException(f"Access denied. {required_role.value} role required")
    
    def has_permission(self, required_role: UserRole) -> bool:
        """
        Check if current user has required permission
        
        Args:
            required_role: Required role level
            
        Returns:
            True if user has permission
        """
        if not self.is_authenticated():
            return False
        
        role_hierarchy = {
            UserRole.ADMIN: 4,
            UserRole.DOCTOR: 3,
            UserRole.NURSE: 2,
            UserRole.RECEPTIONIST: 1
        }
        
        current_level = role_hierarchy.get(self.current_user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return current_level >= required_level
    
    def change_password(self, old_password: str, new_password: str) -> bool:
        """
        Change current user's password
        
        Args:
            old_password: Current password
            new_password: New password
            
        Returns:
            True if password was changed
            
        Raises:
            AuthenticationException: If password change fails
        """
        self.require_authentication()
        
        if not self.current_user.verify_password(old_password):
            raise AuthenticationException("Current password is incorrect")
        
        if len(new_password) < 6:
            raise AuthenticationException("New password must be at least 6 characters long")
        
        # Update password in database
        updates = {'password': new_password}
        success = self.db.update('users', self.current_user.user_id, 'user_id', updates)
        
        if success:
            self.current_user.password = new_password
            return True
        
        raise AuthenticationException("Failed to update password")

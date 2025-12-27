"""
Tests for authentication service
"""

import unittest
import os
import shutil
from app.services.auth_service import AuthService, AuthenticationException
from app.models.user import User, UserRole
from app.utils.db_connector import DatabaseConnector


class TestAuthService(unittest.TestCase):
    """Test cases for authentication service"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create test database in temporary directory
        self.test_data_dir = "test_data"
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        
        self.db = DatabaseConnector(self.test_data_dir)
        self.auth_service = AuthService(self.db)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
    
    def test_successful_login(self):
        """Test successful login with valid credentials"""
        # Use default admin credentials
        user = self.auth_service.login('admin', 'admin123')
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.role, UserRole.ADMIN)
        self.assertTrue(self.auth_service.is_authenticated())
    
    def test_failed_login_invalid_username(self):
        """Test login failure with invalid username"""
        with self.assertRaises(AuthenticationException):
            self.auth_service.login('invalid_user', 'password')
    
    def test_failed_login_invalid_password(self):
        """Test login failure with invalid password"""
        with self.assertRaises(AuthenticationException):
            self.auth_service.login('admin', 'wrong_password')
    
    def test_failed_login_empty_credentials(self):
        """Test login failure with empty credentials"""
        with self.assertRaises(AuthenticationException):
            self.auth_service.login('', '')
    
    def test_logout(self):
        """Test logout functionality"""
        # Login first
        self.auth_service.login('admin', 'admin123')
        self.assertTrue(self.auth_service.is_authenticated())
        
        # Logout
        self.auth_service.logout()
        self.assertFalse(self.auth_service.is_authenticated())
        self.assertIsNone(self.auth_service.get_current_user())
    
    def test_require_authentication(self):
        """Test authentication requirement"""
        # Should raise exception when not authenticated
        with self.assertRaises(AuthenticationException):
            self.auth_service.require_authentication()
        
        # Should not raise after login
        self.auth_service.login('admin', 'admin123')
        try:
            self.auth_service.require_authentication()
        except AuthenticationException:
            self.fail("require_authentication raised exception when authenticated")
    
    def test_permission_checking(self):
        """Test permission checking"""
        # Login as admin
        self.auth_service.login('admin', 'admin123')
        
        # Admin should have all permissions
        self.assertTrue(self.auth_service.has_permission(UserRole.ADMIN))
        self.assertTrue(self.auth_service.has_permission(UserRole.DOCTOR))
        self.assertTrue(self.auth_service.has_permission(UserRole.NURSE))


if __name__ == '__main__':
    unittest.main()

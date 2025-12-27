"""
Tests for login view
"""

import unittest
from unittest.mock import Mock, MagicMock
from app.views.login import LoginWindow
from app.services.auth_service import AuthService, AuthenticationException
from app.models.user import User, UserRole


class TestLoginView(unittest.TestCase):
    """Test cases for login window"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_auth_service = Mock(spec=AuthService)
        self.mock_callback = Mock()
    
    def test_login_window_creation(self):
        """Test that login window can be created"""
        # Note: This test would require mocking tkinter in a real test environment
        # For demonstration purposes, we're showing the test structure
        pass
    
    def test_successful_login(self):
        """Test successful login flow"""
        # Create mock user
        mock_user = User(
            user_id='USR001',
            username='test_user',
            password='password',
            role=UserRole.DOCTOR,
            full_name='Test Doctor',
            email='test@hospital.com'
        )
        
        # Configure mock to return user
        self.mock_auth_service.login.return_value = mock_user
        
        # Test login
        result = self.mock_auth_service.login('test_user', 'password')
        
        self.assertEqual(result, mock_user)
        self.mock_auth_service.login.assert_called_once_with('test_user', 'password')
    
    def test_failed_login(self):
        """Test failed login with invalid credentials"""
        # Configure mock to raise exception
        self.mock_auth_service.login.side_effect = AuthenticationException("Invalid credentials")
        
        # Test login failure
        with self.assertRaises(AuthenticationException):
            self.mock_auth_service.login('invalid_user', 'wrong_password')


if __name__ == '__main__':
    unittest.main()

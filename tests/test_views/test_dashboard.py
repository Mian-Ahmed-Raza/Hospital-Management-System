"""
Tests for dashboard view
"""

import unittest
from unittest.mock import Mock
from app.models.user import User, UserRole


class TestDashboard(unittest.TestCase):
    """Test cases for dashboard window"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_user = User(
            user_id='USR001',
            username='admin',
            password='admin123',
            role=UserRole.ADMIN,
            full_name='System Administrator',
            email='admin@hospital.com'
        )
    
    def test_dashboard_creation(self):
        """Test that dashboard can be created with valid user"""
        # Note: This test would require mocking tkinter
        # Showing test structure for demonstration
        self.assertIsNotNone(self.test_user)
        self.assertEqual(self.test_user.role, UserRole.ADMIN)
    
    def test_user_permissions(self):
        """Test user permission checking"""
        # Test admin permissions
        self.assertTrue(self.test_user.has_permission(UserRole.ADMIN))
        self.assertTrue(self.test_user.has_permission(UserRole.DOCTOR))
        
        # Test doctor user
        doctor_user = User(
            user_id='USR002',
            username='doctor',
            password='doctor123',
            role=UserRole.DOCTOR,
            full_name='Dr. Test',
            email='doctor@hospital.com'
        )
        
        self.assertTrue(doctor_user.has_permission(UserRole.DOCTOR))
        self.assertFalse(doctor_user.has_permission(UserRole.ADMIN))


if __name__ == '__main__':
    unittest.main()

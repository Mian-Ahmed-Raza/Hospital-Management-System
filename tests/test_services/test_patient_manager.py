"""
Tests for patient manager service
"""

import unittest
import os
import shutil
from app.services.patient_manager import PatientManager, PatientManagerException
from app.utils.db_connector import DatabaseConnector


class TestPatientManager(unittest.TestCase):
    """Test cases for patient manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create test database in temporary directory
        self.test_data_dir = "test_data_patients"
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        
        self.db = DatabaseConnector(self.test_data_dir)
        self.patient_manager = PatientManager(self.db)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
    
    def test_register_patient_success(self):
        """Test successful patient registration"""
        patient = self.patient_manager.register_patient(
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-01-01",
            gender="Male",
            phone="1234567890",
            email="john.doe@email.com"
        )
        
        self.assertIsNotNone(patient)
        self.assertEqual(patient.first_name, "John")
        self.assertEqual(patient.last_name, "Doe")
        self.assertTrue(patient.patient_id.startswith("PAT"))
    
    def test_register_patient_missing_required_fields(self):
        """Test patient registration with missing required fields"""
        with self.assertRaises(PatientManagerException):
            self.patient_manager.register_patient(
                first_name="",
                last_name="Doe",
                date_of_birth="1990-01-01",
                gender="Male",
                phone="1234567890"
            )
    
    def test_register_patient_invalid_phone(self):
        """Test patient registration with invalid phone"""
        with self.assertRaises(PatientManagerException):
            self.patient_manager.register_patient(
                first_name="John",
                last_name="Doe",
                date_of_birth="1990-01-01",
                gender="Male",
                phone="123"  # Too short
            )
    
    def test_register_patient_invalid_email(self):
        """Test patient registration with invalid email"""
        with self.assertRaises(PatientManagerException):
            self.patient_manager.register_patient(
                first_name="John",
                last_name="Doe",
                date_of_birth="1990-01-01",
                gender="Male",
                phone="1234567890",
                email="invalid_email"  # Invalid format
            )
    
    def test_get_patient(self):
        """Test retrieving a patient by ID"""
        # Register patient first
        patient = self.patient_manager.register_patient(
            first_name="Jane",
            last_name="Smith",
            date_of_birth="1985-05-15",
            gender="Female",
            phone="9876543210"
        )
        
        # Retrieve patient
        retrieved = self.patient_manager.get_patient(patient.patient_id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.patient_id, patient.patient_id)
        self.assertEqual(retrieved.full_name, "Jane Smith")
    
    def test_get_patient_not_found(self):
        """Test retrieving non-existent patient"""
        patient = self.patient_manager.get_patient("PAT999")
        self.assertIsNone(patient)
    
    def test_search_patients(self):
        """Test searching for patients"""
        # Register multiple patients
        self.patient_manager.register_patient(
            first_name="Alice",
            last_name="Johnson",
            date_of_birth="1992-03-20",
            gender="Female",
            phone="1111111111"
        )
        
        self.patient_manager.register_patient(
            first_name="Bob",
            last_name="Williams",
            date_of_birth="1988-07-10",
            gender="Male",
            phone="2222222222"
        )
        
        # Search by name
        results = self.patient_manager.search_patients(search_term="Alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].first_name, "Alice")
    
    def test_update_patient(self):
        """Test updating patient information"""
        # Register patient
        patient = self.patient_manager.register_patient(
            first_name="Charlie",
            last_name="Brown",
            date_of_birth="1995-09-25",
            gender="Male",
            phone="3333333333"
        )
        
        # Update patient
        success = self.patient_manager.update_patient(
            patient.patient_id,
            email="charlie.brown@email.com"
        )
        
        self.assertTrue(success)
        
        # Verify update
        updated = self.patient_manager.get_patient(patient.patient_id)
        self.assertEqual(updated.email, "charlie.brown@email.com")
    
    def test_delete_patient(self):
        """Test soft delete of patient"""
        # Register patient
        patient = self.patient_manager.register_patient(
            first_name="David",
            last_name="Miller",
            date_of_birth="1980-11-30",
            gender="Male",
            phone="4444444444"
        )
        
        # Delete patient
        success = self.patient_manager.delete_patient(patient.patient_id)
        self.assertTrue(success)
        
        # Verify patient is marked as inactive
        all_patients = self.patient_manager.get_all_patients()
        self.assertEqual(len(all_patients), 0)  # Should not include inactive patients
    
    def test_get_patient_count(self):
        """Test getting total patient count"""
        initial_count = self.patient_manager.get_patient_count()
        
        # Register patients
        self.patient_manager.register_patient(
            first_name="Eva",
            last_name="Davis",
            date_of_birth="1993-04-18",
            gender="Female",
            phone="5555555555"
        )
        
        self.patient_manager.register_patient(
            first_name="Frank",
            last_name="Wilson",
            date_of_birth="1987-08-22",
            gender="Male",
            phone="6666666666"
        )
        
        new_count = self.patient_manager.get_patient_count()
        self.assertEqual(new_count, initial_count + 2)


if __name__ == '__main__':
    unittest.main()

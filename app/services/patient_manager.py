"""
Patient Manager - CRUD operations for patients
Handles patient registration and management
"""

from typing import List, Optional, Dict
from app.models.patient import Patient, PatientException
from app.utils.db_connector import DatabaseConnector
from app.utils.validators import (
    validate_email, validate_phone, validate_date,
    validate_required, ValidationException
)


class PatientManagerException(Exception):
    """Custom exception for patient management errors"""
    pass


class PatientManager:
    """Service for managing patient records"""
    
    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize patient manager
        
        Args:
            db_connector: Database connector instance
        """
        self.db = db_connector
    
    def register_patient(self, first_name: str, last_name: str, date_of_birth: str,
                        gender: str, phone: str, email: str = None, address: str = None,
                        blood_group: str = None, emergency_contact: str = None) -> Patient:
        """
        Register a new patient
        
        Args:
            first_name: Patient's first name
            last_name: Patient's last name
            date_of_birth: Date of birth (YYYY-MM-DD)
            gender: Gender (Male/Female/Other)
            phone: Phone number
            email: Email address (optional)
            address: Home address (optional)
            blood_group: Blood group (optional)
            emergency_contact: Emergency contact number (optional)
            
        Returns:
            Created patient object
            
        Raises:
            PatientManagerException: If registration fails
        """
        try:
            # Validate inputs
            validate_required(first_name, "First name")
            validate_required(last_name, "Last name")
            validate_date(date_of_birth)
            validate_phone(phone)
            
            if email:
                validate_email(email)
            
            # Generate patient ID
            patient_id = self.db.get_next_id('patients', 'PAT')
            
            # Create patient object
            patient = Patient(
                patient_id=patient_id,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                phone=phone,
                email=email,
                address=address,
                blood_group=blood_group,
                emergency_contact=emergency_contact
            )
            
            # Save to database
            self.db.create('patients', patient.to_dict())
            
            return patient
            
        except (ValidationException, PatientException) as e:
            raise PatientManagerException(str(e))
        except Exception as e:
            raise PatientManagerException(f"Failed to register patient: {str(e)}")
    
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """
        Get patient by ID
        
        Args:
            patient_id: Patient ID
            
        Returns:
            Patient object or None
        """
        try:
            patients = self.db.read('patients', {'patient_id': patient_id})
            
            if patients:
                return Patient.from_dict(patients[0])
            
            return None
            
        except Exception as e:
            raise PatientManagerException(f"Failed to retrieve patient: {str(e)}")
    
    def search_patients(self, search_term: str = None, filters: Dict = None) -> List[Patient]:
        """
        Search for patients
        
        Args:
            search_term: Search by name or ID
            filters: Additional filters
            
        Returns:
            List of matching patients
        """
        try:
            # Get all active patients
            all_patients = self.db.read('patients', {'is_active': True})
            
            patients = []
            for data in all_patients:
                patient = Patient.from_dict(data)
                
                # Apply search term
                if search_term:
                    search_lower = search_term.lower()
                    if not (search_lower in patient.full_name.lower() or 
                           search_lower in patient.patient_id.lower() or
                           search_lower in patient.phone):
                        continue
                
                # Apply additional filters
                if filters:
                    match = True
                    for key, value in filters.items():
                        if not hasattr(patient, key) or getattr(patient, key) != value:
                            match = False
                            break
                    if not match:
                        continue
                
                patients.append(patient)
            
            return patients
            
        except Exception as e:
            raise PatientManagerException(f"Failed to search patients: {str(e)}")
    
    def update_patient(self, patient_id: str, **updates) -> bool:
        """
        Update patient information
        
        Args:
            patient_id: Patient ID
            **updates: Fields to update
            
        Returns:
            True if successful
        """
        try:
            # Validate updates if applicable
            if 'email' in updates and updates['email']:
                validate_email(updates['email'])
            
            if 'phone' in updates:
                validate_phone(updates['phone'])
            
            success = self.db.update('patients', patient_id, 'patient_id', updates)
            
            if not success:
                raise PatientManagerException("Patient not found")
            
            return True
            
        except ValidationException as e:
            raise PatientManagerException(str(e))
        except Exception as e:
            raise PatientManagerException(f"Failed to update patient: {str(e)}")
    
    def delete_patient(self, patient_id: str) -> bool:
        """
        Soft delete patient (mark as inactive)
        
        Args:
            patient_id: Patient ID
            
        Returns:
            True if successful
        """
        try:
            return self.db.update('patients', patient_id, 'patient_id', {'is_active': False})
        except Exception as e:
            raise PatientManagerException(f"Failed to delete patient: {str(e)}")
    
    def get_all_patients(self) -> List[Patient]:
        """
        Get all active patients
        
        Returns:
            List of all patients
        """
        try:
            patient_data = self.db.read('patients', {'is_active': True})
            return [Patient.from_dict(data) for data in patient_data]
        except Exception as e:
            raise PatientManagerException(f"Failed to retrieve patients: {str(e)}")
    
    def get_patient_count(self) -> int:
        """
        Get total number of active patients
        
        Returns:
            Number of active patients
        """
        try:
            patients = self.db.read('patients', {'is_active': True})
            return len(patients)
        except Exception as e:
            return 0

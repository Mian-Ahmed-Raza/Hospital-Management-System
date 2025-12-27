"""
Patient Data Models - Patient data entities
Handles patient information and medical records
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


class PatientException(Exception):
    """Custom exception for patient-related errors"""
    pass


@dataclass
class Patient:
    """Patient data model"""
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    emergency_contact: Optional[str] = None
    registration_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    is_active: bool = True
    
    def __post_init__(self):
        """Validate patient data after initialization"""
        if not self.first_name or not self.last_name:
            raise PatientException("First name and last name are required")
        
        if not self.phone or len(self.phone) < 10:
            raise PatientException("Valid phone number is required")
        
        if self.gender not in ['Male', 'Female', 'Other']:
            raise PatientException("Gender must be Male, Female, or Other")
        
        try:
            datetime.strptime(self.date_of_birth, "%Y-%m-%d")
        except ValueError:
            raise PatientException("Date of birth must be in YYYY-MM-DD format")
    
    @property
    def full_name(self) -> str:
        """Get patient's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int:
        """Calculate patient's age"""
        try:
            birth_date = datetime.strptime(self.date_of_birth, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth_date.year
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
            return age
        except:
            return 0
    
    def to_dict(self):
        """Convert patient object to dictionary"""
        return {
            'patient_id': self.patient_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'blood_group': self.blood_group,
            'emergency_contact': self.emergency_contact,
            'registration_date': self.registration_date,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create patient object from dictionary"""
        return cls(
            patient_id=data['patient_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
            gender=data['gender'],
            phone=data['phone'],
            email=data.get('email'),
            address=data.get('address'),
            blood_group=data.get('blood_group'),
            emergency_contact=data.get('emergency_contact'),
            registration_date=data.get('registration_date', datetime.now().strftime("%Y-%m-%d")),
            is_active=data.get('is_active', True)
        )

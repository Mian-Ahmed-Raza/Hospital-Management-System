"""
Appointment Data Models - Appointment record models
Handles appointment scheduling and management
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum


class AppointmentStatus(Enum):
    """Appointment status enumeration"""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AppointmentException(Exception):
    """Custom exception for appointment-related errors"""
    pass


@dataclass
class Appointment:
    """Appointment data model"""
    appointment_id: str
    patient_id: str
    patient_name: str
    doctor_id: str
    doctor_name: str
    appointment_date: str
    appointment_time: str
    department: str
    reason: str
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    notes: Optional[str] = None
    created_at: str = None
    
    def __post_init__(self):
        """Validate appointment data after initialization"""
        if not self.patient_id or not self.doctor_id:
            raise AppointmentException("Patient ID and Doctor ID are required")
        
        if not self.appointment_date or not self.appointment_time:
            raise AppointmentException("Appointment date and time are required")
        
        try:
            datetime.strptime(self.appointment_date, "%Y-%m-%d")
        except ValueError:
            raise AppointmentException("Date must be in YYYY-MM-DD format")
        
        try:
            datetime.strptime(self.appointment_time, "%H:%M")
        except ValueError:
            raise AppointmentException("Time must be in HH:MM format")
        
        if isinstance(self.status, str):
            self.status = AppointmentStatus(self.status)
        
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        """Convert appointment object to dictionary"""
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'patient_name': self.patient_name,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor_name,
            'appointment_date': self.appointment_date,
            'appointment_time': self.appointment_time,
            'department': self.department,
            'reason': self.reason,
            'status': self.status.value,
            'notes': self.notes,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create appointment object from dictionary"""
        return cls(
            appointment_id=data['appointment_id'],
            patient_id=data['patient_id'],
            patient_name=data['patient_name'],
            doctor_id=data['doctor_id'],
            doctor_name=data['doctor_name'],
            appointment_date=data['appointment_date'],
            appointment_time=data['appointment_time'],
            department=data['department'],
            reason=data['reason'],
            status=AppointmentStatus(data.get('status', 'scheduled')),
            notes=data.get('notes'),
            created_at=data.get('created_at')
        )

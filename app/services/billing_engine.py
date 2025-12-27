"""
Billing Engine - Refactored legacy billing logic
Handles billing calculations and invoice generation
"""

from typing import List, Dict, Optional
from datetime import datetime
from app.utils.db_connector import DatabaseConnector


class BillingException(Exception):
    """Custom exception for billing errors"""
    pass


class BillingItem:
    """Represents a single billing item"""
    
    def __init__(self, description: str, quantity: int, unit_price: float):
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
    
    @property
    def total(self) -> float:
        """Calculate total for this item"""
        return self.quantity * self.unit_price
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'description': self.description,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total': self.total
        }


class Invoice:
    """Represents a billing invoice"""
    
    def __init__(self, invoice_id: str, patient_id: str, patient_name: str):
        self.invoice_id = invoice_id
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.items: List[BillingItem] = []
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.discount_percent = 0.0
        self.tax_percent = 0.0
        self.status = "pending"
    
    def add_item(self, description: str, quantity: int, unit_price: float):
        """Add item to invoice"""
        item = BillingItem(description, quantity, unit_price)
        self.items.append(item)
    
    @property
    def subtotal(self) -> float:
        """Calculate subtotal"""
        return sum(item.total for item in self.items)
    
    @property
    def discount_amount(self) -> float:
        """Calculate discount amount"""
        return self.subtotal * (self.discount_percent / 100)
    
    @property
    def tax_amount(self) -> float:
        """Calculate tax amount"""
        return (self.subtotal - self.discount_amount) * (self.tax_percent / 100)
    
    @property
    def total(self) -> float:
        """Calculate total amount"""
        return self.subtotal - self.discount_amount + self.tax_amount
    
    def to_dict(self) -> Dict:
        """Convert invoice to dictionary"""
        return {
            'invoice_id': self.invoice_id,
            'patient_id': self.patient_id,
            'patient_name': self.patient_name,
            'date': self.date,
            'items': [item.to_dict() for item in self.items],
            'subtotal': self.subtotal,
            'discount_percent': self.discount_percent,
            'discount_amount': self.discount_amount,
            'tax_percent': self.tax_percent,
            'tax_amount': self.tax_amount,
            'total': self.total,
            'status': self.status
        }


class BillingEngine:
    """Service for managing billing and invoices"""
    
    # Service pricing catalog
    SERVICES = {
        'consultation': {'name': 'Doctor Consultation', 'price': 500.0},
        'checkup': {'name': 'General Checkup', 'price': 300.0},
        'blood_test': {'name': 'Blood Test', 'price': 400.0},
        'xray': {'name': 'X-Ray', 'price': 800.0},
        'ultrasound': {'name': 'Ultrasound', 'price': 1200.0},
        'mri': {'name': 'MRI Scan', 'price': 5000.0},
        'ct_scan': {'name': 'CT Scan', 'price': 4000.0},
        'ecg': {'name': 'ECG', 'price': 250.0},
        'vaccination': {'name': 'Vaccination', 'price': 150.0},
        'minor_surgery': {'name': 'Minor Surgery', 'price': 10000.0},
        'admission_fee': {'name': 'Hospital Admission', 'price': 2000.0},
        'room_charge': {'name': 'Room Charge (per day)', 'price': 1500.0},
        'medicine': {'name': 'Medicines', 'price': 0.0}  # Variable pricing
    }
    
    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize billing engine
        
        Args:
            db_connector: Database connector instance
        """
        self.db = db_connector
    
    def create_invoice(self, patient_id: str, patient_name: str) -> Invoice:
        """
        Create new invoice
        
        Args:
            patient_id: Patient ID
            patient_name: Patient name
            
        Returns:
            New invoice object
        """
        try:
            invoice_id = self.db.get_next_id('billing', 'INV')
            return Invoice(invoice_id, patient_id, patient_name)
        except Exception as e:
            raise BillingException(f"Failed to create invoice: {str(e)}")
    
    def get_service_price(self, service_code: str) -> Optional[Dict]:
        """
        Get service details from catalog
        
        Args:
            service_code: Service code
            
        Returns:
            Service details or None
        """
        return self.SERVICES.get(service_code)
    
    def save_invoice(self, invoice: Invoice) -> bool:
        """
        Save invoice to database
        
        Args:
            invoice: Invoice object
            
        Returns:
            True if successful
        """
        try:
            self.db.create('billing', invoice.to_dict())
            return True
        except Exception as e:
            raise BillingException(f"Failed to save invoice: {str(e)}")
    
    def get_invoice(self, invoice_id: str) -> Optional[Dict]:
        """
        Get invoice by ID
        
        Args:
            invoice_id: Invoice ID
            
        Returns:
            Invoice data or None
        """
        try:
            invoices = self.db.read('billing', {'invoice_id': invoice_id})
            return invoices[0] if invoices else None
        except Exception as e:
            raise BillingException(f"Failed to retrieve invoice: {str(e)}")
    
    def get_patient_invoices(self, patient_id: str) -> List[Dict]:
        """
        Get all invoices for a patient
        
        Args:
            patient_id: Patient ID
            
        Returns:
            List of invoices
        """
        try:
            return self.db.read('billing', {'patient_id': patient_id})
        except Exception as e:
            raise BillingException(f"Failed to retrieve invoices: {str(e)}")
    
    def mark_invoice_paid(self, invoice_id: str) -> bool:
        """
        Mark invoice as paid
        
        Args:
            invoice_id: Invoice ID
            
        Returns:
            True if successful
        """
        try:
            return self.db.update('billing', invoice_id, 'invoice_id', {'status': 'paid'})
        except Exception as e:
            raise BillingException(f"Failed to update invoice status: {str(e)}")
    
    def calculate_appointment_bill(self, consultation: bool = True, 
                                  tests: List[str] = None) -> float:
        """
        Calculate bill for an appointment
        
        Args:
            consultation: Include consultation fee
            tests: List of test codes
            
        Returns:
            Total amount
        """
        total = 0.0
        
        if consultation:
            total += self.SERVICES['consultation']['price']
        
        if tests:
            for test_code in tests:
                service = self.get_service_price(test_code)
                if service:
                    total += service['price']
        
        return total

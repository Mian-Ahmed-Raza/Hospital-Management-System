"""
Report Generator Service - Generate various reports
Handles report data generation and formatting
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import json


class ReportGenerator:
    """Generate various types of reports"""
    
    def __init__(self, db_connector):
        """
        Initialize report generator
        
        Args:
            db_connector: Database connector instance
        """
        self.db = db_connector
    
    def generate_patient_summary_report(self, start_date=None, end_date=None) -> Dict[str, Any]:
        """
        Generate patient summary report
        
        Args:
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)
            
        Returns:
            Dictionary containing report data
        """
        try:
            # Get all patients
            patients = self.db.read('patients')
            
            # Filter by date if provided
            if start_date and end_date:
                filtered_patients = []
                for p in patients:
                    created_at = p.get('created_at', '')
                    # Convert datetime to date string if needed
                    if hasattr(created_at, 'strftime'):
                        created_at = created_at.strftime('%Y-%m-%d')
                    elif isinstance(created_at, str):
                        # Extract date part from ISO format (e.g., "2025-12-27T11:45:12.854753" -> "2025-12-27")
                        created_at = created_at.split('T')[0]
                    if created_at and start_date <= created_at <= end_date:
                        filtered_patients.append(p)
                patients = filtered_patients
            
            # Calculate statistics
            total_patients = len(patients)
            gender_distribution = {}
            blood_group_distribution = {}
            age_distribution = {'0-18': 0, '19-35': 0, '36-50': 0, '51-65': 0, '65+': 0}
            
            for patient in patients:
                # Gender distribution
                gender = patient.get('gender', 'Unknown')
                gender_distribution[gender] = gender_distribution.get(gender, 0) + 1
                
                # Blood group distribution
                blood_group = patient.get('blood_group', 'Unknown')
                blood_group_distribution[blood_group] = blood_group_distribution.get(blood_group, 0) + 1
                
                # Age distribution
                dob = patient.get('date_of_birth', '')
                if dob:
                    try:
                        birth_year = int(dob.split('-')[0])
                        current_year = datetime.now().year
                        age = current_year - birth_year
                        
                        if age <= 18:
                            age_distribution['0-18'] += 1
                        elif age <= 35:
                            age_distribution['19-35'] += 1
                        elif age <= 50:
                            age_distribution['36-50'] += 1
                        elif age <= 65:
                            age_distribution['51-65'] += 1
                        else:
                            age_distribution['65+'] += 1
                    except (ValueError, IndexError):
                        pass
            
            return {
                'report_type': 'Patient Summary',
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'period': f"{start_date or 'All'} to {end_date or 'All'}",
                'total_patients': total_patients,
                'gender_distribution': gender_distribution,
                'blood_group_distribution': blood_group_distribution,
                'age_distribution': age_distribution,
                'patients': patients
            }
        except Exception as e:
            return {
                'error': str(e),
                'report_type': 'Patient Summary',
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def generate_appointment_report(self, start_date=None, end_date=None) -> Dict[str, Any]:
        """
        Generate appointment report
        
        Args:
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)
            
        Returns:
            Dictionary containing report data
        """
        try:
            # Get all appointments
            appointments = self.db.read('appointments')
            
            # Filter by date if provided
            if start_date and end_date:
                appointments = [a for a in appointments if start_date <= a.get('appointment_date', '') <= end_date]
            
            # Calculate statistics
            total_appointments = len(appointments)
            status_distribution = {}
            department_distribution = {}
            daily_appointments = {}
            
            for appointment in appointments:
                # Status distribution
                status = appointment.get('status', 'Unknown')
                # Convert enum to string if needed
                if hasattr(status, 'value'):
                    status = status.value
                status_distribution[status] = status_distribution.get(status, 0) + 1
                
                # Department distribution
                department = appointment.get('department', 'Unknown')
                department_distribution[department] = department_distribution.get(department, 0) + 1
                
                # Daily appointments
                date = appointment.get('appointment_date', 'Unknown')
                daily_appointments[date] = daily_appointments.get(date, 0) + 1
            
            return {
                'report_type': 'Appointment Report',
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'period': f"{start_date or 'All'} to {end_date or 'All'}",
                'total_appointments': total_appointments,
                'status_distribution': status_distribution,
                'department_distribution': department_distribution,
                'daily_appointments': daily_appointments,
                'appointments': appointments
            }
        except Exception as e:
            return {
                'error': str(e),
                'report_type': 'Appointment Report',
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def generate_financial_report(self, start_date=None, end_date=None) -> Dict[str, Any]:
        """
        Generate financial/billing report
        
        Args:
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)
            
        Returns:
            Dictionary containing report data
        """
        try:
            # Get all billing records
            bills = self.db.read('billing')
            
            # Filter by date if provided
            if start_date and end_date:
                bills = [b for b in bills if start_date <= b.get('bill_date', '') <= end_date]
            
            # Calculate statistics
            total_revenue = 0
            total_pending = 0
            total_paid = 0
            payment_method_distribution = {}
            daily_revenue = {}
            service_revenue = {}
            
            for bill in bills:
                amount = float(bill.get('total_amount', 0))
                status = bill.get('payment_status', 'pending').lower()
                
                total_revenue += amount
                
                if status == 'paid':
                    total_paid += amount
                    payment_method = bill.get('payment_method', 'Unknown')
                    payment_method_distribution[payment_method] = payment_method_distribution.get(payment_method, 0) + amount
                else:
                    total_pending += amount
                
                # Daily revenue
                date = bill.get('bill_date', 'Unknown')
                daily_revenue[date] = daily_revenue.get(date, 0) + amount
                
                # Service revenue
                try:
                    services = json.loads(bill.get('services', '[]'))
                    for service in services:
                        service_name = service.get('description', 'Unknown')
                        service_total = float(service.get('total', 0))
                        service_revenue[service_name] = service_revenue.get(service_name, 0) + service_total
                except (json.JSONDecodeError, TypeError):
                    pass
            
            return {
                'report_type': 'Financial Report',
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'period': f"{start_date or 'All'} to {end_date or 'All'}",
                'total_revenue': total_revenue,
                'total_paid': total_paid,
                'total_pending': total_pending,
                'total_invoices': len(bills),
                'payment_method_distribution': payment_method_distribution,
                'daily_revenue': daily_revenue,
                'service_revenue': service_revenue,
                'bills': bills
            }
        except Exception as e:
            return {
                'error': str(e),
                'report_type': 'Financial Report',
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def generate_department_report(self) -> Dict[str, Any]:
        """
        Generate department-wise statistics report
        
        Returns:
            Dictionary containing report data
        """
        try:
            appointments = self.db.read('appointments')
            
            departments = {}
            
            for appointment in appointments:
                dept = appointment.get('department', 'Unknown')
                
                if dept not in departments:
                    departments[dept] = {
                        'total_appointments': 0,
                        'scheduled': 0,
                        'completed': 0,
                        'cancelled': 0,
                        'confirmed': 0
                    }
                
                departments[dept]['total_appointments'] += 1
                status = appointment.get('status', 'scheduled')
                # Convert enum to string if needed
                if hasattr(status, 'value'):
                    status = status.value
                status = str(status).lower()
                departments[dept][status] = departments[dept].get(status, 0) + 1
            
            return {
                'report_type': 'Department Report',
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'departments': departments
            }
        except Exception as e:
            return {
                'error': str(e),
                'report_type': 'Department Report',
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

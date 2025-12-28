"""Test script to check reports functionality"""

from app.utils.db_connector import DatabaseConnector
from app.services.report_generator import ReportGenerator

try:
    print("Initializing database and report generator...")
    db = DatabaseConnector()
    report_gen = ReportGenerator(db)
    
    print("\n1. Testing Patient Summary Report...")
    patient_report = report_gen.generate_patient_summary_report()
    print(f"   Report Type: {patient_report.get('report_type')}")
    print(f"   Total Patients: {patient_report.get('total_patients')}")
    print(f"   Gender Distribution: {patient_report.get('gender_distribution')}")
    
    print("\n2. Testing Appointment Report...")
    appt_report = report_gen.generate_appointment_report()
    print(f"   Report Type: {appt_report.get('report_type')}")
    print(f"   Total Appointments: {appt_report.get('total_appointments')}")
    
    print("\n3. Testing Financial Report...")
    financial_report = report_gen.generate_financial_report()
    print(f"   Report Type: {financial_report.get('report_type')}")
    print(f"   Total Revenue: {financial_report.get('total_revenue')}")
    
    print("\n✅ All reports generated successfully!")
    
except Exception as e:
    print(f"\n❌ Error occurred: {str(e)}")
    import traceback
    traceback.print_exc()

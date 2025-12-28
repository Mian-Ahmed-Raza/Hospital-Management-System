"""Test the fixed database stats logic"""
from app.utils.db_connector import DatabaseConnector

db = DatabaseConnector()

print("=== Testing Stats Logic ===\n")

# Patients
all_patients = db.read('patients')
active_patients = sum(1 for p in all_patients if p.get('is_active') == True)
total_patients = len(all_patients)
inactive_patients = total_patients - active_patients
print(f"Patients:")
print(f"  Active: {active_patients}")
print(f"  Inactive: {inactive_patients}")
print(f"  Total: {total_patients}")

# Appointments
all_appointments = db.read('appointments')
total_appointments = len(all_appointments)
scheduled = sum(1 for a in all_appointments if str(a.get('status', '')).lower() in ['scheduled', 'appointmentstatusenum.scheduled'])
completed = sum(1 for a in all_appointments if str(a.get('status', '')).lower() in ['completed', 'appointmentstatusenum.completed'])
cancelled = sum(1 for a in all_appointments if str(a.get('status', '')).lower() in ['cancelled', 'appointmentstatusenum.cancelled'])
confirmed = sum(1 for a in all_appointments if str(a.get('status', '')).lower() in ['confirmed', 'appointmentstatusenum.confirmed'])
print(f"\nAppointments:")
print(f"  Total: {total_appointments}")
print(f"  Scheduled: {scheduled}")
print(f"  Confirmed: {confirmed}")
print(f"  Completed: {completed}")
print(f"  Cancelled: {cancelled}")

# Bills
all_bills = db.read('billing')
total_bills = len(all_bills)
paid_bills = sum(1 for b in all_bills if str(b.get('payment_status', '')).lower() == 'paid')
pending_bills = sum(1 for b in all_bills if str(b.get('payment_status', '')).lower() == 'pending')
print(f"\nBills:")
print(f"  Total: {total_bills}")
print(f"  Paid: {paid_bills}")
print(f"  Pending: {pending_bills}")

# Users
all_users = db.read('users')
active_users = sum(1 for u in all_users if u.get('is_active') == True)
total_users = len(all_users)
admins = sum(1 for u in all_users if str(u.get('role', '')).lower() in ['admin', 'userroleenum.admin'] and u.get('is_active') == True)
doctors = sum(1 for u in all_users if str(u.get('role', '')).lower() in ['doctor', 'userroleenum.doctor'] and u.get('is_active') == True)
nurses = sum(1 for u in all_users if str(u.get('role', '')).lower() in ['nurse', 'userroleenum.nurse'] and u.get('is_active') == True)
receptionists = sum(1 for u in all_users if str(u.get('role', '')).lower() in ['receptionist', 'userroleenum.receptionist'] and u.get('is_active') == True)

print(f"\nUsers:")
print(f"  Active: {active_users}")
print(f"  Total: {total_users}")
print(f"  Admins: {admins}")
print(f"  Doctors: {doctors}")
print(f"  Nurses: {nurses}")
print(f"  Receptionists: {receptionists}")

print("\n✅ Test complete!")

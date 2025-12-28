"""Check database values for debugging"""
from app.utils.db_connector import DatabaseConnector

db = DatabaseConnector()

print("=== APPOINTMENTS ===")
appointments = db.read('appointments')
print(f"Total: {len(appointments)}")
for apt in appointments:
    print(f"  {apt.get('appointment_id')}: status={apt.get('status')}")

print("\n=== BILLS ===")
bills = db.read('billing')
print(f"Total: {len(bills)}")
for bill in bills:
    print(f"  {bill.get('bill_id')}: payment_status={bill.get('payment_status')}")

print("\n=== PATIENTS ===")
patients = db.read('patients')
print(f"Total: {len(patients)}")
for p in patients:
    print(f"  {p.get('patient_id')}: is_active={p.get('is_active')}")

print("\n=== USERS ===")
users = db.read('users')
print(f"Total: {len(users)}")
for u in users:
    print(f"  {u.get('user_id')}: is_active={u.get('is_active')}, role={u.get('role')}")

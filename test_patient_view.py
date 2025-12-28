"""Test script to verify patient records are loading correctly"""

from app.utils.db_connector import DatabaseConnector

# Initialize database
db = DatabaseConnector()

# Test reading patients
print("Testing patient data retrieval...")
print("=" * 50)

# Read all patients
all_patients = db.read('patients')
print(f"\n1. Total patients in database: {len(all_patients)}")

# Read active patients only
active_patients = db.read('patients', {'is_active': True})
print(f"2. Active patients: {len(active_patients)}")

# Display patient details
print("\n3. Patient Details:")
for patient in active_patients:
    print(f"   - ID: {patient.get('patient_id')}")
    print(f"     Name: {patient.get('first_name')} {patient.get('last_name')}")
    print(f"     Phone: {patient.get('phone')}")
    print(f"     Active: {patient.get('is_active')}")
    print()

print("=" * 50)
print("\nTest completed successfully!")

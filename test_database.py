"""
Database Integration Test Script
Tests the SQLite database integration
"""

from app.utils.db_connector import DatabaseConnector, DatabaseException
from datetime import datetime


def test_database_connection():
    """Test database connection and initialization"""
    print("Testing database connection...")
    try:
        db = DatabaseConnector()
        print("✓ Database connection successful")
        return db
    except DatabaseException as e:
        print(f"✗ Database connection failed: {str(e)}")
        return None


def test_user_operations(db):
    """Test user CRUD operations"""
    print("\nTesting User Operations...")
    
    try:
        # Test Read (default users should exist)
        users = db.read('users')
        print(f"✓ Read users: Found {len(users)} users")
        
        # Test Create
        new_user = {
            'user_id': db.get_next_id('users', 'USR'),
            'username': 'test_nurse',
            'password': 'test123',
            'role': 'nurse',
            'full_name': 'Test Nurse',
            'email': 'nurse@test.com',
            'phone': '1111111111',
            'is_active': True
        }
        db.create('users', new_user)
        print(f"✓ Created user: {new_user['user_id']}")
        
        # Test Update
        db.update('users', new_user['user_id'], 'user_id', {'phone': '2222222222'})
        updated_user = db.read('users', {'user_id': new_user['user_id']})[0]
        assert updated_user['phone'] == '2222222222'
        print(f"✓ Updated user: {new_user['user_id']}")
        
        # Test Delete
        db.delete('users', new_user['user_id'], 'user_id')
        deleted_user = db.read('users', {'user_id': new_user['user_id']})
        assert len(deleted_user) == 0
        print(f"✓ Deleted user: {new_user['user_id']}")
        
        return True
    except Exception as e:
        print(f"✗ User operations failed: {str(e)}")
        return False


def test_patient_operations(db):
    """Test patient CRUD operations"""
    print("\nTesting Patient Operations...")
    
    try:
        # Test Create
        new_patient = {
            'patient_id': db.get_next_id('patients', 'PAT'),
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'Male',
            'phone': '9999999999',
            'email': 'john.doe@test.com',
            'address': '123 Test St',
            'blood_group': 'O+',
            'registration_date': datetime.now().strftime("%Y-%m-%d"),
            'is_active': True
        }
        db.create('patients', new_patient)
        print(f"✓ Created patient: {new_patient['patient_id']}")
        
        # Test Read with filter
        patients = db.read('patients', {'patient_id': new_patient['patient_id']})
        assert len(patients) == 1
        assert patients[0]['first_name'] == 'John'
        print(f"✓ Read patient: {new_patient['patient_id']}")
        
        # Test Update
        db.update('patients', new_patient['patient_id'], 'patient_id', 
                 {'phone': '8888888888'})
        print(f"✓ Updated patient: {new_patient['patient_id']}")
        
        # Test Delete
        db.delete('patients', new_patient['patient_id'], 'patient_id')
        print(f"✓ Deleted patient: {new_patient['patient_id']}")
        
        return True
    except Exception as e:
        print(f"✗ Patient operations failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_appointment_operations(db):
    """Test appointment CRUD operations"""
    print("\nTesting Appointment Operations...")
    
    try:
        # Create a test patient first
        test_patient = {
            'patient_id': db.get_next_id('patients', 'PAT'),
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1985-05-15',
            'gender': 'Female',
            'phone': '7777777777',
            'registration_date': datetime.now().strftime("%Y-%m-%d"),
            'is_active': True
        }
        db.create('patients', test_patient)
        
        # Get default doctor
        doctors = db.read('users', {'role': 'doctor'})
        if not doctors:
            print("⚠ No doctors found, skipping appointment test")
            return True
        
        doctor = doctors[0]
        
        # Test Create Appointment
        new_appointment = {
            'appointment_id': db.get_next_id('appointments', 'APT'),
            'patient_id': test_patient['patient_id'],
            'patient_name': f"{test_patient['first_name']} {test_patient['last_name']}",
            'doctor_id': doctor['user_id'],
            'doctor_name': doctor['full_name'],
            'appointment_date': '2025-12-30',
            'appointment_time': '10:00',
            'department': 'General Medicine',
            'reason': 'Regular checkup',
            'status': 'scheduled',
            'notes': 'Test appointment'
        }
        db.create('appointments', new_appointment)
        print(f"✓ Created appointment: {new_appointment['appointment_id']}")
        
        # Test Read
        appointments = db.read('appointments', 
                              {'appointment_id': new_appointment['appointment_id']})
        assert len(appointments) == 1
        print(f"✓ Read appointment: {new_appointment['appointment_id']}")
        
        # Test Update
        db.update('appointments', new_appointment['appointment_id'], 
                 'appointment_id', {'status': 'confirmed'})
        print(f"✓ Updated appointment: {new_appointment['appointment_id']}")
        
        # Cleanup
        db.delete('appointments', new_appointment['appointment_id'], 'appointment_id')
        db.delete('patients', test_patient['patient_id'], 'patient_id')
        print(f"✓ Deleted appointment and test patient")
        
        return True
    except Exception as e:
        print(f"✗ Appointment operations failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_id_generation(db):
    """Test ID generation"""
    print("\nTesting ID Generation...")
    
    try:
        user_id = db.get_next_id('users', 'USR')
        patient_id = db.get_next_id('patients', 'PAT')
        appointment_id = db.get_next_id('appointments', 'APT')
        
        print(f"✓ Generated User ID: {user_id}")
        print(f"✓ Generated Patient ID: {patient_id}")
        print(f"✓ Generated Appointment ID: {appointment_id}")
        
        # Verify format
        assert user_id.startswith('USR')
        assert patient_id.startswith('PAT')
        assert appointment_id.startswith('APT')
        
        print("✓ ID generation working correctly")
        return True
    except Exception as e:
        print(f"✗ ID generation failed: {str(e)}")
        return False


def run_all_tests():
    """Run all database integration tests"""
    print("=" * 60)
    print("Database Integration Test Suite")
    print("=" * 60)
    
    # Test connection
    db = test_database_connection()
    if not db:
        print("\n✗ Cannot proceed without database connection")
        return
    
    # Run tests
    results = {
        'ID Generation': test_id_generation(db),
        'User Operations': test_user_operations(db),
        'Patient Operations': test_patient_operations(db),
        'Appointment Operations': test_appointment_operations(db)
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Database integration is working correctly.")
    else:
        print(f"\n⚠ {total_tests - passed_tests} test(s) failed. Please check the errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTests cancelled by user.")
    except Exception as e:
        print(f"\n\n✗ Test suite failed: {str(e)}")
        import traceback
        traceback.print_exc()

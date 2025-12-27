# Database Integration Guide

## Overview

The Hospital Management System has been upgraded from JSON file-based storage to a robust SQLite database using SQLAlchemy ORM. This provides better data integrity, concurrent access support, and improved performance.

## What Changed

### Before (JSON Files)
- Data stored in `data/*.json` files
- Manual file reading/writing
- Limited querying capabilities
- No transaction support

### After (SQLite Database)
- Data stored in `data/hospital.db` SQLite database
- SQLAlchemy ORM for database operations
- Full SQL querying capabilities
- ACID transaction support
- Better data integrity with foreign key constraints

## Database Schema

The system now uses four main tables:

### 1. Users Table
Stores hospital staff (admins, doctors, nurses, receptionists)
- `user_id` (Primary Key): e.g., "USR001"
- `username`: Unique login username
- `password`: User password (Note: Consider hashing in production)
- `role`: admin, doctor, nurse, or receptionist
- `full_name`: User's full name
- `email`: Email address
- `phone`: Contact number
- `specialization`: For doctors (e.g., "Cardiology")
- `is_active`: Account status
- `created_at`: Timestamp

### 2. Patients Table
Stores patient information
- `patient_id` (Primary Key): e.g., "PAT001"
- `first_name`, `last_name`: Patient name
- `date_of_birth`: Format: YYYY-MM-DD
- `gender`: Male, Female, or Other
- `phone`: Contact number
- `email`: Email address (optional)
- `address`: Home address (optional)
- `blood_group`: e.g., "O+", "A-"
- `emergency_contact`: Emergency contact number
- `registration_date`: Date registered
- `is_active`: Account status
- `created_at`: Timestamp

### 3. Appointments Table
Stores appointment records
- `appointment_id` (Primary Key): e.g., "APT001"
- `patient_id`: Reference to patient
- `patient_name`: Patient's full name
- `doctor_id`: Reference to doctor
- `doctor_name`: Doctor's full name
- `appointment_date`: Format: YYYY-MM-DD
- `appointment_time`: Format: HH:MM
- `department`: e.g., "Cardiology"
- `reason`: Reason for visit
- `status`: scheduled, confirmed, completed, or cancelled
- `notes`: Additional notes (optional)
- `created_at`: Timestamp

### 4. Billing Table
Stores billing and invoice information
- `bill_id` (Primary Key): e.g., "INV001"
- `patient_id`: Reference to patient
- `patient_name`: Patient's full name
- `appointment_id`: Related appointment (optional)
- `bill_date`: Invoice date
- `services`: JSON string of services
- `total_amount`: Total bill amount
- `payment_status`: pending, paid, etc.
- `payment_method`: cash, card, insurance, etc.
- `created_at`: Timestamp

## Installation & Setup

### 1. Install Dependencies

First, install the required packages:

```bash
pip install -r requirements.txt
```

This will install:
- `sqlalchemy>=2.0.0` - ORM for database operations
- `alembic>=1.13.0` - Database migration tool (for future schema changes)

### 2. Migrate Existing Data (Optional)

If you have existing JSON data files, run the migration script:

```bash
python migrate_to_database.py
```

This script will:
- Create a new SQLite database at `data/hospital.db`
- Migrate all data from JSON files to the database
- Preserve your original JSON files as backup
- Skip duplicate records

### 3. Test the Integration

Verify everything works correctly:

```bash
python test_database.py
```

This will test:
- Database connection
- ID generation
- User CRUD operations
- Patient CRUD operations
- Appointment CRUD operations

## Usage in Code

The API remains largely the same, so your existing code should work with minimal changes:

### Creating Records

```python
from app.utils.db_connector import DatabaseConnector

db = DatabaseConnector()

# Create a new patient
patient_data = {
    'patient_id': db.get_next_id('patients', 'PAT'),
    'first_name': 'John',
    'last_name': 'Doe',
    'date_of_birth': '1990-01-01',
    'gender': 'Male',
    'phone': '1234567890',
    'registration_date': '2025-12-27',
    'is_active': True
}
db.create('patients', patient_data)
```

### Reading Records

```python
# Get all patients
all_patients = db.read('patients')

# Get patients with filters
male_patients = db.read('patients', {'gender': 'Male'})
specific_patient = db.read('patients', {'patient_id': 'PAT001'})
```

### Updating Records

```python
# Update patient phone number
db.update('patients', 'PAT001', 'patient_id', {
    'phone': '9876543210',
    'email': 'newemail@example.com'
})
```

### Deleting Records

```python
# Delete a patient
db.delete('patients', 'PAT001', 'patient_id')
```

### Generating IDs

```python
# Generate next available ID
next_patient_id = db.get_next_id('patients', 'PAT')  # Returns "PAT001", "PAT002", etc.
next_appointment_id = db.get_next_id('appointments', 'APT')
```

## Database Location

By default, the database is stored at:
```
data/hospital.db
```

You can change this by modifying the `DatabaseConnector` initialization:

```python
# Use custom database location
db = DatabaseConnector(data_dir="custom_data_folder")

# Or use a different database URL
db = DatabaseConnector(database_url="sqlite:///path/to/custom.db")
```

## Advanced Features

### Using Sessions Directly

For complex operations, you can use SQLAlchemy sessions:

```python
from app.utils.db_connector import DatabaseConnector, UserModel

db = DatabaseConnector()
session = db.get_session()

try:
    # Query using SQLAlchemy ORM
    doctors = session.query(UserModel).filter(
        UserModel.role == 'doctor',
        UserModel.is_active == True
    ).all()
    
    # Your operations here
    session.commit()
except Exception as e:
    session.rollback()
    raise
finally:
    session.close()
```

### Database Models

The database models are defined in `app/utils/db_connector.py`:
- `UserModel`
- `PatientModel`
- `AppointmentModel`
- `BillingModel`

These can be used directly for complex queries.

## Backup and Maintenance

### Backup Database

Simply copy the database file:

```bash
# Windows
copy data\hospital.db data\hospital_backup.db

# Linux/Mac
cp data/hospital.db data/hospital_backup.db
```

### Export to JSON (for portability)

```python
import json
from app.utils.db_connector import DatabaseConnector

db = DatabaseConnector()

# Export patients to JSON
patients = db.read('patients')
with open('patients_export.json', 'w') as f:
    json.dump(patients, f, indent=4)
```

### Database Statistics

```python
from app.utils.db_connector import DatabaseConnector

db = DatabaseConnector()

print(f"Total Users: {len(db.read('users'))}")
print(f"Total Patients: {len(db.read('patients'))}")
print(f"Total Appointments: {len(db.read('appointments'))}")
print(f"Active Patients: {len(db.read('patients', {'is_active': True}))}")
```

## Troubleshooting

### Database Locked Error

If you see "database is locked" errors:
- Make sure you're closing sessions properly
- Avoid long-running transactions
- Use `session.close()` in finally blocks

### Migration Issues

If migration fails:
1. Check that JSON files are valid (proper JSON format)
2. Ensure no duplicate IDs in JSON files
3. Check the error message for specific issues
4. Your original JSON files are preserved, so you can retry

### Performance Optimization

For better performance with large datasets:
- Use filters in queries instead of reading all records
- Use sessions for batch operations
- Add indexes if needed (requires schema modification)

## Default Users

The system creates two default users:

1. **Administrator**
   - Username: `admin`
   - Password: `admin123`
   - Role: Admin

2. **Doctor**
   - Username: `doctor`
   - Password: `doctor123`
   - Role: Doctor
   - Specialization: General Medicine

**⚠️ IMPORTANT**: Change these default passwords in production!

## Security Considerations

1. **Password Storage**: Currently passwords are stored in plain text. Consider implementing password hashing using `bcrypt` or similar.

2. **Database Security**: 
   - Restrict file permissions on `hospital.db`
   - Use encrypted connections for remote databases
   - Implement proper authentication

3. **SQL Injection**: Using SQLAlchemy ORM protects against SQL injection, but always validate user input.

## Future Enhancements

Potential improvements for production use:

1. **Password Hashing**: Implement bcrypt/argon2 for password security
2. **Alembic Migrations**: Use Alembic for schema version control
3. **Connection Pooling**: Configure for concurrent access
4. **PostgreSQL/MySQL**: Upgrade to production database
5. **Audit Logging**: Track all database changes
6. **Soft Deletes**: Keep deleted records for history

## Support

For issues or questions:
1. Check the test script output: `python test_database.py`
2. Review error messages in console
3. Check database file exists at `data/hospital.db`
4. Verify all dependencies are installed

## Conclusion

The SQLite database integration provides a solid foundation for the Hospital Management System. The system is now more robust, scalable, and maintainable while maintaining backward compatibility with existing code.

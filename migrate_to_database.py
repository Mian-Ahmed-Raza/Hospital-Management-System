"""
Database Migration Script
Migrates data from JSON files to SQLite database
"""

import json
import os
from pathlib import Path
from app.utils.db_connector import DatabaseConnector, DatabaseException


def load_json_file(filepath: Path):
    """Load data from JSON file"""
    try:
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid JSON in {filepath}: {str(e)}")
        return []
    except Exception as e:
        print(f"Warning: Failed to read {filepath}: {str(e)}")
        return []


def migrate_data():
    """Migrate data from JSON files to SQLite database"""
    print("=" * 60)
    print("Hospital Management System - Database Migration")
    print("=" * 60)
    print("\nThis script will migrate your data from JSON files to SQLite database.")
    
    # Check if JSON data directory exists
    json_data_dir = Path("data")
    if not json_data_dir.exists():
        print("\n✓ No existing JSON data directory found.")
        print("  A new database will be created with default data.")
        db = DatabaseConnector()
        print("\n✓ Database initialized successfully!")
        print(f"  Database location: {db.data_dir / 'hospital.db'}")
        return
    
    # Initialize database
    print("\n[1/5] Initializing new SQLite database...")
    try:
        db = DatabaseConnector()
        print("✓ Database initialized")
    except DatabaseException as e:
        print(f"✗ Failed to initialize database: {str(e)}")
        return
    
    # Migrate tables
    tables = {
        'users': 'users.json',
        'patients': 'patients.json',
        'appointments': 'appointments.json',
        'billing': 'billing.json'
    }
    
    total_migrated = 0
    
    for table, filename in tables.items():
        filepath = json_data_dir / filename
        print(f"\n[{list(tables.keys()).index(table) + 2}/5] Migrating {table}...")
        
        # Load JSON data
        json_data = load_json_file(filepath)
        
        if not json_data:
            print(f"  ℹ No data found in {filename}")
            continue
        
        # Skip default users if they already exist in database
        if table == 'users':
            existing_users = db.read('users')
            if existing_users:
                print(f"  ℹ Skipping users table (default users already exist)")
                continue
        
        # Migrate each record
        migrated_count = 0
        failed_count = 0
        
        for record in json_data:
            try:
                # Check if record already exists (to avoid duplicates)
                id_field_map = {
                    'users': 'user_id',
                    'patients': 'patient_id',
                    'appointments': 'appointment_id',
                    'billing': 'bill_id'
                }
                id_field = id_field_map[table]
                record_id = record.get(id_field)
                
                if record_id:
                    existing = db.read(table, {id_field: record_id})
                    if existing:
                        print(f"  ⚠ Skipping duplicate record: {record_id}")
                        continue
                
                # Create record in database
                db.create(table, record)
                migrated_count += 1
            except Exception as e:
                failed_count += 1
                print(f"  ⚠ Failed to migrate record: {str(e)}")
        
        print(f"  ✓ Migrated {migrated_count} records")
        if failed_count > 0:
            print(f"  ⚠ Failed to migrate {failed_count} records")
        
        total_migrated += migrated_count
    
    print("\n" + "=" * 60)
    print(f"Migration Complete!")
    print(f"Total records migrated: {total_migrated}")
    print(f"Database location: {db.data_dir / 'hospital.db'}")
    print("=" * 60)
    
    # Backup recommendation
    print("\n📝 Recommendation:")
    print("  - Your original JSON files are still in the 'data' folder")
    print("  - Consider backing them up before removing")
    print("  - The application will now use the SQLite database")
    print()


if __name__ == "__main__":
    try:
        migrate_data()
    except KeyboardInterrupt:
        print("\n\nMigration cancelled by user.")
    except Exception as e:
        print(f"\n\n✗ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()

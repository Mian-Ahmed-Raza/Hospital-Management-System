# Hospital Management System - Database Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Hospital Management System                       │
│                          (Tkinter GUI)                               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Services Layer                               │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ AuthService  │  │PatientManager│  │BillingEngine │              │
│  │              │  │              │  │              │              │
│  │ - login()    │  │ - register() │  │ - invoice()  │              │
│  │ - logout()   │  │ - update()   │  │ - payment()  │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                       │
│         └─────────────────┼─────────────────┘                       │
│                           │                                         │
└───────────────────────────┼─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Database Connector Layer                          │
│                  (app/utils/db_connector.py)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │            DatabaseConnector Class                          │    │
│  ├────────────────────────────────────────────────────────────┤    │
│  │  Methods:                                                   │    │
│  │  • create(table, record)      - Insert new record          │    │
│  │  • read(table, filters)       - Query records              │    │
│  │  • update(table, id, updates) - Update existing            │    │
│  │  • delete(table, id)          - Remove record              │    │
│  │  • get_next_id(table, prefix) - Generate ID                │    │
│  │  • get_session()              - Get DB session             │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
└───────────────────────────┬──────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SQLAlchemy ORM Layer                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  UserModel   │  │PatientModel  │  │Appointment   │              │
│  │              │  │              │  │    Model     │              │
│  │ - user_id    │  │ - patient_id │  │ - appt_id    │              │
│  │ - username   │  │ - first_name │  │ - patient_id │              │
│  │ - password   │  │ - last_name  │  │ - doctor_id  │              │
│  │ - role       │  │ - dob        │  │ - date       │              │
│  │ - email      │  │ - gender     │  │ - status     │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                      │
│  ┌──────────────┐                                                   │
│  │BillingModel  │                                                   │
│  │              │                                                   │
│  │ - bill_id    │                                                   │
│  │ - patient_id │                                                   │
│  │ - services   │                                                   │
│  │ - total      │                                                   │
│  └──────────────┘                                                   │
│                                                                      │
└───────────────────────────┬──────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       SQLite Database                                │
│                      (data/hospital.db)                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ╔═══════════════════════════════════════════════════════════╗     │
│  ║                   TABLES                                  ║     │
│  ╠═══════════════════════════════════════════════════════════╣     │
│  ║                                                           ║     │
│  ║  ┌──────────────────────────────────────────────────┐    ║     │
│  ║  │ users                                            │    ║     │
│  ║  │ ──────────────────────────────────────────────── │    ║     │
│  ║  │ • id (PK)          • email                       │    ║     │
│  ║  │ • user_id (Unique) • phone                       │    ║     │
│  ║  │ • username         • specialization              │    ║     │
│  ║  │ • password         • is_active                   │    ║     │
│  ║  │ • role (Enum)      • created_at                  │    ║     │
│  ║  │ • full_name                                      │    ║     │
│  ║  └──────────────────────────────────────────────────┘    ║     │
│  ║                                                           ║     │
│  ║  ┌──────────────────────────────────────────────────┐    ║     │
│  ║  │ patients                                         │    ║     │
│  ║  │ ──────────────────────────────────────────────── │    ║     │
│  ║  │ • id (PK)          • address                     │    ║     │
│  ║  │ • patient_id       • blood_group                 │    ║     │
│  ║  │ • first_name       • emergency_contact           │    ║     │
│  ║  │ • last_name        • registration_date           │    ║     │
│  ║  │ • date_of_birth    • is_active                   │    ║     │
│  ║  │ • gender           • created_at                  │    ║     │
│  ║  │ • phone                                          │    ║     │
│  ║  │ • email                                          │    ║     │
│  ║  └──────────────────────────────────────────────────┘    ║     │
│  ║                                                           ║     │
│  ║  ┌──────────────────────────────────────────────────┐    ║     │
│  ║  │ appointments                                     │    ║     │
│  ║  │ ──────────────────────────────────────────────── │    ║     │
│  ║  │ • id (PK)          • department                  │    ║     │
│  ║  │ • appointment_id   • reason                      │    ║     │
│  ║  │ • patient_id       • status (Enum)               │    ║     │
│  ║  │ • patient_name     • notes                       │    ║     │
│  ║  │ • doctor_id        • created_at                  │    ║     │
│  ║  │ • doctor_name                                    │    ║     │
│  ║  │ • appointment_date                               │    ║     │
│  ║  │ • appointment_time                               │    ║     │
│  ║  └──────────────────────────────────────────────────┘    ║     │
│  ║                                                           ║     │
│  ║  ┌──────────────────────────────────────────────────┐    ║     │
│  ║  │ billing                                          │    ║     │
│  ║  │ ──────────────────────────────────────────────── │    ║     │
│  ║  │ • id (PK)          • total_amount                │    ║     │
│  ║  │ • bill_id          • payment_status              │    ║     │
│  ║  │ • patient_id       • payment_method              │    ║     │
│  ║  │ • patient_name     • created_at                  │    ║     │
│  ║  │ • appointment_id                                 │    ║     │
│  ║  │ • bill_date                                      │    ║     │
│  ║  │ • services (JSON)                                │    ║     │
│  ║  └──────────────────────────────────────────────────┘    ║     │
│  ║                                                           ║     │
│  ╚═══════════════════════════════════════════════════════════╝     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────────┐
│   User GUI   │
│  (Tkinter)   │
└──────┬───────┘
       │
       │ 1. User Action
       │    (Register Patient, 
       │     Book Appointment)
       ▼
┌──────────────────────────┐
│    Service Layer         │
│  (PatientManager, etc.)  │
└──────┬───────────────────┘
       │
       │ 2. Business Logic
       │    Validation
       ▼
┌─────────────────────────┐
│  Database Connector     │
│  (db.create/read/...)   │
└──────┬──────────────────┘
       │
       │ 3. ORM Operations
       │    (SQLAlchemy)
       ▼
┌─────────────────────────┐
│   SQLite Database       │
│   (hospital.db)         │
└──────┬──────────────────┘
       │
       │ 4. Results
       │    
       ▼
┌─────────────────────────┐
│   Back to GUI           │
│   (Display Data)        │
└─────────────────────────┘
```

## Migration Flow

```
┌──────────────────┐
│  JSON Files      │
│  (Old System)    │
│                  │
│ • users.json     │
│ • patients.json  │
│ • appointments   │
│ • billing.json   │
└────────┬─────────┘
         │
         │ migrate_to_database.py
         │
         ▼
┌────────────────────────────┐
│   SQLite Database          │
│   (New System)             │
│                            │
│ • users table              │
│ • patients table           │
│ • appointments table       │
│ • billing table            │
└────────────────────────────┘
         │
         │ All data preserved
         │ + Better performance
         ▼
┌────────────────────────────┐
│   Application continues    │
│   with same API            │
│   (Zero code changes)      │
└────────────────────────────┘
```

## Database Features

### ACID Properties

```
┌────────────────────────────────────────────────────┐
│ A - Atomicity   │ All or nothing transactions     │
│ C - Consistency │ Data integrity maintained       │
│ I - Isolation   │ Concurrent access safe          │
│ D - Durability  │ Data persists after commit      │
└────────────────────────────────────────────────────┘
```

### Indexing Strategy

```
users table:
  PRIMARY: id
  UNIQUE:  user_id, username
  INDEX:   role, is_active

patients table:
  PRIMARY: id
  UNIQUE:  patient_id
  INDEX:   is_active, registration_date

appointments table:
  PRIMARY: id
  UNIQUE:  appointment_id
  INDEX:   patient_id, doctor_id, status, appointment_date

billing table:
  PRIMARY: id
  UNIQUE:  bill_id
  INDEX:   patient_id, payment_status
```

## Backup Strategy

```
┌──────────────────┐
│  Live Database   │
│  hospital.db     │
└────────┬─────────┘
         │
         ├─────────► Daily Backup
         │           hospital_backup_YYYYMMDD.db
         │
         ├─────────► Before Updates
         │           hospital_pre_update.db
         │
         └─────────► JSON Export (optional)
                     data_export_YYYYMMDD.json
```

## Performance Characteristics

```
┌──────────────────────────┬──────────────┬──────────────┐
│ Operation                │ JSON Files   │ SQLite DB    │
├──────────────────────────┼──────────────┼──────────────┤
│ Create Record            │ O(n)         │ O(1)         │
│ Read All Records         │ O(n)         │ O(n)         │
│ Read Filtered            │ O(n)         │ O(log n)     │
│ Update Record            │ O(n)         │ O(log n)     │
│ Delete Record            │ O(n)         │ O(log n)     │
│ Count Records            │ O(n)         │ O(1)         │
│ Concurrent Users         │ ❌ Unsafe    │ ✅ Safe      │
└──────────────────────────┴──────────────┴──────────────┘

n = number of records
```

## Security Model

```
┌─────────────────────────────────────────────────────┐
│             Application Layer                       │
│  • Input validation                                 │
│  • Role-based access control                        │
│  • Session management                               │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│             ORM Layer (SQLAlchemy)                  │
│  • SQL injection prevention                         │
│  • Parameterized queries                            │
│  • Type validation                                  │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│             Database Layer                          │
│  • File permissions (chmod 600)                     │
│  • Transaction isolation                            │
│  • Constraint enforcement                           │
└─────────────────────────────────────────────────────┘
```

## Scalability Path

```
Current:                    Future Options:
┌──────────────┐           ┌──────────────────┐
│   SQLite     │   ───►    │   PostgreSQL     │
│  (hospital.  │           │   (Production)   │
│   db)        │           │                  │
│              │           │  • Multi-user    │
│ • Single     │           │  • Replication   │
│   file       │           │  • Advanced      │
│ • No server  │           │    features      │
│ • Fast       │           │  • Network       │
│              │           │    access        │
└──────────────┘           └──────────────────┘
        │                          │
        │                          │
        └──────────┬───────────────┘
                   │
                   ▼
          Same SQLAlchemy Code!
          (Just change connection string)
```

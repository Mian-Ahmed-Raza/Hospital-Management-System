"""
Database Connector - Database handling using SQLAlchemy
Handles data persistence using SQLite database
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any, Optional, Type
from pathlib import Path
from datetime import datetime
import enum

# Create base class for declarative models
Base = declarative_base()


class DatabaseException(Exception):
    """Custom exception for database operations"""
    pass


# Database Models
class UserRoleEnum(enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    RECEPTIONIST = "receptionist"


class AppointmentStatusEnum(enum.Enum):
    """Appointment status enumeration"""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class UserModel(Base):
    """User database model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRoleEnum), nullable=False)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(20))
    specialization = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)


class PatientModel(Base):
    """Patient database model"""
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(String(20), nullable=False)
    gender = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(200))
    address = Column(Text)
    blood_group = Column(String(10))
    emergency_contact = Column(String(20))
    registration_date = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)


class AppointmentModel(Base):
    """Appointment database model"""
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(String(50), unique=True, nullable=False)
    patient_id = Column(String(50), nullable=False)
    patient_name = Column(String(200), nullable=False)
    doctor_id = Column(String(50), nullable=False)
    doctor_name = Column(String(200), nullable=False)
    appointment_date = Column(String(20), nullable=False)
    appointment_time = Column(String(20), nullable=False)
    department = Column(String(100), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(Enum(AppointmentStatusEnum), default=AppointmentStatusEnum.SCHEDULED)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)


class BillingModel(Base):
    """Billing database model"""
    __tablename__ = 'billing'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    bill_id = Column(String(50), unique=True, nullable=False)
    patient_id = Column(String(50), nullable=False)
    patient_name = Column(String(200), nullable=False)
    appointment_id = Column(String(50))
    bill_date = Column(String(20), nullable=False)
    services = Column(Text, nullable=False)  # JSON string
    total_amount = Column(String(20), nullable=False)
    payment_status = Column(String(50), default='pending')
    payment_method = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)


class DatabaseConnector:
    """Handles database operations using SQLAlchemy and SQLite"""
    
    def __init__(self, database_url: str = None, data_dir: str = "data"):
        """
        Initialize database connector
        
        Args:
            database_url: SQLAlchemy database URL (default: SQLite in data directory)
            data_dir: Directory to store SQLite database file
        """
        if database_url is None:
            self.data_dir = Path(data_dir)
            self._ensure_data_directory()
            db_path = self.data_dir / "hospital.db"
            database_url = f"sqlite:///{db_path}"
        
        try:
            self.engine = create_engine(database_url, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine)
            self._initialize_database()
        except Exception as e:
            raise DatabaseException(f"Failed to initialize database: {str(e)}")
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise DatabaseException(f"Failed to create data directory: {str(e)}")
    
    def _initialize_database(self):
        """Create all tables and add default data"""
        try:
            # Create all tables
            Base.metadata.create_all(self.engine)
            
            # Add default users if table is empty
            session = self.get_session()
            try:
                user_count = session.query(UserModel).count()
                if user_count == 0:
                    self._create_default_users(session)
                session.commit()
            except Exception as e:
                session.rollback()
                raise
            finally:
                session.close()
                
        except Exception as e:
            raise DatabaseException(f"Failed to initialize database: {str(e)}")
    
    def _create_default_users(self, session: Session):
        """Create default admin and doctor users"""
        default_admin = UserModel(
            user_id='USR001',
            username='admin',
            password='admin123',
            role=UserRoleEnum.ADMIN,
            full_name='System Administrator',
            email='admin@hospital.com',
            phone='1234567890',
            specialization=None,
            is_active=True
        )
        
        default_doctor = UserModel(
            user_id='USR002',
            username='doctor',
            password='doctor123',
            role=UserRoleEnum.DOCTOR,
            full_name='Dr. John Smith',
            email='doctor@hospital.com',
            phone='9876543210',
            specialization='General Medicine',
            is_active=True
        )
        
        session.add(default_admin)
        session.add(default_doctor)
    
    def get_session(self) -> Session:
        """
        Get a new database session
        
        Returns:
            SQLAlchemy session object
        """
        return self.SessionLocal()
    
    def _get_model(self, table: str) -> Type[Base]:
        """Get the SQLAlchemy model class for a table name"""
        models = {
            'users': UserModel,
            'patients': PatientModel,
            'appointments': AppointmentModel,
            'billing': BillingModel
        }
        if table not in models:
            raise DatabaseException(f"Unknown table: {table}")
        return models[table]
    
    def _model_to_dict(self, model_instance) -> Dict[str, Any]:
        """Convert SQLAlchemy model instance to dictionary"""
        result = {}
        for column in model_instance.__table__.columns:
            value = getattr(model_instance, column.name)
            # Convert enum to string
            if isinstance(value, enum.Enum):
                value = value.value
            # Convert datetime to string
            elif isinstance(value, datetime):
                value = value.isoformat()
            # Skip internal id field
            if column.name != 'id':
                result[column.name] = value
        return result
    
    def create(self, table: str, record: Dict[str, Any]) -> bool:
        """
        Create a new record
        
        Args:
            table: Table name (e.g., 'users', 'patients')
            record: Record data as dictionary
            
        Returns:
            True if successful
            
        Raises:
            DatabaseException: If creation fails
        """
        session = self.get_session()
        try:
            Model = self._get_model(table)
            
            # Handle enum conversions
            record_copy = record.copy()
            if table == 'users' and 'role' in record_copy:
                if isinstance(record_copy['role'], str):
                    record_copy['role'] = UserRoleEnum(record_copy['role'])
            if table == 'appointments' and 'status' in record_copy:
                if isinstance(record_copy['status'], str):
                    record_copy['status'] = AppointmentStatusEnum(record_copy['status'])
            
            new_record = Model(**record_copy)
            session.add(new_record)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseException(f"Failed to create record: {str(e)}")
        finally:
            session.close()
    
    def read(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Read records with optional filtering
        
        Args:
            table: Table name
            filters: Dictionary of field:value pairs to filter by
            
        Returns:
            List of matching records as dictionaries
            
        Raises:
            DatabaseException: If read fails
        """
        session = self.get_session()
        try:
            Model = self._get_model(table)
            query = session.query(Model)
            
            # Apply filters
            if filters:
                for key, value in filters.items():
                    if hasattr(Model, key):
                        # Handle enum filters
                        if table == 'users' and key == 'role' and isinstance(value, str):
                            value = UserRoleEnum(value)
                        elif table == 'appointments' and key == 'status' and isinstance(value, str):
                            value = AppointmentStatusEnum(value)
                        query = query.filter(getattr(Model, key) == value)
            
            results = query.all()
            return [self._model_to_dict(result) for result in results]
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to read records: {str(e)}")
        finally:
            session.close()
    
    def update(self, table: str, record_id: str, id_field: str, updates: Dict[str, Any]) -> bool:
        """
        Update a record
        
        Args:
            table: Table name
            record_id: ID of record to update
            id_field: Name of ID field (e.g., 'user_id', 'patient_id')
            updates: Dictionary of fields to update
            
        Returns:
            True if successful
            
        Raises:
            DatabaseException: If update fails
        """
        session = self.get_session()
        try:
            Model = self._get_model(table)
            
            # Handle enum conversions in updates
            updates_copy = updates.copy()
            if table == 'users' and 'role' in updates_copy:
                if isinstance(updates_copy['role'], str):
                    updates_copy['role'] = UserRoleEnum(updates_copy['role'])
            if table == 'appointments' and 'status' in updates_copy:
                if isinstance(updates_copy['status'], str):
                    updates_copy['status'] = AppointmentStatusEnum(updates_copy['status'])
            
            # Find and update the record
            record = session.query(Model).filter(
                getattr(Model, id_field) == record_id
            ).first()
            
            if record:
                for key, value in updates_copy.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseException(f"Failed to update record: {str(e)}")
        finally:
            session.close()
    
    def delete(self, table: str, record_id: str, id_field: str) -> bool:
        """
        Delete a record
        
        Args:
            table: Table name
            record_id: ID of record to delete
            id_field: Name of ID field
            
        Returns:
            True if successful
            
        Raises:
            DatabaseException: If deletion fails
        """
        session = self.get_session()
        try:
            Model = self._get_model(table)
            
            # Find and delete the record
            record = session.query(Model).filter(
                getattr(Model, id_field) == record_id
            ).first()
            
            if record:
                session.delete(record)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseException(f"Failed to delete record: {str(e)}")
        finally:
            session.close()
    
    def get_next_id(self, table: str, id_prefix: str) -> str:
        """
        Generate next available ID for a table
        
        Args:
            table: Table name
            id_prefix: Prefix for ID (e.g., 'PAT', 'APT', 'USR')
            
        Returns:
            Next available ID
            
        Raises:
            DatabaseException: If operation fails
        """
        session = self.get_session()
        try:
            Model = self._get_model(table)
            
            # Map table to ID field name
            id_field_map = {
                'users': 'user_id',
                'patients': 'patient_id',
                'appointments': 'appointment_id',
                'billing': 'bill_id'
            }
            
            id_field = id_field_map.get(table)
            if not id_field:
                return f"{id_prefix}001"
            
            # Get all records and find max ID number
            records = session.query(Model).all()
            
            if not records:
                return f"{id_prefix}001"
            
            max_num = 0
            for record in records:
                record_id = getattr(record, id_field)
                if record_id and record_id.startswith(id_prefix):
                    try:
                        num = int(record_id.replace(id_prefix, ''))
                        max_num = max(max_num, num)
                    except ValueError:
                        continue
            
            return f"{id_prefix}{str(max_num + 1).zfill(3)}"
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to generate ID: {str(e)}")
        finally:
            session.close()
    
    def close(self):
        """Close database connection"""
        if hasattr(self, 'engine'):
            self.engine.dispose()


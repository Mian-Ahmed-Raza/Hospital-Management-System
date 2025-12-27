"""
Database/File Connector - Database/File handling
Handles data persistence using JSON files
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path


class DatabaseException(Exception):
    """Custom exception for database operations"""
    pass


class DatabaseConnector:
    """Handles file-based data storage using JSON"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize database connector
        
        Args:
            data_dir: Directory to store data files
        """
        self.data_dir = Path(data_dir)
        self._ensure_data_directory()
        self._initialize_data_files()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise DatabaseException(f"Failed to create data directory: {str(e)}")
    
    def _initialize_data_files(self):
        """Initialize data files with default structure"""
        files = {
            'users.json': [],
            'patients.json': [],
            'appointments.json': [],
            'billing.json': []
        }
        
        for filename, default_data in files.items():
            filepath = self.data_dir / filename
            if not filepath.exists():
                self._write_json(filepath, default_data)
        
        # Create default admin user if users file is empty
        users_file = self.data_dir / 'users.json'
        users = self._read_json(users_file)
        if not users:
            default_admin = {
                'user_id': 'USR001',
                'username': 'admin',
                'password': 'admin123',
                'role': 'admin',
                'full_name': 'System Administrator',
                'email': 'admin@hospital.com',
                'phone': '1234567890',
                'specialization': None,
                'is_active': True
            }
            default_doctor = {
                'user_id': 'USR002',
                'username': 'doctor',
                'password': 'doctor123',
                'role': 'doctor',
                'full_name': 'Dr. John Smith',
                'email': 'doctor@hospital.com',
                'phone': '9876543210',
                'specialization': 'General Medicine',
                'is_active': True
            }
            self._write_json(users_file, [default_admin, default_doctor])
    
    def _read_json(self, filepath: Path) -> List[Dict[str, Any]]:
        """
        Read data from JSON file
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            List of records
        """
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except json.JSONDecodeError as e:
            raise DatabaseException(f"Invalid JSON in {filepath}: {str(e)}")
        except Exception as e:
            raise DatabaseException(f"Failed to read {filepath}: {str(e)}")
    
    def _write_json(self, filepath: Path, data: List[Dict[str, Any]]):
        """
        Write data to JSON file
        
        Args:
            filepath: Path to JSON file
            data: List of records to write
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise DatabaseException(f"Failed to write to {filepath}: {str(e)}")
    
    def create(self, table: str, record: Dict[str, Any]) -> bool:
        """
        Create a new record
        
        Args:
            table: Table name (e.g., 'users', 'patients')
            record: Record data
            
        Returns:
            True if successful
        """
        filepath = self.data_dir / f"{table}.json"
        data = self._read_json(filepath)
        data.append(record)
        self._write_json(filepath, data)
        return True
    
    def read(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Read records with optional filtering
        
        Args:
            table: Table name
            filters: Dictionary of field:value pairs to filter by
            
        Returns:
            List of matching records
        """
        filepath = self.data_dir / f"{table}.json"
        data = self._read_json(filepath)
        
        if not filters:
            return data
        
        # Apply filters
        filtered_data = []
        for record in data:
            match = True
            for key, value in filters.items():
                if key not in record or record[key] != value:
                    match = False
                    break
            if match:
                filtered_data.append(record)
        
        return filtered_data
    
    def update(self, table: str, record_id: str, id_field: str, updates: Dict[str, Any]) -> bool:
        """
        Update a record
        
        Args:
            table: Table name
            record_id: ID of record to update
            id_field: Name of ID field
            updates: Dictionary of fields to update
            
        Returns:
            True if successful
        """
        filepath = self.data_dir / f"{table}.json"
        data = self._read_json(filepath)
        
        updated = False
        for record in data:
            if record.get(id_field) == record_id:
                record.update(updates)
                updated = True
                break
        
        if updated:
            self._write_json(filepath, data)
        
        return updated
    
    def delete(self, table: str, record_id: str, id_field: str) -> bool:
        """
        Delete a record
        
        Args:
            table: Table name
            record_id: ID of record to delete
            id_field: Name of ID field
            
        Returns:
            True if successful
        """
        filepath = self.data_dir / f"{table}.json"
        data = self._read_json(filepath)
        
        original_length = len(data)
        data = [record for record in data if record.get(id_field) != record_id]
        
        if len(data) < original_length:
            self._write_json(filepath, data)
            return True
        
        return False
    
    def get_next_id(self, table: str, id_prefix: str) -> str:
        """
        Generate next available ID for a table
        
        Args:
            table: Table name
            id_prefix: Prefix for ID (e.g., 'PAT', 'APT')
            
        Returns:
            Next available ID
        """
        filepath = self.data_dir / f"{table}.json"
        data = self._read_json(filepath)
        
        if not data:
            return f"{id_prefix}001"
        
        # Extract numeric parts from existing IDs
        max_num = 0
        for record in data:
            # Get the first ID-like field
            record_id = None
            for key, value in record.items():
                if isinstance(value, str) and value.startswith(id_prefix):
                    record_id = value
                    break
            
            if record_id:
                try:
                    num = int(record_id.replace(id_prefix, ''))
                    max_num = max(max_num, num)
                except ValueError:
                    continue
        
        return f"{id_prefix}{str(max_num + 1).zfill(3)}"

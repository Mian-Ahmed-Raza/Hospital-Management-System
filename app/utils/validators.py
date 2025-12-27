"""
Input Validation Module - Exception Handling
Provides validation functions for user inputs
"""

import re
from datetime import datetime
from typing import Optional


class ValidationException(Exception):
    """Custom exception for validation errors"""
    pass


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If email is invalid
    """
    if not email:
        raise ValidationException("Email is required")
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationException("Invalid email format")
    
    return True


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If phone is invalid
    """
    if not phone:
        raise ValidationException("Phone number is required")
    
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    if not cleaned.isdigit():
        raise ValidationException("Phone number must contain only digits")
    
    if len(cleaned) < 10 or len(cleaned) > 15:
        raise ValidationException("Phone number must be between 10 and 15 digits")
    
    return True


def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> bool:
    """
    Validate date format
    
    Args:
        date_str: Date string to validate
        date_format: Expected date format
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If date is invalid
    """
    if not date_str:
        raise ValidationException("Date is required")
    
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        raise ValidationException(f"Date must be in {date_format} format")


def validate_time(time_str: str) -> bool:
    """
    Validate time format (HH:MM)
    
    Args:
        time_str: Time string to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If time is invalid
    """
    if not time_str:
        raise ValidationException("Time is required")
    
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        raise ValidationException("Time must be in HH:MM format")


def validate_required(value: str, field_name: str) -> bool:
    """
    Validate required field
    
    Args:
        value: Value to validate
        field_name: Name of the field
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If value is empty
    """
    if not value or (isinstance(value, str) and not value.strip()):
        raise ValidationException(f"{field_name} is required")
    
    return True


def validate_length(value: str, min_length: int, max_length: Optional[int] = None, field_name: str = "Field") -> bool:
    """
    Validate string length
    
    Args:
        value: Value to validate
        min_length: Minimum length
        max_length: Maximum length (optional)
        field_name: Name of the field
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If length is invalid
    """
    if len(value) < min_length:
        raise ValidationException(f"{field_name} must be at least {min_length} characters long")
    
    if max_length and len(value) > max_length:
        raise ValidationException(f"{field_name} must not exceed {max_length} characters")
    
    return True


def validate_numeric(value: str, field_name: str = "Field") -> bool:
    """
    Validate numeric input
    
    Args:
        value: Value to validate
        field_name: Name of the field
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If value is not numeric
    """
    if not value.replace('.', '', 1).replace('-', '', 1).isdigit():
        raise ValidationException(f"{field_name} must be a valid number")
    
    return True


def validate_blood_group(blood_group: str) -> bool:
    """
    Validate blood group
    
    Args:
        blood_group: Blood group to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If blood group is invalid
    """
    valid_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    
    if blood_group and blood_group not in valid_groups:
        raise ValidationException(f"Invalid blood group. Must be one of: {', '.join(valid_groups)}")
    
    return True


def sanitize_input(value: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        value: Input value to sanitize
        
    Returns:
        Sanitized string
    """
    if not value:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = value.strip()
    sanitized = re.sub(r'[<>\"\'%;()&+]', '', sanitized)
    
    return sanitized

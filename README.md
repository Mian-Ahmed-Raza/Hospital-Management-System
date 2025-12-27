# Hospital Management System

A comprehensive hospital management system built with Python and Tkinter, featuring patient registration, appointment scheduling, billing, and staff management.

## 🏥 Features

- **User Authentication**: Secure login system with role-based access control
- **Patient Management**: Complete patient registration and records management
- **Appointment Scheduling**: Schedule and manage patient appointments
- **Billing System**: Automated billing with service pricing catalog
- **Dashboard**: Intuitive dashboard with real-time statistics
- **Role-Based Access**: Different permissions for Admin, Doctor, Nurse, and Receptionist

## 📋 System Requirements

- Python 3.8 or higher
- Tkinter (usually comes with Python)
- Operating System: Windows, macOS, or Linux

## 🚀 Installation

1. **Clone or download the repository**:
   ```bash
   cd Hospital-Management-System
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app/main.py
   ```

## 👤 Default Login Credentials

The system comes with two default accounts:

### Administrator Account
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: System Administrator

### Doctor Account
- **Username**: `doctor`
- **Password**: `doctor123`
- **Role**: Doctor

## 📁 Project Structure

```
hospital_management_system/
├── app/                        # Main application package
│   ├── __init__.py             # Package initialization
│   ├── main.py                 # Application entry point
│   ├── views/                  # GUI views (Tkinter)
│   │   ├── login.py            # Staff login window
│   │   ├── dashboard.py        # Main navigation hub
│   │   ├── patient_reg.py      # Patient registration interface
│   │   └── appointments.py     # Appointment scheduling window
│   ├── models/                 # Data structures and Exception Handling
│   │   ├── user.py             # Doctor/Admin data models
│   │   ├── patient.py          # Patient data entities
│   │   └── appointment.py      # Appointment record models
│   ├── services/               # Business logic & Refactored code
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── patient_manager.py  # CRUD operations for patients
│   │   └── billing_engine.py   # Billing logic
│   └── utils/                  # Helper functions
│       ├── db_connector.py     # Database/File handling
│       └── validators.py       # Input validation
├── tests/                      # Testing Suite
│   ├── test_views/             # GUI Component testing
│   └── test_services/          # Business logic unit tests
├── docs/                       # Project Documentation
│   ├── process_model.md        # Justification of Process Model
│   └── peer_reviews.md         # Records of walkthroughs/inspections
├── data/                       # Data storage (auto-generated)
├── requirements.txt            # Project dependencies
├── .gitignore                  # Version control exclusions
└── README.md                   # This file
```

## 🎯 Key Features Explained

### 1. Patient Registration
- Register new patients with complete personal information
- Store medical history and emergency contacts
- Automatic patient ID generation
- Input validation and error handling

### 2. Appointment Management
- Schedule appointments with doctors
- View upcoming and past appointments
- Department-wise categorization
- Appointment status tracking (Scheduled, Confirmed, Completed, Cancelled)

### 3. User Management
- Role-based access control (Admin, Doctor, Nurse, Receptionist)
- Secure authentication system
- User profile management
- Permission-based feature access

### 4. Billing System
- Service pricing catalog
- Automatic invoice generation
- Support for consultations, tests, and procedures
- Discount and tax calculation

### 5. Dashboard
- Real-time statistics
- Quick access to all modules
- User-friendly navigation
- Visual indicators for important metrics

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_services/test_auth.py
```

## 📊 Data Storage

The system uses JSON files for data persistence:
- `data/users.json` - User accounts
- `data/patients.json` - Patient records
- `data/appointments.json` - Appointment data
- `data/billing.json` - Billing information

**Note**: For production use, consider migrating to a proper database system (PostgreSQL, MySQL, etc.)

## 🔒 Security Considerations

### Current Implementation
- Input validation to prevent injection attacks
- Role-based access control
- Custom exception handling

### Production Recommendations
- ✅ Implement password hashing (bcrypt)
- ✅ Add SSL/TLS encryption
- ✅ Implement audit logging
- ✅ Add session timeout
- ✅ Implement multi-factor authentication

## 🛠️ Development

### Code Style
The project follows PEP 8 style guidelines for Python code.

### Exception Handling
Comprehensive exception handling is implemented at all layers:
- **Models**: Data validation exceptions
- **Services**: Business logic exceptions
- **Utils**: Validation and database exceptions
- **Views**: User-friendly error messages

## 📖 Usage Guide

### Starting the Application
1. Run `python app/main.py`
2. Login with default credentials
3. Navigate using the dashboard

### Registering a New Patient
1. Click "Patient Registration" on dashboard
2. Fill in required fields (marked with *)
3. Click "Register Patient"
4. Note the generated Patient ID

### Scheduling an Appointment
1. Click "Appointments" on dashboard
2. Enter patient details
3. Select doctor and department
4. Choose date and time
5. Provide reason for visit
6. Click "Schedule Appointment"

## 🤝 Contributing

This project was developed as part of an academic Software Construction and Development course. Contributions and suggestions are welcome!

### Development Process
- **Process Model**: Iterative and Incremental Development
- **Version Control**: Git
- **Testing**: Unit tests with pytest
- **Documentation**: Inline comments and markdown files

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

Hospital Management System Development Team  
Software Construction and Development Course  
December 2025

## 📧 Support

For issues, questions, or suggestions, please contact the development team or create an issue in the project repository.

## 🎓 Academic Context

This project demonstrates:
- ✅ Object-oriented programming principles
- ✅ Design patterns and best practices
- ✅ Exception handling and validation
- ✅ GUI development with Tkinter
- ✅ Unit testing and quality assurance
- ✅ Code refactoring and maintainability
- ✅ Documentation and peer reviews
- ✅ Iterative development methodology

## 🔮 Future Enhancements

- [ ] Database migration (JSON to SQL)
- [ ] Email notifications for appointments
- [ ] SMS reminders
- [ ] Report generation (PDF)
- [ ] Advanced search and filtering
- [ ] Data analytics and insights
- [ ] Mobile app integration
- [ ] Prescription management
- [ ] Lab results tracking
- [ ] Inventory management

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Status**: ✅ Fully Functional

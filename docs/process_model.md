# Process Model Justification

## Selected Process Model: Iterative and Incremental Development

### Overview
The Hospital Management System was developed using an **Iterative and Incremental Development** approach, which is a hybrid model combining elements of both incremental and evolutionary process models.

### Justification

#### 1. **Complex Domain Requirements**
Healthcare management systems involve complex business logic, multiple user roles, and intricate workflows. The iterative approach allowed us to:
- Start with core functionality (authentication, patient registration)
- Gradually add features (appointments, billing) in subsequent iterations
- Refine each module based on feedback and testing

#### 2. **Risk Mitigation**
By developing the system in iterations, we could:
- Identify and address technical challenges early
- Test critical components (data persistence, validation) in isolation
- Adapt to changing requirements without major rework

#### 3. **Continuous Integration and Testing**
Each iteration included:
- Development of new features
- Unit testing of components
- Integration testing of the complete system
- Code refactoring and quality improvements

#### 4. **Stakeholder Feedback**
The iterative model allowed for:
- Early demonstration of working features
- Incorporation of user feedback
- Progressive refinement of the user interface

### Development Iterations

#### Iteration 1: Foundation
- **Goal**: Establish core architecture and data models
- **Deliverables**: 
  - User, Patient, and Appointment models
  - Database connector with JSON file storage
  - Input validation framework
- **Duration**: Week 1-2

#### Iteration 2: Business Logic
- **Goal**: Implement service layer with business rules
- **Deliverables**:
  - Authentication service with role-based access
  - Patient manager with CRUD operations
  - Billing engine with pricing catalog
- **Duration**: Week 3-4

#### Iteration 3: User Interface
- **Goal**: Create interactive GUI using Tkinter
- **Deliverables**:
  - Login window with authentication
  - Main dashboard with navigation
  - Patient registration form
  - Appointment scheduling interface
- **Duration**: Week 5-6

#### Iteration 4: Testing and Refinement
- **Goal**: Comprehensive testing and bug fixes
- **Deliverables**:
  - Unit tests for services
  - Integration tests for views
  - Documentation and code cleanup
- **Duration**: Week 7-8

### Benefits Realized

1. **Flexibility**: Adapted to requirement changes without disrupting completed work
2. **Quality**: Continuous testing ensured high code quality
3. **Maintainability**: Modular architecture made the system easy to maintain
4. **User Satisfaction**: Regular demonstrations built confidence in the system

### Comparison with Other Models

#### Why Not Waterfall?
- Healthcare requirements evolve; waterfall's rigid structure would not accommodate changes
- Late testing in waterfall would have discovered critical issues too late

#### Why Not Pure Agile?
- Academic project constraints required structured planning
- Documentation requirements suited iterative approach better

#### Why Not Spiral?
- Lower risk profile didn't justify the overhead of formal risk analysis in each cycle
- Smaller team size made spiral's extensive documentation unnecessary

### Exception Handling Strategy

Throughout development, we implemented comprehensive exception handling:
- **Custom Exceptions**: Created domain-specific exceptions (UserException, PatientException, etc.)
- **Validation Layer**: Input validation in utils/validators.py prevents invalid data
- **Service Layer**: Business logic includes error handling and rollback mechanisms
- **GUI Layer**: User-friendly error messages guide users when issues occur

### Conclusion

The Iterative and Incremental Development model proved ideal for this project, balancing structure with flexibility, enabling continuous improvement, and delivering a robust, maintainable hospital management system.

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Author**: HMS Development Team

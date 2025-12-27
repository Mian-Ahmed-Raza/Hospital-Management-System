# Billing Module - User Guide

## Overview

The Billing Module is a comprehensive invoice and payment management system integrated into the Hospital Management System. It allows healthcare staff to create invoices, track payments, and manage billing records efficiently.

## Features

### ✨ Key Features

1. **Invoice Creation**
   - Create detailed invoices for patients
   - Add multiple services/items to each invoice
   - Calculate totals with discounts and taxes
   - Support for various payment methods

2. **Service Catalog**
   - Pre-defined medical services with pricing
   - Consultations, tests, procedures
   - Customizable quantities

3. **Payment Tracking**
   - Track payment status (Pending/Paid)
   - Multiple payment methods (Cash, Card, Insurance, etc.)
   - Payment history for each patient

4. **Invoice Management**
   - Search and filter invoices
   - View detailed invoice information
   - Mark invoices as paid
   - Print-ready invoice format

## Available Services

| Service Code | Description | Price (₹) |
|-------------|-------------|----------|
| `consultation` | Doctor Consultation | 500 |
| `checkup` | General Checkup | 300 |
| `blood_test` | Blood Test | 400 |
| `xray` | X-Ray | 800 |
| `ultrasound` | Ultrasound | 1,200 |
| `mri` | MRI Scan | 5,000 |
| `ct_scan` | CT Scan | 4,000 |
| `ecg` | ECG | 250 |
| `vaccination` | Vaccination | 150 |
| `minor_surgery` | Minor Surgery | 10,000 |
| `admission_fee` | Hospital Admission | 2,000 |
| `room_charge` | Room Charge (per day) | 1,500 |
| `medicine` | Medicines | Variable |

## How to Use

### Accessing the Billing Module

1. Log in to the Hospital Management System
2. From the dashboard, click **"💰 Billing"**
3. The Billing window will open

### Creating a New Invoice

#### Step 1: Patient Selection

1. Click **"+ New"** button in the invoice list
2. Enter the **Patient ID** in the Patient Information section
3. Click **"Search"** to load patient details
4. Verify the patient name is displayed

#### Step 2: Adding Services

1. In the **Services & Items** section:
   - Select a service from the dropdown menu
   - Enter the quantity (default is 1)
   - Click **"+ Add"** to add the service to the invoice

2. Repeat to add multiple services
3. All added services will appear in the services list

#### Step 3: Billing Details

1. Enter **Discount** percentage (if applicable)
2. Enter **Tax** percentage (if applicable)
3. Select **Payment Method**:
   - Cash
   - Card
   - Insurance
   - Online Payment
   - Cheque

#### Step 4: Calculate and Save

1. Click **"Calculate Total"** to see:
   - Subtotal
   - Discount amount
   - Tax amount
   - Final total

2. Review the invoice details

3. Click **"💾 Save Invoice"** to save to database

4. Confirmation message will appear

### Viewing Invoice Details

1. **Search for Invoice**:
   - Use the search box to find invoices by:
     - Invoice ID
     - Patient name

2. **Select Invoice**:
   - Click on any invoice in the list
   - Details will appear in the "Invoice Details" tab

3. **Invoice Information Displayed**:
   - Invoice ID and date
   - Patient information
   - List of services with quantities and prices
   - Payment details
   - Current status (PENDING/PAID)

### Managing Payments

#### Mark Invoice as Paid

1. Select an invoice from the list
2. Go to the "Invoice Details" tab
3. Click **"✓ Mark as Paid"**
4. Confirm the action
5. Invoice status will update to "PAID"

#### Print Invoice

1. Select an invoice from the list
2. Go to the "Invoice Details" tab
3. Click **"🖨 Print"**
4. (In production: generates PDF and sends to printer)

## Example Workflow

### Scenario: Patient Visit and Billing

**Patient**: John Doe (PAT001)
**Services**: Doctor consultation + Blood test

1. **Create Invoice**:
   ```
   Patient ID: PAT001
   Patient Name: John Doe (auto-filled)
   ```

2. **Add Services**:
   ```
   Service: consultation - Doctor Consultation (₹500)
   Quantity: 1
   [Add]
   
   Service: blood_test - Blood Test (₹400)
   Quantity: 1
   [Add]
   ```

3. **Apply Billing Details**:
   ```
   Discount: 10%
   Tax: 5%
   Payment Method: Card
   ```

4. **Calculate**:
   ```
   Subtotal:        ₹900.00
   Discount (10%):  -₹90.00
   Tax (5%):        ₹40.50
   ─────────────────────────
   TOTAL:           ₹850.50
   ```

5. **Save Invoice**: INV001 created successfully!

## Tips & Best Practices

### ✅ Do's

- Always search and verify patient details before creating an invoice
- Double-check service selection and quantities
- Calculate total before saving
- Review invoice details after creation
- Mark invoices as paid promptly after payment received
- Use appropriate payment method

### ❌ Don'ts

- Don't create invoices without valid patient information
- Don't skip the calculate step
- Don't save incomplete invoices
- Don't forget to apply discounts or taxes when applicable

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Search Patient | Tab to search field |
| Add Service | After selecting service, press Enter |
| Calculate Total | Alt + C (when in billing window) |
| Save Invoice | Alt + S (when in billing window) |

## Data Storage

### Invoice Data Structure

Invoices are stored in the `billing` table with the following fields:

```python
{
    'bill_id': 'INV001',           # Unique invoice ID
    'patient_id': 'PAT001',        # Patient reference
    'patient_name': 'John Doe',    # Patient name
    'appointment_id': None,        # Optional appointment link
    'bill_date': '2025-12-27',     # Invoice date
    'services': '[...]',           # JSON array of services
    'total_amount': '850.50',      # Final amount
    'payment_status': 'pending',   # pending or paid
    'payment_method': 'Card'       # Payment method used
}
```

### Services Data Format

Each service in the invoice is stored as:

```json
{
    "description": "Doctor Consultation",
    "quantity": 1,
    "unit_price": 500.0,
    "total": 500.0
}
```

## API Reference

### For Developers

#### Creating Invoice Programmatically

```python
from app.services.billing_engine import BillingEngine
from app.utils.db_connector import DatabaseConnector

db = DatabaseConnector()
billing = BillingEngine(db)

# Create invoice
invoice = billing.create_invoice('PAT001', 'John Doe')

# Add services
invoice.add_item('Doctor Consultation', 1, 500.0)
invoice.add_item('Blood Test', 1, 400.0)

# Set discount and tax
invoice.discount_percent = 10
invoice.tax_percent = 5

# Calculate totals
print(f"Total: ₹{invoice.total}")

# Save to database
billing.save_invoice(invoice)
```

#### Retrieving Invoices

```python
# Get specific invoice
invoice_data = billing.get_invoice('INV001')

# Get all invoices for a patient
patient_invoices = billing.get_patient_invoices('PAT001')

# Mark as paid
billing.mark_invoice_paid('INV001')
```

## Troubleshooting

### Common Issues

#### 1. Patient Not Found

**Problem**: "No patient found with ID: PAT001"

**Solution**:
- Verify patient ID is correct
- Ensure patient exists in Patient Records
- Check patient registration is complete

#### 2. Service Not Adding

**Problem**: Service doesn't appear in list

**Solution**:
- Ensure patient is selected first
- Verify service is selected from dropdown
- Check quantity is a valid number
- Try refreshing the service selection

#### 3. Calculate Button Not Working

**Problem**: Total not calculating

**Solution**:
- Ensure at least one service is added
- Check discount/tax values are valid numbers
- Try clearing and re-entering values

#### 4. Invoice Not Saving

**Problem**: "Failed to save invoice"

**Solution**:
- Ensure all required fields are filled
- Calculate total before saving
- Check database connection
- Verify patient information is complete

## Reporting

### Available Reports (Coming Soon)

Future versions will include:

1. **Daily Sales Report**: Total revenue per day
2. **Payment Status Report**: Pending vs. Paid invoices
3. **Patient Billing History**: All invoices for a patient
4. **Service Revenue Report**: Revenue by service type
5. **Outstanding Payments**: List of pending invoices

## Security & Permissions

### Role-Based Access

- **Admin**: Full access to all billing functions
- **Doctor**: Can create invoices, view all invoices
- **Receptionist**: Can create invoices, mark as paid
- **Nurse**: View-only access (limited)

### Audit Trail

All billing operations are logged with:
- User who created/modified invoice
- Timestamp of operation
- Changes made to invoice status

## Integration

### With Other Modules

1. **Patient Records**: 
   - Link invoices to patient records
   - View billing history from patient details

2. **Appointments**:
   - Create invoice from appointment
   - Link appointment to invoice

3. **Reports**:
   - Generate financial reports
   - Export billing data

## Customization

### Adding Custom Services

To add new services to the catalog, modify `app/services/billing_engine.py`:

```python
SERVICES = {
    # ... existing services ...
    'new_service': {
        'name': 'New Service Name',
        'price': 1000.0
    }
}
```

### Changing Currency

To change from ₹ (Rupees) to another currency:

1. Edit `app/views/billing.py`
2. Replace all `₹` symbols with your currency symbol
3. Update price formatting if needed

## Support

For issues or questions about the billing module:

1. Check this documentation
2. Review error messages in the application
3. Check database connectivity
4. Verify patient records are up to date

## Future Enhancements

Planned features for future releases:

- [ ] PDF invoice generation
- [ ] Email invoices to patients
- [ ] Recurring billing for subscriptions
- [ ] Insurance claim integration
- [ ] Multi-currency support
- [ ] Partial payment tracking
- [ ] Refund management
- [ ] Discount codes/coupons
- [ ] Automated payment reminders
- [ ] Online payment gateway integration

---

**Version**: 1.0  
**Last Updated**: December 27, 2025  
**Module**: Billing & Invoice Management

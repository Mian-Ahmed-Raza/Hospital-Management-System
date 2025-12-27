# Hospital Management System - Dark Theme Documentation

## Theme Overview
The entire Hospital Management System has been updated with a modern, professional dark theme that provides excellent visual consistency and reduced eye strain.

## Color Palette

### Primary Colors
- **Main Background**: `#1a1a2e` - Deep navy blue for primary background
- **Panel Background**: `#16213e` - Slightly lighter navy for cards and panels
- **Text Primary**: `#ffffff` - White for main text
- **Text Secondary**: `#7f8c8d` - Light gray for labels and secondary text

### Accent Colors
- **Primary Accent**: `#3498db` - Bright blue for highlights and interactive elements
- **Success**: `#2ecc71` - Green for success states and confirmations
- **Danger**: `#e74c3c` - Red for warnings and delete actions
- **Neutral**: `#95a5a6` - Gray for secondary buttons

### Hover States
- **Blue Hover**: `#2980b9` - Darker blue for button hover
- **Green Hover**: `#27ae60` - Darker green for success button hover
- **Gray Hover**: `#7f8c8d` - Darker gray for neutral button hover

## Typography
- **Font Family**: Segoe UI throughout the application
- **Headings**: 
  - Main titles: 14-16pt bold
  - Section headers: 13pt bold
  - Form labels: 10pt regular
- **Body Text**: 10pt regular
- **Buttons**: 10-11pt with some bold variants

## Component Styling

### Windows
- **Background**: Dark navy (`#1a1a2e`)
- **Title Bar**: System default with custom title text
- **Dimensions**: Responsive to content, minimum 800x600px

### Cards/Panels
- **Background**: `#16213e`
- **Border**: None (flat design)
- **Shadow Effect**: Layered frames with slight offset
- **Padding**: 20px internal padding

### Input Fields
- **Background**: `#1a1a2e`
- **Text Color**: `#ffffff`
- **Border**: Flat design (no border)
- **Cursor**: `#3498db` (blue)
- **Padding**: 10px vertical, full horizontal

### Buttons
- **Primary Action**: `#2ecc71` (green) with `#27ae60` hover
- **Secondary Action**: `#3498db` (blue) with `#2980b9` hover
- **Neutral Action**: `#95a5a6` (gray) with `#7f8c8d` hover
- **Danger Action**: `#e74c3c` (red) with `#c0392b` hover
- **Style**: Flat design with hover effects
- **Cursor**: Hand pointer on hover

### Dropdowns (Combobox)
- **Style**: `Dark.TCombobox` custom ttk style
- **Background**: `#16213e`
- **Text Color**: `#ffffff`
- **Arrow Color**: `#3498db`
- **Font**: Segoe UI 10pt

### Tables (Treeview)
- **Style**: `Dark.Treeview` custom ttk style
- **Background**: `#1a1a2e`
- **Text Color**: `#ffffff`
- **Heading Background**: `#16213e`
- **Heading Text**: `#2ecc71` (green) bold
- **Selection**: `#3498db` (blue highlight)

### Text Areas
- **Background**: `#1a1a2e`
- **Text Color**: `#ffffff`
- **Border**: Wrapped in `#16213e` frame for subtle border effect
- **Cursor**: `#3498db`

## Icon Usage
The system uses emoji icons for visual enhancement:
- 🏥 Hospital/Medical
- 👤 User/Profile
- 🔒 Security/Lock
- 📋 Forms/Documents
- 📞 Contact
- 📅 Calendar/Appointments
- 🔍 Search
- ✓ Confirm/Success
- ✖ Cancel/Close
- ⟳ Refresh/Reload

## Files Updated

### Fully Themed Views
1. **app/views/login.py** - Login window with shadow effects and hover states
2. **app/views/dashboard.py** - Dashboard with stats cards and navigation
3. **app/views/patient_reg.py** - Patient registration form with scrollable fields
4. **app/views/appointments.py** - Appointment scheduling with form and list view

### Component Patterns

#### Shadow Effect Pattern
```python
# Create shadow layer
shadow = tk.Frame(parent, bg='#0f1419')
shadow.place(x=5, y=5, width=width, height=height)

# Create main content layer
content = tk.Frame(parent, bg='#16213e')
content.place(x=0, y=0, width=width, height=height)
```

#### Hover Effect Pattern
```python
button = tk.Button(parent, text="Button", bg='#3498db')
button.bind('<Enter>', lambda e: button.config(bg='#2980b9'))
button.bind('<Leave>', lambda e: button.config(bg='#3498db'))
```

#### Form Field Pattern
```python
# Label
tk.Label(
    parent,
    text="Label:",
    font=('Segoe UI', 10),
    bg='#16213e',
    fg='#7f8c8d'
).pack(anchor='w')

# Entry
entry = tk.Entry(
    parent,
    font=('Segoe UI', 10),
    bg='#1a1a2e',
    fg='#ffffff',
    relief='flat',
    bd=0,
    insertbackground='#3498db'
)
entry.pack(fill='x', ipady=5)
```

## Accessibility Considerations
- **Contrast Ratio**: All text meets WCAG AA standards
- **Focus Indicators**: Blue cursor and selection highlights
- **Hover States**: Clear visual feedback on interactive elements
- **Font Size**: Minimum 10pt for readability

## User Experience Benefits
1. **Reduced Eye Strain**: Dark theme is easier on the eyes in low-light environments
2. **Professional Appearance**: Modern, consistent design throughout
3. **Visual Hierarchy**: Clear distinction between different UI elements
4. **Interactive Feedback**: Hover effects provide immediate user feedback
5. **Visual Consistency**: Same color palette and styling across all windows

## Testing Recommendations
- Test in different lighting conditions
- Verify all hover states work correctly
- Ensure text remains readable in all contexts
- Check that dropdowns and comboboxes display properly
- Validate form submissions work with themed inputs

## Future Enhancements
- Add theme toggle (light/dark mode)
- Implement custom color scheme preferences
- Add animation transitions for smoother interactions
- Consider accessibility settings for high contrast mode

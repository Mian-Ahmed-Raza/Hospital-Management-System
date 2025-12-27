"""
Patient Registration Window - Patient registration interface
Handles new patient registration and patient information updates
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from app.services.patient_manager import PatientManager, PatientManagerException
from app.utils.db_connector import DatabaseConnector


class PatientRegistrationWindow:
    """Patient registration window"""
    
    def __init__(self, db_connector: DatabaseConnector, patient_manager: PatientManager):
        """
        Initialize patient registration window
        
        Args:
            db_connector: Database connector instance
            patient_manager: Patient manager instance
        """
        self.db = db_connector
        self.patient_manager = patient_manager
        
        self.window = tk.Toplevel()
        self.window.title("Patient Registration")
        self.window.geometry("700x700")
        self.window.resizable(False, False)
        
        # Center window
        self._center_window()
        
        # Create UI
        self._create_widgets()
    
    def _center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create UI widgets"""
        # Set window background
        self.window.configure(bg='#1a1a2e')
        
        # Header with modern styling
        header_frame = tk.Frame(self.window, bg='#16213e', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Icon and title
        header_content = tk.Frame(header_frame, bg='#16213e')
        header_content.pack(expand=True)
        
        icon_label = tk.Label(
            header_content,
            text="👤",
            font=('Segoe UI Emoji', 24),
            bg='#16213e',
            fg='#3498db'
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        title_label = tk.Label(
            header_content,
            text="Patient Registration",
            font=('Segoe UI', 18, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        title_label.pack(side='left')
        
        # Main form frame with scrollbar
        main_frame = tk.Frame(self.window, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas for scrolling
        canvas = tk.Canvas(main_frame, bg='#1a1a2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Form fields
        self._create_form_fields(scrollable_frame)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Buttons frame
        button_frame = tk.Frame(self.window, bg='#1a1a2e')
        button_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        register_btn = tk.Button(
            button_frame,
            text="✓ Register Patient",
            font=('Segoe UI', 12, 'bold'),
            bg='#2ecc71',
            fg='white',
            activebackground='#27ae60',
            activeforeground='white',
            width=20,
            height=2,
            cursor='hand2',
            relief='flat',
            bd=0,
            command=self.register_patient
        )
        register_btn.pack(side='left', padx=(0, 10))
        register_btn.bind('<Enter>', lambda e: register_btn.config(bg='#27ae60'))
        register_btn.bind('<Leave>', lambda e: register_btn.config(bg='#2ecc71'))
        
        clear_btn = tk.Button(
            button_frame,
            text="↺ Clear Form",
            font=('Segoe UI', 12),
            bg='#34495e',
            fg='white',
            activebackground='#2c3e50',
            activeforeground='white',
            width=15,
            height=2,
            cursor='hand2',
            relief='flat',
            bd=0,
            command=self.clear_form
        )
        clear_btn.pack(side='left')
        clear_btn.bind('<Enter>', lambda e: clear_btn.config(bg='#2c3e50'))
        clear_btn.bind('<Leave>', lambda e: clear_btn.config(bg='#34495e'))
    
    def _create_form_fields(self, parent):
        """Create form input fields"""
        # Personal Information Section
        section_label = tk.Label(
            parent,
            text="📋 Personal Information",
            font=('Segoe UI', 13, 'bold'),
            bg='#1a1a2e',
            fg='#3498db'
        )
        section_label.pack(anchor='w', pady=(10, 15))
        
        # First Name
        self._create_field(parent, "First Name *", "first_name")
        
        # Last Name
        self._create_field(parent, "Last Name *", "last_name")
        
        # Date of Birth
        dob_frame = tk.Frame(parent, bg='#1a1a2e')
        dob_frame.pack(fill='x', pady=8)
        
        tk.Label(
            dob_frame,
            text="Date of Birth * (YYYY-MM-DD):",
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#7f8c8d'
        ).pack(anchor='w')
        
        entry_bg = tk.Frame(dob_frame, bg='#16213e', relief='flat')
        entry_bg.pack(fill='x', pady=(5, 0))
        
        self.dob_entry = tk.Entry(
            entry_bg,
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#ffffff',
            relief='flat',
            bd=0,
            insertbackground='#3498db'
        )
        self.dob_entry.pack(fill='x', padx=10, pady=10)
        self.dob_entry.insert(0, "2000-01-01")
        
        # Gender
        gender_frame = tk.Frame(parent, bg='#1a1a2e')
        gender_frame.pack(fill='x', pady=8)
        
        tk.Label(
            gender_frame,
            text="Gender *:",
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#7f8c8d'
        ).pack(anchor='w')
        
        self.gender_var = tk.StringVar(value="Male")
        gender_options = tk.Frame(gender_frame, bg='#1a1a2e')
        gender_options.pack(anchor='w', pady=(5, 0))
        
        for gender in ['Male', 'Female', 'Other']:
            tk.Radiobutton(
                gender_options,
                text=gender,
                variable=self.gender_var,
                value=gender,
                font=('Segoe UI', 10),
                bg='#1a1a2e',
                fg='#ffffff',
                selectcolor='#16213e',
                activebackground='#1a1a2e',
                activeforeground='#ffffff'
            ).pack(side='left', padx=(0, 15))
        
        # Contact Information
        section_label = tk.Label(
            parent,
            text="📞 Contact Information",
            font=('Segoe UI', 13, 'bold'),
            bg='#1a1a2e',
            fg='#3498db'
        )
        section_label.pack(anchor='w', pady=(20, 15))
        
        # Phone
        self._create_field(parent, "Phone Number *", "phone")
        
        # Email
        self._create_field(parent, "Email", "email")
        
        # Address
        self._create_field(parent, "Address", "address", height=3)
        
        # Medical Information
        section_label = tk.Label(
            parent,
            text="🏥 Medical Information",
            font=('Segoe UI', 13, 'bold'),
            bg='#1a1a2e',
            fg='#3498db'
        )
        section_label.pack(anchor='w', pady=(20, 15))
        
        # Blood Group
        blood_frame = tk.Frame(parent, bg='#1a1a2e')
        blood_frame.pack(fill='x', pady=8)
        
        tk.Label(
            blood_frame,
            text="Blood Group:",
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#7f8c8d'
        ).pack(anchor='w')
        
        self.blood_group_var = tk.StringVar()
        
        # Style the combobox
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Dark.TCombobox', 
                       fieldbackground='#16213e',
                       background='#16213e',
                       foreground='#ffffff',
                       arrowcolor='#3498db')
        
        blood_combo = ttk.Combobox(
            blood_frame,
            textvariable=self.blood_group_var,
            values=['', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
            state='readonly',
            font=('Segoe UI', 10),
            style='Dark.TCombobox'
        )
        blood_combo.pack(fill='x', pady=(5, 0))
        blood_combo.set('')
        
        # Emergency Contact
        self._create_field(parent, "Emergency Contact", "emergency_contact")
    
    def _create_field(self, parent, label_text, field_name, height=1):
        """Create a form field"""
        field_frame = tk.Frame(parent, bg='#1a1a2e')
        field_frame.pack(fill='x', pady=8)
        
        label = tk.Label(
            field_frame,
            text=label_text + ":",
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#7f8c8d'
        )
        label.pack(anchor='w')
        
        entry_bg = tk.Frame(field_frame, bg='#16213e', relief='flat')
        entry_bg.pack(fill='x', pady=(5, 0))
        
        if height > 1:
            entry = tk.Text(
                entry_bg,
                font=('Segoe UI', 10),
                bg='#16213e',
                fg='#ffffff',
                relief='flat',
                bd=0,
                height=height,
                insertbackground='#3498db'
            )
        else:
            entry = tk.Entry(
                entry_bg,
                font=('Segoe UI', 10),
                bg='#16213e',
                fg='#ffffff',
                relief='flat',
                bd=0,
                insertbackground='#3498db'
            )
        
        entry.pack(fill='x', padx=10, pady=10)
        setattr(self, f"{field_name}_entry", entry)
    
    def register_patient(self):
        """Handle patient registration"""
        try:
            # Get form values
            first_name = self.first_name_entry.get().strip()
            last_name = self.last_name_entry.get().strip()
            dob = self.dob_entry.get().strip()
            gender = self.gender_var.get()
            phone = self.phone_entry.get().strip()
            email = self.email_entry.get().strip() or None
            address = self.address_entry.get("1.0", tk.END).strip() or None
            blood_group = self.blood_group_var.get() or None
            emergency_contact = self.emergency_contact_entry.get().strip() or None
            
            # Register patient
            patient = self.patient_manager.register_patient(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                gender=gender,
                phone=phone,
                email=email,
                address=address,
                blood_group=blood_group,
                emergency_contact=emergency_contact
            )
            
            # Ensure window stays on top for messagebox
            self.window.lift()
            self.window.focus_force()
            
            messagebox.showinfo(
                "Success",
                f"Patient registered successfully!\n\nPatient ID: {patient.patient_id}\nName: {patient.full_name}",
                parent=self.window
            )
            
            self.clear_form()
            
        except PatientManagerException as e:
            # Keep window open and show error
            self.window.lift()
            self.window.focus_force()
            messagebox.showerror("Registration Failed", str(e), parent=self.window)
        except Exception as e:
            # Keep window open and show error
            self.window.lift()
            self.window.focus_force()
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.window)
    
    def clear_form(self):
        """Clear all form fields"""
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, "2000-01-01")
        self.gender_var.set("Male")
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete("1.0", tk.END)
        self.blood_group_var.set('')
        self.emergency_contact_entry.delete(0, tk.END)
        self.first_name_entry.focus()

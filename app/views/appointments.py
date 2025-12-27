"""
Appointments Window - Appointment scheduling window
Handles appointment creation, viewing, and management
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from app.models.user import User
from app.models.appointment import Appointment, AppointmentStatus, AppointmentException
from app.utils.db_connector import DatabaseConnector
from app.utils.validators import validate_date, validate_time, ValidationException


class AppointmentsWindow:
    """Appointments management window"""
    
    def __init__(self, db_connector: DatabaseConnector, user: User):
        """
        Initialize appointments window
        
        Args:
            db_connector: Database connector instance
            user: Current logged-in user
        """
        self.db = db_connector
        self.user = user
        
        self.window = tk.Toplevel()
        self.window.title("Appointment Management")
        self.window.geometry("1000x700")
        
        # Center window
        self._center_window()
        
        # Create UI
        self._create_widgets()
        
        # Load appointments
        self.load_appointments()
    
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
        # Header
        header_frame = tk.Frame(self.window, bg='#2ecc71', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Appointment Management",
            font=('Arial', 16, 'bold'),
            bg='#2ecc71',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # Main container
        main_container = tk.Frame(self.window, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left panel - New Appointment Form
        left_panel = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self._create_appointment_form(left_panel)
        
        # Right panel - Appointments List
        right_panel = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self._create_appointments_list(right_panel)
    
    def _create_appointment_form(self, parent):
        """Create new appointment form"""
        form_title = tk.Label(
            parent,
            text="Schedule New Appointment",
            font=('Arial', 13, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        form_title.pack(pady=(15, 20))
        
        form_frame = tk.Frame(parent, bg='white')
        form_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Patient ID
        self._create_form_field(form_frame, "Patient ID:", "patient_id")
        
        # Patient Name
        self._create_form_field(form_frame, "Patient Name:", "patient_name")
        
        # Doctor
        tk.Label(
            form_frame,
            text="Doctor:",
            font=('Arial', 10),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(10, 5))
        
        self.doctor_var = tk.StringVar()
        doctors = self.db.read('users', {'role': 'doctor', 'is_active': True})
        doctor_names = [f"{d['full_name']} ({d['specialization']})" for d in doctors]
        
        self.doctors_data = doctors  # Store for later use
        
        doctor_combo = ttk.Combobox(
            form_frame,
            textvariable=self.doctor_var,
            values=doctor_names,
            state='readonly',
            font=('Arial', 10)
        )
        doctor_combo.pack(fill='x', pady=(0, 10))
        if doctor_names:
            doctor_combo.set(doctor_names[0])
        
        # Department
        tk.Label(
            form_frame,
            text="Department:",
            font=('Arial', 10),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(10, 5))
        
        self.department_var = tk.StringVar()
        departments = ['General Medicine', 'Cardiology', 'Pediatrics', 'Orthopedics', 
                      'Neurology', 'Dermatology', 'ENT', 'Emergency']
        
        dept_combo = ttk.Combobox(
            form_frame,
            textvariable=self.department_var,
            values=departments,
            state='readonly',
            font=('Arial', 10)
        )
        dept_combo.pack(fill='x', pady=(0, 10))
        dept_combo.set('General Medicine')
        
        # Date
        self._create_form_field(form_frame, "Date (YYYY-MM-DD):", "date")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Time
        self._create_form_field(form_frame, "Time (HH:MM):", "time")
        self.time_entry.insert(0, "09:00")
        
        # Reason
        tk.Label(
            form_frame,
            text="Reason for Visit:",
            font=('Arial', 10),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(10, 5))
        
        self.reason_entry = tk.Text(
            form_frame,
            font=('Arial', 10),
            relief='solid',
            bd=1,
            height=3
        )
        self.reason_entry.pack(fill='x', pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill='x', pady=(10, 0))
        
        schedule_btn = tk.Button(
            button_frame,
            text="Schedule Appointment",
            font=('Arial', 11, 'bold'),
            bg='#2ecc71',
            fg='white',
            cursor='hand2',
            relief='flat',
            command=self.schedule_appointment
        )
        schedule_btn.pack(fill='x', pady=(0, 5))
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear Form",
            font=('Arial', 10),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            relief='flat',
            command=self.clear_form
        )
        clear_btn.pack(fill='x')
    
    def _create_form_field(self, parent, label_text, field_name):
        """Create a form field"""
        tk.Label(
            parent,
            text=label_text,
            font=('Arial', 10),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(10, 5))
        
        entry = tk.Entry(
            parent,
            font=('Arial', 10),
            relief='solid',
            bd=1
        )
        entry.pack(fill='x', pady=(0, 10))
        setattr(self, f"{field_name}_entry", entry)
    
    def _create_appointments_list(self, parent):
        """Create appointments list view"""
        list_title = tk.Label(
            parent,
            text="Upcoming Appointments",
            font=('Arial', 13, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        list_title.pack(pady=(15, 20))
        
        # Search frame
        search_frame = tk.Frame(parent, bg='white')
        search_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="Search:",
            font=('Arial', 10),
            bg='white'
        ).pack(side='left', padx=(0, 10))
        
        self.search_entry = tk.Entry(
            search_frame,
            font=('Arial', 10),
            relief='solid',
            bd=1
        )
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_appointments())
        
        search_btn = tk.Button(
            search_frame,
            text="Refresh",
            font=('Arial', 9),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            relief='flat',
            command=self.load_appointments
        )
        search_btn.pack(side='right')
        
        # Treeview for appointments
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient='vertical')
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        # Treeview
        self.appointments_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Patient', 'Doctor', 'Date', 'Time', 'Status'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=self.appointments_tree.yview)
        hsb.config(command=self.appointments_tree.xview)
        
        # Define columns
        self.appointments_tree.heading('ID', text='ID')
        self.appointments_tree.heading('Patient', text='Patient')
        self.appointments_tree.heading('Doctor', text='Doctor')
        self.appointments_tree.heading('Date', text='Date')
        self.appointments_tree.heading('Time', text='Time')
        self.appointments_tree.heading('Status', text='Status')
        
        self.appointments_tree.column('ID', width=80)
        self.appointments_tree.column('Patient', width=120)
        self.appointments_tree.column('Doctor', width=120)
        self.appointments_tree.column('Date', width=100)
        self.appointments_tree.column('Time', width=80)
        self.appointments_tree.column('Status', width=100)
        
        self.appointments_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Context menu
        self.appointments_tree.bind('<Button-3>', self.show_context_menu)
    
    def schedule_appointment(self):
        """Schedule a new appointment"""
        try:
            # Get form values
            patient_id = self.patient_id_entry.get().strip()
            patient_name = self.patient_name_entry.get().strip()
            date = self.date_entry.get().strip()
            time = self.time_entry.get().strip()
            reason = self.reason_entry.get("1.0", tk.END).strip()
            
            # Get selected doctor
            doctor_idx = self.doctor_var.get()
            if not doctor_idx or not self.doctors_data:
                raise AppointmentException("Please select a doctor")
            
            # Find doctor from combo selection
            for doctor in self.doctors_data:
                if f"{doctor['full_name']} ({doctor['specialization']})" == doctor_idx:
                    doctor_id = doctor['user_id']
                    doctor_name = doctor['full_name']
                    break
            else:
                raise AppointmentException("Invalid doctor selection")
            
            department = self.department_var.get()
            
            # Validate
            if not patient_id or not patient_name:
                raise AppointmentException("Patient ID and Name are required")
            
            validate_date(date)
            validate_time(time)
            
            if not reason:
                raise AppointmentException("Reason for visit is required")
            
            # Generate appointment ID
            appointment_id = self.db.get_next_id('appointments', 'APT')
            
            # Create appointment
            appointment = Appointment(
                appointment_id=appointment_id,
                patient_id=patient_id,
                patient_name=patient_name,
                doctor_id=doctor_id,
                doctor_name=doctor_name,
                appointment_date=date,
                appointment_time=time,
                department=department,
                reason=reason
            )
            
            # Save to database
            self.db.create('appointments', appointment.to_dict())
            
            messagebox.showinfo(
                "Success",
                f"Appointment scheduled successfully!\n\nAppointment ID: {appointment_id}\nDate: {date} at {time}"
            )
            
            self.clear_form()
            self.load_appointments()
            
        except (AppointmentException, ValidationException) as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def load_appointments(self):
        """Load appointments into treeview"""
        # Clear existing items
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        # Get search term
        search_term = self.search_entry.get().strip().lower()
        
        # Load appointments
        appointments = self.db.read('appointments')
        
        # Sort by date and time (newest first)
        appointments.sort(
            key=lambda x: f"{x.get('appointment_date', '')} {x.get('appointment_time', '')}",
            reverse=True
        )
        
        # Insert into treeview
        for appt in appointments:
            # Apply search filter
            if search_term:
                searchable = f"{appt.get('appointment_id', '')} {appt.get('patient_name', '')} {appt.get('doctor_name', '')}".lower()
                if search_term not in searchable:
                    continue
            
            self.appointments_tree.insert('', tk.END, values=(
                appt.get('appointment_id', ''),
                appt.get('patient_name', ''),
                appt.get('doctor_name', ''),
                appt.get('appointment_date', ''),
                appt.get('appointment_time', ''),
                appt.get('status', '').title()
            ))
    
    def show_context_menu(self, event):
        """Show context menu for appointment"""
        item = self.appointments_tree.identify_row(event.y)
        if item:
            self.appointments_tree.selection_set(item)
            menu = tk.Menu(self.window, tearoff=0)
            menu.add_command(label="View Details", command=self.view_appointment_details)
            menu.add_command(label="Cancel Appointment", command=self.cancel_appointment)
            menu.post(event.x_root, event.y_root)
    
    def view_appointment_details(self):
        """View selected appointment details"""
        selection = self.appointments_tree.selection()
        if not selection:
            return
        
        values = self.appointments_tree.item(selection[0])['values']
        appt_id = values[0]
        
        appointments = self.db.read('appointments', {'appointment_id': appt_id})
        if appointments:
            appt = appointments[0]
            details = f"""
Appointment Details

ID: {appt.get('appointment_id')}
Patient: {appt.get('patient_name')} (ID: {appt.get('patient_id')})
Doctor: {appt.get('doctor_name')}
Department: {appt.get('department')}
Date: {appt.get('appointment_date')}
Time: {appt.get('appointment_time')}
Status: {appt.get('status', '').title()}
Reason: {appt.get('reason')}
            """
            messagebox.showinfo("Appointment Details", details.strip())
    
    def cancel_appointment(self):
        """Cancel selected appointment"""
        selection = self.appointments_tree.selection()
        if not selection:
            return
        
        values = self.appointments_tree.item(selection[0])['values']
        appt_id = values[0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this appointment?"):
            self.db.update('appointments', appt_id, 'appointment_id', {'status': 'cancelled'})
            messagebox.showinfo("Success", "Appointment cancelled successfully")
            self.load_appointments()
    
    def clear_form(self):
        """Clear appointment form"""
        self.patient_id_entry.delete(0, tk.END)
        self.patient_name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "09:00")
        self.reason_entry.delete("1.0", tk.END)
        self.patient_id_entry.focus()

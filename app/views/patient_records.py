"""
Patient Records Window - View and search patient records
Displays all registered patients with search functionality
"""

import tkinter as tk
from tkinter import messagebox, ttk
from app.utils.db_connector import DatabaseConnector


class PatientRecordsWindow:
    """Patient records viewer window"""
    
    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize patient records window
        
        Args:
            db_connector: Database connector instance
        """
        self.db = db_connector
        
        self.window = tk.Toplevel()
        self.window.title("Patient Records")
        self.window.geometry("1200x700")
        
        # Center window
        self._center_window()
        
        # Create UI
        self._create_widgets()
        
        # Load patients
        self.load_patients()
    
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
            text="👥",
            font=('Segoe UI Emoji', 24),
            bg='#16213e',
            fg='#3498db'
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        title_label = tk.Label(
            header_content,
            text="Patient Records",
            font=('Segoe UI', 18, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        title_label.pack(side='left')
        
        # Main container
        main_container = tk.Frame(self.window, bg='#16213e', relief='flat', bd=0)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Search frame
        search_frame = tk.Frame(main_container, bg='#16213e')
        search_frame.pack(fill='x', padx=20, pady=(20, 15))
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=('Segoe UI', 11),
            bg='#16213e',
            fg='#7f8c8d'
        ).pack(side='left', padx=(0, 15))
        
        self.search_entry = tk.Entry(
            search_frame,
            font=('Segoe UI', 11),
            bg='#1a1a2e',
            fg='#ffffff',
            relief='flat',
            bd=0,
            insertbackground='#3498db'
        )
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(0, 15), ipady=8)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_patients())
        
        # Refresh button
        refresh_btn = tk.Button(
            search_frame,
            text="⟳ Refresh",
            font=('Segoe UI', 10),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            relief='flat',
            bd=0,
            command=self.load_patients
        )
        refresh_btn.pack(side='right', padx=5)
        refresh_btn.bind('<Enter>', lambda e: refresh_btn.config(bg='#2980b9'))
        refresh_btn.bind('<Leave>', lambda e: refresh_btn.config(bg='#3498db'))
        
        # Stats label
        self.stats_label = tk.Label(
            main_container,
            text="Total Patients: 0",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#7f8c8d'
        )
        self.stats_label.pack(anchor='w', padx=20, pady=(0, 10))
        
        # Treeview frame
        tree_frame = tk.Frame(main_container, bg='#16213e')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Configure treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('PatientRecords.Treeview',
                       background='#1a1a2e',
                       foreground='#ffffff',
                       fieldbackground='#1a1a2e',
                       borderwidth=0,
                       font=('Segoe UI', 9))
        style.configure('PatientRecords.Treeview.Heading',
                       background='#16213e',
                       foreground='#3498db',
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'))
        style.map('PatientRecords.Treeview',
                 background=[('selected', '#3498db')])
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient='vertical')
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        # Treeview
        self.patients_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Name', 'DOB', 'Gender', 'Phone', 'Email', 'Blood Group', 'Address'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            style='PatientRecords.Treeview'
        )
        
        vsb.config(command=self.patients_tree.yview)
        hsb.config(command=self.patients_tree.xview)
        
        # Define columns
        self.patients_tree.heading('ID', text='Patient ID')
        self.patients_tree.heading('Name', text='Full Name')
        self.patients_tree.heading('DOB', text='Date of Birth')
        self.patients_tree.heading('Gender', text='Gender')
        self.patients_tree.heading('Phone', text='Phone')
        self.patients_tree.heading('Email', text='Email')
        self.patients_tree.heading('Blood Group', text='Blood Group')
        self.patients_tree.heading('Address', text='Address')
        
        self.patients_tree.column('ID', width=100, anchor='center')
        self.patients_tree.column('Name', width=150)
        self.patients_tree.column('DOB', width=100, anchor='center')
        self.patients_tree.column('Gender', width=80, anchor='center')
        self.patients_tree.column('Phone', width=120)
        self.patients_tree.column('Email', width=180)
        self.patients_tree.column('Blood Group', width=100, anchor='center')
        self.patients_tree.column('Address', width=200)
        
        self.patients_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Context menu
        self.patients_tree.bind('<Double-Button-1>', self.view_patient_details)
        self.patients_tree.bind('<Button-3>', self.show_context_menu)
    
    def load_patients(self):
        """Load patients into treeview"""
        try:
            # Clear existing items
            for item in self.patients_tree.get_children():
                self.patients_tree.delete(item)
            
            # Get search term
            search_term = self.search_entry.get().strip().lower()
            
            # Load patients - filter for active patients only
            patients = self.db.read('patients', {'is_active': True})
            
            # Debug output
            print(f"DEBUG: Loaded {len(patients)} active patients from database")
            
            # Sort by patient ID
            patients.sort(key=lambda x: x.get('patient_id', ''))
            
            displayed_count = 0
            # Insert into treeview
            for patient in patients:
                # Apply search filter
                if search_term:
                    searchable = f"{patient.get('patient_id', '')} {patient.get('first_name', '')} {patient.get('last_name', '')} {patient.get('phone', '')} {patient.get('email', '')}".lower()
                    if search_term not in searchable:
                        continue
                
                full_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}"
                
                self.patients_tree.insert('', tk.END, values=(
                    patient.get('patient_id', ''),
                    full_name,
                    patient.get('date_of_birth', ''),
                    patient.get('gender', ''),
                    patient.get('phone', ''),
                    patient.get('email', ''),
                    patient.get('blood_group', ''),
                    patient.get('address', '')
                ))
                displayed_count += 1
                print(f"DEBUG: Inserted patient {patient.get('patient_id')} - {full_name}")
            
            # Update stats
            total = len(patients)
            if search_term:
                self.stats_label.config(text=f"Showing {displayed_count} of {total} patients")
            else:
                self.stats_label.config(text=f"Total Patients: {total}")
            
            print(f"DEBUG: Display complete - {displayed_count} patients shown")
            
        except Exception as e:
            print(f"ERROR in load_patients: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load patients: {str(e)}")
    
    def show_context_menu(self, event):
        """Show context menu for patient"""
        item = self.patients_tree.identify_row(event.y)
        if item:
            self.patients_tree.selection_set(item)
            menu = tk.Menu(self.window, tearoff=0, bg='#16213e', fg='#ffffff', font=('Segoe UI', 9))
            menu.add_command(label="View Details", command=self.view_patient_details)
            menu.add_command(label="Delete Patient", command=self.delete_patient)
            menu.post(event.x_root, event.y_root)
    
    def view_patient_details(self, event=None):
        """View selected patient details"""
        selection = self.patients_tree.selection()
        if not selection:
            return
        
        values = self.patients_tree.item(selection[0])['values']
        patient_id = values[0]
        
        patients = self.db.read('patients', {'patient_id': patient_id})
        if patients:
            patient = patients[0]
            
            # Create details window
            details_window = tk.Toplevel(self.window)
            details_window.title(f"Patient Details - {patient_id}")
            details_window.geometry("500x600")
            details_window.configure(bg='#1a1a2e')
            details_window.transient(self.window)
            details_window.grab_set()
            
            # Header
            header = tk.Frame(details_window, bg='#16213e', height=60)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            tk.Label(
                header,
                text=f"👤 Patient Information",
                font=('Segoe UI', 16, 'bold'),
                bg='#16213e',
                fg='#3498db'
            ).pack(expand=True)
            
            # Scrollable content
            canvas = tk.Canvas(details_window, bg='#1a1a2e', highlightthickness=0)
            scrollbar = tk.Scrollbar(details_window, orient='vertical', command=canvas.yview)
            content_frame = tk.Frame(canvas, bg='#1a1a2e')
            
            canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side='right', fill='y')
            canvas.pack(side='left', fill='both', expand=True)
            
            canvas_window = canvas.create_window((0, 0), window=content_frame, anchor='nw')
            
            def configure_scroll(event):
                canvas.configure(scrollregion=canvas.bbox('all'))
                canvas.itemconfig(canvas_window, width=event.width)
            
            content_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
            canvas.bind('<Configure>', configure_scroll)
            
            # Patient details
            details = [
                ("Patient ID", patient.get('patient_id', 'N/A')),
                ("First Name", patient.get('first_name', 'N/A')),
                ("Last Name", patient.get('last_name', 'N/A')),
                ("Date of Birth", patient.get('date_of_birth', 'N/A')),
                ("Gender", patient.get('gender', 'N/A')),
                ("Phone Number", patient.get('phone', 'N/A')),
                ("Email", patient.get('email', 'N/A')),
                ("Address", patient.get('address', 'N/A')),
                ("Blood Group", patient.get('blood_group', 'N/A')),
                ("Emergency Contact", patient.get('emergency_contact', 'N/A')),
            ]
            
            for label, value in details:
                detail_frame = tk.Frame(content_frame, bg='#16213e')
                detail_frame.pack(fill='x', padx=20, pady=8)
                
                tk.Label(
                    detail_frame,
                    text=label + ":",
                    font=('Segoe UI', 10, 'bold'),
                    bg='#16213e',
                    fg='#7f8c8d',
                    anchor='w'
                ).pack(anchor='w', padx=15, pady=(10, 5))
                
                tk.Label(
                    detail_frame,
                    text=str(value),
                    font=('Segoe UI', 11),
                    bg='#16213e',
                    fg='#ffffff',
                    anchor='w',
                    wraplength=430
                ).pack(anchor='w', padx=15, pady=(0, 10))
            
            # Close button
            close_btn = tk.Button(
                content_frame,
                text="✖ Close",
                font=('Segoe UI', 11, 'bold'),
                bg='#95a5a6',
                fg='white',
                cursor='hand2',
                relief='flat',
                bd=0,
                command=details_window.destroy
            )
            close_btn.pack(pady=20)
            close_btn.bind('<Enter>', lambda e: close_btn.config(bg='#7f8c8d'))
            close_btn.bind('<Leave>', lambda e: close_btn.config(bg='#95a5a6'))
    
    def delete_patient(self):
        """Delete selected patient"""
        selection = self.patients_tree.selection()
        if not selection:
            return
        
        values = self.patients_tree.item(selection[0])['values']
        patient_id = values[0]
        patient_name = values[1]
        
        if messagebox.askyesno("Confirm Delete", 
                               f"Are you sure you want to delete patient '{patient_name}' (ID: {patient_id})?\n\nThis action cannot be undone."):
            self.db.delete('patients', patient_id, 'patient_id')
            messagebox.showinfo("Success", "Patient deleted successfully")
            self.load_patients()

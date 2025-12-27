"""
Dashboard Window - Main navigation hub
Main application interface with navigation to all features
"""

import tkinter as tk
from tkinter import messagebox
from app.models.user import User
from app.services.auth_service import AuthService
from app.services.patient_manager import PatientManager
from app.utils.db_connector import DatabaseConnector


class Dashboard:
    """Main dashboard window"""
    
    def __init__(self, user: User, auth_service: AuthService, db_connector: DatabaseConnector):
        """
        Initialize dashboard
        
        Args:
            user: Current logged-in user
            auth_service: Authentication service
            db_connector: Database connector
        """
        self.user = user
        self.auth_service = auth_service
        self.db = db_connector
        self.patient_manager = PatientManager(db_connector)
        
        self.window = tk.Tk()
        self.window.title("Hospital Management System - Dashboard")
        self.window.geometry("900x600")
        self.window.resizable(False, False)
        
        # Center window
        self._center_window()
        
        # Create UI
        self._create_widgets()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
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
        # Header frame
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Hospital Management System",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side='left', padx=20, pady=20)
        
        # User info
        user_label = tk.Label(
            header_frame,
            text=f"Welcome, {self.user.full_name} ({self.user.role.value.title()})",
            font=('Arial', 11),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        user_label.pack(side='right', padx=20)
        
        # Main content area
        content_frame = tk.Frame(self.window, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Stats frame
        stats_frame = tk.Frame(content_frame, bg='#ecf0f1')
        stats_frame.pack(fill='x', pady=(0, 20))
        
        self._create_stats_cards(stats_frame)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(content_frame, bg='#ecf0f1')
        nav_frame.pack(fill='both', expand=True)
        
        self._create_navigation_buttons(nav_frame)
        
        # Footer frame
        footer_frame = tk.Frame(self.window, bg='#34495e', height=50)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        logout_btn = tk.Button(
            footer_frame,
            text="Logout",
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            width=15,
            cursor='hand2',
            relief='flat',
            command=self.logout
        )
        logout_btn.pack(side='right', padx=20, pady=10)
    
    def _create_stats_cards(self, parent):
        """Create statistics cards"""
        # Get statistics
        total_patients = self.patient_manager.get_patient_count()
        total_appointments = len(self.db.read('appointments'))
        
        stats = [
            ("Total Patients", total_patients, "#3498db"),
            ("Total Appointments", total_appointments, "#2ecc71"),
            ("Active Users", len(self.db.read('users', {'is_active': True})), "#e67e22")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(parent, bg=color, relief='raised', bd=2)
            card.pack(side='left', fill='both', expand=True, padx=10)
            
            value_label = tk.Label(
                card,
                text=str(value),
                font=('Arial', 28, 'bold'),
                bg=color,
                fg='white'
            )
            value_label.pack(pady=(15, 5))
            
            title_label = tk.Label(
                card,
                text=label,
                font=('Arial', 12),
                bg=color,
                fg='white'
            )
            title_label.pack(pady=(0, 15))
    
    def _create_navigation_buttons(self, parent):
        """Create navigation buttons"""
        buttons = [
            ("👤 Patient Registration", self.open_patient_registration, "#3498db"),
            ("📅 Appointments", self.open_appointments, "#2ecc71"),
            ("💰 Billing", self.open_billing, "#e67e22"),
            ("📊 Reports", self.open_reports, "#9b59b6"),
            ("👥 Patient Records", self.open_patient_records, "#1abc9c"),
            ("⚙️ Settings", self.open_settings, "#34495e")
        ]
        
        row = 0
        col = 0
        for text, command, color in buttons:
            btn = tk.Button(
                parent,
                text=text,
                font=('Arial', 13),
                bg=color,
                fg='white',
                width=25,
                height=3,
                cursor='hand2',
                relief='flat',
                command=command
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(3):
            parent.grid_rowconfigure(i, weight=1)
        for i in range(2):
            parent.grid_columnconfigure(i, weight=1)
    
    def open_patient_registration(self):
        """Open patient registration window"""
        from app.views.patient_reg import PatientRegistrationWindow
        PatientRegistrationWindow(self.db, self.patient_manager)
    
    def open_appointments(self):
        """Open appointments window"""
        from app.views.appointments import AppointmentsWindow
        AppointmentsWindow(self.db, self.user)
    
    def open_billing(self):
        """Open billing window"""
        messagebox.showinfo("Billing", "Billing module - Coming soon!")
    
    def open_reports(self):
        """Open reports window"""
        messagebox.showinfo("Reports", "Reports module - Coming soon!")
    
    def open_patient_records(self):
        """Open patient records window"""
        messagebox.showinfo("Patient Records", "Patient records viewer - Coming soon!")
    
    def open_settings(self):
        """Open settings window"""
        messagebox.showinfo("Settings", "Settings module - Coming soon!")
    
    def logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.auth_service.logout()
            self.window.destroy()
            
            # Restart application
            from app.main import main
            main()
    
    def on_closing(self):
        """Handle window close"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.window.destroy()
    
    def run(self):
        """Start the dashboard"""
        self.window.mainloop()

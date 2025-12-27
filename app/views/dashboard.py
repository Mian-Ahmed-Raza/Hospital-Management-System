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
        # Set window background
        self.window.configure(bg='#1a1a2e')
        
        # Header frame with modern styling
        header_frame = tk.Frame(self.window, bg='#16213e', height=90)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Icon and Title container
        title_container = tk.Frame(header_frame, bg='#16213e')
        title_container.pack(side='left', padx=25, pady=20)
        
        # Medical icon
        icon_label = tk.Label(
            title_container,
            text="🏥",
            font=('Segoe UI Emoji', 28),
            bg='#16213e',
            fg='#3498db'
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        # Title
        title_label = tk.Label(
            title_container,
            text="Hospital Management System",
            font=('Segoe UI', 20, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        title_label.pack(side='left')
        
        # User info with modern styling
        user_container = tk.Frame(header_frame, bg='#16213e')
        user_container.pack(side='right', padx=25)
        
        user_icon = tk.Label(
            user_container,
            text="👤",
            font=('Segoe UI Emoji', 16),
            bg='#16213e',
            fg='#3498db'
        )
        user_icon.pack(side='left', padx=(0, 10))
        
        user_label = tk.Label(
            user_container,
            text=f"{self.user.full_name}\n{self.user.role.value.title()}",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#ffffff',
            justify='left'
        )
        user_label.pack(side='left')
        
        # Main content area
        content_frame = tk.Frame(self.window, bg='#1a1a2e')
        content_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Stats frame
        stats_frame = tk.Frame(content_frame, bg='#1a1a2e')
        stats_frame.pack(fill='x', pady=(0, 25))
        
        self._create_stats_cards(stats_frame)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(content_frame, bg='#1a1a2e')
        nav_frame.pack(fill='both', expand=True)
        
        self._create_navigation_buttons(nav_frame)
        
        # Footer frame
        footer_frame = tk.Frame(self.window, bg='#16213e', height=50)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        # Logout button with modern styling
        logout_btn = tk.Button(
            footer_frame,
            text="🚪 Logout",
            font=('Segoe UI', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            activeforeground='white',
            width=15,
            cursor='hand2',
            relief='flat',
            bd=0,
            command=self.logout
        )
        logout_btn.pack(side='right', padx=25, pady=10)
        logout_btn.bind('<Enter>', lambda e: logout_btn.config(bg='#c0392b'))
        logout_btn.bind('<Leave>', lambda e: logout_btn.config(bg='#e74c3c'))
    
    def _create_stats_cards(self, parent):
        """Create statistics cards"""
        # Get statistics
        total_patients = self.patient_manager.get_patient_count()
        total_appointments = len(self.db.read('appointments'))
        
        stats = [
            ("👥 Total Patients", total_patients, "#3498db", "#2980b9"),
            ("📅 Appointments", total_appointments, "#2ecc71", "#27ae60"),
            ("👨‍⚕️ Active Users", len(self.db.read('users', {'is_active': True})), "#e67e22", "#d35400")
        ]
        
        for i, (label, value, color, hover_color) in enumerate(stats):
            # Card container with modern shadow effect
            card_container = tk.Frame(parent, bg='#1a1a2e')
            card_container.pack(side='left', fill='both', expand=True, padx=8)
            
            # Shadow effect
            shadow = tk.Frame(card_container, bg='#0d0d1a', relief='flat')
            shadow.place(relx=0, rely=0.03, relwidth=1, relheight=1)
            
            # Main card
            card = tk.Frame(card_container, bg='#16213e', relief='flat', bd=0)
            card.place(relx=0, rely=0, relwidth=1, relheight=0.97)
            
            # Colored accent bar at top
            accent = tk.Frame(card, bg=color, height=4)
            accent.pack(fill='x')
            
            value_label = tk.Label(
                card,
                text=str(value),
                font=('Segoe UI', 36, 'bold'),
                bg='#16213e',
                fg='#ffffff'
            )
            value_label.pack(pady=(20, 5))
            
            title_label = tk.Label(
                card,
                text=label,
                font=('Segoe UI', 11),
                bg='#16213e',
                fg='#7f8c8d'
            )
            title_label.pack(pady=(0, 20))
    
    def _create_navigation_buttons(self, parent):
        """Create navigation buttons"""
        buttons = [
            ("👤 Patient Registration", self.open_patient_registration, "#3498db", "#2980b9"),
            ("📅 Appointments", self.open_appointments, "#2ecc71", "#27ae60"),
            ("💰 Billing", self.open_billing, "#e67e22", "#d35400"),
            ("📊 Reports", self.open_reports, "#9b59b6", "#8e44ad"),
            ("👥 Patient Records", self.open_patient_records, "#1abc9c", "#16a085"),
            ("⚙️ Settings", self.open_settings, "#34495e", "#2c3e50")
        ]
        
        row = 0
        col = 0
        for text, command, color, hover_color in buttons:
            # Button container for shadow effect
            btn_container = tk.Frame(parent, bg='#1a1a2e')
            btn_container.grid(row=row, column=col, padx=12, pady=12, sticky='nsew')
            
            # Shadow
            shadow = tk.Frame(btn_container, bg='#0d0d1a')
            shadow.place(relx=0.02, rely=0.02, relwidth=1, relheight=1)
            
            # Main button
            btn = tk.Button(
                btn_container,
                text=text,
                font=('Segoe UI', 13, 'bold'),
                bg=color,
                fg='white',
                activebackground=hover_color,
                activeforeground='white',
                cursor='hand2',
                relief='flat',
                bd=0,
                command=command
            )
            btn.place(relx=0, rely=0, relwidth=1, relheight=0.98)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn, hc=hover_color: b.config(bg=hc))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=c))
            
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

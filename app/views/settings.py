"""
Settings Window - Application settings and user preferences
Allows users to manage their profile, change password, and configure system settings
"""

import tkinter as tk
from tkinter import messagebox, ttk
from app.models.user import User
from app.utils.validators import validate_email, validate_phone, ValidationException


class SettingsWindow:
    """Settings and preferences window"""
    
    def __init__(self, user: User, db_connector, auth_service):
        """
        Initialize settings window
        
        Args:
            user: Current logged-in user
            db_connector: Database connector instance
            auth_service: Authentication service instance
        """
        self.user = user
        self.db = db_connector
        self.auth_service = auth_service
        
        self.window = tk.Toplevel()
        self.window.title("Settings & Preferences")
        self.window.geometry("1000x700")
        self.window.configure(bg='#1a1a2e')
        
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
        # Header
        header_frame = tk.Frame(self.window, bg='#16213e', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Icon and title
        header_content = tk.Frame(header_frame, bg='#16213e')
        header_content.pack(expand=True)
        
        icon_label = tk.Label(
            header_content,
            text="⚙️",
            font=('Segoe UI Emoji', 24),
            bg='#16213e',
            fg='#3498db'
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        title_label = tk.Label(
            header_content,
            text="Settings & Preferences",
            font=('Segoe UI', 18, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        title_label.pack(side='left')
        
        # Close button
        close_btn = tk.Button(
            header_frame,
            text="✕ Close",
            font=('Segoe UI', 10),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            cursor='hand2',
            relief='flat',
            bd=0,
            command=self.window.destroy,
            width=10
        )
        close_btn.pack(side='right', padx=25)
        
        # Main content
        content_frame = tk.Frame(self.window, bg='#1a1a2e')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left panel - Settings categories
        left_panel = tk.Frame(content_frame, bg='#16213e', width=200)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self._create_category_menu(left_panel)
        
        # Right panel - Settings content
        right_panel = tk.Frame(content_frame, bg='#16213e')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Create notebook for different settings sections
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Style notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#16213e', borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background='#1a1a2e',
                       foreground='#ffffff',
                       padding=[20, 10],
                       font=('Segoe UI', 10))
        style.map('TNotebook.Tab',
                 background=[('selected', '#3498db')],
                 foreground=[('selected', '#ffffff')])
        
        # Create tabs
        self._create_profile_tab()
        self._create_security_tab()
        self._create_system_tab()
        self._create_about_tab()
    
    def _create_category_menu(self, parent):
        """Create category menu"""
        tk.Label(
            parent,
            text="Categories",
            font=('Segoe UI', 12, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        ).pack(pady=(20, 15), padx=15)
        
        categories = [
            ("👤 Profile", 0),
            ("🔒 Security", 1),
            ("🖥️ System", 2),
            ("ℹ️ About", 3)
        ]
        
        for text, tab_index in categories:
            btn = tk.Button(
                parent,
                text=text,
                font=('Segoe UI', 10),
                bg='#1a1a2e',
                fg='#ffffff',
                activebackground='#3498db',
                activeforeground='#ffffff',
                cursor='hand2',
                relief='flat',
                bd=0,
                anchor='w',
                command=lambda idx=tab_index: self.notebook.select(idx)
            )
            btn.pack(fill='x', padx=10, pady=5, ipady=8)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#3498db'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#1a1a2e'))
    
    def _create_profile_tab(self):
        """Create profile settings tab"""
        profile_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(profile_frame, text='👤 Profile')
        
        # Scrollable content
        canvas = tk.Canvas(profile_frame, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(profile_frame, orient='vertical', command=canvas.yview)
        content = tk.Frame(canvas, bg='#16213e')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas_window = canvas.create_window((0, 0), window=content, anchor='nw')
        
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.itemconfig(canvas_window, width=event.width)
        
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', configure_scroll)
        
        # Profile information
        tk.Label(
            content,
            text="Profile Information",
            font=('Segoe UI', 14, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        ).pack(anchor='w', pady=(20, 15), padx=20)
        
        # User info fields
        fields = [
            ("User ID:", self.user.user_id, False),
            ("Username:", self.user.username, False),
            ("Full Name:", self.user.full_name, True),
            ("Email:", self.user.email, True),
            ("Phone:", self.user.phone, True),
            ("Role:", self.user.role.value.title(), False),
        ]
        
        if self.user.role.value == 'doctor':
            fields.append(("Specialization:", self.user.specialization, True))
        
        self.profile_entries = {}
        
        for label, value, editable in fields:
            field_frame = tk.Frame(content, bg='#16213e')
            field_frame.pack(fill='x', padx=20, pady=8)
            
            tk.Label(
                field_frame,
                text=label,
                font=('Segoe UI', 10, 'bold'),
                bg='#16213e',
                fg='#7f8c8d',
                width=15,
                anchor='w'
            ).pack(side='left', padx=(0, 10))
            
            if editable:
                entry = tk.Entry(
                    field_frame,
                    font=('Segoe UI', 10),
                    bg='#1a1a2e',
                    fg='#ffffff',
                    insertbackground='#ffffff',
                    relief='flat',
                    bd=0
                )
                entry.insert(0, value or '')
                entry.pack(side='left', fill='x', expand=True, ipady=8, padx=5)
                self.profile_entries[label.rstrip(':')] = entry
            else:
                tk.Label(
                    field_frame,
                    text=value,
                    font=('Segoe UI', 10),
                    bg='#1a1a2e',
                    fg='#ffffff',
                    anchor='w',
                    relief='flat'
                ).pack(side='left', fill='x', expand=True, ipady=8, padx=5)
        
        # Save button
        save_btn = tk.Button(
            content,
            text="💾 Save Changes",
            font=('Segoe UI', 11, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            cursor='hand2',
            relief='flat',
            bd=0,
            command=self.save_profile
        )
        save_btn.pack(pady=20)
        save_btn.bind('<Enter>', lambda e: save_btn.config(bg='#2980b9'))
        save_btn.bind('<Leave>', lambda e: save_btn.config(bg='#3498db'))
    
    def _create_security_tab(self):
        """Create security settings tab"""
        security_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(security_frame, text='🔒 Security')
        
        # Content container
        content = tk.Frame(security_frame, bg='#16213e')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Change password section
        tk.Label(
            content,
            text="Change Password",
            font=('Segoe UI', 14, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        ).pack(anchor='w', pady=(10, 20))
        
        # Current password
        self._create_password_field(content, "Current Password:", 'current_password')
        
        # New password
        self._create_password_field(content, "New Password:", 'new_password')
        
        # Confirm password
        self._create_password_field(content, "Confirm Password:", 'confirm_password')
        
        # Change password button
        change_btn = tk.Button(
            content,
            text="🔒 Change Password",
            font=('Segoe UI', 11, 'bold'),
            bg='#e67e22',
            fg='white',
            activebackground='#d35400',
            cursor='hand2',
            relief='flat',
            bd=0,
            command=self.change_password
        )
        change_btn.pack(pady=20)
        change_btn.bind('<Enter>', lambda e: change_btn.config(bg='#d35400'))
        change_btn.bind('<Leave>', lambda e: change_btn.config(bg='#e67e22'))
        
        # Security tips
        tips_frame = tk.LabelFrame(
            content,
            text="🛡️ Security Tips",
            font=('Segoe UI', 11, 'bold'),
            bg='#1a1a2e',
            fg='#3498db',
            relief='flat'
        )
        tips_frame.pack(fill='x', pady=(30, 0))
        
        tips = [
            "• Use a strong password with at least 8 characters",
            "• Include uppercase, lowercase, numbers, and symbols",
            "• Don't share your password with anyone",
            "• Change your password regularly",
            "• Don't use the same password for multiple accounts"
        ]
        
        for tip in tips:
            tk.Label(
                tips_frame,
                text=tip,
                font=('Segoe UI', 9),
                bg='#1a1a2e',
                fg='#7f8c8d',
                anchor='w'
            ).pack(anchor='w', padx=15, pady=5)
    
    def _create_password_field(self, parent, label_text, var_name):
        """Create password field with show/hide toggle"""
        field_frame = tk.Frame(parent, bg='#16213e')
        field_frame.pack(fill='x', pady=8)
        
        tk.Label(
            field_frame,
            text=label_text,
            font=('Segoe UI', 10, 'bold'),
            bg='#16213e',
            fg='#7f8c8d',
            width=18,
            anchor='w'
        ).pack(side='left', padx=(0, 10))
        
        entry_frame = tk.Frame(field_frame, bg='#1a1a2e')
        entry_frame.pack(side='left', fill='x', expand=True)
        
        entry = tk.Entry(
            entry_frame,
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=0,
            show='•'
        )
        entry.pack(side='left', fill='x', expand=True, ipady=8, padx=5)
        setattr(self, var_name, entry)
        
        # Show/hide button
        show_var = tk.BooleanVar(value=False)
        
        def toggle_password():
            if show_var.get():
                entry.config(show='')
                toggle_btn.config(text='👁️')
            else:
                entry.config(show='•')
                toggle_btn.config(text='👁️‍🗨️')
            show_var.set(not show_var.get())
        
        toggle_btn = tk.Button(
            entry_frame,
            text='👁️‍🗨️',
            font=('Segoe UI', 9),
            bg='#1a1a2e',
            fg='#3498db',
            activebackground='#1a1a2e',
            cursor='hand2',
            relief='flat',
            bd=0,
            command=toggle_password
        )
        toggle_btn.pack(side='right', padx=5)
    
    def _create_system_tab(self):
        """Create system settings tab"""
        system_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(system_frame, text='🖥️ System')
        
        # Scrollable content
        canvas = tk.Canvas(system_frame, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(system_frame, orient='vertical', command=canvas.yview)
        content = tk.Frame(canvas, bg='#16213e')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas_window = canvas.create_window((0, 0), window=content, anchor='nw')
        
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.itemconfig(canvas_window, width=event.width)
        
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', configure_scroll)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Add padding container
        padded_content = tk.Frame(content, bg='#16213e')
        padded_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Database information header with refresh button
        db_header_frame = tk.Frame(padded_content, bg='#16213e')
        db_header_frame.pack(fill='x', pady=(10, 20))
        
        tk.Label(
            db_header_frame,
            text="Database Information",
            font=('Segoe UI', 14, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        ).pack(side='left')
        
        refresh_btn = tk.Button(
            db_header_frame,
            text="⟳ Refresh",
            font=('Segoe UI', 9),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            cursor='hand2',
            relief='flat',
            bd=0,
            command=lambda: self._refresh_db_stats(self.db_stats_labels)
        )
        refresh_btn.pack(side='right', padx=5)
        refresh_btn.bind('<Enter>', lambda e: refresh_btn.config(bg='#2980b9'))
        refresh_btn.bind('<Leave>', lambda e: refresh_btn.config(bg='#3498db'))
        
        self.db_info_frame = tk.Frame(padded_content, bg='#1a1a2e')
        self.db_info_frame.pack(fill='x', pady=10)
        
        # Store label references for updating
        self.db_stats_labels = {}
        
        # Get and display database stats
        self._display_db_stats()
        
        # Application preferences
        tk.Label(
            padded_content,
            text="Application Preferences",
            font=('Segoe UI', 14, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        ).pack(anchor='w', pady=(30, 20))
        
        prefs_frame = tk.Frame(padded_content, bg='#1a1a2e')
        prefs_frame.pack(fill='x', pady=10)
        
        # Theme info
        pref_item = tk.Frame(prefs_frame, bg='#1a1a2e')
        pref_item.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            pref_item,
            text="Current Theme:",
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#7f8c8d',
            width=20,
            anchor='w'
        ).pack(side='left')
        
        tk.Label(
            pref_item,
            text="Dark Theme",
            font=('Segoe UI', 10, 'bold'),
            bg='#1a1a2e',
            fg='#3498db',
            anchor='w'
        ).pack(side='left')
    
    def _create_about_tab(self):
        """Create about tab"""
        about_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(about_frame, text='ℹ️ About')
        
        content = tk.Frame(about_frame, bg='#16213e')
        content.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Logo/Icon
        tk.Label(
            content,
            text="🏥",
            font=('Segoe UI Emoji', 48),
            bg='#16213e',
            fg='#3498db'
        ).pack(pady=(20, 10))
        
        # Application name
        tk.Label(
            content,
            text="Hospital Management System",
            font=('Segoe UI', 18, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        ).pack(pady=5)
        
        # Version
        tk.Label(
            content,
            text="Version 1.0.0",
            font=('Segoe UI', 11),
            bg='#16213e',
            fg='#7f8c8d'
        ).pack(pady=5)
        
        # Description
        tk.Label(
            content,
            text="A comprehensive hospital management solution\n"
                 "for patient records, appointments, billing, and reporting.",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#7f8c8d',
            justify='center'
        ).pack(pady=20)
        
        # Features
        features_frame = tk.LabelFrame(
            content,
            text="Key Features",
            font=('Segoe UI', 11, 'bold'),
            bg='#1a1a2e',
            fg='#3498db',
            relief='flat'
        )
        features_frame.pack(fill='x', pady=20)
        
        features = [
            "✓ Patient Registration & Management",
            "✓ Appointment Scheduling",
            "✓ Billing & Invoicing",
            "✓ Comprehensive Reporting",
            "✓ User Access Control",
            "✓ Database Integration"
        ]
        
        for feature in features:
            tk.Label(
                features_frame,
                text=feature,
                font=('Segoe UI', 10),
                bg='#1a1a2e',
                fg='#ffffff',
                anchor='w'
            ).pack(anchor='w', padx=20, pady=5)
        
        # Copyright
        tk.Label(
            content,
            text="© 2025 Hospital Management System\nAll rights reserved.",
            font=('Segoe UI', 9),
            bg='#16213e',
            fg='#7f8c8d',
            justify='center'
        ).pack(pady=20)
    
    def save_profile(self):
        """Save profile changes"""
        try:
            updates = {}
            
            # Get updated values
            if 'Full Name' in self.profile_entries:
                full_name = self.profile_entries['Full Name'].get().strip()
                if full_name:
                    updates['full_name'] = full_name
            
            if 'Email' in self.profile_entries:
                email = self.profile_entries['Email'].get().strip()
                if email:
                    validate_email(email)
                    updates['email'] = email
            
            if 'Phone' in self.profile_entries:
                phone = self.profile_entries['Phone'].get().strip()
                if phone:
                    validate_phone(phone)
                    updates['phone'] = phone
            
            if 'Specialization' in self.profile_entries:
                specialization = self.profile_entries['Specialization'].get().strip()
                if specialization:
                    updates['specialization'] = specialization
            
            if not updates:
                messagebox.showinfo("Info", "No changes to save.", parent=self.window)
                return
            
            # Update database
            success = self.db.update('users', self.user.user_id, 'user_id', updates)
            
            if success:
                # Update user object
                for key, value in updates.items():
                    setattr(self.user, key, value)
                
                messagebox.showinfo("Success", "Profile updated successfully!", parent=self.window)
            else:
                messagebox.showerror("Error", "Failed to update profile.", parent=self.window)
                
        except ValidationException as e:
            messagebox.showerror("Validation Error", str(e), parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save profile: {str(e)}", parent=self.window)
    
    def change_password(self):
        """Change user password"""
        try:
            current_password = self.current_password.get()
            new_password = self.new_password.get()
            confirm_password = self.confirm_password.get()
            
            # Validate inputs
            if not all([current_password, new_password, confirm_password]):
                messagebox.showerror("Error", "All password fields are required.", parent=self.window)
                return
            
            # Verify current password
            if current_password != self.user.password:
                messagebox.showerror("Error", "Current password is incorrect.", parent=self.window)
                return
            
            # Check if new passwords match
            if new_password != confirm_password:
                messagebox.showerror("Error", "New passwords do not match.", parent=self.window)
                return
            
            # Validate new password
            if len(new_password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters long.", parent=self.window)
                return
            
            if new_password == current_password:
                messagebox.showerror("Error", "New password must be different from current password.", parent=self.window)
                return
            
            # Update password
            success = self.db.update('users', self.user.user_id, 'user_id', {'password': new_password})
            
            if success:
                self.user.password = new_password
                
                # Clear fields
                self.current_password.delete(0, tk.END)
                self.new_password.delete(0, tk.END)
                self.confirm_password.delete(0, tk.END)
                
                messagebox.showinfo("Success", 
                                  "Password changed successfully!\n\n"
                                  "Please remember your new password.",
                                  parent=self.window)
            else:
                messagebox.showerror("Error", "Failed to change password.", parent=self.window)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password: {str(e)}", parent=self.window)
    
    def _display_db_stats(self):
        """Display database statistics"""
        try:
            # Clear existing stats
            for widget in self.db_info_frame.winfo_children():
                widget.destroy()
            
            # Get database stats with proper error handling
            try:
                all_patients = self.db.read('patients')
                active_patients = sum(1 for p in all_patients if p.get('is_active') == True)
                total_patients = len(all_patients)
                inactive_patients = total_patients - active_patients
            except Exception as e:
                print(f"Error reading patients: {e}")
                active_patients = total_patients = inactive_patients = 0
            
            try:
                all_appointments = self.db.read('appointments')
                total_appointments = len(all_appointments)
                # Count by status - handle both enum and string values
                scheduled = sum(1 for a in all_appointments if str(a.get('status', '')).lower() in ['scheduled', 'appointmentstatusenum.scheduled'])
                completed = sum(1 for a in all_appointments if str(a.get('status', '')).lower() in ['completed', 'appointmentstatusenum.completed'])
                cancelled = sum(1 for a in all_appointments if str(a.get('status', '')).lower() in ['cancelled', 'appointmentstatusenum.cancelled'])
                confirmed = sum(1 for a in all_appointments if str(a.get('status', '')).lower() in ['confirmed', 'appointmentstatusenum.confirmed'])
            except Exception as e:
                print(f"Error reading appointments: {e}")
                total_appointments = scheduled = completed = cancelled = confirmed = 0
            
            try:
                all_bills = self.db.read('billing')
                total_bills = len(all_bills)
                paid_bills = sum(1 for b in all_bills if str(b.get('payment_status', '')).lower() == 'paid')
                pending_bills = sum(1 for b in all_bills if str(b.get('payment_status', '')).lower() == 'pending')
            except Exception as e:
                print(f"Error reading billing: {e}")
                total_bills = paid_bills = pending_bills = 0
            
            try:
                all_users = self.db.read('users')
                active_users = sum(1 for u in all_users if u.get('is_active') == True)
                total_users = len(all_users)
                # Count by role
                admins = sum(1 for u in all_users if str(u.get('role', '')).lower() in ['admin', 'userroleenum.admin'] and u.get('is_active') == True)
                doctors = sum(1 for u in all_users if str(u.get('role', '')).lower() in ['doctor', 'userroleenum.doctor'] and u.get('is_active') == True)
                nurses = sum(1 for u in all_users if str(u.get('role', '')).lower() in ['nurse', 'userroleenum.nurse'] and u.get('is_active') == True)
                receptionists = sum(1 for u in all_users if str(u.get('role', '')).lower() in ['receptionist', 'userroleenum.receptionist'] and u.get('is_active') == True)
            except Exception as e:
                print(f"Error reading users: {e}")
                active_users = total_users = admins = doctors = nurses = receptionists = 0
            
            # Display stats with more detail
            stats = [
                ("Active Patients", active_patients, '#2ecc71'),
                ("Inactive Patients", inactive_patients, '#95a5a6'),
            ]
            
            # Only show appointments section if there are any
            if total_appointments > 0:
                stats.extend([
                    ("Total Appointments", total_appointments, '#3498db'),
                    ("  ├─ Scheduled", scheduled, '#e67e22'),
                    ("  ├─ Confirmed", confirmed, '#3498db'),
                    ("  ├─ Completed", completed, '#2ecc71'),
                    ("  └─ Cancelled", cancelled, '#e74c3c'),
                ])
            else:
                stats.append(("Total Appointments", 0, '#95a5a6'))
            
            # Only show bills section if there are any
            if total_bills > 0:
                stats.extend([
                    ("Total Bills", total_bills, '#9b59b6'),
                    ("  ├─ Paid", paid_bills, '#2ecc71'),
                    ("  └─ Pending", pending_bills, '#e67e22'),
                ])
            else:
                stats.append(("Total Bills", 0, '#95a5a6'))
            
            # User stats with role breakdown
            stats.extend([
                ("Active Users", active_users, '#1abc9c'),
                ("  ├─ Admins", admins, '#e74c3c'),
                ("  ├─ Doctors", doctors, '#3498db'),
                ("  ├─ Nurses", nurses, '#2ecc71'),
                ("  └─ Receptionists", receptionists, '#e67e22'),
            ])
            
            for label, value, color in stats:
                stat_frame = tk.Frame(self.db_info_frame, bg='#1a1a2e')
                stat_frame.pack(fill='x', padx=15, pady=3)
                
                is_subitem = label.startswith('  ')
                label_font = ('Segoe UI', 9) if is_subitem else ('Segoe UI', 10)
                value_font = ('Segoe UI', 9, 'bold') if is_subitem else ('Segoe UI', 10, 'bold')
                
                tk.Label(
                    stat_frame,
                    text=label + ":",
                    font=label_font,
                    bg='#1a1a2e',
                    fg='#7f8c8d',
                    width=22,
                    anchor='w'
                ).pack(side='left')
                
                value_label = tk.Label(
                    stat_frame,
                    text=str(value),
                    font=value_font,
                    bg='#1a1a2e',
                    fg=color,
                    anchor='w'
                )
                value_label.pack(side='left')
                
                # Store reference for updates
                self.db_stats_labels[label] = value_label
                
        except Exception as e:
            print(f"Error displaying database stats: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load database statistics: {str(e)}", parent=self.window)
    
    def _refresh_db_stats(self, labels_dict):
        """Refresh database statistics"""
        try:
            print("Refreshing database statistics...")
            self._display_db_stats()
            messagebox.showinfo("Success", "Database statistics refreshed!", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh statistics: {str(e)}", parent=self.window)


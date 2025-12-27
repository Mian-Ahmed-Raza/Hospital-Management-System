"""
Login Window - Staff login window
Handles user authentication interface
"""

import tkinter as tk
from tkinter import messagebox, ttk
from app.services.auth_service import AuthService, AuthenticationException


class LoginWindow:
    """Login window for staff authentication"""
    
    def __init__(self, auth_service: AuthService, on_success_callback):
        """
        Initialize login window
        
        Args:
            auth_service: Authentication service instance
            on_success_callback: Function to call on successful login
        """
        self.auth_service = auth_service
        self.on_success_callback = on_success_callback
        
        self.window = tk.Tk()
        self.window.title("Hospital Management System - Login")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        
        # Center window
        self._center_window()
        
        # Configure style
        self._setup_styles()
        
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
    
    def _setup_styles(self):
        """Setup UI styles"""
        self.window.configure(bg='#1a1a2e')
    
    def _create_widgets(self):
        """Create UI widgets"""
        # Main container with gradient-like effect
        main_frame = tk.Frame(self.window, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both')
        
        # Header section with medical theme
        header_frame = tk.Frame(main_frame, bg='#16213e', height=180)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Medical icon (using text)
        icon_label = tk.Label(
            header_frame,
            text="🏥",
            font=('Segoe UI Emoji', 60),
            bg='#16213e',
            fg='#0f4c75'
        )
        icon_label.pack(pady=(30, 10))
        
        # Title with modern styling
        title_label = tk.Label(
            header_frame,
            text="Hospital Management System",
            font=('Segoe UI', 22, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Secure Staff Portal",
            font=('Segoe UI', 11),
            bg='#16213e',
            fg='#3498db'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Login form container with shadow effect
        form_container = tk.Frame(main_frame, bg='#1a1a2e')
        form_container.pack(pady=40, padx=50, fill='both', expand=True)
        
        # Shadow effect frame
        shadow_frame = tk.Frame(form_container, bg='#0d0d1a', relief='flat')
        shadow_frame.place(relx=0.5, rely=0.5, anchor='center', 
                          relwidth=0.95, relheight=0.85)
        
        # Main form frame (appears to float above shadow)
        form_frame = tk.Frame(form_container, bg='#16213e', relief='flat', bd=0)
        form_frame.place(relx=0.5, rely=0.5, anchor='center', 
                        relwidth=0.92, relheight=0.82)
        
        # Login header
        form_title = tk.Label(
            form_frame,
            text="Sign In",
            font=('Segoe UI', 18, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        form_title.pack(pady=(40, 30))
        
        # Username field with modern styling
        username_container = tk.Frame(form_frame, bg='#16213e')
        username_container.pack(pady=(0, 25), padx=40, fill='x')
        
        username_label = tk.Label(
            username_container,
            text="USERNAME",
            font=('Segoe UI', 9, 'bold'),
            bg='#16213e',
            fg='#7f8c8d'
        )
        username_label.pack(anchor='w', pady=(0, 8))
        
        username_frame = tk.Frame(username_container, bg='#1a1a2e', relief='flat', bd=0)
        username_frame.pack(fill='x')
        
        user_icon = tk.Label(
            username_frame,
            text="👤",
            font=('Segoe UI Emoji', 14),
            bg='#1a1a2e',
            fg='#3498db'
        )
        user_icon.pack(side='left', padx=(15, 10), pady=12)
        
        self.username_entry = tk.Entry(
            username_frame,
            font=('Segoe UI', 11),
            bg='#1a1a2e',
            fg='#ffffff',
            relief='flat',
            bd=0,
            insertbackground='#3498db'
        )
        self.username_entry.pack(side='left', fill='x', expand=True, pady=12, padx=(0, 15))
        self.username_entry.focus()
        
        # Password field with modern styling
        password_container = tk.Frame(form_frame, bg='#16213e')
        password_container.pack(pady=(0, 25), padx=40, fill='x')
        
        password_label = tk.Label(
            password_container,
            text="PASSWORD",
            font=('Segoe UI', 9, 'bold'),
            bg='#16213e',
            fg='#7f8c8d'
        )
        password_label.pack(anchor='w', pady=(0, 8))
        
        password_frame = tk.Frame(password_container, bg='#1a1a2e', relief='flat', bd=0)
        password_frame.pack(fill='x')
        
        pass_icon = tk.Label(
            password_frame,
            text="🔒",
            font=('Segoe UI Emoji', 14),
            bg='#1a1a2e',
            fg='#3498db'
        )
        pass_icon.pack(side='left', padx=(15, 10), pady=12)
        
        self.password_entry = tk.Entry(
            password_frame,
            font=('Segoe UI', 11),
            bg='#1a1a2e',
            fg='#ffffff',
            show='●',
            relief='flat',
            bd=0,
            insertbackground='#3498db'
        )
        self.password_entry.pack(side='left', fill='x', expand=True, pady=12, padx=(0, 15))
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        # Login button with hover effect
        login_btn = tk.Button(
            form_frame,
            text="LOGIN",
            font=('Segoe UI', 12, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            width=25,
            height=2,
            cursor='hand2',
            relief='flat',
            bd=0,
            command=self.login
        )
        login_btn.pack(pady=(20, 20), padx=40, fill='x')
        
        # Add hover effect
        login_btn.bind('<Enter>', lambda e: login_btn.config(bg='#2980b9'))
        login_btn.bind('<Leave>', lambda e: login_btn.config(bg='#3498db'))
        
        # Divider
        divider = tk.Frame(form_frame, bg='#2c3e50', height=1)
        divider.pack(fill='x', padx=40, pady=20)
        
        # Info section
        info_frame = tk.Frame(form_frame, bg='#16213e')
        info_frame.pack(pady=(10, 20))
        
        info_title = tk.Label(
            info_frame,
            text="Default Test Accounts",
            font=('Segoe UI', 9, 'bold'),
            bg='#16213e',
            fg='#7f8c8d'
        )
        info_title.pack()
        
        admin_info = tk.Label(
            info_frame,
            text="Admin: admin / admin123",
            font=('Segoe UI', 9),
            bg='#16213e',
            fg='#95a5a6'
        )
        admin_info.pack(pady=(5, 2))
        
        doctor_info = tk.Label(
            info_frame,
            text="Doctor: doctor / doctor123",
            font=('Segoe UI', 9),
            bg='#16213e',
            fg='#95a5a6'
        )
        doctor_info.pack(pady=(2, 0))
        
        # Footer
        footer_label = tk.Label(
            main_frame,
            text="© 2025 Hospital Management System | Secure Login",
            font=('Segoe UI', 8),
            bg='#1a1a2e',
            fg='#4a5568'
        )
        footer_label.pack(side='bottom', pady=15)
    
    def login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        try:
            # Attempt authentication
            user = self.auth_service.login(username, password)
            
            # Success
            messagebox.showinfo("Success", f"Welcome, {user.full_name}!")
            self.window.destroy()
            self.on_success_callback(user)
            
        except AuthenticationException as e:
            messagebox.showerror("Login Failed", str(e))
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def run(self):
        """Start the login window"""
        self.window.mainloop()

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
        self.window.geometry("500x400")
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
        self.window.configure(bg='#f0f0f0')
    
    def _create_widgets(self):
        """Create UI widgets"""
        # Main frame
        main_frame = tk.Frame(self.window, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Hospital Management System",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Staff Login",
            font=('Arial', 14),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Login form frame
        form_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        form_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Username
        username_label = tk.Label(
            form_frame,
            text="Username:",
            font=('Arial', 11),
            bg='white',
            fg='#2c3e50'
        )
        username_label.pack(pady=(30, 5), anchor='w', padx=30)
        
        self.username_entry = tk.Entry(
            form_frame,
            font=('Arial', 11),
            width=30,
            relief='solid',
            bd=1
        )
        self.username_entry.pack(pady=(0, 15), padx=30)
        self.username_entry.focus()
        
        # Password
        password_label = tk.Label(
            form_frame,
            text="Password:",
            font=('Arial', 11),
            bg='white',
            fg='#2c3e50'
        )
        password_label.pack(pady=(10, 5), anchor='w', padx=30)
        
        self.password_entry = tk.Entry(
            form_frame,
            font=('Arial', 11),
            width=30,
            show='●',
            relief='solid',
            bd=1
        )
        self.password_entry.pack(pady=(0, 20), padx=30)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        # Login button
        login_btn = tk.Button(
            form_frame,
            text="Login",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            width=20,
            height=2,
            cursor='hand2',
            relief='flat',
            command=self.login
        )
        login_btn.pack(pady=(10, 20))
        
        # Info label
        info_label = tk.Label(
            main_frame,
            text="Default credentials: admin / admin123 or doctor / doctor123",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#95a5a6'
        )
        info_label.pack(pady=(10, 0))
    
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

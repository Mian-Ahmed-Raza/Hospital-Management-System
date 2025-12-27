"""
Billing Window - Invoice and payment management
Handles billing, invoice generation, and payment tracking
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
from app.services.billing_engine import BillingEngine, Invoice, BillingException
from app.utils.db_connector import DatabaseConnector


class BillingWindow:
    """Billing and invoice management window"""
    
    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize billing window
        
        Args:
            db_connector: Database connector instance
        """
        self.db = db_connector
        self.billing_engine = BillingEngine(db_connector)
        self.current_invoice = None
        
        self.window = tk.Toplevel()
        self.window.title("Billing & Invoice Management")
        self.window.geometry("1200x700")
        self.window.resizable(False, False)
        
        # Center window
        self._center_window()
        
        # Create UI
        self._create_widgets()
        
        # Load data
        self._load_invoices()
    
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
        
        # Header
        header_frame = tk.Frame(self.window, bg='#16213e', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="💰 Billing & Invoice Management",
            font=('Segoe UI', 18, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        title_label.pack(side='left', padx=25, pady=20)
        
        # Close button
        close_btn = tk.Button(
            header_frame,
            text="✖ Close",
            font=('Segoe UI', 10, 'bold'),
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
        
        # Left panel - Invoice list
        left_panel = tk.Frame(content_frame, bg='#16213e', width=400)
        left_panel.pack(side='left', fill='both', expand=False, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self._create_invoice_list(left_panel)
        
        # Right panel - Invoice creation/details
        right_panel = tk.Frame(content_frame, bg='#16213e')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self._create_invoice_form(right_panel)
    
    def _create_invoice_list(self, parent):
        """Create invoice list panel"""
        # Header
        list_header = tk.Frame(parent, bg='#16213e')
        list_header.pack(fill='x', padx=15, pady=(15, 10))
        
        tk.Label(
            list_header,
            text="Invoice List",
            font=('Segoe UI', 14, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        ).pack(side='left')
        
        # New invoice button
        new_btn = tk.Button(
            list_header,
            text="+ New",
            font=('Segoe UI', 9, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            cursor='hand2',
            relief='flat',
            command=self.create_new_invoice
        )
        new_btn.pack(side='right')
        
        # Search frame
        search_frame = tk.Frame(parent, bg='#16213e')
        search_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="🔍",
            font=('Segoe UI', 12),
            bg='#16213e',
            fg='#7f8c8d'
        ).pack(side='left', padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self._filter_invoices())
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=0
        )
        search_entry.pack(side='left', fill='x', expand=True, ipady=5)
        
        # Treeview for invoices
        tree_frame = tk.Frame(parent, bg='#1a1a2e')
        tree_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        self.invoice_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Patient', 'Amount', 'Status'),
            show='headings',
            height=15,
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.invoice_tree.yview)
        
        # Configure columns
        self.invoice_tree.heading('ID', text='Invoice ID')
        self.invoice_tree.heading('Patient', text='Patient')
        self.invoice_tree.heading('Amount', text='Amount')
        self.invoice_tree.heading('Status', text='Status')
        
        self.invoice_tree.column('ID', width=80)
        self.invoice_tree.column('Patient', width=150)
        self.invoice_tree.column('Amount', width=80)
        self.invoice_tree.column('Status', width=70)
        
        self.invoice_tree.pack(fill='both', expand=True)
        
        # Bind selection event
        self.invoice_tree.bind('<<TreeviewSelect>>', self._on_invoice_select)
        
        # Configure treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview',
                       background='#1a1a2e',
                       foreground='#ffffff',
                       fieldbackground='#1a1a2e',
                       borderwidth=0)
        style.map('Treeview', background=[('selected', '#3498db')])
        style.configure('Treeview.Heading',
                       background='#16213e',
                       foreground='#ffffff',
                       borderwidth=0)
    
    def _create_invoice_form(self, parent):
        """Create invoice creation/details form"""
        # Notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Create Invoice Tab
        create_tab = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(create_tab, text='Create Invoice')
        self._create_invoice_creation_form(create_tab)
        
        # Invoice Details Tab
        details_tab = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(details_tab, text='Invoice Details')
        self._create_invoice_details_view(details_tab)
        
        # Configure notebook style
        style = ttk.Style()
        style.configure('TNotebook', background='#16213e', borderwidth=0)
        style.configure('TNotebook.Tab',
                       background='#16213e',
                       foreground='#ffffff',
                       padding=[20, 10])
        style.map('TNotebook.Tab',
                 background=[('selected', '#3498db')],
                 foreground=[('selected', '#ffffff')])
    
    def _create_invoice_creation_form(self, parent):
        """Create form for new invoice"""
        # Scrollable canvas
        canvas = tk.Canvas(parent, bg='#1a1a2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Patient Selection Section
        section1 = tk.LabelFrame(
            scrollable_frame,
            text="Patient Information",
            font=('Segoe UI', 11, 'bold'),
            bg='#16213e',
            fg='#ffffff',
            relief='flat'
        )
        section1.pack(fill='x', padx=20, pady=(20, 10))
        
        # Patient ID
        tk.Label(
            section1,
            text="Patient ID:",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#ffffff'
        ).grid(row=0, column=0, sticky='w', padx=15, pady=10)
        
        self.patient_id_var = tk.StringVar()
        patient_id_entry = tk.Entry(
            section1,
            textvariable=self.patient_id_var,
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            width=30
        )
        patient_id_entry.grid(row=0, column=1, padx=15, pady=10, sticky='ew')
        
        search_patient_btn = tk.Button(
            section1,
            text="Search",
            font=('Segoe UI', 9),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            cursor='hand2',
            relief='flat',
            command=self.search_patient
        )
        search_patient_btn.grid(row=0, column=2, padx=15, pady=10)
        
        # Patient Name (readonly)
        tk.Label(
            section1,
            text="Patient Name:",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#ffffff'
        ).grid(row=1, column=0, sticky='w', padx=15, pady=10)
        
        self.patient_name_var = tk.StringVar()
        patient_name_entry = tk.Entry(
            section1,
            textvariable=self.patient_name_var,
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#7f8c8d',
            state='readonly',
            width=30
        )
        patient_name_entry.grid(row=1, column=1, columnspan=2, padx=15, pady=10, sticky='ew')
        
        section1.columnconfigure(1, weight=1)
        
        # Services Section
        section2 = tk.LabelFrame(
            scrollable_frame,
            text="Services & Items",
            font=('Segoe UI', 11, 'bold'),
            bg='#16213e',
            fg='#ffffff',
            relief='flat'
        )
        section2.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Service selection
        service_frame = tk.Frame(section2, bg='#16213e')
        service_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            service_frame,
            text="Service:",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#ffffff'
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.service_var = tk.StringVar()
        service_combo = ttk.Combobox(
            service_frame,
            textvariable=self.service_var,
            font=('Segoe UI', 10),
            state='readonly',
            width=28
        )
        service_combo['values'] = self._get_service_list()
        service_combo.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(
            service_frame,
            text="Qty:",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#ffffff'
        ).grid(row=0, column=2, padx=(20, 5), pady=5)
        
        self.quantity_var = tk.StringVar(value="1")
        qty_entry = tk.Entry(
            service_frame,
            textvariable=self.quantity_var,
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            width=5
        )
        qty_entry.grid(row=0, column=3, padx=5, pady=5)
        
        add_service_btn = tk.Button(
            service_frame,
            text="+ Add",
            font=('Segoe UI', 9, 'bold'),
            bg='#2ecc71',
            fg='white',
            activebackground='#27ae60',
            cursor='hand2',
            relief='flat',
            command=self.add_service_to_invoice
        )
        add_service_btn.grid(row=0, column=4, padx=10, pady=5)
        
        # Services list
        self.services_text = tk.Text(
            section2,
            height=8,
            font=('Courier New', 9),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            wrap='word'
        )
        self.services_text.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        # Billing details
        section3 = tk.LabelFrame(
            scrollable_frame,
            text="Billing Details",
            font=('Segoe UI', 11, 'bold'),
            bg='#16213e',
            fg='#ffffff',
            relief='flat'
        )
        section3.pack(fill='x', padx=20, pady=10)
        
        details_frame = tk.Frame(section3, bg='#16213e')
        details_frame.pack(fill='x', padx=15, pady=10)
        
        # Discount
        tk.Label(
            details_frame,
            text="Discount (%):",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#ffffff'
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.discount_var = tk.StringVar(value="0")
        discount_entry = tk.Entry(
            details_frame,
            textvariable=self.discount_var,
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            width=10
        )
        discount_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        # Tax
        tk.Label(
            details_frame,
            text="Tax (%):",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#ffffff'
        ).grid(row=0, column=2, sticky='w', padx=(30, 0), pady=5)
        
        self.tax_var = tk.StringVar(value="0")
        tax_entry = tk.Entry(
            details_frame,
            textvariable=self.tax_var,
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            width=10
        )
        tax_entry.grid(row=0, column=3, padx=10, pady=5, sticky='w')
        
        # Payment method
        tk.Label(
            details_frame,
            text="Payment Method:",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#ffffff'
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        self.payment_method_var = tk.StringVar(value="Cash")
        payment_combo = ttk.Combobox(
            details_frame,
            textvariable=self.payment_method_var,
            font=('Segoe UI', 10),
            state='readonly',
            width=18
        )
        payment_combo['values'] = ['Cash', 'Card', 'Insurance', 'Online Payment', 'Cheque']
        payment_combo.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky='w')
        
        # Total section
        total_frame = tk.Frame(section3, bg='#3498db')
        total_frame.pack(fill='x', padx=15, pady=(10, 15))
        
        tk.Label(
            total_frame,
            text="Total Amount:",
            font=('Segoe UI', 14, 'bold'),
            bg='#3498db',
            fg='#ffffff'
        ).pack(side='left', padx=15, pady=10)
        
        self.total_amount_var = tk.StringVar(value="₹ 0.00")
        tk.Label(
            total_frame,
            textvariable=self.total_amount_var,
            font=('Segoe UI', 18, 'bold'),
            bg='#3498db',
            fg='#ffffff'
        ).pack(side='right', padx=15, pady=10)
        
        # Action buttons
        button_frame = tk.Frame(scrollable_frame, bg='#1a1a2e')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        calculate_btn = tk.Button(
            button_frame,
            text="Calculate Total",
            font=('Segoe UI', 10, 'bold'),
            bg='#9b59b6',
            fg='white',
            activebackground='#8e44ad',
            cursor='hand2',
            relief='flat',
            width=15,
            command=self.calculate_total
        )
        calculate_btn.pack(side='left', padx=5)
        
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Invoice",
            font=('Segoe UI', 10, 'bold'),
            bg='#2ecc71',
            fg='white',
            activebackground='#27ae60',
            cursor='hand2',
            relief='flat',
            width=15,
            command=self.save_invoice
        )
        save_btn.pack(side='left', padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear Form",
            font=('Segoe UI', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            cursor='hand2',
            relief='flat',
            width=15,
            command=self.clear_form
        )
        clear_btn.pack(side='left', padx=5)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def _create_invoice_details_view(self, parent):
        """Create invoice details view"""
        # Details display
        details_frame = tk.Frame(parent, bg='#1a1a2e')
        details_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Invoice header
        header_frame = tk.Frame(details_frame, bg='#16213e')
        header_frame.pack(fill='x', pady=(0, 15))
        
        self.detail_invoice_id = tk.Label(
            header_frame,
            text="Invoice #: -",
            font=('Segoe UI', 14, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        self.detail_invoice_id.pack(side='left', padx=15, pady=15)
        
        self.detail_status = tk.Label(
            header_frame,
            text="Status: -",
            font=('Segoe UI', 11),
            bg='#16213e',
            fg='#7f8c8d'
        )
        self.detail_status.pack(side='right', padx=15, pady=15)
        
        # Invoice details text
        self.details_text = tk.Text(
            details_frame,
            font=('Courier New', 10),
            bg='#16213e',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            wrap='word',
            state='disabled'
        )
        self.details_text.pack(fill='both', expand=True)
        
        # Action buttons
        action_frame = tk.Frame(details_frame, bg='#1a1a2e')
        action_frame.pack(fill='x', pady=(15, 0))
        
        mark_paid_btn = tk.Button(
            action_frame,
            text="✓ Mark as Paid",
            font=('Segoe UI', 10, 'bold'),
            bg='#2ecc71',
            fg='white',
            activebackground='#27ae60',
            cursor='hand2',
            relief='flat',
            width=15,
            command=self.mark_invoice_paid
        )
        mark_paid_btn.pack(side='left', padx=5)
        
        print_btn = tk.Button(
            action_frame,
            text="🖨 Print",
            font=('Segoe UI', 10, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            cursor='hand2',
            relief='flat',
            width=15,
            command=self.print_invoice
        )
        print_btn.pack(side='left', padx=5)
    
    def _get_service_list(self):
        """Get list of available services"""
        services = self.billing_engine.SERVICES
        return [f"{code} - {data['name']} (₹{data['price']})" 
                for code, data in services.items()]
    
    def search_patient(self):
        """Search for patient by ID"""
        patient_id = self.patient_id_var.get().strip()
        if not patient_id:
            self.window.lift()
            self.window.focus_force()
            messagebox.showwarning("Input Required", "Please enter a Patient ID", parent=self.window)
            return
        
        try:
            patients = self.db.read('patients', {'patient_id': patient_id})
            if patients:
                patient = patients[0]
                name = f"{patient['first_name']} {patient['last_name']}"
                self.patient_name_var.set(name)
                self.window.lift()
                self.window.focus_force()
                messagebox.showinfo("Success", f"Patient found: {name}", parent=self.window)
            else:
                self.patient_name_var.set("")
                self.window.lift()
                self.window.focus_force()
                messagebox.showwarning("Not Found", f"No patient found with ID: {patient_id}", parent=self.window)
        except Exception as e:
            self.window.lift()
            self.window.focus_force()
            messagebox.showerror("Error", f"Failed to search patient: {str(e)}", parent=self.window)
    
    def create_new_invoice(self):
        """Create a new invoice"""
        self.clear_form()
        self.notebook.select(0)  # Switch to create tab
    
    def add_service_to_invoice(self):
        """Add service to current invoice"""
        if not self.patient_id_var.get():
            self.window.lift()
            self.window.focus_force()
            messagebox.showwarning("Patient Required", "Please select a patient first", parent=self.window)
            return
        
        if not self.service_var.get():
            self.window.lift()
            self.window.focus_force()
            messagebox.showwarning("Service Required", "Please select a service", parent=self.window)
            return
        
        try:
            # Parse service code
            service_code = self.service_var.get().split(' - ')[0]
            quantity = int(self.quantity_var.get())
            
            service_info = self.billing_engine.get_service_price(service_code)
            if not service_info:
                self.window.lift()
                self.window.focus_force()
                messagebox.showerror("Error", "Invalid service selected", parent=self.window)
                return
            
            # Create invoice if not exists
            if not self.current_invoice:
                self.current_invoice = self.billing_engine.create_invoice(
                    self.patient_id_var.get(),
                    self.patient_name_var.get()
                )
            
            # Add item
            self.current_invoice.add_item(
                service_info['name'],
                quantity,
                service_info['price']
            )
            
            # Update display
            self._update_services_display()
            
            # Clear service selection
            self.service_var.set('')
            self.quantity_var.set('1')
            
        except ValueError:
            self.window.lift()
            self.window.focus_force()
            messagebox.showerror("Error", "Invalid quantity", parent=self.window)
        except Exception as e:
            self.window.lift()
            self.window.focus_force()
            messagebox.showerror("Error", f"Failed to add service: {str(e)}", parent=self.window)
    
    def _update_services_display(self):
        """Update services display"""
        if not self.current_invoice:
            return
        
        self.services_text.delete('1.0', tk.END)
        
        text = "SERVICES\n"
        text += "-" * 60 + "\n"
        text += f"{'Description':<30} {'Qty':>5} {'Price':>10} {'Total':>10}\n"
        text += "-" * 60 + "\n"
        
        for item in self.current_invoice.items:
            text += f"{item.description:<30} {item.quantity:>5} "
            text += f"₹{item.unit_price:>8.2f} ₹{item.total:>8.2f}\n"
        
        text += "-" * 60 + "\n"
        text += f"{'Subtotal:':<48} ₹{self.current_invoice.subtotal:>9.2f}\n"
        
        self.services_text.insert('1.0', text)
    
    def calculate_total(self):
        """Calculate invoice total"""
        if not self.current_invoice or not self.current_invoice.items:
            self.window.lift()
            self.window.focus_force()
            messagebox.showwarning("No Items", "Please add services to the invoice", parent=self.window)
            return
        
        try:
            # Set discount and tax
            self.current_invoice.discount_percent = float(self.discount_var.get() or 0)
            self.current_invoice.tax_percent = float(self.tax_var.get() or 0)
            
            # Update display
            self._update_services_display()
            
            # Show calculation
            calc_text = f"\nDiscount ({self.current_invoice.discount_percent}%):"
            calc_text += f"{' ' * 30} -₹{self.current_invoice.discount_amount:>8.2f}\n"
            calc_text += f"Tax ({self.current_invoice.tax_percent}%):"
            calc_text += f"{' ' * 35} ₹{self.current_invoice.tax_amount:>8.2f}\n"
            calc_text += "=" * 60 + "\n"
            calc_text += f"{'TOTAL AMOUNT:':<48} ₹{self.current_invoice.total:>9.2f}\n"
            
            self.services_text.insert(tk.END, calc_text)
            
            # Update total label
            self.total_amount_var.set(f"₹ {self.current_invoice.total:.2f}")
            
        except ValueError:
            self.window.lift()
            self.window.focus_force()
            messagebox.showerror("Error", "Invalid discount or tax value", parent=self.window)
    
    def save_invoice(self):
        """Save invoice to database"""
        if not self.current_invoice or not self.current_invoice.items:
            self.window.lift()
            self.window.focus_force()
            messagebox.showwarning("No Items", "Please add services to the invoice", parent=self.window)
            return
        
        try:
            # Calculate final total
            self.calculate_total()
            
            # Prepare billing data
            bill_data = {
                'bill_id': self.current_invoice.invoice_id,
                'patient_id': self.current_invoice.patient_id,
                'patient_name': self.current_invoice.patient_name,
                'appointment_id': None,
                'bill_date': datetime.now().strftime("%Y-%m-%d"),
                'services': json.dumps([item.to_dict() for item in self.current_invoice.items]),
                'total_amount': str(self.current_invoice.total),
                'payment_status': 'pending',
                'payment_method': self.payment_method_var.get()
            }
            
            # Save to database
            self.db.create('billing', bill_data)
            
            # Ensure window stays on top
            self.window.lift()
            self.window.focus_force()
            
            messagebox.showinfo("Success", 
                              f"Invoice {self.current_invoice.invoice_id} saved successfully!",
                              parent=self.window)
            
            # Reload list and clear form
            self._load_invoices()
            self.clear_form()
            
        except Exception as e:
            self.window.lift()
            self.window.focus_force()
            messagebox.showerror("Error", f"Failed to save invoice: {str(e)}", parent=self.window)
    
    def clear_form(self):
        """Clear invoice form"""
        self.patient_id_var.set('')
        self.patient_name_var.set('')
        self.service_var.set('')
        self.quantity_var.set('1')
        self.discount_var.set('0')
        self.tax_var.set('0')
        self.payment_method_var.set('Cash')
        self.total_amount_var.set('₹ 0.00')
        self.services_text.delete('1.0', tk.END)
        self.current_invoice = None
    
    def _load_invoices(self):
        """Load all invoices"""
        try:
            # Clear existing items
            for item in self.invoice_tree.get_children():
                self.invoice_tree.delete(item)
            
            # Load from database
            invoices = self.db.read('billing')
            
            # Sort by date (newest first)
            invoices.sort(key=lambda x: x.get('bill_date', ''), reverse=True)
            
            # Add to tree
            for invoice in invoices:
                status = invoice.get('payment_status', 'pending').upper()
                amount = float(invoice.get('total_amount', 0))
                
                self.invoice_tree.insert('', 'end', values=(
                    invoice.get('bill_id', ''),
                    invoice.get('patient_name', ''),
                    f"₹{amount:.2f}",
                    status
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load invoices: {str(e)}")
    
    def _filter_invoices(self):
        """Filter invoices based on search"""
        search_term = self.search_var.get().lower()
        
        # Clear tree
        for item in self.invoice_tree.get_children():
            self.invoice_tree.delete(item)
        
        # Load and filter
        try:
            invoices = self.db.read('billing')
            
            for invoice in invoices:
                # Check if matches search
                if (search_term in invoice.get('bill_id', '').lower() or
                    search_term in invoice.get('patient_name', '').lower()):
                    
                    status = invoice.get('payment_status', 'pending').upper()
                    amount = float(invoice.get('total_amount', 0))
                    
                    self.invoice_tree.insert('', 'end', values=(
                        invoice.get('bill_id', ''),
                        invoice.get('patient_name', ''),
                        f"₹{amount:.2f}",
                        status
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter invoices: {str(e)}")
    
    def _on_invoice_select(self, event):
        """Handle invoice selection"""
        selection = self.invoice_tree.selection()
        if not selection:
            return
        
        # Get selected invoice
        item = self.invoice_tree.item(selection[0])
        invoice_id = item['values'][0]
        
        # Load invoice details
        try:
            invoices = self.db.read('billing', {'bill_id': invoice_id})
            if invoices:
                self._display_invoice_details(invoices[0])
                self.notebook.select(1)  # Switch to details tab
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load invoice: {str(e)}")
    
    def _display_invoice_details(self, invoice_data):
        """Display invoice details"""
        # Update header
        self.detail_invoice_id.config(text=f"Invoice #: {invoice_data['bill_id']}")
        
        status = invoice_data.get('payment_status', 'pending').upper()
        status_color = '#2ecc71' if status == 'PAID' else '#e67e22'
        self.detail_status.config(text=f"Status: {status}", fg=status_color)
        
        # Parse services
        try:
            services = json.loads(invoice_data.get('services', '[]'))
        except:
            services = []
        
        # Build details text
        details = "=" * 70 + "\n"
        details += "                     INVOICE DETAILS\n"
        details += "=" * 70 + "\n\n"
        
        details += f"Invoice ID:        {invoice_data['bill_id']}\n"
        details += f"Date:              {invoice_data.get('bill_date', 'N/A')}\n"
        details += f"Patient ID:        {invoice_data.get('patient_id', 'N/A')}\n"
        details += f"Patient Name:      {invoice_data.get('patient_name', 'N/A')}\n"
        details += f"Payment Method:    {invoice_data.get('payment_method', 'N/A')}\n"
        details += f"Status:            {status}\n\n"
        
        details += "=" * 70 + "\n"
        details += "SERVICES\n"
        details += "=" * 70 + "\n"
        details += f"{'Description':<35} {'Qty':>5} {'Price':>12} {'Total':>12}\n"
        details += "-" * 70 + "\n"
        
        subtotal = 0
        for service in services:
            desc = service.get('description', 'N/A')
            qty = service.get('quantity', 0)
            price = service.get('unit_price', 0)
            total = service.get('total', 0)
            subtotal += total
            
            details += f"{desc:<35} {qty:>5} ₹{price:>10.2f} ₹{total:>10.2f}\n"
        
        details += "-" * 70 + "\n"
        details += f"{'Subtotal:':<56} ₹{subtotal:>11.2f}\n"
        
        total_amount = float(invoice_data.get('total_amount', 0))
        details += "=" * 70 + "\n"
        details += f"{'TOTAL AMOUNT:':<56} ₹{total_amount:>11.2f}\n"
        details += "=" * 70 + "\n"
        
        # Update text widget
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert('1.0', details)
        self.details_text.config(state='disabled')
        
        # Store current invoice ID
        self.selected_invoice_id = invoice_data['bill_id']
    
    def mark_invoice_paid(self):
        """Mark selected invoice as paid"""
        if not hasattr(self, 'selected_invoice_id'):
            messagebox.showwarning("No Selection", "Please select an invoice first")
            return
        
        if messagebox.askyesno("Confirm", "Mark this invoice as paid?"):
            try:
                self.db.update('billing', self.selected_invoice_id, 'bill_id', 
                             {'payment_status': 'paid'})
                messagebox.showinfo("Success", "Invoice marked as paid")
                self._load_invoices()
                
                # Reload details
                invoices = self.db.read('billing', {'bill_id': self.selected_invoice_id})
                if invoices:
                    self._display_invoice_details(invoices[0])
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update invoice: {str(e)}")
    
    def print_invoice(self):
        """Print invoice"""
        if not hasattr(self, 'selected_invoice_id'):
            messagebox.showwarning("No Selection", "Please select an invoice first")
            return
        
        messagebox.showinfo("Print", "Print functionality - Coming soon!\n\n"
                          "In production, this would:\n"
                          "- Generate PDF invoice\n"
                          "- Send to printer\n"
                          "- Email to patient")

    def run(self):
        """Start the billing window"""
        self.window.mainloop()

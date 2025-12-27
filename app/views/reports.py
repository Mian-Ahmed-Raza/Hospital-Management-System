"""
Reports Window - Generate and view various reports
Displays patient, appointment, financial, and statistical reports
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from app.services.report_generator import ReportGenerator


class ReportsWindow:
    """Reports generation and viewing window"""
    
    def __init__(self, db_connector):
        """
        Initialize reports window
        
        Args:
            db_connector: Database connector instance
        """
        self.db = db_connector
        self.report_generator = ReportGenerator(db_connector)
        self.current_report = None
        
        self.window = tk.Toplevel()
        self.window.title("Reports & Analytics")
        self.window.geometry("1400x800")
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
            text="📊",
            font=('Segoe UI Emoji', 24),
            bg='#16213e',
            fg='#3498db'
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        title_label = tk.Label(
            header_content,
            text="Reports & Analytics",
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
        
        # Left panel - Report options
        left_panel = tk.Frame(content_frame, bg='#16213e', width=350)
        left_panel.pack(side='left', fill='both', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self._create_report_options(left_panel)
        
        # Right panel - Report display
        right_panel = tk.Frame(content_frame, bg='#16213e')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self._create_report_display(right_panel)
    
    def _create_report_options(self, parent):
        """Create report options panel"""
        # Header
        options_header = tk.Label(
            parent,
            text="📋 Report Types",
            font=('Segoe UI', 14, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        options_header.pack(pady=(20, 20), padx=20)
        
        # Date range selection
        date_frame = tk.Frame(parent, bg='#16213e')
        date_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(
            date_frame,
            text="Date Range:",
            font=('Segoe UI', 11, 'bold'),
            bg='#16213e',
            fg='#3498db'
        ).pack(anchor='w', pady=(0, 10))
        
        # Start date
        tk.Label(
            date_frame,
            text="From:",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#7f8c8d'
        ).pack(anchor='w', pady=(5, 2))
        
        self.start_date_var = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        start_date_entry = tk.Entry(
            date_frame,
            textvariable=self.start_date_var,
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=0
        )
        start_date_entry.pack(fill='x', ipady=8, pady=(0, 10))
        
        # End date
        tk.Label(
            date_frame,
            text="To:",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#7f8c8d'
        ).pack(anchor='w', pady=(5, 2))
        
        self.end_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        end_date_entry = tk.Entry(
            date_frame,
            textvariable=self.end_date_var,
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=0
        )
        end_date_entry.pack(fill='x', ipady=8)
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=20, pady=20)
        
        # Report buttons
        reports = [
            ("📊 Patient Summary", self.generate_patient_report, '#3498db'),
            ("📅 Appointment Report", self.generate_appointment_report, '#9b59b6'),
            ("💰 Financial Report", self.generate_financial_report, '#2ecc71'),
            ("🏥 Department Report", self.generate_department_report, '#e67e22'),
        ]
        
        for text, command, color in reports:
            btn = tk.Button(
                parent,
                text=text,
                font=('Segoe UI', 11, 'bold'),
                bg=color,
                fg='white',
                activebackground=self._darken_color(color),
                cursor='hand2',
                relief='flat',
                command=command
            )
            btn.pack(fill='x', padx=20, pady=5, ipady=12)
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=20, pady=20)
        
        # Export button
        export_btn = tk.Button(
            parent,
            text="📥 Export Report",
            font=('Segoe UI', 10, 'bold'),
            bg='#34495e',
            fg='white',
            activebackground='#2c3e50',
            cursor='hand2',
            relief='flat',
            command=self.export_report
        )
        export_btn.pack(fill='x', padx=20, pady=5, ipady=10)
    
    def _create_report_display(self, parent):
        """Create report display panel"""
        # Header with report title
        display_header = tk.Frame(parent, bg='#16213e')
        display_header.pack(fill='x', padx=20, pady=(20, 10))
        
        self.report_title = tk.Label(
            display_header,
            text="Select a report type to generate",
            font=('Segoe UI', 14, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        self.report_title.pack(side='left')
        
        self.report_timestamp = tk.Label(
            display_header,
            text="",
            font=('Segoe UI', 10),
            bg='#16213e',
            fg='#7f8c8d'
        )
        self.report_timestamp.pack(side='right')
        
        # Canvas with scrollbar for report content
        canvas_container = tk.Frame(parent, bg='#16213e')
        canvas_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        canvas = tk.Canvas(canvas_container, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient='vertical', command=canvas.yview)
        
        self.report_frame = tk.Frame(canvas, bg='#16213e')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas_window = canvas.create_window((0, 0), window=self.report_frame, anchor='nw')
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        self.report_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', configure_scroll_region)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Welcome message
        welcome_label = tk.Label(
            self.report_frame,
            text="📊 Welcome to Reports & Analytics\n\n"
                 "Select a report type from the left panel to get started.\n\n"
                 "Available Reports:\n"
                 "• Patient Summary - Demographics and statistics\n"
                 "• Appointment Report - Scheduling analytics\n"
                 "• Financial Report - Revenue and billing insights\n"
                 "• Department Report - Department-wise performance",
            font=('Segoe UI', 11),
            bg='#16213e',
            fg='#7f8c8d',
            justify='left'
        )
        welcome_label.pack(pady=50, padx=30)
    
    def generate_patient_report(self):
        """Generate patient summary report"""
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        
        self.current_report = self.report_generator.generate_patient_summary_report(start_date, end_date)
        self._display_patient_report()
    
    def generate_appointment_report(self):
        """Generate appointment report"""
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        
        self.current_report = self.report_generator.generate_appointment_report(start_date, end_date)
        self._display_appointment_report()
    
    def generate_financial_report(self):
        """Generate financial report"""
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        
        self.current_report = self.report_generator.generate_financial_report(start_date, end_date)
        self._display_financial_report()
    
    def generate_department_report(self):
        """Generate department report"""
        self.current_report = self.report_generator.generate_department_report()
        self._display_department_report()
    
    def _display_patient_report(self):
        """Display patient summary report"""
        # Clear existing content
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        report = self.current_report
        
        # Update header
        self.report_title.config(text=report['report_type'])
        self.report_timestamp.config(text=f"Generated: {report['generated_at']}")
        
        if 'error' in report:
            tk.Label(
                self.report_frame,
                text=f"❌ Error generating report: {report['error']}",
                font=('Segoe UI', 11),
                bg='#16213e',
                fg='#e74c3c'
            ).pack(pady=20)
            return
        
        # Summary statistics
        stats_frame = tk.Frame(self.report_frame, bg='#1a1a2e')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        self._create_stat_card(stats_frame, "Total Patients", report['total_patients'], '#3498db', 0)
        
        # Gender distribution
        gender_frame = tk.LabelFrame(
            self.report_frame,
            text="👥 Gender Distribution",
            font=('Segoe UI', 12, 'bold'),
            bg='#1a1a2e',
            fg='#3498db',
            relief='flat'
        )
        gender_frame.pack(fill='x', padx=20, pady=10)
        
        for gender, count in report['gender_distribution'].items():
            self._create_progress_bar(gender_frame, gender, count, report['total_patients'])
        
        # Blood group distribution
        blood_frame = tk.LabelFrame(
            self.report_frame,
            text="🩸 Blood Group Distribution",
            font=('Segoe UI', 12, 'bold'),
            bg='#1a1a2e',
            fg='#e74c3c',
            relief='flat'
        )
        blood_frame.pack(fill='x', padx=20, pady=10)
        
        for blood_group, count in report['blood_group_distribution'].items():
            self._create_progress_bar(blood_frame, blood_group, count, report['total_patients'])
        
        # Age distribution
        age_frame = tk.LabelFrame(
            self.report_frame,
            text="📈 Age Distribution",
            font=('Segoe UI', 12, 'bold'),
            bg='#1a1a2e',
            fg='#9b59b6',
            relief='flat'
        )
        age_frame.pack(fill='x', padx=20, pady=10)
        
        for age_range, count in report['age_distribution'].items():
            self._create_progress_bar(age_frame, age_range, count, report['total_patients'])
    
    def _display_appointment_report(self):
        """Display appointment report"""
        # Clear existing content
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        report = self.current_report
        
        # Update header
        self.report_title.config(text=report['report_type'])
        self.report_timestamp.config(text=f"Generated: {report['generated_at']}")
        
        if 'error' in report:
            tk.Label(
                self.report_frame,
                text=f"❌ Error generating report: {report['error']}",
                font=('Segoe UI', 11),
                bg='#16213e',
                fg='#e74c3c'
            ).pack(pady=20)
            return
        
        # Summary statistics
        stats_frame = tk.Frame(self.report_frame, bg='#1a1a2e')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        self._create_stat_card(stats_frame, "Total Appointments", report['total_appointments'], '#9b59b6', 0)
        
        # Status distribution
        status_frame = tk.LabelFrame(
            self.report_frame,
            text="📊 Appointment Status",
            font=('Segoe UI', 12, 'bold'),
            bg='#1a1a2e',
            fg='#9b59b6',
            relief='flat'
        )
        status_frame.pack(fill='x', padx=20, pady=10)
        
        for status, count in report['status_distribution'].items():
            self._create_progress_bar(status_frame, status.title(), count, report['total_appointments'])
        
        # Department distribution
        dept_frame = tk.LabelFrame(
            self.report_frame,
            text="🏥 Department-wise Appointments",
            font=('Segoe UI', 12, 'bold'),
            bg='#1a1a2e',
            fg='#3498db',
            relief='flat'
        )
        dept_frame.pack(fill='x', padx=20, pady=10)
        
        for dept, count in report['department_distribution'].items():
            self._create_progress_bar(dept_frame, dept, count, report['total_appointments'])
    
    def _display_financial_report(self):
        """Display financial report"""
        # Clear existing content
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        report = self.current_report
        
        # Update header
        self.report_title.config(text=report['report_type'])
        self.report_timestamp.config(text=f"Generated: {report['generated_at']}")
        
        if 'error' in report:
            tk.Label(
                self.report_frame,
                text=f"❌ Error generating report: {report['error']}",
                font=('Segoe UI', 11),
                bg='#16213e',
                fg='#e74c3c'
            ).pack(pady=20)
            return
        
        # Summary statistics
        stats_frame = tk.Frame(self.report_frame, bg='#1a1a2e')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        self._create_stat_card(stats_frame, "Total Revenue", f"PKR {report['total_revenue']:.2f}", '#2ecc71', 0)
        self._create_stat_card(stats_frame, "Paid", f"PKR {report['total_paid']:.2f}", '#27ae60', 1)
        self._create_stat_card(stats_frame, "Pending", f"PKR {report['total_pending']:.2f}", '#e67e22', 2)
        self._create_stat_card(stats_frame, "Invoices", report['total_invoices'], '#3498db', 3)
        
        # Payment method distribution
        if report['payment_method_distribution']:
            payment_frame = tk.LabelFrame(
                self.report_frame,
                text="💳 Payment Methods",
                font=('Segoe UI', 12, 'bold'),
                bg='#1a1a2e',
                fg='#2ecc71',
                relief='flat'
            )
            payment_frame.pack(fill='x', padx=20, pady=10)
            
            total_paid = report['total_paid']
            for method, amount in report['payment_method_distribution'].items():
                self._create_progress_bar(payment_frame, f"{method} (PKR {amount:.2f})", amount, total_paid)
        
        # Top services by revenue
        if report['service_revenue']:
            service_frame = tk.LabelFrame(
                self.report_frame,
                text="🏥 Top Services by Revenue",
                font=('Segoe UI', 12, 'bold'),
                bg='#1a1a2e',
                fg='#3498db',
                relief='flat'
            )
            service_frame.pack(fill='x', padx=20, pady=10)
            
            # Sort services by revenue
            sorted_services = sorted(report['service_revenue'].items(), key=lambda x: x[1], reverse=True)[:10]
            total_service_revenue = sum(report['service_revenue'].values())
            
            for service, amount in sorted_services:
                self._create_progress_bar(service_frame, f"{service} (PKR {amount:.2f})", amount, total_service_revenue)
    
    def _display_department_report(self):
        """Display department report"""
        # Clear existing content
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        report = self.current_report
        
        # Update header
        self.report_title.config(text=report['report_type'])
        self.report_timestamp.config(text=f"Generated: {report['generated_at']}")
        
        if 'error' in report:
            tk.Label(
                self.report_frame,
                text=f"❌ Error generating report: {report['error']}",
                font=('Segoe UI', 11),
                bg='#16213e',
                fg='#e74c3c'
            ).pack(pady=20)
            return
        
        # Department cards
        for dept_name, dept_data in report['departments'].items():
            dept_frame = tk.LabelFrame(
                self.report_frame,
                text=f"🏥 {dept_name}",
                font=('Segoe UI', 12, 'bold'),
                bg='#1a1a2e',
                fg='#e67e22',
                relief='flat'
            )
            dept_frame.pack(fill='x', padx=20, pady=10)
            
            # Stats row
            stats_row = tk.Frame(dept_frame, bg='#1a1a2e')
            stats_row.pack(fill='x', padx=10, pady=10)
            
            total = dept_data['total_appointments']
            
            # Create mini stat cards
            stats = [
                ("Total", total, '#3498db'),
                ("Scheduled", dept_data.get('scheduled', 0), '#e67e22'),
                ("Completed", dept_data.get('completed', 0), '#2ecc71'),
                ("Cancelled", dept_data.get('cancelled', 0), '#e74c3c'),
            ]
            
            for i, (label, value, color) in enumerate(stats):
                stat_card = tk.Frame(stats_row, bg=color, relief='flat')
                stat_card.grid(row=0, column=i, padx=5, sticky='ew')
                stats_row.grid_columnconfigure(i, weight=1)
                
                tk.Label(
                    stat_card,
                    text=str(value),
                    font=('Segoe UI', 16, 'bold'),
                    bg=color,
                    fg='white'
                ).pack(pady=(10, 0))
                
                tk.Label(
                    stat_card,
                    text=label,
                    font=('Segoe UI', 9),
                    bg=color,
                    fg='white'
                ).pack(pady=(0, 10))
    
    def _create_stat_card(self, parent, label, value, color, column):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=color, relief='flat')
        card.grid(row=0, column=column, padx=5, pady=5, sticky='ew')
        parent.grid_columnconfigure(column, weight=1)
        
        tk.Label(
            card,
            text=str(value),
            font=('Segoe UI', 20, 'bold'),
            bg=color,
            fg='white'
        ).pack(pady=(15, 5))
        
        tk.Label(
            card,
            text=label,
            font=('Segoe UI', 10),
            bg=color,
            fg='white'
        ).pack(pady=(0, 15))
    
    def _create_progress_bar(self, parent, label, value, total):
        """Create a progress bar with label"""
        if total == 0:
            percentage = 0
        else:
            percentage = (value / total) * 100
        
        row = tk.Frame(parent, bg='#1a1a2e')
        row.pack(fill='x', padx=15, pady=8)
        
        # Label and value
        label_frame = tk.Frame(row, bg='#1a1a2e')
        label_frame.pack(fill='x')
        
        tk.Label(
            label_frame,
            text=label,
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#ffffff'
        ).pack(side='left')
        
        tk.Label(
            label_frame,
            text=f"{value} ({percentage:.1f}%)",
            font=('Segoe UI', 10),
            bg='#1a1a2e',
            fg='#7f8c8d'
        ).pack(side='right')
        
        # Progress bar
        progress_bg = tk.Frame(row, bg='#16213e', height=8)
        progress_bg.pack(fill='x', pady=(5, 0))
        
        progress_fill = tk.Frame(progress_bg, bg='#3498db', height=8)
        progress_fill.place(relwidth=percentage/100, relheight=1)
    
    def export_report(self):
        """Export current report to text file"""
        if not self.current_report:
            messagebox.showwarning("No Report", "Please generate a report first", parent=self.window)
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                f.write(f"{'='*80}\n")
                f.write(f"{self.current_report['report_type'].upper()}\n")
                f.write(f"{'='*80}\n\n")
                f.write(f"Generated: {self.current_report['generated_at']}\n")
                
                if 'period' in self.current_report:
                    f.write(f"Period: {self.current_report['period']}\n")
                
                f.write(f"\n{'-'*80}\n\n")
                
                # Write report data based on type
                for key, value in self.current_report.items():
                    if key not in ['report_type', 'generated_at', 'period', 'patients', 'appointments', 'bills', 'error']:
                        f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                
                f.write(f"\n{'='*80}\n")
            
            messagebox.showinfo("Success", f"Report exported to {filename}", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}", parent=self.window)
    
    def _darken_color(self, hex_color):
        """Darken a hex color by 20%"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * 0.8) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
    
    def run(self):
        """Start the reports window"""
        self.window.mainloop()

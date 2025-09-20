#!/usr/bin/env python3
"""
Unsafe File Scanner - GUI Application
A graphical user interface for the Unsafe File Scanner tool.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import os
import sys
from pathlib import Path
from unsafe_file_scanner import UnsafeFileScanner
import webbrowser


class UnsafeFileScannerGUI:
    """Main GUI application class."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Unsafe File Scanner - Professional Security Tool")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # Configure window icon and styling
        self.root.configure(bg='#f0f0f0')
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Variables
        self.scanner = None
        self.scan_thread = None
        self.is_scanning = False
        self.scan_results = []
        
        # Create GUI elements
        self.create_widgets()
        self.setup_layout()
        
        # Load default configuration
        self.load_default_config()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="15")
        
        # Header section with professional styling
        self.header_frame = ttk.Frame(self.main_frame)
        
        # Title with professional styling
        self.title_label = ttk.Label(
            self.header_frame, 
            text="🔒 Unsafe File Scanner", 
            font=("Segoe UI", 24, "bold"),
            foreground="#2c3e50"
        )
        
        # Subtitle
        self.subtitle_label = ttk.Label(
            self.header_frame,
            text="Professional Security Analysis & File Permission Monitoring",
            font=("Segoe UI", 11),
            foreground="#7f8c8d"
        )
        
        # Status indicator
        self.status_indicator = ttk.Label(
            self.header_frame,
            text="● Ready",
            font=("Segoe UI", 10, "bold"),
            foreground="#27ae60"
        )
        
        # Main content area
        self.content_frame = ttk.Frame(self.main_frame)
        
        # Left panel - Controls
        self.left_panel = ttk.LabelFrame(self.content_frame, text="Scan Configuration", padding="15")
        
        # Directory selection
        self.dir_frame = ttk.Frame(self.left_panel)
        self.dir_label = ttk.Label(self.dir_frame, text="Target Directories:", font=("Segoe UI", 10, "bold"))
        self.dir_entry = ttk.Entry(self.dir_frame, width=50)
        self.dir_browse_btn = ttk.Button(self.dir_frame, text="📁 Browse", command=self.browse_directories)
        self.dir_add_btn = ttk.Button(self.dir_frame, text="➕ Add", command=self.add_directory)
        self.dir_clear_btn = ttk.Button(self.dir_frame, text="🗑️ Clear", command=self.clear_directories)
        
        # Directory listbox
        self.dir_listbox = tk.Listbox(self.dir_frame, height=6, selectmode=tk.MULTIPLE)
        self.dir_listbox.bind('<Double-1>', self.remove_selected_dirs)
        
        # Output file
        self.output_frame = ttk.Frame(self.left_panel)
        self.output_label = ttk.Label(self.output_frame, text="Output File:", font=("Segoe UI", 10, "bold"))
        self.output_file_entry = ttk.Entry(self.output_frame, width=50)
        self.output_file_browse_btn = ttk.Button(self.output_frame, text="💾 Browse", command=self.browse_output_file)
        
        # Scan options
        self.options_frame = ttk.Frame(self.left_panel)
        self.verbose_var = tk.BooleanVar()
        self.verbose_check = ttk.Checkbutton(
            self.options_frame, 
            text="Verbose Output", 
            variable=self.verbose_var
        )
        
        self.log_level_label = ttk.Label(self.options_frame, text="Log Level:")
        self.log_level_combo = ttk.Combobox(
            self.options_frame, 
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            state="readonly",
            width=12
        )
        self.log_level_combo.set("INFO")
        
        # Control buttons with professional styling
        self.control_frame = ttk.Frame(self.left_panel)
        
        # Main control buttons
        self.scan_btn = ttk.Button(
            self.control_frame, 
            text="🚀 Start Security Scan", 
            command=self.start_scan,
            style="Accent.TButton"
        )
        self.stop_btn = ttk.Button(
            self.control_frame, 
            text="⏹️ Stop Scan", 
            command=self.stop_scan,
            state="disabled"
        )
        self.clear_btn = ttk.Button(
            self.control_frame, 
            text="🗑️ Clear Results", 
            command=self.clear_results
        )
        self.export_btn = ttk.Button(
            self.control_frame, 
            text="📊 Export Results", 
            command=self.export_results,
            state="disabled"
        )
        
        # Quick action buttons
        self.quick_scan_btn = ttk.Button(
            self.control_frame,
            text="⚡ Quick Scan",
            command=self.quick_scan
        )
        self.demo_btn = ttk.Button(
            self.control_frame,
            text="🎯 Run Demo",
            command=self.run_demo
        )
        
        # Right panel - Results
        self.right_panel = ttk.LabelFrame(self.content_frame, text="Scan Results", padding="15")
        
        # Results summary with professional styling
        self.summary_frame = ttk.Frame(self.right_panel)
        self.summary_label = ttk.Label(
            self.summary_frame, 
            text="No security scan performed yet", 
            font=("Segoe UI", 12, "bold"),
            foreground="#34495e"
        )
        
        # Security metrics frame
        self.metrics_frame = ttk.Frame(self.right_panel)
        self.files_scanned_label = ttk.Label(self.metrics_frame, text="Files: 0", font=("Segoe UI", 9))
        self.unsafe_files_label = ttk.Label(self.metrics_frame, text="Unsafe: 0", font=("Segoe UI", 9))
        self.scan_time_label = ttk.Label(self.metrics_frame, text="Time: 0.00s", font=("Segoe UI", 9))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.right_panel, 
            mode='indeterminate',
            length=400
        )
        
        # Results tabs
        self.results_notebook = ttk.Notebook(self.right_panel)
        
        # Summary tab
        self.summary_tab = ttk.Frame(self.results_notebook)
        self.summary_text = scrolledtext.ScrolledText(
            self.summary_tab, 
            height=12, 
            wrap=tk.WORD
        )
        
        # Detailed results tab
        self.details_tab = ttk.Frame(self.results_notebook)
        self.details_tree = ttk.Treeview(
            self.details_tab,
            columns=("path", "permissions", "owner", "group", "risk", "issues"),
            show="headings",
            height=12
        )
        
        # Configure treeview columns
        self.details_tree.heading("path", text="File Path")
        self.details_tree.heading("permissions", text="Permissions")
        self.details_tree.heading("owner", text="Owner")
        self.details_tree.heading("group", text="Group")
        self.details_tree.heading("risk", text="Risk Level")
        self.details_tree.heading("issues", text="Issues")
        
        self.details_tree.column("path", width=300)
        self.details_tree.column("permissions", width=100)
        self.details_tree.column("owner", width=80)
        self.details_tree.column("group", width=80)
        self.details_tree.column("risk", width=80)
        self.details_tree.column("issues", width=200)
        
        # Scrollbar for treeview
        self.details_scrollbar = ttk.Scrollbar(
            self.details_tab, 
            orient="vertical", 
            command=self.details_tree.yview
        )
        self.details_tree.configure(yscrollcommand=self.details_scrollbar.set)
        
        # Raw JSON tab
        self.json_tab = ttk.Frame(self.results_notebook)
        self.json_text = scrolledtext.ScrolledText(
            self.json_tab, 
            height=12, 
            wrap=tk.WORD
        )
        
        # Add tabs
        self.results_notebook.add(self.summary_tab, text="Summary")
        self.results_notebook.add(self.details_tab, text="Detailed Results")
        self.results_notebook.add(self.json_tab, text="Raw JSON")
        
        # Status bar
        self.status_bar_frame = ttk.Frame(self.main_frame)
        self.status_label = ttk.Label(
            self.status_bar_frame, 
            text="Ready", 
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Segoe UI", 9)
        )
        
        # Menu bar
        self.create_menu()
    
    def create_menu(self):
        """Create menu bar."""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Export Results", command=self.export_results)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        self.tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Run Test Scan", command=self.run_test_scan)
        self.tools_menu.add_command(label="Run Demo", command=self.run_demo)
        self.tools_menu.add_separator()
        self.tools_menu.add_command(label="Open Log File", command=self.open_log_file)
        
        # Help menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.help_menu.add_command(label="Documentation", command=self.open_documentation)
    
    def setup_layout(self):
        """Setup the layout of widgets."""
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Header section
        self.header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        self.header_frame.columnconfigure(0, weight=1)
        
        # Title and subtitle
        self.title_label.grid(row=0, column=0, sticky=tk.W)
        self.subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.status_indicator.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        
        # Content area
        self.content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=2)
        self.content_frame.rowconfigure(0, weight=1)
        
        # Left panel - Controls
        self.left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        self.left_panel.columnconfigure(0, weight=1)
        
        # Directory selection
        self.dir_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.dir_frame.columnconfigure(1, weight=1)
        
        self.dir_label.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 5))
        self.dir_entry.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 5))
        self.dir_browse_btn.grid(row=2, column=0, padx=(0, 5), pady=(5, 0))
        self.dir_add_btn.grid(row=2, column=1, padx=(0, 5), pady=(5, 0))
        self.dir_clear_btn.grid(row=2, column=2, pady=(5, 0))
        
        self.dir_listbox.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Output file
        self.output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.output_frame.columnconfigure(1, weight=1)
        
        self.output_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        self.output_file_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        self.output_file_browse_btn.grid(row=1, column=2, padx=(5, 0), pady=(0, 5))
        
        # Scan options
        self.options_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.verbose_check.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        self.log_level_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 5))
        self.log_level_combo.grid(row=0, column=2, sticky=tk.W)
        
        # Control buttons
        self.control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.columnconfigure(1, weight=1)
        self.control_frame.columnconfigure(2, weight=1)
        self.control_frame.columnconfigure(3, weight=1)
        
        # Main control buttons
        self.scan_btn.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        self.stop_btn.grid(row=0, column=1, padx=(0, 5), sticky=(tk.W, tk.E))
        self.clear_btn.grid(row=0, column=2, padx=(0, 5), sticky=(tk.W, tk.E))
        self.export_btn.grid(row=0, column=3, sticky=(tk.W, tk.E))
        
        # Quick action buttons
        self.quick_scan_btn.grid(row=1, column=0, columnspan=2, padx=(0, 5), sticky=(tk.W, tk.E), pady=(5, 0))
        self.demo_btn.grid(row=1, column=2, columnspan=2, padx=(5, 0), sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Right panel - Results
        self.right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.right_panel.columnconfigure(0, weight=1)
        self.right_panel.rowconfigure(3, weight=1)
        
        # Results summary
        self.summary_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.summary_label.grid(row=0, column=0, sticky=tk.W)
        
        # Security metrics
        self.metrics_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.files_scanned_label.grid(row=0, column=0, padx=(0, 20))
        self.unsafe_files_label.grid(row=0, column=1, padx=(0, 20))
        self.scan_time_label.grid(row=0, column=2)
        
        # Progress bar
        self.progress_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Results notebook
        self.results_notebook.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Summary tab content
        self.summary_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Details tab content
        self.details_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.details_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # JSON tab content
        self.json_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_bar_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    def load_default_config(self):
        """Load default configuration."""
        self.output_file_entry.insert(0, "scan_results.json")
    
    def browse_directories(self):
        """Browse for directories to scan."""
        directory = filedialog.askdirectory(title="Select Directory to Scan")
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def add_directory(self):
        """Add directory to scan list."""
        directory = self.dir_entry.get().strip()
        if directory and os.path.exists(directory):
            self.dir_listbox.insert(tk.END, directory)
            self.dir_entry.delete(0, tk.END)
        elif directory:
            messagebox.showerror("Error", f"Directory does not exist: {directory}")
    
    def clear_directories(self):
        """Clear all directories from scan list."""
        self.dir_listbox.delete(0, tk.END)
    
    def remove_selected_dirs(self, event):
        """Remove selected directories from list."""
        selected = self.dir_listbox.curselection()
        for index in reversed(selected):
            self.dir_listbox.delete(index)
    
    
    def browse_output_file(self):
        """Browse for output file."""
        filename = filedialog.asksaveasfilename(
            title="Save Scan Results As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_entry.delete(0, tk.END)
            self.output_file_entry.insert(0, filename)
    
    def start_scan(self):
        """Start the scan process."""
        # Get directories to scan
        directories = list(self.dir_listbox.get(0, tk.END))
        if not directories:
            messagebox.showerror("Error", "Please select at least one directory to scan")
            return
        
        # Update UI
        self.is_scanning = True
        self.scan_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.progress_bar.start()
        self.status_indicator.config(text="● Scanning...", foreground="#3498db")
        self.status_label.config(text="Scanning...")
        
        # Reset status indicators
        self.files_scanned_label.config(text="Files: 0")
        self.unsafe_files_label.config(text="Unsafe: 0")
        self.scan_time_label.config(text="Time: 0.00s")
        
        # Clear previous results
        self.clear_results()
        
        # Start scan in separate thread
        self.scan_thread = threading.Thread(target=self.run_scan, args=(directories,))
        self.scan_thread.daemon = True
        self.scan_thread.start()
    
    def run_scan(self, directories):
        """Run the actual scan."""
        try:
            # Create scanner
            self.scanner = UnsafeFileScanner()
            
            # Set output file
            output_file = self.output_file_entry.get().strip()
            if output_file:
                self.scanner.config['output_file'] = output_file
            
            # Set verbose mode
            if self.verbose_var.get():
                self.scanner.config['verbose'] = True
            
            # Set log level
            self.scanner.config['log_level'] = self.log_level_combo.get()
            self.scanner.setup_logging()
            
            # Run scan
            self.scanner.run_scan(directories)
            
            # Update UI with results
            self.root.after(0, self.scan_completed)
            
        except Exception as e:
            self.root.after(0, lambda: self.scan_error(str(e)))
    
    def scan_completed(self):
        """Handle scan completion."""
        self.is_scanning = False
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.progress_bar.stop()
        self.status_indicator.config(text="● Scan Complete", foreground="#27ae60")
        self.status_label.config(text="Scan completed")
        self.export_btn.config(state="normal")
        
        # Update status indicators
        if self.scanner:
            stats = self.scanner.scan_stats
            self.files_scanned_label.config(text=f"Files: {stats['total_files']}")
            self.unsafe_files_label.config(text=f"Unsafe: {stats['unsafe_files']}")
            self.scan_time_label.config(text=f"Time: {stats['scan_duration']:.2f}s")
        
        # Update results
        self.update_results()
        
        messagebox.showinfo("Scan Complete", "Security scan completed successfully!")
    
    def scan_error(self, error_message):
        """Handle scan error."""
        self.is_scanning = False
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.progress_bar.stop()
        self.status_indicator.config(text="● Scan Failed", foreground="#e74c3c")
        self.status_label.config(text="Scan failed")
        
        messagebox.showerror("Scan Error", f"Scan failed: {error_message}")
    
    def stop_scan(self):
        """Stop the current scan."""
        if self.is_scanning:
            self.is_scanning = False
            self.scan_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.progress_bar.stop()
            self.status_indicator.config(text="● Scan Stopped", foreground="#e74c3c")
            self.status_label.config(text="Scan stopped")
    
    def update_results(self):
        """Update the results display."""
        if not self.scanner:
            return
        
        # Update summary
        stats = self.scanner.scan_stats
        summary_text = f"""
Scan Summary:
=============
Total files scanned: {stats['total_files']}
Unsafe files found: {stats['unsafe_files']}
SUID files: {stats['suid_files']}
SGID files: {stats['sgid_files']}
World-writable files: {stats['world_writable']}
Non-owner writable files: {stats['non_owner_writable']}
Scan duration: {stats['scan_duration']:.2f} seconds

Risk Level Breakdown:
- HIGH: {len([f for f in self.scanner.unsafe_files if f.risk_level == 'HIGH'])}
- MEDIUM: {len([f for f in self.scanner.unsafe_files if f.risk_level == 'MEDIUM'])}
- LOW: {len([f for f in self.scanner.unsafe_files if f.risk_level == 'LOW'])}
"""
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(1.0, summary_text)
        
        # Update detailed results
        self.details_tree.delete(*self.details_tree.get_children())
        for file in self.scanner.unsafe_files:
            self.details_tree.insert("", "end", values=(
                file.path,
                file.permissions,
                file.owner,
                file.group,
                file.risk_level,
                ", ".join(file.issues)
            ))
        
        # Update JSON results
        report = self.scanner.generate_report()
        self.json_text.delete(1.0, tk.END)
        self.json_text.insert(1.0, json.dumps(report, indent=2))
        
        # Update summary label
        self.summary_label.config(
            text=f"Scan completed - {stats['unsafe_files']} unsafe files found"
        )
    
    def clear_results(self):
        """Clear all results."""
        self.summary_text.delete(1.0, tk.END)
        self.details_tree.delete(*self.details_tree.get_children())
        self.json_text.delete(1.0, tk.END)
        self.summary_label.config(text="No security scan performed yet")
        self.export_btn.config(state="disabled")
        self.status_indicator.config(text="● Ready", foreground="#27ae60")
        self.files_scanned_label.config(text="Files: 0")
        self.unsafe_files_label.config(text="Unsafe: 0")
        self.scan_time_label.config(text="Time: 0.00s")
    
    def export_results(self):
        """Export results to file."""
        if not self.scanner:
            messagebox.showerror("Error", "No results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    report = self.scanner.generate_report()
                    with open(filename, 'w') as f:
                        json.dump(report, f, indent=2)
                else:
                    # Export as text
                    with open(filename, 'w') as f:
                        f.write(self.summary_text.get(1.0, tk.END))
                        f.write("\n\nDetailed Results:\n")
                        f.write("=" * 50 + "\n")
                        for file in self.scanner.unsafe_files:
                            f.write(f"File: {file.path}\n")
                            f.write(f"  Permissions: {file.permissions}\n")
                            f.write(f"  Owner: {file.owner}, Group: {file.group}\n")
                            f.write(f"  Risk Level: {file.risk_level}\n")
                            f.write(f"  Issues: {', '.join(file.issues)}\n\n")
                
                messagebox.showinfo("Success", f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {e}")
    
    def run_test_scan(self):
        """Run a test scan with sample files."""
        try:
            import test_scanner
            test_scanner.main()
            messagebox.showinfo("Test Complete", "Test scan completed. Check the console for results.")
        except Exception as e:
            messagebox.showerror("Error", f"Test scan failed: {e}")
    
    def quick_scan(self):
        """Perform a quick scan of the current directory."""
        current_dir = os.getcwd()
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(0, current_dir)
        self.add_directory()
        self.start_scan()
    
    def run_demo(self):
        """Run the demo script."""
        try:
            import demo
            demo.main()
            messagebox.showinfo("Demo Complete", "Demo completed. Check the console for results.")
        except Exception as e:
            messagebox.showerror("Error", f"Demo failed: {e}")
    
    def open_log_file(self):
        """Open the log file."""
        log_file = "unsafe_file_scanner.log"
        if os.path.exists(log_file):
            try:
                if sys.platform.startswith('win'):
                    os.startfile(log_file)
                else:
                    webbrowser.open(log_file)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open log file: {e}")
        else:
            messagebox.showinfo("Info", "No log file found")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
Unsafe File Scanner - GUI Version 1.0.0

A graphical user interface for the Unsafe File Scanner tool.

Features:
• Scan directories for unsafe file permissions
• Detect SUID/SGID binaries
• Find world-writable files
• Identify non-owner writable files
• Generate detailed reports
• Export results in multiple formats

Developed with Python and tkinter.
        """
        messagebox.showinfo("About", about_text)
    
    def open_documentation(self):
        """Open documentation."""
        try:
            webbrowser.open("README.md")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open documentation: {e}")


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    
    # Set professional style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure professional colors
    style.configure('Accent.TButton', 
                   background='#3498db', 
                   foreground='white',
                   font=('Segoe UI', 10, 'bold'),
                   padding=(10, 5))
    
    style.map('Accent.TButton',
              background=[('active', '#2980b9')])
    
    # Configure label frames
    style.configure('TLabelframe', 
                   background='#f8f9fa',
                   borderwidth=1,
                   relief='solid')
    
    style.configure('TLabelframe.Label',
                   background='#f8f9fa',
                   font=('Segoe UI', 10, 'bold'),
                   foreground='#2c3e50')
    
    # Create and run the application
    app = UnsafeFileScannerGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Set window icon if available
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()

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

# Import new features
try:
    from realtime_monitor import RealTimeMonitorGUI, check_watchdog_availability
    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False
    RealTimeMonitorGUI = None
    check_watchdog_availability = None

try:
    from rule_engine import RuleEngine
    RULE_ENGINE_AVAILABLE = True
except ImportError:
    RULE_ENGINE_AVAILABLE = False
    RuleEngine = None


class UnsafeFileScannerGUI:
    """Main GUI application class."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Unsafe File Scanner - Professional Security Tool")
        self.root.geometry("1600x1000")
        self.root.minsize(1400, 900)
        
        # Modern dark theme configuration
        self.root.configure(bg='#0d1117')
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Modern window styling
        self.root.attributes('-alpha', 0.98)  # Slight transparency for modern look
        
        # Variables
        self.scanner = None
        self.scan_thread = None
        self.is_scanning = False
        self.scan_results = []
        
        # Real-time monitoring
        self.realtime_monitor = None
        self.is_monitoring = False
        
        # Rule engine
        self.rule_engine = None
        
        # Create modern GUI elements
        self.create_modern_widgets()
        self.setup_modern_layout()
        
        # Apply modern theme
        self.apply_modern_theme()
        
        # Load default configuration
        self.load_default_config()
    
    def create_modern_widgets(self):
        """Create modern 2025-style GUI widgets."""
        # Main container with modern dark theme
        self.main_frame = tk.Frame(self.root, bg='#0d1117', padx=25, pady=25)
        
        # Modern header section with glassmorphism effect
        self.header_frame = tk.Frame(self.main_frame, bg='#161b22', relief='flat', bd=0)
        
        # Modern title with premium typography
        self.title_label = tk.Label(
            self.header_frame, 
            text="🔒 Unsafe File Scanner", 
            font=("SF Pro Display", 36, "bold"),
            fg='#ffffff',
            bg='#161b22'
        )
        
        # Modern subtitle with subtle styling
        self.subtitle_label = tk.Label(
            self.header_frame,
            text="Professional Security Analysis & File Permission Monitoring",
            font=("SF Pro Text", 16),
            fg='#8b949e',
            bg='#161b22'
        )
        
        # Modern status indicator with animated appearance
        self.status_indicator = tk.Label(
            self.header_frame,
            text="● Ready to Scan",
            font=("SF Pro Text", 14, "bold"),
            fg='#3fb950',
            bg='#161b22'
        )
        
        # Modern content area with dark theme
        self.content_frame = tk.Frame(self.main_frame, bg='#0d1117')
        
        # Modern left panel with glassmorphism card design
        self.left_panel = tk.Frame(
            self.content_frame, 
            bg='#161b22',
            relief='flat',
            bd=0
        )
        
        # Modern panel title
        self.panel_title = tk.Label(
            self.left_panel,
            text="🔧 Scan Configuration",
            font=("SF Pro Text", 18, "bold"),
            fg='#ffffff',
            bg='#161b22'
        )
        
        # Modern directory selection with sleek design
        self.dir_frame = tk.Frame(self.left_panel, bg='#161b22')
        self.dir_label = tk.Label(
            self.dir_frame, 
            text="Target Directory", 
            font=("SF Pro Text", 14, "bold"),
            fg='#ffffff',
            bg='#161b22'
        )
        
        # Modern entry field with dark theme
        self.dir_entry = tk.Entry(
            self.dir_frame, 
            width=45, 
            font=("SF Pro Text", 12),
            bg='#21262d',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=8
        )
        
        # Modern browse button with gradient-like effect
        self.dir_browse_btn = tk.Button(
            self.dir_frame, 
            text="📁 Select Folder", 
            command=self.browse_directories,
            font=("SF Pro Text", 12, "bold"),
            bg='#238636',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        
        # Modern output file section
        self.output_frame = tk.Frame(self.left_panel, bg='#161b22')
        self.output_label = tk.Label(
            self.output_frame, 
            text="Output File", 
            font=("SF Pro Text", 14, "bold"),
            fg='#ffffff',
            bg='#161b22'
        )
        
        # Modern output entry field
        self.output_file_entry = tk.Entry(
            self.output_frame, 
            width=45, 
            font=("SF Pro Text", 12),
            bg='#21262d',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=8
        )
        
        # Modern output browse button
        self.output_file_browse_btn = tk.Button(
            self.output_frame, 
            text="💾 Browse", 
            command=self.browse_output_file,
            font=("SF Pro Text", 12, "bold"),
            bg='#1f6feb',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        
        # Modern control buttons section
        self.control_frame = tk.Frame(self.left_panel, bg='#161b22')
        
        # Modern primary scan button with premium styling
        self.scan_btn = tk.Button(
            self.control_frame, 
            text="🚀 Start Security Scan", 
            command=self.start_scan,
            font=("SF Pro Text", 14, "bold"),
            bg='#238636',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        
        # Modern secondary buttons
        self.stop_btn = tk.Button(
            self.control_frame, 
            text="⏹️ Stop Scan", 
            command=self.stop_scan,
            state="disabled",
            font=("SF Pro Text", 12, "bold"),
            bg='#da3633',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        
        self.clear_btn = tk.Button(
            self.control_frame, 
            text="🗑️ Clear Results", 
            command=self.clear_results,
            font=("SF Pro Text", 12, "bold"),
            bg='#6f42c1',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        
        self.export_btn = tk.Button(
            self.control_frame, 
            text="📊 Export Results", 
            command=self.export_results,
            state="disabled",
            font=("SF Pro Text", 12, "bold"),
            bg='#1f6feb',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        
        # Modern advanced features section with professional styling
        self.advanced_frame = tk.Frame(
            self.left_panel, 
            bg='#161b22',
            relief='flat',
            bd=0
        )
        
        # Advanced features title
        self.advanced_title = tk.Label(
            self.advanced_frame,
            text="⚙️ Advanced Features",
            font=("SF Pro Text", 16, "bold"),
            fg='#ffffff',
            bg='#161b22'
        )
        
        # Modern real-time monitoring button with improved styling
        self.realtime_btn = tk.Button(
            self.advanced_frame,
            text="👁️ Start Real-time Monitor",
            command=self.toggle_realtime_monitoring,
            state="normal" if REALTIME_AVAILABLE else "disabled",
            font=("SF Pro Text", 12, "bold"),
            bg='#f85149' if REALTIME_AVAILABLE else '#6c757d',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            width=18
        )
        
        # Modern rules management button with improved styling
        self.rules_btn = tk.Button(
            self.advanced_frame,
            text="⚙️ Manage Rules",
            command=self.open_rules_manager,
            state="normal" if RULE_ENGINE_AVAILABLE else "disabled",
            font=("SF Pro Text", 12, "bold"),
            bg='#8b5cf6' if RULE_ENGINE_AVAILABLE else '#6c757d',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            width=18
        )
        
        # Modern real-time monitoring controls
        self.realtime_controls_frame = tk.Frame(self.advanced_frame, bg='#161b22')
        
        # Real-time controls title
        self.realtime_controls_title = tk.Label(
            self.realtime_controls_frame,
            text="Real-time Controls",
            font=("SF Pro Text", 12, "bold"),
            fg='#8b949e',
            bg='#161b22'
        )
        
        # Modern real-time control buttons with improved styling
        self.view_realtime_btn = tk.Button(
            self.realtime_controls_frame,
            text="📊 View Results",
            command=self.view_realtime_results,
            state="disabled",
            font=("SF Pro Text", 11, "bold"),
            bg='#6c757d',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            width=12
        )
        
        self.export_realtime_btn = tk.Button(
            self.realtime_controls_frame,
            text="💾 Export Results",
            command=self.export_realtime_results,
            state="disabled",
            font=("SF Pro Text", 11, "bold"),
            bg='#6c757d',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            width=12
        )
        
        self.clear_realtime_btn = tk.Button(
            self.realtime_controls_frame,
            text="🗑️ Clear Results",
            command=self.clear_realtime_results,
            state="disabled",
            font=("SF Pro Text", 11, "bold"),
            bg='#6c757d',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            width=12
        )
        
        # Modern export format section
        self.export_format_frame = tk.Frame(self.advanced_frame, bg='#161b22')
        
        # Export format title
        self.export_format_title = tk.Label(
            self.export_format_frame,
            text="Export Format",
            font=("SF Pro Text", 12, "bold"),
            fg='#8b949e',
            bg='#161b22'
        )
        
        # Modern export format combobox
        self.export_format_combo = tk.StringVar(value="JSON")
        self.export_format_menu = tk.OptionMenu(
            self.export_format_frame,
            self.export_format_combo,
            "JSON", "CSV", "HTML"
        )
        self.export_format_menu.config(
            font=("SF Pro Text", 10),
            bg='#21262d',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        
        # Modern right panel - Results with professional styling
        self.right_panel = tk.Frame(
            self.content_frame, 
            bg='#161b22',
            relief='flat',
            bd=0
        )
        
        # Results panel title
        self.results_title = tk.Label(
            self.right_panel,
            text="📊 Scan Results",
            font=("SF Pro Text", 18, "bold"),
            fg='#ffffff',
            bg='#161b22'
        )
        
        # Modern results summary section
        self.summary_frame = tk.Frame(self.right_panel, bg='#161b22')
        self.summary_label = tk.Label(
            self.summary_frame, 
            text="No security scan performed yet", 
            font=("SF Pro Text", 12, "bold"),
            fg='#8b949e',
            bg='#161b22'
        )
        
        # Modern security metrics frame
        self.metrics_frame = tk.Frame(self.right_panel, bg='#161b22')
        
        # Modern metrics labels with professional styling
        self.files_scanned_label = tk.Label(
            self.metrics_frame, 
            text="Files: 0", 
            font=("SF Pro Text", 11, "bold"),
            fg='#58a6ff',
            bg='#161b22'
        )
        self.unsafe_files_label = tk.Label(
            self.metrics_frame, 
            text="Unsafe: 0", 
            font=("SF Pro Text", 11, "bold"),
            fg='#f85149',
            bg='#161b22'
        )
        self.scan_time_label = tk.Label(
            self.metrics_frame, 
            text="Time: 0.00s", 
            font=("SF Pro Text", 11, "bold"),
            fg='#3fb950',
            bg='#161b22'
        )
        
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
            anchor=tk.W
        )
    
    
    def setup_modern_layout(self):
        """Setup modern 2025-style layout."""
        # Main frame with modern spacing
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Modern header section with padding
        self.header_frame.pack(fill=tk.X, pady=(0, 30), padx=20)
        
        # Modern title layout with centered alignment
        self.title_label.pack(anchor=tk.W, pady=(20, 5))
        self.subtitle_label.pack(anchor=tk.W, pady=(0, 10))
        self.status_indicator.pack(anchor=tk.W, pady=(0, 20))
        
        # Modern content area with side-by-side layout
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Modern left panel with card-like appearance
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Panel title
        self.panel_title.pack(anchor=tk.W, pady=(20, 20), padx=20)
        
        # Modern directory selection layout
        self.dir_frame.pack(fill=tk.X, pady=(0, 25), padx=20)
        
        self.dir_label.pack(anchor=tk.W, pady=(0, 10))
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.dir_browse_btn.pack(side=tk.RIGHT)
        
        # Modern output file layout
        self.output_frame.pack(fill=tk.X, pady=(0, 25), padx=20)
        
        self.output_label.pack(anchor=tk.W, pady=(0, 10))
        self.output_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.output_file_browse_btn.pack(side=tk.RIGHT)
        
        # Modern control buttons layout
        self.control_frame.pack(fill=tk.X, pady=(0, 25), padx=20)
        
        # Main scan button (prominent)
        self.scan_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Secondary buttons in a row
        button_row = tk.Frame(self.control_frame, bg='#161b22')
        button_row.pack(fill=tk.X, pady=(0, 10))
        
        self.stop_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.clear_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Export button (full width)
        self.export_btn.pack(fill=tk.X)
        
        # Modern advanced features layout
        self.advanced_frame.pack(fill=tk.X, pady=(0, 25), padx=20)
        
        # Advanced features title with separator
        self.advanced_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Visual separator line
        separator_line = tk.Frame(self.advanced_frame, height=1, bg='#30363d')
        separator_line.pack(fill=tk.X, pady=(0, 15))
        
        # Modern advanced features buttons - properly aligned
        advanced_buttons_frame = tk.Frame(self.advanced_frame, bg='#161b22')
        advanced_buttons_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create a centered container for the buttons
        buttons_container = tk.Frame(advanced_buttons_frame, bg='#161b22')
        buttons_container.pack(expand=True, fill=tk.X)
        
        # Buttons with proper spacing and alignment
        self.realtime_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.rules_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Modern real-time monitoring controls
        self.realtime_controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Real-time controls title
        self.realtime_controls_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Real-time controls in a professional grid layout
        realtime_controls_grid = tk.Frame(self.realtime_controls_frame, bg='#161b22')
        realtime_controls_grid.pack(fill=tk.X, pady=(10, 0))
        
        # First row - View and Export buttons
        controls_row1 = tk.Frame(realtime_controls_grid, bg='#161b22')
        controls_row1.pack(fill=tk.X, pady=(0, 8))
        
        self.view_realtime_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.export_realtime_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(8, 0))
        
        # Second row - Clear button (centered)
        controls_row2 = tk.Frame(realtime_controls_grid, bg='#161b22')
        controls_row2.pack(fill=tk.X)
        
        self.clear_realtime_btn.pack(anchor=tk.CENTER, pady=(0, 0))
        
        # Modern export format layout
        self.export_format_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Export format title
        self.export_format_title.pack(anchor=tk.W, pady=(0, 8))
        
        # Export format menu
        self.export_format_menu.pack(anchor=tk.W)
        
        # Modern right panel - Results
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Results panel title
        self.results_title.pack(anchor=tk.W, pady=(20, 20), padx=20)
        
        # Modern results summary
        self.summary_frame.pack(fill=tk.X, pady=(0, 15), padx=20)
        self.summary_label.pack(anchor=tk.W)
        
        # Modern security metrics
        self.metrics_frame.pack(fill=tk.X, pady=(0, 15), padx=20)
        
        # Metrics in a row
        metrics_row = tk.Frame(self.metrics_frame, bg='#161b22')
        metrics_row.pack(fill=tk.X)
        
        self.files_scanned_label.pack(side=tk.LEFT, padx=(0, 20))
        self.unsafe_files_label.pack(side=tk.LEFT, padx=(0, 20))
        self.scan_time_label.pack(side=tk.RIGHT)
        
        # Modern progress bar
        self.progress_bar.pack(fill=tk.X, pady=(0, 15), padx=20)
        
        # Modern results notebook
        self.results_notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Modern tab content - all use pack
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        self.details_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Modern JSON tab content
        self.json_text.pack(fill=tk.BOTH, expand=True)
        
        # Modern status bar
        self.status_bar_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def load_default_config(self):
        """Load default configuration."""
        self.output_file_entry.insert(0, "scan_results.json")
    
    def apply_modern_theme(self):
        """Apply modern 2025 theme with hover effects and animations."""
        # Configure button hover effects
        def add_hover_effect(button, hover_color, normal_color):
            def on_enter(e):
                button.config(bg=hover_color)
            def on_leave(e):
                button.config(bg=normal_color)
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        
        # Apply hover effects to buttons with professional colors
        add_hover_effect(self.dir_browse_btn, '#2ea043', '#238636')
        add_hover_effect(self.output_file_browse_btn, '#388bfd', '#1f6feb')
        add_hover_effect(self.scan_btn, '#2ea043', '#238636')
        add_hover_effect(self.stop_btn, '#f85149', '#da3633')
        add_hover_effect(self.clear_btn, '#8b5cf6', '#6f42c1')
        add_hover_effect(self.export_btn, '#388bfd', '#1f6feb')
        
        # Advanced features hover effects
        add_hover_effect(self.realtime_btn, '#f85149', '#f85149')
        add_hover_effect(self.rules_btn, '#8b5cf6', '#8b5cf6')
        add_hover_effect(self.view_realtime_btn, '#58a6ff', '#6c757d')
        add_hover_effect(self.export_realtime_btn, '#58a6ff', '#6c757d')
        add_hover_effect(self.clear_realtime_btn, '#f85149', '#6c757d')
        
        # Configure entry field focus effects
        def add_focus_effect(entry):
            def on_focus_in(e):
                entry.config(bg='#30363d', relief='solid', bd=1)
            def on_focus_out(e):
                entry.config(bg='#21262d', relief='flat', bd=8)
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        
        add_focus_effect(self.dir_entry)
        add_focus_effect(self.output_file_entry)
    
    def browse_directories(self):
        """Browse for directories to scan."""
        directory = filedialog.askdirectory(title="Select Directory to Scan")
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    
    
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
        # Get directory to scan
        directory = self.dir_entry.get().strip()
        if not directory:
            messagebox.showerror("Error", "Please select a directory to scan")
            return
        
        if not os.path.exists(directory):
            messagebox.showerror("Error", f"Directory does not exist: {directory}")
            return
        
        directories = [directory]
        
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
        
        # Get selected export format
        export_format = self.export_format_combo.get().lower()
        
        # Set default extension based on format
        if export_format == "json":
            default_ext = ".json"
            filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
        elif export_format == "csv":
            default_ext = ".csv"
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        elif export_format == "html":
            default_ext = ".html"
            filetypes = [("HTML files", "*.html"), ("All files", "*.*")]
        else:
            default_ext = ".json"
            filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
        
        filename = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=default_ext,
            filetypes=filetypes
        )
        
        if filename:
            try:
                # Generate report
                report = self.scanner.generate_report()
                
                # Save based on format
                if export_format == "json":
                    with open(filename, 'w') as f:
                        json.dump(report, f, indent=2)
                elif export_format == "csv":
                    self.scanner.save_report(report, filename)
                elif export_format == "html":
                    self.scanner.save_report(report, filename)
                else:
                    # Fallback to JSON
                    with open(filename, 'w') as f:
                        json.dump(report, f, indent=2)
                
                messagebox.showinfo("Success", f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {e}")
    
    
    def toggle_realtime_monitoring(self):
        """Toggle real-time monitoring."""
        if not REALTIME_AVAILABLE:
            messagebox.showerror("Error", "Real-time monitoring not available. Install watchdog library.")
            return
        
        if not self.is_monitoring:
            # Start monitoring
            directories = list(self.dir_listbox.get(0, tk.END))
            if not directories:
                messagebox.showerror("Error", "Please select directories to monitor")
                return
            
            try:
                if not self.realtime_monitor:
                    self.realtime_monitor = RealTimeMonitorGUI(
                        self.scanner, 
                        self.on_realtime_alert
                    )
                
                self.realtime_monitor.start_monitoring(directories)
                self.is_monitoring = True
                self.realtime_btn.config(text="⏹️ Stop Monitor")
                self.status_indicator.config(text="● Monitoring...", foreground="#e74c3c")
                
                # Enable real-time monitoring controls when monitoring starts
                self.view_realtime_btn.config(state="normal")
                self.export_realtime_btn.config(state="normal")
                self.clear_realtime_btn.config(state="normal")
                
                messagebox.showinfo("Success", "Real-time monitoring started")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start monitoring: {e}")
        else:
            # Stop monitoring
            try:
                self.realtime_monitor.stop_monitoring()
                self.is_monitoring = False
                self.realtime_btn.config(text="👁️ Start Real-time Monitor")
                self.status_indicator.config(text="● Ready", foreground="#27ae60")
                messagebox.showinfo("Success", "Real-time monitoring stopped")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop monitoring: {e}")
    
    def on_realtime_alert(self, unsafe_file):
        """Handle real-time monitoring alerts."""
        # Add to results
        self.scan_results.append(unsafe_file)
        
        # Update GUI
        self.update_results_display()
        
        # Enable real-time monitoring controls
        self.view_realtime_btn.config(state="normal")
        self.export_realtime_btn.config(state="normal")
        self.clear_realtime_btn.config(state="normal")
        
        # Show notification
        messagebox.showwarning(
            "Security Alert", 
            f"Unsafe file detected:\n{unsafe_file.path}\nRisk: {unsafe_file.risk_level}"
        )
    
    def update_results_display(self):
        """Update the results display with real-time monitoring results."""
        if not self.scan_results:
            return
        
        # Update the main results display to show real-time results
        if self.scanner:
            # Temporarily replace scanner results with real-time results
            original_files = self.scanner.unsafe_files
            self.scanner.unsafe_files = self.scan_results
            
            # Update the display
            self.update_results()
            
            # Restore original results
            self.scanner.unsafe_files = original_files
    
    def view_realtime_results(self):
        """View real-time monitoring results in a new window."""
        if not self.scan_results:
            messagebox.showinfo("Info", "No real-time monitoring results to display")
            return
        
        # Create results window
        results_window = tk.Toplevel(self.root)
        results_window.title("Real-time Monitoring Results")
        results_window.geometry("1000x600")
        
        # Create frame for results
        results_frame = ttk.Frame(results_window)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            results_frame, 
            text=f"Real-time Monitoring Results ({len(self.scan_results)} files detected)",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Results treeview
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("timestamp", "path", "permissions", "owner", "group", "risk", "issues"),
            show="headings",
            height=15
        )
        
        # Configure columns
        tree.heading("timestamp", text="Detected At")
        tree.heading("path", text="File Path")
        tree.heading("permissions", text="Permissions")
        tree.heading("owner", text="Owner")
        tree.heading("group", text="Group")
        tree.heading("risk", text="Risk Level")
        tree.heading("issues", text="Issues")
        
        tree.column("timestamp", width=120)
        tree.column("path", width=300)
        tree.column("permissions", width=100)
        tree.column("owner", width=80)
        tree.column("group", width=80)
        tree.column("risk", width=80)
        tree.column("issues", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate results
        for i, file in enumerate(self.scan_results):
            # Get current timestamp for display
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            tree.insert("", "end", values=(
                timestamp,
                file.path,
                file.permissions,
                file.owner,
                file.group,
                file.risk_level,
                ", ".join(file.issues)
            ))
        
        # Buttons
        button_frame = ttk.Frame(results_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Export Results", command=lambda: self.export_realtime_results()).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear Results", command=lambda: self.clear_realtime_results()).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Close", command=results_window.destroy).pack(side=tk.RIGHT)
    
    def export_realtime_results(self):
        """Export real-time monitoring results."""
        if not self.scan_results:
            messagebox.showinfo("Info", "No real-time monitoring results to export")
            return
        
        # Get selected export format
        export_format = self.export_format_combo.get().lower()
        
        # Set default extension based on format
        if export_format == "json":
            default_ext = ".json"
            filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
        elif export_format == "csv":
            default_ext = ".csv"
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        elif export_format == "html":
            default_ext = ".html"
            filetypes = [("HTML files", "*.html"), ("All files", "*.*")]
        else:
            default_ext = ".json"
            filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
        
        filename = filedialog.asksaveasfilename(
            title="Export Real-time Monitoring Results",
            defaultextension=default_ext,
            filetypes=filetypes
        )
        
        if filename:
            try:
                # Create a temporary scanner to use its export methods
                temp_scanner = UnsafeFileScanner()
                temp_scanner.unsafe_files = self.scan_results
                
                # Generate report
                report = temp_scanner.generate_report()
                
                # Save based on format
                if export_format == "json":
                    with open(filename, 'w') as f:
                        json.dump(report, f, indent=2)
                elif export_format == "csv":
                    temp_scanner.save_report(report, filename)
                elif export_format == "html":
                    temp_scanner.save_report(report, filename)
                else:
                    # Fallback to JSON
                    with open(filename, 'w') as f:
                        json.dump(report, f, indent=2)
                
                messagebox.showinfo("Success", f"Real-time monitoring results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export real-time results: {e}")
    
    def clear_realtime_results(self):
        """Clear real-time monitoring results."""
        if not self.scan_results:
            messagebox.showinfo("Info", "No real-time monitoring results to clear")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all real-time monitoring results?"):
            self.scan_results.clear()
            self.view_realtime_btn.config(state="disabled")
            self.export_realtime_btn.config(state="disabled")
            self.clear_realtime_btn.config(state="disabled")
            messagebox.showinfo("Success", "Real-time monitoring results cleared")
    
    
    def open_rules_manager(self):
        """Open rules management window."""
        if not RULE_ENGINE_AVAILABLE:
            messagebox.showerror("Error", "Rule engine not available")
            return
        
        # Create rules manager window
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Rules Manager")
        rules_window.geometry("800x600")
        
        # Create rule engine if not exists
        if not self.rule_engine:
            self.rule_engine = RuleEngine()
        
        # Rules list
        rules_frame = ttk.Frame(rules_window)
        rules_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(rules_frame, text="Security Rules", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Rules treeview
        rules_tree = ttk.Treeview(rules_frame, columns=("Type", "Risk", "Enabled"), show="tree headings")
        rules_tree.heading("#0", text="Rule Name")
        rules_tree.heading("Type", text="Type")
        rules_tree.heading("Risk", text="Risk Level")
        rules_tree.heading("Enabled", text="Enabled")
        
        # Populate rules
        for rule in self.rule_engine.rules:
            rules_tree.insert("", tk.END, text=rule.name, values=(
                rule.rule_type.value,
                rule.risk_level.value,
                "Yes" if rule.enabled else "No"
            ))
        
        rules_tree.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(rules_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Enable Selected", command=lambda: self.toggle_rule(rules_tree, True)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Disable Selected", command=lambda: self.toggle_rule(rules_tree, False)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save Rules", command=lambda: self.save_rules()).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Close", command=rules_window.destroy).pack(side=tk.RIGHT)
    
    def toggle_rule(self, rules_tree, enable):
        """Toggle rule enabled/disabled state."""
        selection = rules_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a rule")
            return
        
        for item in selection:
            rule_name = rules_tree.item(item, "text")
            for rule in self.rule_engine.rules:
                if rule.name == rule_name:
                    rule.enabled = enable
                    rules_tree.set(item, "Enabled", "Yes" if enable else "No")
                    break
    
    def save_rules(self):
        """Save rules to file."""
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Rules",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.rule_engine.save_rules_to_file(filename)
                messagebox.showinfo("Success", f"Rules saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save rules: {e}")


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

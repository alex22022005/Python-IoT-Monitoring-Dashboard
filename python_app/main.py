"""
Main Python Application for IoT Monitoring System
3-page GUI: Past Data, Live Data, Future Predictions
"""

import tkinter as tk
from tkinter import ttk
import threading
import json
from datetime import datetime

from pages.live_data import LiveDataPage
from pages.past_data import PastDataPage  
from pages.predictions import PredictionsPage
from data.data_manager import DataManager
from utils.theme_manager import theme_manager

class IoTMonitorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IoT Monitoring System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)  # Set minimum window size
        
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Create top frame for controls
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        # Add theme toggle button
        self.setup_theme_controls()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(5, 10))
        
        # Initialize pages
        self.live_page = LiveDataPage(self.notebook, self.data_manager)
        self.past_page = PastDataPage(self.notebook, self.data_manager)
        self.predictions_page = PredictionsPage(self.notebook, self.data_manager)
        
        # Add pages to notebook
        self.notebook.add(self.live_page.frame, text="Live Data")
        self.notebook.add(self.past_page.frame, text="Past Data")
        self.notebook.add(self.predictions_page.frame, text="Predictions")
        
        # Register theme callback
        theme_manager.register_callback(self.on_theme_changed)
        
        # Register connection status callback
        self.data_manager.register_status_callback(self.update_connection_status)
        
        # Apply initial theme
        self.apply_theme()
        
        # Start data collection thread
        self.start_data_collection()
    
    def setup_theme_controls(self):
        """Setup theme toggle controls"""
        # Title label
        title_label = ttk.Label(self.top_frame, text="IoT Monitoring System", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(side='left')
        
        # Theme toggle button
        self.theme_button = ttk.Button(self.top_frame, text="🌙 Dark Mode", 
                                      command=self.toggle_theme, width=12)
        self.theme_button.pack(side='right', padx=(0, 10))
        
        # Connection status
        self.status_label = ttk.Label(self.top_frame, text="Status: Connecting...", 
                                     font=('Arial', 9))
        self.status_label.pack(side='right', padx=20)
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        theme_manager.toggle_theme()
        
        # Update button text
        if theme_manager.is_dark_mode:
            self.theme_button.configure(text="☀️ Light Mode")
        else:
            self.theme_button.configure(text="🌙 Dark Mode")
    
    def on_theme_changed(self, is_dark_mode):
        """Called when theme changes with smooth transition"""
        # Apply theme to main window first
        self.apply_theme()
        
        # Update all pages with smooth transition
        try:
            self.live_page.apply_theme()
            self.past_page.apply_theme()
            self.predictions_page.apply_theme()
        except Exception as e:
            print(f"Theme transition warning: {e}")
        
        # Force update to prevent visual glitches
        self.root.update_idletasks()
    
    def apply_theme(self):
        """Apply current theme to main window with enhanced styling"""
        theme = theme_manager.get_current_theme()
        
        try:
            self.root.configure(bg=theme['bg'])
            theme_manager.configure_widget(self.top_frame, 'frame')
            
            # Configure enhanced ttk styling
            style = ttk.Style()
            
            if theme_manager.is_dark_mode:
                style.theme_use('clam')
                
                # Enhanced dark theme styling with better text visibility
                style.configure('TLabel', 
                              background=theme['bg'], 
                              foreground='#ffffff',         # Force white text for better visibility
                              font=('Segoe UI', 9, 'normal'))
                
                style.configure('TFrame', 
                              background=theme['bg'],
                              relief='flat',
                              borderwidth=0)
                
                # Enhanced button styling with maximum contrast for dark mode
                style.configure('TButton', 
                              background='#1e40af',         # Dark blue background for better contrast
                              foreground='#ffffff',         # Pure white text
                              borderwidth=2,
                              relief='raised',
                              focuscolor='none',
                              font=('Segoe UI', 9, 'bold'),
                              padding=(12, 6),              # More padding for better appearance
                              insertcolor='#ffffff')        # Ensure cursor is white
                
                style.map('TButton',
                         background=[('active', '#2563eb'),    # Brighter blue on hover
                                   ('pressed', '#1d4ed8'),     # Darker blue on press
                                   ('disabled', '#64748b'),    # Gray when disabled
                                   ('focus', '#2563eb')],      # Blue when focused
                         foreground=[('active', '#ffffff'),    # Pure white text on hover
                                   ('pressed', '#ffffff'),     # Pure white text on press
                                   ('disabled', '#e5e7eb'),    # Light gray when disabled
                                   ('focus', '#ffffff')],      # Pure white text when focused
                         relief=[('pressed', 'sunken'),
                                ('active', 'raised'),
                                ('focus', 'raised')],
                         bordercolor=[('focus', '#ffffff')])
                
                style.configure('TNotebook', 
                              background=theme['bg'],
                              borderwidth=0,
                              tabmargins=[0, 0, 0, 0])     # Remove tab margins for smoother appearance
                
                style.configure('TNotebook.Tab', 
                              background=theme['button_bg'],
                              foreground='#ffffff',         # White text for tabs
                              padding=[20, 8],
                              font=('Segoe UI', 10),
                              focuscolor='none')            # Remove focus outline
                
                style.map('TNotebook.Tab',
                         background=[('selected', theme['accent2']),
                                   ('active', theme['accent3']),
                                   ('!active', theme['button_bg'])],  # Consistent inactive state
                         foreground=[('selected', '#ffffff'),
                                   ('active', '#ffffff'),
                                   ('!active', '#ffffff')])
                
                style.configure('TLabelFrame', 
                              background=theme['card_bg'],
                              foreground='#ffffff',         # White text for label frames
                              borderwidth=1,
                              relief='solid',
                              font=('Segoe UI', 9, 'bold'))
                
                style.configure('TCombobox', 
                              fieldbackground=theme['entry_bg'],
                              background=theme['button_bg'],
                              foreground=theme['entry_fg'],
                              borderwidth=1,
                              font=('Segoe UI', 9))
                
            else:
                style.theme_use('default')
                
                # Enhanced light theme styling with smooth transitions
                style.configure('TLabel', 
                              background=theme['bg'], 
                              foreground=theme['fg'],
                              font=('Segoe UI', 9))
                
                # Light mode notebook styling for consistency
                style.configure('TNotebook', 
                              background=theme['bg'],
                              borderwidth=0,
                              tabmargins=[0, 0, 0, 0])     # Remove tab margins for smoother appearance
                
                style.configure('TNotebook.Tab', 
                              padding=[20, 8],
                              font=('Segoe UI', 10),
                              focuscolor='none')            # Remove focus outline
                
                style.map('TNotebook.Tab',
                         background=[('selected', theme['accent2']),
                                   ('active', theme['accent3'])],
                         focuscolor=[('!focus', 'none')])  # Remove focus effects
                
                style.configure('TFrame', 
                              background=theme['bg'],
                              relief='flat')
                
                # Enhanced button styling for light mode
                style.configure('TButton', 
                              background='#1e40af',         # Dark blue background
                              foreground='#ffffff',         # Pure white text
                              borderwidth=2,
                              relief='raised',
                              focuscolor='none',
                              font=('Segoe UI', 9, 'bold'),
                              padding=(12, 6),              # More padding for better appearance
                              insertcolor='#ffffff')        # Ensure cursor is white
                
                style.map('TButton',
                         background=[('active', '#2563eb'),    # Lighter blue on hover
                                   ('pressed', '#1d4ed8'),     # Darker blue on press
                                   ('disabled', '#64748b'),    # Gray when disabled
                                   ('focus', '#2563eb')],      # Blue when focused
                         foreground=[('active', '#ffffff'),    # Pure white text on hover
                                   ('pressed', '#ffffff'),     # Pure white text on press
                                   ('disabled', '#e5e7eb'),    # Light gray when disabled
                                   ('focus', '#ffffff')],      # Pure white text when focused
                         relief=[('pressed', 'sunken'),
                                ('active', 'raised'),
                                ('focus', 'raised')],
                         bordercolor=[('focus', '#ffffff')])
                
                style.configure('TNotebook.Tab', 
                              padding=[20, 8],
                              font=('Segoe UI', 10))
                
                style.map('TNotebook.Tab',
                         background=[('selected', theme['accent2']),
                                   ('active', theme['accent3'])])
                
                style.configure('TLabelFrame', 
                              background=theme['card_bg'],
                              foreground=theme['fg'],
                              borderwidth=1,
                              relief='solid',
                              font=('Segoe UI', 9, 'bold'))
                
        except tk.TclError:
            pass
    
    def update_connection_status(self, status, message):
        """Update connection status display with better visibility"""
        theme = theme_manager.get_current_theme()
        
        if status == "connecting":
            color = "#ff8c00" if theme_manager.is_dark_mode else "#ff6600"  # Orange
            self.status_label.configure(text="Status: Connecting...", foreground=color)
        elif status == "connected":
            color = "#00ff00" if theme_manager.is_dark_mode else "#008000"  # Green
            self.status_label.configure(text="Status: Connected ✓", foreground=color)
        elif status == "demo":
            color = "#00bfff" if theme_manager.is_dark_mode else "#0066cc"  # Blue
            self.status_label.configure(text="Status: Demo Mode 🎭", foreground=color)
        elif status == "error":
            color = "#ff4444" if theme_manager.is_dark_mode else "#cc0000"  # Red
            self.status_label.configure(text=f"Status: Error ✗", foreground=color)
        else:
            color = "#ffffff" if theme_manager.is_dark_mode else "#666666"  # Gray
            self.status_label.configure(text=f"Status: {message}", foreground=color)
    
    def start_data_collection(self):
        """Start background thread for data collection"""
        collection_thread = threading.Thread(target=self.data_manager.start_collection, daemon=True)
        collection_thread.start()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = IoTMonitorApp()
    app.run()
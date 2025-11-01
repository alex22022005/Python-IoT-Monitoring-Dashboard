"""
Past Data Page - Historical data analysis and visualization
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme_manager import theme_manager

class PastDataPage:
    def __init__(self, parent, data_manager):
        self.parent = parent
        self.data_manager = data_manager
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = ttk.Label(self.frame, text="Historical Data Analysis", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Controls frame with better alignment
        controls_frame = ttk.LabelFrame(self.frame, text="Controls", padding=8)
        controls_frame.pack(fill='x', padx=15, pady=5)
        
        # Configure grid columns for proper alignment
        controls_frame.columnconfigure(1, weight=0)
        controls_frame.columnconfigure(3, weight=1)
        
        # Row 1: Show records control
        ttk.Label(controls_frame, text="Show:", font=('Arial', 9, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.range_var = tk.StringVar(value="50")
        range_combo = ttk.Combobox(controls_frame, textvariable=self.range_var, 
                                  values=["25", "50", "100", "200"], width=8)
        range_combo.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        range_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_data())
        
        ttk.Label(controls_frame, text="records").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        
        # Buttons frame for better alignment
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.grid(row=0, column=3, padx=10, pady=5, sticky='e')
        
        refresh_btn = ttk.Button(buttons_frame, text="Refresh", command=self.refresh_data)
        refresh_btn.pack(side='left', padx=2)
        
        export_btn = ttk.Button(buttons_frame, text="Export CSV", command=self.export_data)
        export_btn.pack(side='left', padx=2)
        
        csv_btn = ttk.Button(buttons_frame, text="Open Folder", command=self.open_csv_folder)
        csv_btn.pack(side='left', padx=2)
        
        # Statistics frame
        self.setup_statistics()
        
        # Chart
        self.setup_chart()
        
        # Load initial data
        self.refresh_data()
    
    def setup_statistics(self):
        """Setup statistics display"""
        stats_frame = ttk.LabelFrame(self.frame, text="Statistics", padding=8)
        stats_frame.pack(fill='x', padx=20, pady=5)
        
        # Configure grid for responsive layout with smaller minimum widths for better scaling
        stats_frame.columnconfigure(0, weight=1, minsize=100)
        stats_frame.columnconfigure(1, weight=1, minsize=100)
        stats_frame.columnconfigure(2, weight=1, minsize=100)
        stats_frame.columnconfigure(3, weight=1, minsize=100)
        
        # Voltage stats
        voltage_frame = ttk.Frame(stats_frame)
        voltage_frame.grid(row=0, column=0, padx=3, pady=2, sticky='new')
        
        ttk.Label(voltage_frame, text="Voltage", font=('Arial', 9, 'bold')).pack(anchor='w')
        self.voltage_avg_var = tk.StringVar(value="Avg: 0.00 V")
        self.voltage_min_var = tk.StringVar(value="Min: 0.00 V")
        self.voltage_max_var = tk.StringVar(value="Max: 0.00 V")
        
        ttk.Label(voltage_frame, textvariable=self.voltage_avg_var, font=('Arial', 8)).pack(anchor='w')
        ttk.Label(voltage_frame, textvariable=self.voltage_min_var, font=('Arial', 8)).pack(anchor='w')
        ttk.Label(voltage_frame, textvariable=self.voltage_max_var, font=('Arial', 8)).pack(anchor='w')
        
        # Current stats
        current_frame = ttk.Frame(stats_frame)
        current_frame.grid(row=0, column=1, padx=3, pady=2, sticky='new')
        
        ttk.Label(current_frame, text="Current", font=('Arial', 9, 'bold')).pack(anchor='w')
        self.current_avg_var = tk.StringVar(value="Avg: 0.00 A")
        self.current_min_var = tk.StringVar(value="Min: 0.00 A")
        self.current_max_var = tk.StringVar(value="Max: 0.00 A")
        
        ttk.Label(current_frame, textvariable=self.current_avg_var, font=('Arial', 8)).pack(anchor='w')
        ttk.Label(current_frame, textvariable=self.current_min_var, font=('Arial', 8)).pack(anchor='w')
        ttk.Label(current_frame, textvariable=self.current_max_var, font=('Arial', 8)).pack(anchor='w')
        
        # Temperature stats
        temp_frame = ttk.Frame(stats_frame)
        temp_frame.grid(row=0, column=2, padx=3, pady=2, sticky='new')
        
        ttk.Label(temp_frame, text="Temperature", font=('Arial', 9, 'bold')).pack(anchor='w')
        self.temp_avg_var = tk.StringVar(value="Avg: 0.0 °C")
        self.temp_min_var = tk.StringVar(value="Min: 0.0 °C")
        self.temp_max_var = tk.StringVar(value="Max: 0.0 °C")
        
        ttk.Label(temp_frame, textvariable=self.temp_avg_var, font=('Arial', 8)).pack(anchor='w')
        ttk.Label(temp_frame, textvariable=self.temp_min_var, font=('Arial', 8)).pack(anchor='w')
        ttk.Label(temp_frame, textvariable=self.temp_max_var, font=('Arial', 8)).pack(anchor='w')
        
        # Record count and power
        info_frame = ttk.Frame(stats_frame)
        info_frame.grid(row=0, column=3, padx=3, pady=2, sticky='new')
        
        ttk.Label(info_frame, text="Storage Info", font=('Arial', 9, 'bold')).pack(anchor='w')
        self.record_count_var = tk.StringVar(value="Records: 0")
        self.avg_power_var = tk.StringVar(value="Avg Power: 0.0 W")
        self.csv_info_var = tk.StringVar(value="CSV: Not available")
        ttk.Label(info_frame, textvariable=self.record_count_var, font=('Arial', 8)).pack(anchor='w')
        ttk.Label(info_frame, textvariable=self.avg_power_var, font=('Arial', 8)).pack(anchor='w')
        ttk.Label(info_frame, textvariable=self.csv_info_var, font=('Arial', 8)).pack(anchor='w')
    
    def setup_chart(self):
        """Setup historical data chart with proper sizing"""
        # Create matplotlib figure with better sizing to show all elements
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(12, 7))
        # No suptitle needed - clean layout with individual chart titles
        
        # Get colors for enhanced styling
        colors = theme_manager.get_matplotlib_colors()
        
        # Voltage plot with responsive styling and smooth lines
        self.ax1.set_title('⚡ Voltage (V)', fontsize=10, pad=6, weight='bold')
        self.ax1.set_ylabel('Voltage (V)', fontsize=8, weight='bold')
        self.voltage_line, = self.ax1.plot([], [], color=colors['voltage_color'], linewidth=2.0, alpha=0.8, linestyle='-', marker='', markersize=0)
        self.ax1.grid(True, alpha=0.3, linestyle='--')
        self.ax1.tick_params(labelsize=7)
        self.ax1.set_ylim(2.5, 6.0)
        
        # Current plot with responsive styling and smooth lines
        self.ax2.set_title('🔌 Current (A)', fontsize=10, pad=6, weight='bold')
        self.ax2.set_ylabel('Current (A)', fontsize=8, weight='bold')
        self.current_line, = self.ax2.plot([], [], color=colors['current_color'], linewidth=2.0, alpha=0.8, linestyle='-', marker='', markersize=0)
        self.ax2.grid(True, alpha=0.3, linestyle='--')
        self.ax2.tick_params(labelsize=7)
        self.ax2.set_ylim(0, 3.0)
        
        # Temperature plot with responsive styling and smooth lines
        self.ax3.set_title('🌡️ Temperature (°C)', fontsize=10, pad=6, weight='bold')
        self.ax3.set_ylabel('Temperature (°C)', fontsize=8, weight='bold')
        self.ax3.set_xlabel('Time', fontsize=8, weight='bold')
        self.temp_line, = self.ax3.plot([], [], color=colors['temp_color'], linewidth=2.0, alpha=0.8, linestyle='-', marker='', markersize=0)
        self.ax3.grid(True, alpha=0.3, linestyle='--')
        self.ax3.tick_params(labelsize=7)
        self.ax3.set_ylim(15, 40)
        
        # Responsive layout that prevents text overlap on smaller screens
        self.fig.tight_layout(pad=1.0, h_pad=0.6)
        self.fig.subplots_adjust(bottom=0.08, top=0.94, left=0.10, right=0.96)
        
        # Embed in tkinter with optimized spacing
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True, padx=8, pady=(3, 10))
        
        # Apply initial theme
        self.apply_theme()
    
    def refresh_data(self):
        """Refresh data from database and update displays"""
        try:
            # Get data limit
            range_val = self.range_var.get()
            limit = None if range_val == "All" else int(range_val)
            
            # Get historical data
            data = self.data_manager.get_historical_data(limit)
            
            if not data:
                return
            
            # Convert to pandas DataFrame for easier analysis
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')  # Sort by time
            
            # Update statistics
            self.update_statistics(df)
            
            # Update chart
            self.update_chart(df)
            
        except Exception as e:
            print(f"Error refreshing data: {e}")
    
    def update_statistics(self, df):
        """Update statistics display"""
        if df.empty:
            return
        
        # Voltage statistics
        voltage_avg = df['voltage'].mean()
        voltage_min = df['voltage'].min()
        voltage_max = df['voltage'].max()
        
        self.voltage_avg_var.set(f"Avg: {voltage_avg:.2f} V")
        self.voltage_min_var.set(f"Min: {voltage_min:.2f} V")
        self.voltage_max_var.set(f"Max: {voltage_max:.2f} V")
        
        # Current statistics
        current_avg = df['current'].mean()
        current_min = df['current'].min()
        current_max = df['current'].max()
        
        self.current_avg_var.set(f"Avg: {current_avg:.2f} A")
        self.current_min_var.set(f"Min: {current_min:.2f} A")
        self.current_max_var.set(f"Max: {current_max:.2f} A")
        
        # Temperature statistics
        temp_avg = df['temperature'].mean()
        temp_min = df['temperature'].min()
        temp_max = df['temperature'].max()
        
        self.temp_avg_var.set(f"Avg: {temp_avg:.1f} °C")
        self.temp_min_var.set(f"Min: {temp_min:.1f} °C")
        self.temp_max_var.set(f"Max: {temp_max:.1f} °C")
        
        # Power and record count
        df['power'] = df['voltage'] * df['current']
        power_avg = df['power'].mean()
        
        self.record_count_var.set(f"Records: {len(df)}")
        self.avg_power_var.set(f"Avg Power: {power_avg:.1f} W")
        
        # Update CSV info
        csv_info = self.data_manager.get_csv_info()
        if csv_info.get('exists', False):
            self.csv_info_var.set(f"CSV: {csv_info['record_count']} records ({csv_info['size_kb']} KB)")
        else:
            self.csv_info_var.set("CSV: Not available")
    
    def update_chart(self, df):
        """Update historical data chart with lively styling like live data page"""
        if df.empty:
            self.show_no_data_message()
            return
        
        # Update line data (same approach as live data page)
        self.voltage_line.set_data(df['timestamp'], df['voltage'])
        self.current_line.set_data(df['timestamp'], df['current'])
        self.temp_line.set_data(df['timestamp'], df['temperature'])
        
        # Auto-scale axes (same as live data page)
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()
        self.ax3.relim()
        self.ax3.autoscale_view()
        
        # Maintain realistic scales
        self.ax1.set_ylim(2.5, 6.0)
        self.ax2.set_ylim(0, 3.0)
        self.ax3.set_ylim(15, 40)
        
        # Format x-axis with responsive sizing for smaller screens
        self.ax3.tick_params(axis='x', rotation=45, labelsize=7)
        self.ax1.tick_params(axis='x', labelbottom=False)
        self.ax2.tick_params(axis='x', labelbottom=False)
        
        # Force canvas update (same as live data)
        self.canvas.draw_idle()
    
    def show_no_data_message(self):
        """Show message when no data is available"""
        colors = theme_manager.get_matplotlib_colors()
        text_color = colors['text_color']
        
        # Clear and show message on middle chart
        self.voltage_line.set_data([], [])
        self.current_line.set_data([], [])
        self.temp_line.set_data([], [])
        
        self.ax2.text(0.5, 0.5, '📊 No Historical Data Available\n\nStart collecting sensor data\nto see historical trends', 
                     ha='center', va='center', transform=self.ax2.transAxes, fontsize=12, 
                     color=text_color, weight='bold')
        
        self.canvas.draw()
    
    def export_data(self):
        """Export data to CSV file"""
        try:
            from tkinter import filedialog
            
            # Get data
            data = self.data_manager.get_historical_data()
            if not data:
                tk.messagebox.showwarning("No Data", "No data available to export")
                return
            
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                df = pd.DataFrame(data)
                df.to_csv(filename, index=False)
                tk.messagebox.showinfo("Export Complete", f"Data exported to {filename}")
                
        except Exception as e:
            tk.messagebox.showerror("Export Error", f"Failed to export data: {e}")
    
    def open_csv_folder(self):
        """Open the CSV data folder in file explorer"""
        try:
            import os
            import subprocess
            import platform
            
            # Get the CSV directory directly from data manager
            csv_dir = self.data_manager.get_csv_directory()
            
            # Debug: Print the path being used (console only)
            print(f"🔍 Opening folder: {csv_dir}")
            print(f"📁 Folder exists: {os.path.exists(csv_dir)}")
            
            # Ensure the directory exists
            if not os.path.exists(csv_dir):
                os.makedirs(csv_dir, exist_ok=True)
                print(f"📁 Created folder: {csv_dir}")
            
            # Open folder based on operating system (without check=True to prevent error dialogs)
            if platform.system() == "Windows":
                subprocess.run(['explorer', csv_dir])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', csv_dir])
            else:  # Linux
                subprocess.run(['xdg-open', csv_dir])
            
            # Success confirmation in console only (no popup)
            print(f"✅ Successfully opened folder: {csv_dir}")
                
        except Exception as e:
            import tkinter as tk
            csv_dir_info = csv_dir if 'csv_dir' in locals() else 'Unknown'
            print(f"❌ Error opening folder: {e}")
            tk.messagebox.showerror("Error Opening Folder", 
                f"Failed to open data folder.\n\n" +
                f"Error: {e}\n\n" +
                f"Folder location: {csv_dir_info}\n\n" +
                f"You can manually navigate to this folder in File Explorer.")
    
    def apply_theme(self):
        """Apply current theme with perfect dark/light mode compatibility"""
        colors = theme_manager.get_matplotlib_colors()
        theme = theme_manager.get_current_theme()
        
        # Update figure background for dark/light mode
        self.fig.patch.set_facecolor(colors['figure_bg'])
        
        # Enhanced chart titles with dark mode support
        titles = ['⚡ Voltage (V)', '🔌 Current (A)', '🌡️ Temperature (°C)']
        
        for i, ax in enumerate([self.ax1, self.ax2, self.ax3]):
            # Set background colors for dark/light mode
            ax.set_facecolor(colors['axes_bg'])
            
            # Enhanced text colors for perfect visibility in both modes
            ax.tick_params(colors=colors['text_color'], labelsize=8, 
                          which='both', direction='out', length=4, width=1)
            ax.xaxis.label.set_color(colors['text_color'])
            ax.yaxis.label.set_color(colors['text_color'])
            
            # Enhanced title styling with maximum contrast for dark mode
            title_color = '#ffffff' if theme_manager.is_dark_mode else '#212529'
            ax.title.set_color(title_color)
            ax.title.set_text(titles[i])
            ax.title.set_fontweight('bold')
            ax.title.set_fontsize(11)
            ax.title.set_bbox(dict(boxstyle="round,pad=0.3", 
                                 facecolor=colors['axes_bg'], 
                                 edgecolor='none', 
                                 alpha=0.8))
            
            # Enhanced grid with better dark mode visibility
            grid_alpha = 0.5 if theme_manager.is_dark_mode else 0.3
            ax.grid(True, alpha=grid_alpha, color=colors['grid_color'], 
                   linestyle='--', linewidth=0.8)
            
            # Set realistic scales like other pages
            if i == 0:  # Voltage
                ax.set_ylim(2.5, 6.0)
            elif i == 1:  # Current
                ax.set_ylim(0, 3.0)
            elif i == 2:  # Temperature
                ax.set_ylim(15, 40)
            
            # Enhanced spine styling with better dark mode support
            spine_alpha = 0.9 if theme_manager.is_dark_mode else 0.7
            for spine in ax.spines.values():
                spine.set_color(colors['text_color'])
                spine.set_alpha(spine_alpha)
                spine.set_linewidth(1.2)
        
        # No suptitle needed - individual chart titles are sufficient
        
        # Apply theme to tkinter widgets with enhanced dark mode support
        try:
            theme_manager.configure_widget(self.frame, 'frame')
        except Exception as e:
            print(f"Theme application warning: {e}")
        
        # Force canvas refresh to apply theme changes immediately
        if hasattr(self, 'canvas'):
            try:
                self.canvas.draw()  # Force immediate redraw instead of idle
                self.canvas.flush_events()  # Ensure all events are processed
            except Exception as e:
                print(f"Canvas refresh warning: {e}")
"""
Live Data Page - Real-time sensor readings display
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import collections
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme_manager import theme_manager

class LiveDataPage:
    def __init__(self, parent, data_manager):
        self.parent = parent
        self.data_manager = data_manager
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        
        # Data storage for real-time plotting
        self.max_points = 50
        self.voltage_data = collections.deque(maxlen=self.max_points)
        self.temp_data = collections.deque(maxlen=self.max_points)
        self.current_data = collections.deque(maxlen=self.max_points)
        self.time_data = collections.deque(maxlen=self.max_points)
        
        self.setup_ui()
        self.start_animation()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = ttk.Label(self.frame, text="Live Sensor Data", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Current readings frame
        readings_frame = ttk.LabelFrame(self.frame, text="Current Readings", padding=12)
        readings_frame.pack(fill='x', padx=20, pady=8)
        
        # Configure grid weights for responsive layout with smaller minimum widths
        readings_frame.columnconfigure(1, weight=1, minsize=60)
        readings_frame.columnconfigure(3, weight=1, minsize=60)
        
        # Voltage display with responsive font sizes
        self.voltage_var = tk.StringVar(value="0.00 V")
        voltage_label = ttk.Label(readings_frame, text="Voltage:", font=('Arial', 9))
        voltage_value = ttk.Label(readings_frame, textvariable=self.voltage_var, font=('Arial', 11, 'bold'))
        voltage_label.grid(row=0, column=0, sticky='w', padx=(3, 8), pady=3)
        voltage_value.grid(row=0, column=1, sticky='w', padx=(0, 15), pady=3)
        
        # Current display with responsive font sizes
        self.current_var = tk.StringVar(value="0.00 A")
        current_label = ttk.Label(readings_frame, text="Current:", font=('Arial', 9))
        current_value = ttk.Label(readings_frame, textvariable=self.current_var, font=('Arial', 11, 'bold'))
        current_label.grid(row=0, column=2, sticky='w', padx=(3, 8), pady=3)
        current_value.grid(row=0, column=3, sticky='w', padx=(0, 15), pady=3)
        
        # Temperature display with responsive font sizes
        self.temp_var = tk.StringVar(value="0.0 °C")
        temp_label = ttk.Label(readings_frame, text="Temperature:", font=('Arial', 9))
        temp_value = ttk.Label(readings_frame, textvariable=self.temp_var, font=('Arial', 11, 'bold'))
        temp_label.grid(row=1, column=0, sticky='w', padx=(3, 8), pady=3)
        temp_value.grid(row=1, column=1, sticky='w', padx=(0, 15), pady=3)
        
        # Power display with responsive font sizes
        self.power_var = tk.StringVar(value="0.0 W")
        power_label = ttk.Label(readings_frame, text="Power:", font=('Arial', 9))
        power_value = ttk.Label(readings_frame, textvariable=self.power_var, font=('Arial', 11, 'bold'))
        power_label.grid(row=1, column=2, sticky='w', padx=(3, 8), pady=3)
        power_value.grid(row=1, column=3, sticky='w', padx=(0, 15), pady=3)
        
        # Last update display with responsive font sizes
        self.update_var = tk.StringVar(value="Never")
        update_label = ttk.Label(readings_frame, text="Last Update:", font=('Arial', 8))
        update_value = ttk.Label(readings_frame, textvariable=self.update_var, font=('Arial', 8))
        update_label.grid(row=2, column=0, sticky='w', padx=(3, 8), pady=3)
        update_value.grid(row=2, column=1, sticky='w', padx=(0, 15), pady=3)
        
        # Real-time chart
        self.setup_chart()
    
    def setup_chart(self):
        """Setup real-time chart"""
        # Create matplotlib figure with 3 subplots and better spacing
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(11, 7))
        # No suptitle needed - clean layout with individual chart titles
        
        # Get colors for enhanced styling
        colors = theme_manager.get_matplotlib_colors()
        
        # Voltage plot with responsive styling and smooth lines
        self.ax1.set_title('⚡ Voltage (V)', fontsize=10, pad=6, weight='bold')
        self.ax1.set_ylabel('Voltage (V)', fontsize=8, weight='bold')
        self.voltage_line, = self.ax1.plot([], [], color=colors['voltage_color'], linewidth=2.0, alpha=0.8, linestyle='-', marker='', markersize=0)
        self.ax1.grid(True, alpha=0.3, linestyle='--')
        self.ax1.tick_params(labelsize=7)
        
        # Current plot with responsive styling and smooth lines
        self.ax2.set_title('🔌 Current (A)', fontsize=10, pad=6, weight='bold')
        self.ax2.set_ylabel('Current (A)', fontsize=8, weight='bold')
        self.current_line, = self.ax2.plot([], [], color=colors['current_color'], linewidth=2.0, alpha=0.8, linestyle='-', marker='', markersize=0)
        self.ax2.grid(True, alpha=0.3, linestyle='--')
        self.ax2.tick_params(labelsize=7)
        
        # Temperature plot with responsive styling and smooth lines
        self.ax3.set_title('🌡️ Temperature (°C)', fontsize=10, pad=6, weight='bold')
        self.ax3.set_ylabel('Temperature (°C)', fontsize=8, weight='bold')
        self.ax3.set_xlabel('Time', fontsize=8, weight='bold')
        self.temp_line, = self.ax3.plot([], [], color=colors['temp_color'], linewidth=2.0, alpha=0.8, linestyle='-', marker='', markersize=0)
        self.ax3.grid(True, alpha=0.3, linestyle='--')
        self.ax3.tick_params(labelsize=7)
        
        # Responsive layout that prevents text overlap on smaller screens
        self.fig.tight_layout(pad=1.0, h_pad=0.6)
        self.fig.subplots_adjust(bottom=0.08, top=0.94, left=0.10, right=0.96)
        
        # Embed in tkinter with optimized spacing
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=8, pady=(3, 10))
        
        # Apply initial theme
        self.apply_theme()
    
    def start_animation(self):
        """Start real-time animation"""
        self.animation = FuncAnimation(self.fig, self.update_chart, interval=1000, blit=False, cache_frame_data=False)
        print("🔄 Started live data animation")
    
    def update_chart(self, frame):
        """Update chart with new data"""
        try:
            # Get latest data
            latest = self.data_manager.get_latest_data()
            
            if latest and latest.get('timestamp'):
                # Calculate power
                power = latest['voltage'] * latest['current']
                
                # Update text displays
                self.voltage_var.set(f"{latest['voltage']:.2f} V")
                self.current_var.set(f"{latest['current']:.2f} A")
                self.temp_var.set(f"{latest['temperature']:.1f} °C")
                self.power_var.set(f"{power:.2f} W")
                self.update_var.set(latest['timestamp'].strftime("%H:%M:%S"))
                
                # Add to data collections
                current_time = latest['timestamp']
                self.time_data.append(current_time)
                self.voltage_data.append(latest['voltage'])
                self.current_data.append(latest['current'])
                self.temp_data.append(latest['temperature'])
                
                # Update plots
                if len(self.time_data) > 1:
                    self.voltage_line.set_data(list(self.time_data), list(self.voltage_data))
                    self.current_line.set_data(list(self.time_data), list(self.current_data))
                    self.temp_line.set_data(list(self.time_data), list(self.temp_data))
                    
                    # Auto-scale axes
                    self.ax1.relim()
                    self.ax1.autoscale_view()
                    self.ax2.relim()
                    self.ax2.autoscale_view()
                    self.ax3.relim()
                    self.ax3.autoscale_view()
                    
                    # Format x-axis with responsive sizing for smaller screens
                    self.ax3.tick_params(axis='x', rotation=45, labelsize=7)
                    self.ax1.tick_params(axis='x', labelbottom=False)
                    self.ax2.tick_params(axis='x', labelbottom=False)
                    
                    # Force canvas update
                    self.canvas.draw_idle()
            else:
                # No data available yet
                if frame % 10 == 0:  # Print every 10 frames to avoid spam
                    print("⏳ Waiting for sensor data...")
        
        except Exception as e:
            print(f"Error updating live chart: {e}")
        
        return self.voltage_line, self.current_line, self.temp_line
    
    def apply_theme(self):
        """Apply current theme to charts and widgets with enhanced styling"""
        colors = theme_manager.get_matplotlib_colors()
        theme = theme_manager.get_current_theme()
        
        # Update figure and axes colors with enhanced styling
        self.fig.patch.set_facecolor(colors['figure_bg'])
        
        # Enhanced chart styling
        chart_configs = [
            (self.ax1, self.voltage_line, colors['voltage_color'], '⚡ Voltage (V)'),
            (self.ax2, self.current_line, colors['current_color'], '🔌 Current (A)'),
            (self.ax3, self.temp_line, colors['temp_color'], '🌡️ Temperature (°C)')
        ]
        
        for ax, line, line_color, title in chart_configs:
            ax.set_facecolor(colors['axes_bg'])
            ax.tick_params(colors=colors['text_color'], labelsize=8)
            ax.xaxis.label.set_color(colors['text_color'])
            ax.yaxis.label.set_color(colors['text_color'])
            # Enhanced title styling with maximum contrast for dark mode
            title_color = '#ffffff' if theme_manager.is_dark_mode else '#212529'
            ax.title.set_color(title_color)
            ax.title.set_text(title)
            ax.title.set_fontweight('bold')
            ax.title.set_bbox(dict(boxstyle="round,pad=0.3", 
                                 facecolor=colors['axes_bg'], 
                                 edgecolor='none', 
                                 alpha=0.8))
            ax.grid(True, alpha=0.3, color=colors['grid_color'], linestyle='--')
            
            # Enhanced spine styling
            for spine in ax.spines.values():
                spine.set_color(colors['text_color'])
                spine.set_alpha(0.7)
            
            # Update line colors
            line.set_color(line_color)
            line.set_linewidth(2.5)
            line.set_alpha(0.9)
        
        # No suptitle needed - individual chart titles are sufficient
        
        # Apply theme to tkinter widgets
        try:
            theme_manager.configure_widget(self.frame, 'frame')
        except:
            pass
        
        # Force canvas refresh to apply theme changes immediately
        if hasattr(self, 'canvas'):
            try:
                self.canvas.draw()  # Force immediate redraw instead of idle
                self.canvas.flush_events()  # Ensure all events are processed
            except Exception as e:
                print(f"Canvas refresh warning: {e}")
"""
Theme Manager for Dark/Light Mode Toggle
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib import style

class ThemeManager:
    def __init__(self):
        self.is_dark_mode = False
        self.callbacks = []
        
        # Define enhanced color schemes with hybrid colors
        self.light_theme = {
            'bg': '#f8f9fa',  # Soft white background
            'fg': '#212529',  # Dark gray text
            'select_bg': '#007bff',  # Modern blue
            'select_fg': '#ffffff',
            'entry_bg': '#ffffff',
            'entry_fg': '#495057',
            'button_bg': '#007bff',  # Blue button for better visibility
            'button_fg': '#ffffff',  # White text for contrast
            'frame_bg': '#ffffff',  # Pure white frames
            'label_bg': '#f8f9fa',
            'label_fg': '#343a40',
            'accent': '#28a745',  # Green accent
            'accent2': '#17a2b8',  # Cyan accent
            'accent3': '#ffc107',  # Yellow accent
            'warning': '#fd7e14',  # Orange warning
            'danger': '#dc3545',  # Red danger
            'card_bg': '#ffffff',
            'border': '#dee2e6',
            'shadow': '#00000010'
        }
        
        self.dark_theme = {
            'bg': '#1a1d23',  # Deep dark blue-gray
            'fg': '#e9ecef',  # Light gray text
            'select_bg': '#0d6efd',  # Bright blue
            'select_fg': '#ffffff',
            'entry_bg': '#2d3748',  # Dark gray input
            'entry_fg': '#e2e8f0',
            'button_bg': '#1e40af',  # Dark blue button for maximum contrast
            'button_fg': '#ffffff',  # Pure white text for maximum visibility
            'frame_bg': '#1f2937',  # Dark frame
            'label_bg': '#1a1d23',
            'label_fg': '#cbd5e0',
            'accent': '#10b981',  # Emerald green
            'accent2': '#06b6d4',  # Cyan
            'accent3': '#f59e0b',  # Amber
            'warning': '#f97316',  # Orange
            'danger': '#ef4444',  # Red
            'card_bg': '#1f2937',
            'border': '#374151',
            'shadow': '#00000030'
        }
    
    def get_current_theme(self):
        """Get current theme colors"""
        return self.dark_theme if self.is_dark_mode else self.light_theme
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()
        
        # Notify all registered callbacks
        for callback in self.callbacks:
            callback(self.is_dark_mode)
    
    def register_callback(self, callback):
        """Register a callback to be called when theme changes"""
        self.callbacks.append(callback)
    
    def apply_theme(self):
        """Apply current theme to matplotlib with proper figure updates"""
        if self.is_dark_mode:
            plt.style.use('dark_background')
            # Set matplotlib rcParams for dark theme
            plt.rcParams.update({
                'figure.facecolor': '#1a1d23',
                'axes.facecolor': '#1f2937',
                'axes.edgecolor': '#e9ecef',
                'axes.labelcolor': '#e9ecef',
                'text.color': '#e9ecef',
                'xtick.color': '#e9ecef',
                'ytick.color': '#e9ecef',
                'grid.color': '#374151',
                'axes.spines.left': True,
                'axes.spines.bottom': True,
                'axes.spines.top': True,
                'axes.spines.right': True
            })
        else:
            plt.style.use('default')
            # Set matplotlib rcParams for light theme
            plt.rcParams.update({
                'figure.facecolor': '#f8f9fa',
                'axes.facecolor': '#ffffff',
                'axes.edgecolor': '#212529',
                'axes.labelcolor': '#212529',
                'text.color': '#212529',
                'xtick.color': '#212529',
                'ytick.color': '#212529',
                'grid.color': '#dee2e6',
                'axes.spines.left': True,
                'axes.spines.bottom': True,
                'axes.spines.top': True,
                'axes.spines.right': True
            })
    
    def configure_widget(self, widget, widget_type='default'):
        """Configure a widget with current theme"""
        theme = self.get_current_theme()
        
        try:
            if widget_type == 'frame':
                widget.configure(bg=theme['frame_bg'])
            elif widget_type == 'label':
                widget.configure(bg=theme['label_bg'], fg=theme['label_fg'])
            elif widget_type == 'button':
                widget.configure(bg=theme['button_bg'], fg=theme['button_fg'])
            elif widget_type == 'entry':
                widget.configure(bg=theme['entry_bg'], fg=theme['entry_fg'])
            else:
                # Default configuration
                if hasattr(widget, 'configure'):
                    widget.configure(bg=theme['bg'], fg=theme['fg'])
        except tk.TclError:
            # Some widgets don't support all options
            pass
    
    def get_matplotlib_colors(self):
        """Get colors for matplotlib plots with enhanced styling"""
        if self.is_dark_mode:
            return {
                'figure_bg': '#1a1d23',  # Deep background
                'axes_bg': '#1f2937',    # Slightly lighter for contrast
                'text_color': '#e9ecef',
                'grid_color': '#374151',
                'line_colors': ['#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'],  # Vibrant colors
                'voltage_color': '#06b6d4',    # Cyan for voltage
                'current_color': '#10b981',    # Green for current  
                'temp_color': '#f59e0b',       # Amber for temperature
                'power_color': '#ec4899'       # Pink for power
            }
        else:
            return {
                'figure_bg': '#f8f9fa',  # Soft background
                'axes_bg': '#ffffff',    # Pure white
                'text_color': '#212529',
                'grid_color': '#dee2e6',
                'line_colors': ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#e83e8c'],  # Modern colors
                'voltage_color': '#007bff',    # Blue for voltage
                'current_color': '#28a745',    # Green for current
                'temp_color': '#fd7e14',       # Orange for temperature  
                'power_color': '#e83e8c'       # Pink for power
            }
    
    def get_gradient_colors(self):
        """Get gradient colors for enhanced UI elements"""
        if self.is_dark_mode:
            return {
                'primary_start': '#0d6efd',
                'primary_end': '#0a58ca',
                'success_start': '#10b981',
                'success_end': '#059669',
                'warning_start': '#f59e0b',
                'warning_end': '#d97706',
                'danger_start': '#ef4444',
                'danger_end': '#dc2626'
            }
        else:
            return {
                'primary_start': '#007bff',
                'primary_end': '#0056b3',
                'success_start': '#28a745',
                'success_end': '#1e7e34',
                'warning_start': '#ffc107',
                'warning_end': '#e0a800',
                'danger_start': '#dc3545',
                'danger_end': '#c82333'
            }

# Global theme manager instance
theme_manager = ThemeManager()
"""
Predictions Page - Future data predictions using machine learning
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme_manager import theme_manager

class PredictionsPage:
    def __init__(self, parent, data_manager):
        self.parent = parent
        self.data_manager = data_manager
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        
        # Prediction models
        self.voltage_model = None
        self.current_model = None
        self.temp_model = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = ttk.Label(self.frame, text="Predictive Analytics", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Controls frame with better organization
        controls_frame = ttk.LabelFrame(self.frame, text="Prediction Settings", padding=10)
        controls_frame.pack(fill='x', padx=15, pady=5)
        
        # Configure grid for better alignment
        controls_frame.columnconfigure(2, weight=1)
        controls_frame.columnconfigure(5, weight=1)
        
        # Row 1: Main prediction controls
        ttk.Label(controls_frame, text="Predict:", font=('Arial', 9, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.predict_minutes_var = tk.StringVar(value="10")
        minutes_combo = ttk.Combobox(controls_frame, textvariable=self.predict_minutes_var,
                                   values=["1", "5", "10", "15", "30", "60"], width=6)
        minutes_combo.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        minutes_combo.bind('<<ComboboxSelected>>', lambda e: self.generate_predictions())
        
        ttk.Label(controls_frame, text="minutes").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        
        ttk.Label(controls_frame, text="Data Points:", font=('Arial', 9, 'bold')).grid(row=0, column=3, padx=(20, 5), pady=5, sticky='w')
        
        self.data_range_var = tk.StringVar(value="100")
        data_combo = ttk.Combobox(controls_frame, textvariable=self.data_range_var,
                                values=["50", "100", "200", "500"], width=6)
        data_combo.grid(row=0, column=4, padx=5, pady=5, sticky='w')
        data_combo.bind('<<ComboboxSelected>>', lambda e: self.generate_predictions())
        
        ttk.Label(controls_frame, text="records").grid(row=0, column=5, padx=5, pady=5, sticky='w')
        
        # Row 2: Model and view controls
        ttk.Label(controls_frame, text="Model:", font=('Arial', 9, 'bold')).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        self.model_var = tk.StringVar(value="Polynomial")
        model_combo = ttk.Combobox(controls_frame, textvariable=self.model_var,
                                  values=["Linear", "Polynomial", "Advanced"], width=10)
        model_combo.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        model_combo.bind('<<ComboboxSelected>>', lambda e: self.generate_predictions())
        
        ttk.Label(controls_frame, text="View:", font=('Arial', 9, 'bold')).grid(row=1, column=3, padx=(20, 5), pady=5, sticky='w')
        
        self.zoom_var = tk.StringVar(value="Auto")
        zoom_combo = ttk.Combobox(controls_frame, textvariable=self.zoom_var,
                                values=["Auto", "Last 1H", "Last 6H", "All Data"], width=10)
        zoom_combo.grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky='w')
        zoom_combo.bind('<<ComboboxSelected>>', lambda e: self.generate_predictions())
        
        # Row 3: Action buttons
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.grid(row=2, column=0, columnspan=6, pady=10, sticky='w')
        
        predict_btn = ttk.Button(buttons_frame, text="🚀 Generate Predictions", 
                               command=self.generate_predictions)
        predict_btn.pack(side='left', padx=5)
        
        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_check = ttk.Checkbutton(buttons_frame, text="Auto-refresh (10s)", 
                                   variable=self.auto_refresh_var, command=self.toggle_auto_refresh)
        auto_check.pack(side='left', padx=20)
        
        # Prediction chart
        self.setup_chart()
        
        # Start auto-refresh timer
        self.auto_refresh_timer = None
        self.toggle_auto_refresh()
        
        # Generate initial predictions
        self.generate_predictions()
    

    
    def setup_chart(self):
        """Setup prediction chart with proper sizing and no redundant titles"""
        # Create matplotlib figure with better sizing
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(12, 8))
        
        # Get colors for styling
        colors = theme_manager.get_matplotlib_colors()
        
        # Voltage plot with responsive spacing
        self.ax1.set_title('⚡ Voltage Prediction', fontsize=11, pad=8, weight='bold')
        self.ax1.set_ylabel('Voltage (V)', fontsize=9, weight='bold')
        self.ax1.grid(True, alpha=0.4, linestyle='--')
        self.ax1.tick_params(labelsize=8)
        self.ax1.set_ylim(2.5, 6.0)
        import numpy as np
        self.ax1.set_yticks(np.arange(2.5, 6.5, 0.5))
        
        # Current plot with responsive spacing
        self.ax2.set_title('🔌 Current Prediction', fontsize=11, pad=8, weight='bold')
        self.ax2.set_ylabel('Current (A)', fontsize=9, weight='bold')
        self.ax2.grid(True, alpha=0.4, linestyle='--')
        self.ax2.tick_params(labelsize=8)
        self.ax2.set_ylim(0, 3.0)
        self.ax2.set_yticks(np.arange(0, 3.5, 0.5))
        
        # Temperature plot with responsive spacing
        self.ax3.set_title('🌡️ Temperature Prediction', fontsize=11, pad=8, weight='bold')
        self.ax3.set_ylabel('Temperature (°C)', fontsize=9, weight='bold')
        self.ax3.set_xlabel('Time', fontsize=9, weight='bold')
        self.ax3.grid(True, alpha=0.4, linestyle='--')
        self.ax3.tick_params(labelsize=8)
        self.ax3.set_ylim(15, 40)
        
        # Responsive layout that prevents text overlap on smaller screens
        self.fig.tight_layout(pad=1.2, h_pad=0.8)
        self.fig.subplots_adjust(bottom=0.10, top=0.94, left=0.10, right=0.96)
        
        # Embed in tkinter with optimized spacing
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True, padx=8, pady=(3, 15))
        
        # Add navigation toolbar with minimal spacing
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar_frame = ttk.Frame(self.frame)
        toolbar_frame.pack(fill='x', padx=8, pady=(0, 5))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        
        # Apply initial theme
        self.apply_theme()
    
    def generate_predictions(self):
        """Generate enhanced predictions with 30-minute focus and smart data handling"""
        try:
            # Get historical data based on user selection
            data_range = self.data_range_var.get()
            if data_range == "All":
                data = self.data_manager.get_historical_data(10000)  # Get all available data
            else:
                data = self.data_manager.get_historical_data(int(data_range))
            
            if len(data) < 10:  # Need minimum data for predictions
                self.show_insufficient_data()
                return
            
            # Convert to DataFrame and clean data
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Remove outliers and invalid data
            df = self.clean_data(df)
            
            if len(df) < 10:
                self.show_insufficient_data()
                return
            
            # Prepare data for ML with enhanced features
            X, y_voltage, y_current, y_temp = self.prepare_enhanced_data(df)
            
            # Train enhanced models
            self.train_enhanced_models(X, y_voltage, y_current, y_temp)
            
            # Generate predictions with 30-minute focus
            predictions = self.predict_future_enhanced(df)
            
            # Update chart with zoom functionality
            self.update_enhanced_chart(df, predictions)
            
            # Model info removed for cleaner interface
            print(f"✅ Generated predictions using {len(df)} data points with {self.model_var.get()} model")
            
        except Exception as e:
            print(f"Error generating predictions: {e}")
            self.show_error_message(str(e))
    
    def clean_data(self, df):
        """Clean and filter data for better predictions"""
        # Remove rows with all zeros (inactive periods)
        df = df[(df['voltage'] != 0) | (df['current'] != 0) | (df['temperature'] != 0)]
        
        # Remove extreme outliers using IQR method
        for column in ['voltage', 'current', 'temperature']:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        
        return df
    
    def prepare_enhanced_data(self, df):
        """Prepare enhanced data for machine learning with time-based features"""
        # Convert timestamps to minutes since first reading for better 30-min predictions
        start_time = df['timestamp'].iloc[0]
        df['minutes'] = (df['timestamp'] - start_time).dt.total_seconds() / 60
        
        # Add time-based features for better predictions
        df['hour_of_day'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['minute_of_hour'] = df['timestamp'].dt.minute
        
        # Create feature matrix with multiple time scales
        X = np.column_stack([
            df['minutes'].values,
            df['hour_of_day'].values,
            df['minute_of_hour'].values,
            np.sin(2 * np.pi * df['hour_of_day'] / 24),  # Cyclical hour feature
            np.cos(2 * np.pi * df['hour_of_day'] / 24)
        ])
        
        y_voltage = df['voltage'].values
        y_current = df['current'].values
        y_temp = df['temperature'].values
        
        return X, y_voltage, y_current, y_temp
    
    def prepare_data(self, df):
        """Prepare data for machine learning (legacy method for compatibility)"""
        return self.prepare_enhanced_data(df)
    
    def train_enhanced_models(self, X, y_voltage, y_current, y_temp):
        """Train enhanced prediction models with better algorithms"""
        model_type = self.model_var.get()
        
        if model_type == "Advanced":
            # Advanced models with regularization
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.linear_model import Ridge
            
            self.voltage_model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=10)
            self.current_model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=10)
            self.temp_model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=10)
            
        elif model_type == "Polynomial":
            # Enhanced polynomial regression with regularization
            from sklearn.linear_model import Ridge
            self.voltage_model = Pipeline([
                ('poly', PolynomialFeatures(degree=3, include_bias=False)),
                ('ridge', Ridge(alpha=0.1))
            ])
            self.current_model = Pipeline([
                ('poly', PolynomialFeatures(degree=3, include_bias=False)),
                ('ridge', Ridge(alpha=0.1))
            ])
            self.temp_model = Pipeline([
                ('poly', PolynomialFeatures(degree=3, include_bias=False)),
                ('ridge', Ridge(alpha=0.1))
            ])
        else:
            # Enhanced linear regression with regularization
            from sklearn.linear_model import Ridge
            self.voltage_model = Ridge(alpha=0.1)
            self.current_model = Ridge(alpha=0.1)
            self.temp_model = Ridge(alpha=0.1)
        
        # Train models
        self.voltage_model.fit(X, y_voltage)
        self.current_model.fit(X, y_current)
        self.temp_model.fit(X, y_temp)
    
    def train_models(self, X, y_voltage, y_current, y_temp):
        """Train prediction models (legacy method for compatibility)"""
        return self.train_enhanced_models(X, y_voltage, y_current, y_temp)
    
    def predict_future_enhanced(self, df):
        """Generate enhanced future predictions with 30-minute focus"""
        predict_minutes = int(self.predict_minutes_var.get())
        
        # Get time range for predictions
        last_time = df['timestamp'].iloc[-1]
        start_time = df['timestamp'].iloc[0]
        
        # Create future time points with higher resolution for 30-minute predictions
        future_times = []
        future_features = []
        
        # Generate predictions with adaptive time step for smoother curves
        if predict_minutes <= 10:
            time_step = 1  # 1-minute steps for short predictions
        elif predict_minutes <= 30:
            time_step = 2  # 2-minute steps for medium predictions
        else:
            time_step = 5  # 5-minute steps for longer predictions
        
        num_steps = predict_minutes // time_step
        
        for i in range(1, num_steps + 1):
            future_time = last_time + timedelta(minutes=i * time_step)
            future_times.append(future_time)
            
            # Calculate features for future time
            minutes_since_start = (future_time - start_time).total_seconds() / 60
            hour_of_day = future_time.hour
            minute_of_hour = future_time.minute
            
            features = [
                minutes_since_start,
                hour_of_day,
                minute_of_hour,
                np.sin(2 * np.pi * hour_of_day / 24),
                np.cos(2 * np.pi * hour_of_day / 24)
            ]
            future_features.append(features)
        
        # Make predictions
        X_future = np.array(future_features)
        voltage_pred = self.voltage_model.predict(X_future)
        current_pred = self.current_model.predict(X_future)
        temp_pred = self.temp_model.predict(X_future)
        
        # Clamp predictions to realistic ranges (same as other pages)
        voltage_pred = np.clip(voltage_pred, 2.5, 6.0)  # Realistic voltage range
        current_pred = np.clip(current_pred, 0.0, 3.0)  # Realistic current range
        temp_pred = np.clip(temp_pred, 15.0, 40.0)      # Realistic temperature range
        
        # Add confidence intervals (simple approach using recent variance)
        recent_data = df.tail(50)  # Last 50 points for variance calculation
        voltage_std = recent_data['voltage'].std()
        current_std = recent_data['current'].std()
        temp_std = recent_data['temperature'].std()
        
        return {
            'times': future_times,
            'voltage': voltage_pred,
            'current': current_pred,
            'temperature': temp_pred,
            'voltage_confidence': voltage_std,
            'current_confidence': current_std,
            'temp_confidence': temp_std
        }
    
    def predict_future(self, df):
        """Generate future predictions (legacy method for compatibility)"""
        return self.predict_future_enhanced(df)
    
    def update_enhanced_chart(self, historical_df, predictions):
        """Update prediction chart with enhanced features and zoom functionality"""
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        # Get enhanced colors
        colors = theme_manager.get_matplotlib_colors()
        
        # Apply zoom settings
        zoom_df = self.apply_zoom_filter(historical_df)
        
        # Plot historical data with smooth, blended lines
        self.ax1.plot(zoom_df['timestamp'], zoom_df['voltage'], 
                     color=colors['voltage_color'], label='📊 Historical Data', linewidth=2.0, alpha=0.7,
                     linestyle='-', marker='', markersize=0)
        self.ax2.plot(zoom_df['timestamp'], zoom_df['current'], 
                     color=colors['current_color'], label='📊 Historical Data', linewidth=2.0, alpha=0.7,
                     linestyle='-', marker='', markersize=0)
        self.ax3.plot(zoom_df['timestamp'], zoom_df['temperature'], 
                     color=colors['temp_color'], label='📊 Historical Data', linewidth=2.0, alpha=0.7,
                     linestyle='-', marker='', markersize=0)
        
        # Plot predictions with smooth, blended lines
        pred_color_v = '#ff6b6b' if theme_manager.is_dark_mode else '#e74c3c'
        pred_color_c = '#4ecdc4' if theme_manager.is_dark_mode else '#16a085'
        pred_color_t = '#45b7d1' if theme_manager.is_dark_mode else '#3498db'
        
        self.ax1.plot(predictions['times'], predictions['voltage'], 
                     color=pred_color_v, linestyle='-', label='🔮 30-Min Prediction', 
                     linewidth=2.5, alpha=0.8, marker='', markersize=0)
        self.ax2.plot(predictions['times'], predictions['current'], 
                     color=pred_color_c, linestyle='-', label='🔮 30-Min Prediction', 
                     linewidth=2.5, alpha=0.8, marker='', markersize=0)
        self.ax3.plot(predictions['times'], predictions['temperature'], 
                     color=pred_color_t, linestyle='-', label='🔮 30-Min Prediction', 
                     linewidth=2.5, alpha=0.8, marker='', markersize=0)
        
        # Add confidence bands if available
        if 'voltage_confidence' in predictions:
            voltage_upper = predictions['voltage'] + predictions['voltage_confidence']
            voltage_lower = predictions['voltage'] - predictions['voltage_confidence']
            self.ax1.fill_between(predictions['times'], voltage_lower, voltage_upper, 
                                alpha=0.2, color=pred_color_v, label='Confidence Band')
            
            current_upper = predictions['current'] + predictions['current_confidence']
            current_lower = predictions['current'] - predictions['current_confidence']
            self.ax2.fill_between(predictions['times'], current_lower, current_upper, 
                                alpha=0.2, color=pred_color_c, label='Confidence Band')
            
            temp_upper = predictions['temperature'] + predictions['temp_confidence']
            temp_lower = predictions['temperature'] - predictions['temp_confidence']
            self.ax3.fill_between(predictions['times'], temp_lower, temp_upper, 
                                alpha=0.2, color=pred_color_t, label='Confidence Band')
        
        # Add vertical line at prediction start with better styling
        if len(predictions['times']) > 0:
            prediction_start = predictions['times'][0]
            line_color = '#ffd700' if theme_manager.is_dark_mode else '#f39c12'
            self.ax1.axvline(x=prediction_start, color=line_color, linestyle=':', alpha=0.8, linewidth=2, label='Prediction Start')
            self.ax2.axvline(x=prediction_start, color=line_color, linestyle=':', alpha=0.8, linewidth=2)
            self.ax3.axvline(x=prediction_start, color=line_color, linestyle=':', alpha=0.8, linewidth=2)
        
        # Enhanced formatting with responsive spacing to prevent text overlap
        self.ax1.set_title('⚡ Voltage Prediction', fontsize=11, weight='bold', pad=8)
        self.ax1.set_ylabel('Voltage (V)', fontsize=9, weight='bold')
        self.ax1.grid(True, alpha=0.3, linestyle='--')
        self.ax1.legend(fontsize=8, framealpha=0.9, loc='upper left')
        # Set realistic voltage scale (2.5V to 6V) with 0.5V increments
        self.ax1.set_ylim(2.5, 6.0)
        self.ax1.set_yticks(np.arange(2.5, 6.5, 0.5))
        
        self.ax2.set_title('🔌 Current Prediction', fontsize=11, weight='bold', pad=8)
        self.ax2.set_ylabel('Current (A)', fontsize=9, weight='bold')
        self.ax2.grid(True, alpha=0.3, linestyle='--')
        self.ax2.legend(fontsize=8, framealpha=0.9, loc='upper left')
        # Set realistic current scale (0A to 3A) with 0.5A increments
        self.ax2.set_ylim(0, 3.0)
        self.ax2.set_yticks(np.arange(0, 3.5, 0.5))
        
        self.ax3.set_title('🌡️ Temperature Prediction', fontsize=11, weight='bold', pad=8)
        self.ax3.set_ylabel('Temperature (°C)', fontsize=9, weight='bold')
        self.ax3.set_xlabel('Time', fontsize=9, weight='bold')
        self.ax3.grid(True, alpha=0.3, linestyle='--')
        self.ax3.legend(fontsize=8, framealpha=0.9, loc='upper left')
        # Set realistic temperature scale (15°C to 40°C)
        self.ax3.set_ylim(15, 40)
        
        # Format x-axis with responsive spacing to prevent overlap
        self.ax3.tick_params(axis='x', rotation=45, labelsize=8)
        self.ax1.tick_params(axis='x', labelbottom=False, labelsize=8)
        self.ax2.tick_params(axis='x', labelbottom=False, labelsize=8)
        self.ax1.tick_params(axis='y', labelsize=8)
        self.ax2.tick_params(axis='y', labelsize=8)
        self.ax3.tick_params(axis='y', labelsize=8)
        
        # Maintain responsive layout that prevents text overlap
        self.fig.subplots_adjust(left=0.10, right=0.96, top=0.94, bottom=0.10, hspace=0.3)
        self.canvas.draw()
    
    def apply_zoom_filter(self, df):
        """Apply zoom filter based on user selection"""
        zoom_setting = self.zoom_var.get()
        
        if zoom_setting == "Last Hour":
            cutoff_time = df['timestamp'].max() - timedelta(hours=1)
            return df[df['timestamp'] >= cutoff_time]
        elif zoom_setting == "Last 6H":
            cutoff_time = df['timestamp'].max() - timedelta(hours=6)
            return df[df['timestamp'] >= cutoff_time]
        elif zoom_setting == "Last 24H":
            cutoff_time = df['timestamp'].max() - timedelta(hours=24)
            return df[df['timestamp'] >= cutoff_time]
        elif zoom_setting == "All Data":
            return df
        else:  # Auto
            # Auto-select based on data amount
            if len(df) > 1000:
                cutoff_time = df['timestamp'].max() - timedelta(hours=6)
                return df[df['timestamp'] >= cutoff_time]
            else:
                return df
    
    def update_chart(self, historical_df, predictions):
        """Update prediction chart (legacy method for compatibility)"""
        return self.update_enhanced_chart(historical_df, predictions)
    

    
    def apply_theme(self):
        """Apply current theme with perfect dark/light mode compatibility"""
        colors = theme_manager.get_matplotlib_colors()
        theme = theme_manager.get_current_theme()
        
        # Update figure background for dark/light mode
        self.fig.patch.set_facecolor(colors['figure_bg'])
        
        # Enhanced chart styling with perfect dark mode support
        chart_configs = [
            (self.ax1, '⚡ Voltage Prediction', (2.5, 6.0)),
            (self.ax2, '🔌 Current Prediction', (0, 3.0)),
            (self.ax3, '🌡️ Temperature Prediction', (15, 40))
        ]
        
        for i, (ax, title, y_range) in enumerate(chart_configs):
            # Set background colors for dark/light mode
            ax.set_facecolor(colors['axes_bg'])
            
            # Enhanced text colors for perfect visibility in both modes
            ax.tick_params(colors=colors['text_color'], labelsize=10, 
                          which='both', direction='out', length=4, width=1)
            ax.xaxis.label.set_color(colors['text_color'])
            ax.yaxis.label.set_color(colors['text_color'])
            
            # Enhanced title styling with maximum contrast for dark mode
            title_color = '#ffffff' if theme_manager.is_dark_mode else '#212529'
            ax.title.set_color(title_color)
            ax.title.set_text(title)
            ax.title.set_fontweight('bold')
            ax.title.set_fontsize(13)
            ax.title.set_bbox(dict(boxstyle="round,pad=0.3", 
                                 facecolor=colors['axes_bg'], 
                                 edgecolor='none', 
                                 alpha=0.8))
            
            # Enhanced grid with better dark mode visibility
            grid_alpha = 0.6 if theme_manager.is_dark_mode else 0.4
            ax.grid(True, alpha=grid_alpha, color=colors['grid_color'], 
                   linestyle='--', linewidth=0.8)
            
            # Set realistic scales consistent with other pages
            ax.set_ylim(y_range[0], y_range[1])
            
            # Set custom tick spacing for voltage and current (0.5 increments)
            if i == 0:  # Voltage
                ax.set_yticks(np.arange(2.5, 6.5, 0.5))
            elif i == 1:  # Current
                ax.set_yticks(np.arange(0, 3.5, 0.5))
            # Temperature keeps default ticks for better readability
            
            # Enhanced spine styling with better dark mode support
            spine_alpha = 0.9 if theme_manager.is_dark_mode else 0.7
            for spine in ax.spines.values():
                spine.set_color(colors['text_color'])
                spine.set_alpha(spine_alpha)
                spine.set_linewidth(1.2)
            
            # Update legend styling with dark mode support
            legend = ax.get_legend()
            if legend:
                legend.get_frame().set_facecolor(colors['axes_bg'])
                legend.get_frame().set_alpha(0.95)
                legend.get_frame().set_edgecolor(colors['text_color'])
                legend.get_frame().set_linewidth(0.8)
                for text in legend.get_texts():
                    text.set_color(colors['text_color'])
                    text.set_fontsize(9)
        
        # No suptitle needed - individual chart titles are sufficient
        
        # Apply theme to tkinter widgets with enhanced dark mode support
        try:
            theme_manager.configure_widget(self.frame, 'frame')
            # Ensure toolbar also follows theme
            if hasattr(self, 'toolbar'):
                toolbar_bg = theme['bg'] if theme_manager.is_dark_mode else '#f0f0f0'
                self.toolbar.configure(bg=toolbar_bg)
        except Exception as e:
            print(f"Theme application warning: {e}")
        
        # Force canvas refresh to apply theme changes immediately
        if hasattr(self, 'canvas'):
            try:
                self.canvas.draw()  # Force immediate redraw instead of idle
                self.canvas.flush_events()  # Ensure all events are processed
            except Exception as e:
                print(f"Canvas refresh warning: {e}")
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality"""
        if self.auto_refresh_var.get():
            self.start_auto_refresh()
        else:
            self.stop_auto_refresh()
    
    def start_auto_refresh(self):
        """Start auto-refresh timer"""
        if self.auto_refresh_timer:
            self.frame.after_cancel(self.auto_refresh_timer)
        
        # Refresh every 10 seconds for more responsive updates
        self.auto_refresh_timer = self.frame.after(10000, self.auto_refresh_callback)
    
    def stop_auto_refresh(self):
        """Stop auto-refresh timer"""
        if self.auto_refresh_timer:
            self.frame.after_cancel(self.auto_refresh_timer)
            self.auto_refresh_timer = None
    
    def auto_refresh_callback(self):
        """Auto-refresh callback"""
        if self.auto_refresh_var.get():
            self.generate_predictions()
            self.start_auto_refresh()  # Schedule next refresh
    
    def show_insufficient_data(self):
        """Show enhanced message when insufficient data for predictions"""
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        colors = theme_manager.get_matplotlib_colors()
        text_color = colors['text_color']
        
        self.ax1.text(0.5, 0.5, '📊 Insufficient Data for Predictions\n\nNeed at least 10 data points\nCurrently collecting sensor data...', 
                     ha='center', va='center', transform=self.ax1.transAxes, fontsize=14, 
                     color=text_color, weight='bold')
        self.ax2.text(0.5, 0.5, '⏳ Collecting Data...\n\nPlease wait while the system\ngathers sensor readings', 
                     ha='center', va='center', transform=self.ax2.transAxes, fontsize=14,
                     color=text_color, weight='bold')
        self.ax3.text(0.5, 0.5, '🔄 Auto-refresh enabled\n\nPredictions will appear\nautomatically when ready', 
                     ha='center', va='center', transform=self.ax3.transAxes, fontsize=14,
                     color=text_color, weight='bold')
        
        # Apply theme to empty charts with realistic scales
        chart_configs = [
            (self.ax1, (2.5, 6.0)),
            (self.ax2, (0, 3.0)),
            (self.ax3, (15, 40))
        ]
        
        for i, (ax, y_range) in enumerate(chart_configs):
            ax.set_facecolor(colors['axes_bg'])
            ax.set_ylim(y_range[0], y_range[1])  # Set realistic scales
            
            # Set custom tick spacing for voltage and current (0.5 increments)
            if i == 0:  # Voltage
                ax.set_yticks(np.arange(2.5, 6.5, 0.5))
            elif i == 1:  # Current
                ax.set_yticks(np.arange(0, 3.5, 0.5))
            # Temperature keeps default ticks
            
            for spine in ax.spines.values():
                spine.set_color(colors['text_color'])
                spine.set_alpha(0.3)
        
        self.canvas.draw()
    
    def show_error_message(self, error_msg):
        """Show error message on charts"""
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        colors = theme_manager.get_matplotlib_colors()
        text_color = '#ff6b6b' if theme_manager.is_dark_mode else '#e74c3c'
        
        self.ax1.text(0.5, 0.5, f'❌ Prediction Error\n\n{error_msg}', 
                     ha='center', va='center', transform=self.ax1.transAxes, fontsize=12, 
                     color=text_color, weight='bold')
        self.ax2.text(0.5, 0.5, '🔧 Troubleshooting Tips:\n\n• Check data quality\n• Try different model\n• Reduce prediction time', 
                     ha='center', va='center', transform=self.ax2.transAxes, fontsize=11,
                     color=colors['text_color'])
        self.ax3.text(0.5, 0.5, '🔄 Click "Generate Predictions"\nto try again', 
                     ha='center', va='center', transform=self.ax3.transAxes, fontsize=12,
                     color=colors['text_color'], weight='bold')
        
        self.canvas.draw()
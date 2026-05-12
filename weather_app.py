import requests
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.ensemble import RandomForestClassifier
import pickle
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuration
API_KEY = "your_weather_api"  # Replace with your OpenWeatherMap API key
UNITS = "metric"  # "metric" for Celsius, "imperial" for Fahrenheit

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Weather Detection")
        self.setup_ui()
        self.load_model()
        
    def setup_ui(self):
        """Create graphical interface"""
        # Location Entry
        ttk.Label(self.root, text="Latitude:").grid(row=0, column=0, padx=5, pady=5)
        self.lat_entry = ttk.Entry(self.root)
        self.lat_entry.grid(row=0, column=1, padx=5, pady=5)
        self.lat_entry.insert(0, "51.5074")  # Default London
        
        ttk.Label(self.root, text="Longitude:").grid(row=1, column=0, padx=5, pady=5)
        self.lon_entry = ttk.Entry(self.root)
        self.lon_entry.grid(row=1, column=1, padx=5, pady=5)
        self.lon_entry.insert(0, "-0.1278")
        
        # Buttons
        ttk.Button(self.root, text="Get Current Weather", command=self.get_current).grid(row=2, column=0, columnspan=2)
        ttk.Button(self.root, text="5-Day Forecast", command=self.get_forecast).grid(row=3, column=0, columnspan=2)
        
        # Results Display
        self.result_text = tk.Text(self.root, height=15, width=60)
        self.result_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        # Alert System
        self.alert_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.alert_var, foreground="red").grid(row=5, column=0, columnspan=2)
        
        # Graph Frame
        self.graph_frame = ttk.Frame(self.root)
        self.graph_frame.grid(row=0, column=2, rowspan=6, padx=10)
        
    def load_model(self):
        """Load or create weather prediction model"""
        try:
            with open('weather_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
        except:
            self.train_model()
            
    def train_model(self):
        """Train weather prediction model with sample data"""
        training_data = {
            'temperature': [28, 15, 32, 10, 22, 18, 25, 8, 30, 12],  # Changed from 'temp'
            'humidity': [65, 85, 50, 70, 60, 80, 55, 90, 45, 75],
            'pressure': [1012, 1008, 1015, 1020, 1010, 1005, 1013, 1025, 1011, 1009],
            'wind_speed': [5, 12, 8, 3, 15, 20, 7, 2, 10, 18],
            'weather': ['Clear', 'Rain', 'Clear', 'Snow', 'Clouds', 'Rain', 'Clear', 'Snow', 'Clear', 'Rain']
        }
        df = pd.DataFrame(training_data)
        X = df.drop('weather', axis=1)
        y = df['weather']
        
        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X, y)
        
        with open('weather_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        print("Model trained and saved successfully!")

    def fetch_weather(self, lat, lon, forecast=False):
        """Fetch weather data from API"""
        endpoint = "forecast" if forecast else "weather"
        url = f"https://api.openweathermap.org/data/2.5/{endpoint}?lat={lat}&lon={lon}&appid={API_KEY}&units={UNITS}"
        
        try:
            response = requests.get(url).json()
            if response.get('cod') != 200 and response.get('cod') != "200":
                raise ValueError(f"API Error: {response.get('message', 'Unknown error')}")
            return response
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")
            return None
    
    def get_current(self):
        """Get and display current weather"""
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid coordinates")
            return
            
        data = self.fetch_weather(lat, lon)
        if not data:
            return
            
        # Extract current weather (using 'temperature' instead of 'temp')
        current = {
            'temperature': data['main']['temp'],  # Key changed to match training
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'weather': data['weather'][0]['main'],
            'time': datetime.fromtimestamp(data['dt'])
        }
        
        # Prepare features with CORRECT column names
        features = pd.DataFrame([[
            current['temperature'],
            current['humidity'],
            current['pressure'],
            current['wind_speed']
        ]], columns=['temperature', 'humidity', 'pressure', 'wind_speed'])  # Matches training
        
        # Make prediction
        try:
            prediction = self.model.predict(features)[0]
        except Exception as e:
            messagebox.showerror("Prediction Error", f"Model failed: {str(e)}")
            return
        
        # Display results
        result = (
            f"=== CURRENT WEATHER ===\n"
            f"Location: Latitude {lat}, Longitude {lon}\n"
            f"Time: {current['time']}\n"
            f"Temperature: {current['temperature']}°C\n"
            f"Humidity: {current['humidity']}%\n"
            f"Pressure: {current['pressure']} hPa\n"
            f"Wind Speed: {current['wind_speed']} m/s\n"
            f"Weather: {current['weather']}\n"
            f"Model Prediction: {prediction}\n"
        )
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)
        
        # Check for alerts
        self.check_alerts(current)
        
        # Plot current data
        self.plot_data([current], "Current Weather")
    
    def get_forecast(self):
        """Get and display 5-day forecast"""
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid coordinates")
            return
            
        data = self.fetch_weather(lat, lon, forecast=True)
        if not data:
            return
            
        # Process forecast data
        forecasts = []
        for item in data['list'][:40:8]:  # Get one forecast per day
            forecasts.append({
                'temperature': item['main']['temp'],  # Key changed to match training
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'],
                'weather': item['weather'][0]['main'],
                'time': datetime.fromtimestamp(item['dt'])
            })
        
        # Display forecast
        result = "=== 5-DAY FORECAST ===\n"
        for fc in forecasts:
            result += (
                f"\nDate: {fc['time'].strftime('%Y-%m-%d %H:%M')}\n"
                f"Temperature: {fc['temperature']}°C\n"
                f"Weather: {fc['weather']}\n"
                f"Humidity: {fc['humidity']}%\n"
            )
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)
        
        # Plot forecast
        self.plot_data(forecasts, "5-Day Forecast")
    
    def check_alerts(self, weather_data):
        """Generate weather alerts"""
        alerts = []
        if weather_data['temperature'] > 30:
            alerts.append("Heat Warning: High temperature")
        if weather_data['temperature'] < 0:
            alerts.append("Freeze Warning: Low temperature")
        if weather_data['wind_speed'] > 10:
            alerts.append("Wind Alert: Strong winds")
        if weather_data['weather'] in ['Rain', 'Snow']:
            alerts.append(f"Precipitation Alert: {weather_data['weather']} expected")
        
        if alerts:
            self.alert_var.set("\n".join(alerts))
        else:
            self.alert_var.set("No weather alerts")
    
    def plot_data(self, weather_data, title):
        """Visualize weather data"""
        # Clear previous graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Prepare data
        dates = [wd['time'] for wd in weather_data]
        temps = [wd['temperature'] for wd in weather_data]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dates, temps, marker='o')
        ax.set_title(title)
        ax.set_ylabel("Temperature (°C)")
        ax.grid(True)
        fig.autofmt_xdate()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop() 

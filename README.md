# 🌤️ Smart Weather Forecast App

A smart weather forecasting desktop application built with Python that uses **Machine Learning** and the **OpenWeatherMap API** to detect, predict, and visualize weather conditions in real time.

---

## 📌 Features

-  Get **real-time weather data** for any location using coordinates
-  View **5-Day weather forecast**
-  **ML-based weather prediction** using Random Forest Classifier
-  **Automatic weather alerts** for extreme conditions
-  **Temperature graph visualization**
-  Simple and clean **desktop GUI** using Tkinter

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Tkinter | Desktop GUI |
| OpenWeatherMap API | Real-time weather data |
| Scikit-learn | Machine Learning (Random Forest) |
| Pandas | Data handling |
| Matplotlib | Data visualization |
| Pickle | ML model saving/loading |

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Muthumari10/smart-weather-forecast-app.git
cd smart-weather-forecast-app
```

### 2. Install Required Libraries
```bash
pip install requests pandas scikit-learn matplotlib
```

### 3. Get API Key
- Sign up at [openweathermap.org](https://openweathermap.org)
- Go to **API Keys** tab
- Copy your API key

### 4. Add API Key to Code
Open `weather_app.py` and replace:
```python
API_KEY = "your_weather_api"
```
With your actual API key:
```python
API_KEY = "your_actual_api_key_here"
```

### 5. Run the App
```bash
python weather_app.py
```

---

## 🚀 How to Use

1. **Enter Coordinates** — Type latitude and longitude of any location
2. Click **"Get Current Weather"** — View real-time weather data
3. Click **"5-Day Forecast"** — View weather for next 5 days
4. View **temperature graph** on the right side
5. Check **red alert bar** at the bottom for weather warnings

---

## 📍 Sample Coordinates

| City | Latitude | Longitude |
|------|----------|-----------|
| Chennai | 13.0827 | 80.2707 |
| Mumbai | 19.0760 | 72.8777 |
| Delhi | 28.6139 | 77.2090 |
| London | 51.5074 | -0.1278 |

---

## ⚠️ Weather Alerts

The app automatically generates alerts for:
- 🔥 Temperature above **30°C** — Heat Warning
- ❄️ Temperature below **0°C** — Freeze Warning
- 💨 Wind speed above **10 m/s** — Wind Alert
- 🌧️ Rain or Snow detected — Precipitation Alert

---

## 🤖 Machine Learning Model

- Uses **Random Forest Classifier** from Scikit-learn
- Trained on weather features: Temperature, Humidity, Pressure, Wind Speed
- Predicts weather conditions: Clear, Rain, Snow, Clouds
- Model is saved as `weather_model.pkl` for reuse

---

## 📁 Project Structure

```
smart-weather-forecast-app/
├── weather_app.py        # Main application file
├── weather_model.pkl     # Saved ML model (auto-generated)
├── README.md             # Project documentation
├── .gitignore            # Git ignore file
└── LICENSE               # MIT License
```

---

## 👩‍💻 Author

**Muthumari**
- GitHub: [@Muthumari10](https://github.com/Muthumari10)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

⭐ **If you found this project helpful, please give it a star on GitHub!**

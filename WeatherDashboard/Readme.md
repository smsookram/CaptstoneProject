# 🌦️ Weather Dashboard App

A feature-rich Python desktop weather application built with **CustomTkinter/Tkinter**, designed to be both functional and engaging. It combines real-time and historical weather data, personalized themes, activity suggestions, and a trivia game to deliver a multifaceted experience.

---

## 🚀 Core Features

- **Current Weather:**  
  Fetches and displays current weather for any user-entered city via the **OpenWeatherMap API**.

- **6-Hour Forecast:**  
  Displays a short-term forecast (next 6 hours) using **Open-Meteo** on the same widget as the current weather.

- **Theme Selector Popup:**  
  On startup, users choose between **Marvel** or **Anime** themes for visual personalization.

- **City Comparison:**  
  Side-by-side comparison of two cities showing temperature trends over the last 5 days using Open-Meteo data visualized in graphs.

- **Activity Suggester:**  
  Suggests activities based on current weather conditions, temperature, and time of day (indoor/outdoor logic can be extended).

- **Dark/Light Mode Toggle:**  
  Users can toggle between time-of-day based light and dark modes in the settings tab. Theme colors update dynamically.

- **Trivia Game (Group Feature):**  
  Uses historical 2024 weather data compiled into a CSV to generate a multiple-choice trivia game. Tracks wins/losses with visual feedback.

- **Persistence & Logging:**  
  Saves the last searched city, logs weather lookups, and maintains modular config/state management.

---

## 🐞 Known Issues

- **Theme Toggle Flicker:**  
  Background image sometimes disappears or reverts shortly after toggling dark/light mode.

- **Get Weather Button Visibility:**  
  The addition of the hourly forecast causes the “Get Weather” button to be hidden unless the window is maximized or in full-screen mode.

- **Horizontal Scrolling:**  
  Vertical scrolling works in scrollable panes; left-to-right (horizontal) scrolling is not currently functioning as desired.

- **Trivia Answer Duplication:**  
  Duplicate choices can appear in trivia questions, and selecting one may activate all duplicates.

---

## 💡 Planned Improvements/Bug Fixes

- **Animated Weather Effects:**  
  Overlay animations (rain, cloud, sun, snow, etc.) based on current weather condition to make the UI feel more alive.

- **Enhanced Activity Suggester:**  
  - Let users choose indoor vs outdoor preferences.  
  - Incorporate the hourly forecast to tailor suggestions proactively.  
  - Add emojis and richer formatting to the suggestion output.

- **Trivia UX Upgrades:**  
  - Eliminate duplicate answers.  
  - Add celebratory feedback (e.g., confetti, custom victory screens).  
  - Improve end-of-game messaging.

- **Layout/Responsiveness:**  
  Fix sizing issues so core controls (like the Get Weather button) remain visible at common window sizes.

- **Scrolling Polish:**  
  Enable smooth and intuitive horizontal scrolling where needed.

---

## 🗂️ Folder Structure
weatherDashboard/
├── main.py # Application launcher
|___gui.py
|___.env
|___.gitignore
|___assets/(anime, marvel, effects)
|___config/#weather_api.py
├── core/ # Core modules (weather API wrappers, storage, error handling, weather collector)
|___data/ (last city, weather history, columbus csv, combined weather csv)
├── features/ # Extra features: city comparison, activity suggester, trivia
|___tests(error handling, test import, test trivia, test weather)
└── utils/ # Helpers (styling, animations, scrollable frame, geocoding, etc.)

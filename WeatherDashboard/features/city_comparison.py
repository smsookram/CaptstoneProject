import customtkinter as ctk
from tkinter import messagebox
from core.weather_api import get_weather
from core.error_handling import WeatherAPIError  # Make sure this import matches your project structure
import datetime
from utils.geocode import geocode_city
from open_meteo import OpenMeteo
from open_meteo.models import HourlyParameters
import aiohttp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import asyncio


class CityComparisonTab(ctk.CTkFrame):
    def __init__(self, master, colors, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.colors = colors
        self.unit_var = ctk.StringVar(value="C")

        self.grid_rowconfigure(2, weight=1)   # results_frame row
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.city1_entry = ctk.CTkEntry(self, placeholder_text="Enter First City", width=200)
        self.city1_entry.grid(row=0, column=0, padx=10, pady=10)
        self.city1_entry.bind("<Return>", lambda event: self.compare_weather())

        self.city2_entry = ctk.CTkEntry(self, placeholder_text="Enter Second City", width=200)
        self.city2_entry.grid(row=0, column=1, padx=10, pady=10)
        self.city2_entry.bind("<Return>", lambda event: self.compare_weather())

        self.unit_toggle = ctk.CTkButton(self, text="Switch °C / °F", command=self.toggle_unit)
        self.unit_toggle.grid(row=0, column=2, padx=10)

        self.compare_button = ctk.CTkButton(self, text="Compare", command=self.compare_weather)
        self.compare_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.grid(row=2, column=0, columnspan=3, pady=10)

        self.results_frame.grid_rowconfigure(3, weight=1)  # graphs row
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(1, weight=1)
        self.city1_label = ctk.CTkLabel(self.results_frame, text="", font=("Helvetica", 16, "bold"))
        self.city1_label.grid(row=0, column=0, padx=20)

        self.city2_label = ctk.CTkLabel(self.results_frame, text="", font=("Helvetica", 16, "bold"))
        self.city2_label.grid(row=0, column=1, padx=20)

        self.temp1_label = ctk.CTkLabel(self.results_frame, text="", font=("Helvetica", 14))
        self.temp1_label.grid(row=1, column=0, padx=20)

        self.temp2_label = ctk.CTkLabel(self.results_frame, text="", font=("Helvetica", 14))
        self.temp2_label.grid(row=1, column=1, padx=20)

        self.desc1_label = ctk.CTkLabel(self.results_frame, text="", font=("Helvetica", 12))
        self.desc1_label.grid(row=2, column=0, padx=20)

        self.desc2_label = ctk.CTkLabel(self.results_frame, text="", font=("Helvetica", 12))
        self.desc2_label.grid(row=2, column=1, padx=20)

        # Graph containers
        self.city1_graph_container = ctk.CTkFrame(self.results_frame)
        self.city1_graph_container.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.city2_graph_container = ctk.CTkFrame(self.results_frame)
        self.city2_graph_container.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        self.update_colors(colors)

    def update_colors(self, colors):
        self.colors = colors

        # Frame background
        self.configure(fg_color=colors["bg"])
        self.results_frame.configure(fg_color=colors["bg"])

        # Entries background/text colors
        for entry in [self.city1_entry, self.city2_entry]:
            entry.configure(fg_color=colors["bg"], text_color=colors["fg"], placeholder_text_color=colors["accent"])

        # Button color
        self.unit_toggle.configure(fg_color=colors["accent"], hover_color=colors["accent"]) 
        self.compare_button.configure(fg_color=colors["accent"], hover_color=colors["accent"])

        # Labels text colors
        for label in [self.city1_label, self.city2_label, self.temp1_label, self.temp2_label, self.desc1_label, self.desc2_label]:
            label.configure(text_color=colors["fg"])

    def toggle_unit(self):
        current = self.unit_var.get()
        new_unit = "F" if current == "C" else "C"
        self.unit_var.set(new_unit)
        print(f"Toggled unit to: {new_unit}")  # Debug print to console
        self.compare_weather()  # Trigger re-compare with new unit

    def compare_weather(self):
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        if not city1 or not city2:
            messagebox.showerror("Input Error", "Please enter both cities.")
            return

        units = "imperial" if self.unit_var.get() == "F" else "metric"

        try:
            weather1 = get_weather(city1, units=units)
        except WeatherAPIError as e:
            messagebox.showerror("Error", f"Error retrieving weather for {city1}: {e}")
            return

        try:
            weather2 = get_weather(city2, units=units)
        except WeatherAPIError as e:
            messagebox.showerror("Error", f"Error retrieving weather for {city2}: {e}")
            return
        

        # Clear labels before setting new text to avoid layering
        for label in [self.city1_label, self.temp1_label, self.desc1_label,
                      self.city2_label, self.temp2_label, self.desc2_label]:
            label.configure(text="")

        self.city1_label.configure(text=weather1["city"])
        self.temp1_label.configure(text=f"{weather1['temp']}°{self.unit_var.get()}")
        self.desc1_label.configure(text=weather1["description"].title())

        self.city2_label.configure(text=weather2["city"])
        self.temp2_label.configure(text=f"{weather2['temp']}°{self.unit_var.get()}")
        self.desc2_label.configure(text=weather2["description"].title())

        # Fetch graph data and draw graphs asynchronously
        asyncio.run(self.update_graphs(city1, city2))

    async def update_graphs(self, city1, city2):
        try:
            units = "imperial" if self.unit_var.get() == "F" else "metric"
            history1 = await self.fetch_history(city1, timezone="auto", units=units)
            history2 = await self.fetch_history(city2, timezone="auto", units=units)

            # Calculate global min/max for y-axis
            daily_avg1 = self._daily_avg_temps(history1["time"], history1["temp"])
            daily_avg2 = self._daily_avg_temps(history2["time"], history2["temp"])

            all_temps = daily_avg1 + daily_avg2
            y_min = min(all_temps) - 2  # small padding below
            y_max = max(all_temps) + 2  # small padding above

            self.draw_graph(history1, self.city1_graph_container, city1, weather_type="temp", y_limits=(y_min, y_max))
            self.draw_graph(history2, self.city2_graph_container, city2, weather_type="temp", y_limits=(y_min, y_max))

        except Exception as e:
            messagebox.showerror("Graph Error", str(e))

    async def fetch_history(self, city, timezone, units="metric"):
        lat, lon = await geocode_city(city)
        end = datetime.date.today() - datetime.timedelta(days=1)
        start = end - datetime.timedelta(days=6)

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&hourly=temperature_2m,precipitation"
            f"&start_date={start}&end_date={end}"
            f"&timezone={timezone}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                hourly = data["hourly"]
                temps = hourly["temperature_2m"]

                # Convert temps to Fahrenheit if needed
                if units == "imperial":
                    temps = [(t * 9/5) + 32 for t in temps]

                return {
                    "time": [datetime.datetime.fromisoformat(t) for t in hourly["time"]],
                    "temp": temps,
                    "precip": hourly["precipitation"]
                }

    def _daily_avg_temps(self, times, temps):
        dates = [t.date() for t in times]
        daily_avg = {}
        for d, v in zip(dates, temps):
            daily_avg.setdefault(d, []).append(v)
        return [np.mean(daily_avg[day]) for day in sorted(daily_avg.keys())]

    def draw_graph(self, data, container, title, weather_type="temp", y_limits=None):
        for widget in container.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)

        # Group data by day to reduce points
        times = data["time"]
        values = data["temp"] if weather_type == "temp" else data["precip"]

        # Convert times to dates (no hours)
        dates = [t.date() for t in times]

        # Aggregate by day - compute average temperature per day
        daily_avg = {}
        for d, v in zip(dates, values):
            daily_avg.setdefault(d, []).append(v)
        days = list(daily_avg.keys())
        avg_temps = [np.mean(daily_avg[day]) for day in days]

        ax.plot(days, avg_temps, color=self.colors["accent"], marker='o')

        ax.set_title(f"{title} - {'Temperature' if weather_type == 'temp' else 'Precipitation (mm)'}", fontsize=9)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # Format date labels like 'Jul 23'
        ax.xaxis.set_major_locator(mdates.DayLocator())  # Show tick for each day

        if y_limits:
            ax.set_ylim(y_limits[0], y_limits[1])
            ticks = np.arange(y_limits[0], y_limits[1]+1, 2)
            ax.set_yticks(ticks)

        fig.autofmt_xdate()
        fig.tight_layout(pad=1.5)

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

        plt.close(fig)  # Close figure to free memory and suppress warnings
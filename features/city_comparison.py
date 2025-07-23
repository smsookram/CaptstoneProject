import customtkinter as ctk
from tkinter import messagebox
from core.weather_api import get_weather

class CityComparisonTab(ctk.CTkFrame):
    def __init__(self, master, colors, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.colors = colors
        self.unit_var = ctk.StringVar(value="C")

        self.city1_entry = ctk.CTkEntry(self, placeholder_text="Enter First City", width=200)
        self.city1_entry.grid(row=0, column=0, padx=10, pady=10)

        self.city2_entry = ctk.CTkEntry(self, placeholder_text="Enter Second City", width=200)
        self.city2_entry.grid(row=0, column=1, padx=10, pady=10)

        self.unit_toggle = ctk.CTkButton(self, text="Switch °C / °F", command=self.toggle_unit)
        self.unit_toggle.grid(row=0, column=2, padx=10)

        self.compare_button = ctk.CTkButton(self, text="Compare", command=self.compare_weather)
        self.compare_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.grid(row=2, column=0, columnspan=3, pady=10)

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

    def toggle_unit(self):
        current = self.unit_var.get()
        self.unit_var.set("F" if current == "C" else "C")

    def compare_weather(self):
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        if not city1 or not city2:
            messagebox.showerror("Input Error", "Please enter both cities.")
            return

        units = "imperial" if self.unit_var.get() == "F" else "metric"

        weather1 = get_weather(city1, units=units)
        weather2 = get_weather(city2, units=units)

        if weather1 and weather2:
            self.city1_label.configure(text=weather1["city"])
            self.temp1_label.configure(text=f"{weather1['temp']}°{self.unit_var.get()}")
            self.desc1_label.configure(text=weather1["description"].title())

            self.city2_label.configure(text=weather2["city"])
            self.temp2_label.configure(text=f"{weather2['temp']}°{self.unit_var.get()}")
            self.desc2_label.configure(text=weather2["description"].title())
        else:
            messagebox.showerror("Error", "Could not retrieve weather for one or both cities.")


import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
from core.weather_api import get_weather
from core.storage import save_last_city, load_last_city, log_weather_data
from utils.scrollable_frame import ScrollableFrame
from utils.style import get_theme_colors, get_background_image_path, get_time_of_day
from utils.animations import apply_weather_effect
from features.city_comparison import CityComparisonTab
from features.activity_suggester import suggest_activities
import features.trivia as trivia_module

class WeatherDashboardApp:
    def __init__(self, root, user_theme):
        self.app = root
        self.user_theme = user_theme
        self.current_time_mode = get_time_of_day()

        self.colors = get_theme_colors(self.user_theme, self.current_time_mode)
        self.bg_image_path = get_background_image_path(self.user_theme, self.current_time_mode)

        self.setup_window()
        self.load_background()
        self.create_tabs()
        self.create_weather_tab()
        self.create_city_comparison_tab()
        self.create_activity_tab()
        self.create_settings_tab()
        self.create_trivia_tab()
        self.load_last_city_and_fetch()

    def setup_window(self):
        self.app.title("Weather Dashboard")
        self.app.geometry("800x600")
        self.app.resizable(True, True)
        self.resize_job = None
        self.app.bind("<Configure>", self.resize_bg)

    def load_background(self):
        self.original_bg_image = Image.open(self.bg_image_path)
        self.bg_photo = CTkImage(light_image=self.original_bg_image, size=(800, 600))
        self.bg_label = ctk.CTkLabel(self.app, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()

    def resize_bg(self, event):
        if event.widget == self.app:
            if self.resize_job is not None:
                self.app.after_cancel(self.resize_job)

            def do_resize():
                new_width = event.width
                new_height = event.height
                resized_img = self.original_bg_image.resize((new_width, new_height), Image.LANCZOS)
                new_bg_photo = CTkImage(light_image=resized_img, size=(new_width, new_height))
                self.bg_label.configure(image=new_bg_photo)
                self.bg_label.image = new_bg_photo  # Keep reference

            self.resize_job = self.app.after(200, do_resize)

    def create_tabs(self):
        self.tabview = ctk.CTkTabview(
            self.app,
            width=600,
            height=450,
            segmented_button_selected_color=self.colors["accent"],
            fg_color="#f0f0f0",
            border_width=1,
            corner_radius=15
        )
        self.tabview.pack(expand=True, fill="both", padx=20, pady=20)

        self.weather_tab = self.tabview.add("Weather")
        self.weather_anim_frame = ctk.CTkFrame(self.weather_tab, fg_color=self.colors["bg"])
        self.weather_anim_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.weather_anim_frame.lower()

        self.city_compare_tab = self.tabview.add("City Comparison")
        self.city_compare_tab.grid_rowconfigure(0, weight=1)
        self.city_compare_tab.grid_columnconfigure(0, weight=1)

        self.activity_tab = self.tabview.add("Activities")
        self.settings_tab = self.tabview.add("Settings")

        self.trivia_tab = self.tabview.add("Trivia")

    def create_weather_tab(self):
        self.city_entry = ctk.CTkEntry(self.weather_tab, placeholder_text="Enter City", width=200)
        self.city_entry.pack(pady=10)
        self.city_entry.bind("<Return>", lambda e: self.fetch_weather())

        self.weather_label = ctk.CTkLabel(self.weather_tab, text="", text_color=self.colors["fg"], font=("Helvetica", 20))
        self.weather_label.pack(pady=5)

        self.temp_label = ctk.CTkLabel(self.weather_tab, text="", text_color="black", font=("Helvetica", 40, "bold"))
        self.temp_label.pack(pady=5)

        self.desc_label = ctk.CTkLabel(self.weather_tab, text="", text_color=self.colors["accent"], font=("Helvetica", 18))
        self.desc_label.pack(pady=5)

        self.feels_like_label = ctk.CTkLabel(self.weather_tab, text="", text_color="gray", font=("Helvetica", 14))
        self.feels_like_label.pack(pady=2)

        self.humidity_label = ctk.CTkLabel(self.weather_tab, text="", text_color="gray", font=("Helvetica", 14))
        self.humidity_label.pack(pady=2)

        self.high_low_label = ctk.CTkLabel(self.weather_tab, text="", text_color="gray", font=("Helvetica", 14))
        self.high_low_label.pack(pady=2)

        self.unit_var = ctk.StringVar(value="C")

        self.unit_toggle = ctk.CTkButton(self.weather_tab, text="Switch °C / °F", command=self.toggle_unit)
        self.unit_toggle.pack(pady=5)

        self.fetch_button = ctk.CTkButton(self.weather_tab, text="Get Weather", command=self.fetch_weather, fg_color=self.colors["accent"])
        self.fetch_button.pack(pady=10)

    def fetch_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Input Error", "Please enter a city.")
            return

        try:
            units = "imperial" if self.unit_var.get() == "F" else "metric"
            weather = get_weather(city, units=units)
            if weather:
                self.weather_label.configure(text=weather["city"])
                self.temp_label.configure(text=f"{weather['temp']}°{self.unit_var.get()}")
                self.desc_label.configure(text=weather["description"].title())
                self.feels_like_label.configure(text=f"Feels like: {weather['feels_like']}°{self.unit_var.get()}")
                self.humidity_label.configure(text=f"Humidity: {weather['humidity']}%")
                self.high_low_label.configure(
                    text=f"High: {weather['temp_max']}° / Low: {weather['temp_min']}°"
                )

                apply_weather_effect(self.weather_anim_frame, weather["description"], bg_color=self.colors["bg"])
                save_last_city(city)
                log_weather_data(city, weather["temp"], weather["description"])
            else:
                messagebox.showerror("Error", "Could not retrieve weather.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_unit(self):
        current = self.unit_var.get()
        self.unit_var.set("F" if current == "C" else "C")
        self.fetch_weather()

    def create_city_comparison_tab(self):
        scrollable = ScrollableFrame(self.city_compare_tab)
        scrollable.grid(row=0, column=0, sticky="nsew")
        self.city_compare_tab.grid_rowconfigure(0, weight=1)
        self.city_compare_tab.grid_columnconfigure(0, weight=1)

        scrollable.grid_rowconfigure(0, weight=1)
        scrollable.grid_columnconfigure(0, weight=1)

        self.city_compare_frame = CityComparisonTab(scrollable.scrollable_frame, colors=self.colors)
        self.city_compare_frame.grid(row=0, column=0, sticky="nsew")
        scrollable.scrollable_frame.grid_rowconfigure(0, weight=1)
        scrollable.scrollable_frame.grid_columnconfigure(0, weight=1)

    def create_activity_tab(self):
        self.activity_city_entry = ctk.CTkEntry(self.activity_tab, placeholder_text="Enter City", width=200)
        self.activity_city_entry.pack(pady=10)

        self.activity_suggestions_box = ctk.CTkTextbox(self.activity_tab, height=200, width=400)
        self.activity_suggestions_box.pack(pady=10)

        self.activity_suggest_btn = ctk.CTkButton(self.activity_tab, text="Suggest Activities", command=self.on_activity_suggest_click)
        self.activity_suggest_btn.pack(pady=5)

        self.activity_city_entry.bind("<Return>", lambda e: self.on_activity_suggest_click())

    def on_activity_suggest_click(self):
        city = self.activity_city_entry.get().strip()
        if not city:
            messagebox.showerror("Input Error", "Please enter a city.")
            return

        try:
            units = "imperial" if self.unit_var.get() == "F" else "metric"
            weather = get_weather(city, units=units)

            weather_desc = weather["description"]
            temperature = weather["temp"]

            suggestions = suggest_activities(weather_desc, temperature)

            self.activity_suggestions_box.delete("1.0", "end")
            self.activity_suggestions_box.insert("end", f"Weather: {weather_desc.title()} ({temperature}°{self.unit_var.get()})\n\n")
            for activity in suggestions:
                self.activity_suggestions_box.insert("end", f"- {activity}\n")

        except Exception as e:
            self.activity_suggestions_box.delete("1.0", "end")
            self.activity_suggestions_box.insert("end", f"Error: {e}")
    
    def create_trivia_tab(self):
    # Feedback area
        self.trivia_feedback_frame = ctk.CTkFrame(self.trivia_tab)
        self.trivia_feedback_frame.pack(pady=10, fill="x")

        self.trivia_question_label = ctk.CTkLabel(self.trivia_tab, text="", font=("Helvetica", 18), wraplength=550)
        self.trivia_question_label.pack(pady=15)

    # Choices frame for radio buttons
        self.trivia_choices_frame = ctk.CTkFrame(self.trivia_tab)
        self.trivia_choices_frame.pack(pady=10)

    # Submit button
        self.trivia_submit_btn = ctk.CTkButton(self.trivia_tab, text="Submit Answer", command=self.trivia_check_answer)
        self.trivia_submit_btn.pack(pady=10)

        self.trivia_tab.bind("<Return>", self.trivia_check_answer)

    # Restart button
        self.trivia_restart_btn = ctk.CTkButton(self.trivia_tab, text="Restart Trivia", command=self.reset_trivia)
        self.trivia_restart_btn.pack(pady=5)

        self.trivia_feedback_labels = []

    # Load questions
        self.trivia_questions = trivia_module.get_five_questions()
        self.trivia_current_question_idx = 0
        self.trivia_correct_count = 0
        self.trivia_wrong_count = 0

        self.load_trivia_question()

    
    def load_trivia_question(self):
    # Clear old choices
        for widget in self.trivia_choices_frame.winfo_children():
            widget.destroy()

        if self.trivia_current_question_idx >= len(self.trivia_questions):
            self.end_trivia()
            return

        q = self.trivia_questions[self.trivia_current_question_idx]
        self.trivia_question_label.configure(
            text=f"Question {self.trivia_current_question_idx + 1}: {q['question']}",
            text_color="red"
    )

        self.trivia_selected_option = tk.StringVar()

        self.trivia_option_buttons = []
        for option in q["choices"]:
            btn = ctk.CTkRadioButton(self.trivia_choices_frame, text=option, variable=self.trivia_selected_option, value=option)
            btn.pack(anchor="w", pady=2)
            self.trivia_option_buttons.append(btn)

    def trivia_check_answer(self, event=None):
        selected = self.trivia_selected_option.get()

        if not selected:
            messagebox.showerror("Input Error", "Please select an answer.")
            return

        q = self.trivia_questions[self.trivia_current_question_idx]
        correct = selected == q["answer"]

        symbol = "✔️" if correct else "❌"
        color = "green" if correct else "red"

        lbl = ctk.CTkLabel(self.trivia_feedback_frame, text=symbol, text_color=color, font=("Helvetica", 32))
        lbl.pack(side="left", padx=5)
        self.trivia_feedback_labels.append(lbl)

        self.trivia_question_label.configure(text_color=color)
        self.app.after(1000, lambda: self.trivia_question_label.configure(text_color="white"))

        if correct:
            self.trivia_correct_count += 1
        else:
            self.trivia_wrong_count += 1

        self.trivia_current_question_idx += 1

        self.app.after(1500, self.check_trivia_game_end)


    def check_trivia_game_end(self):
        def show_result_and_reset(message):
            messagebox.showinfo("Trivia Result", message)
            self.disable_trivia()

        if self.trivia_correct_count >= 3:
            show_result_and_reset("🎉 Congratulations! You won the trivia game!")
        elif self.trivia_wrong_count >= 3:
            show_result_and_reset("❌ Sorry, you lost the trivia game.")
        elif self.trivia_current_question_idx >= 5:
            show_result_and_reset(
                f"Game over! You got {self.trivia_correct_count} correct and {self.trivia_wrong_count} wrong."
        )
        else:
            self.load_trivia_question()

    def disable_trivia(self):
        self.trivia_submit_btn.configure(state="disabled")

    def reset_trivia(self):
    # Clear feedback
        for lbl in self.trivia_feedback_labels:
            lbl.destroy()
        self.trivia_feedback_labels.clear()

    # Reset counters and enable inputs
        self.trivia_current_question_idx = 0
        self.trivia_correct_count = 0
        self.trivia_wrong_count = 0
        self.trivia_submit_btn.configure(state="normal")
        self.trivia_questions = trivia_module.get_five_questions()
        self.load_trivia_question()

    def end_trivia(self):
        messagebox.showinfo("Trivia Result", f"Game completed! Correct: {self.trivia_correct_count}, Wrong: {self.trivia_wrong_count}")
        self.disable_trivia()

    def create_settings_tab(self):
        self.toggle_btn = ctk.CTkButton(self.settings_tab, text="Toggle Light/Dark Mode", command=self.toggle_time_mode)
        self.toggle_btn.pack(pady=20)

    def toggle_time_mode(self):
        self.current_time_mode = "night" if self.current_time_mode == "day" else "day"
        self.colors = get_theme_colors(self.user_theme, self.current_time_mode)
        self.bg_image_path = get_background_image_path(self.user_theme, self.current_time_mode)

        # Reload background
        new_bg_image = Image.open(self.bg_image_path)
        new_bg_photo = CTkImage(light_image=new_bg_image, size=(800, 600))
        self.bg_label.configure(image=new_bg_photo)
        self.bg_label.image = new_bg_photo  # keep reference

        # Update widget colors
        self.weather_label.configure(text_color=self.colors["fg"])
        self.temp_label.configure(text_color="black")
        self.desc_label.configure(text_color=self.colors["accent"])
        self.fetch_button.configure(fg_color=self.colors["accent"])
        self.tabview.configure(segmented_button_selected_color=self.colors["accent"])
        self.city_compare_frame.update_colors(self.colors)

    def load_last_city_and_fetch(self):
        last_city = load_last_city()
        if last_city:
            self.city_entry.insert(0, last_city)
            self.fetch_weather()
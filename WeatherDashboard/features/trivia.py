import os
import pandas as pd
import random

# Load and clean the CSV data once
df = pd.read_csv("weatherdashboard/data/combined_weather_data.csv")

# Drop rows with NaN values in key columns for trivia
df = df.dropna(subset=["city", "temperature_2m_mean (°F)", "time"])

# Convert temperature column to numeric 
df["temperature_2m_mean (°F)"] = pd.to_numeric(df["temperature_2m_mean (°F)"], errors="coerce")
df = df.dropna(subset=["temperature_2m_mean (°F)"])

def get_five_questions():
    questions = []

    sampled_rows = df.sample(n=5)  # Get 5 random rows

    for _, row in sampled_rows.iterrows():
        correct_city = row["city"]
        date = row["time"]

        question_types = ["avg_temp", "max_temp", "min_temp", "weather_code", "wind_speed", "humidity"]

        qtype = random.choice(question_types)

        if qtype == "avg_temp":
            correct_answer = round(float(row["temperature_2m_mean (°F)"]), 1)
            wrong_choices = df[df["city"] != correct_city]["temperature_2m_mean (°F)"].sample(3).apply(lambda x: round(float(x), 1)).tolist()
            question_text = f"What was the average temperature in {correct_city} on {date}?"
            unit = "°F"

        elif qtype == "max_temp":
            correct_answer = round(float(row["temperature_2m_max (°F)"]), 1)
            wrong_choices = df[df["city"] != correct_city]["temperature_2m_max (°F)"].sample(3).apply(lambda x: round(float(x), 1)).tolist()
            question_text = f"What was the maximum temperature in {correct_city} on {date}?"
            unit = "°F"

        elif qtype == "min_temp":
            correct_answer = round(float(row["temperature_2m_min (°F)"]), 1)
            wrong_choices = df[df["city"] != correct_city]["temperature_2m_min (°F)"].sample(3).apply(lambda x: round(float(x), 1)).tolist()
            question_text = f"What was the minimum temperature in {correct_city} on {date}?"
            unit = "°F"

        elif qtype == "weather_code":
            # weather_code is numeric, map to description or just ask about it
            correct_answer = row["weather_code (wmo code)"]
            wrong_choices = df[df["city"] != correct_city]["weather_code (wmo code)"].sample(3).tolist()
            question_text = f"What was the weather code in {correct_city} on {date}?"
            unit = ""

        elif qtype == "wind_speed":
            correct_answer = round(float(row["wind_speed_10m_max (mp/h)"]), 1)
            wrong_choices = df[df["city"] != correct_city]["wind_speed_10m_max (mp/h)"].sample(3).apply(lambda x: round(float(x), 1)).tolist()
            question_text = f"What was the max wind speed (mph) in {correct_city} on {date}?"
            unit = "mph"

        elif qtype == "humidity":
            correct_answer = round(float(row["relative_humidity_2m_mean (%)"]), 1)
            wrong_choices = df[df["city"] != correct_city]["relative_humidity_2m_mean (%)"].sample(3).apply(lambda x: round(float(x), 1)).tolist()
            question_text = f"What was the average humidity (%) in {correct_city} on {date}?"
            unit = "%"

        else:
            # fallback, treat as avg temp
            correct_answer = round(float(row["temperature_2m_mean (°F)"]), 1)
            wrong_choices = df[df["city"] != correct_city]["temperature_2m_mean (°F)"].sample(3).apply(lambda x: round(float(x), 1)).tolist()
            question_text = f"What was the average temperature in {correct_city} on {date}?"
            unit = "°F"

        choices = [f"{c} {unit}" for c in wrong_choices + [correct_answer]]
        random.shuffle(choices)

        question = {
            "question": question_text,
            "choices": choices,
            "answer": f"{correct_answer} {unit}",
            "type": "multiple"
        }

        questions.append(question)

    return questions


# quick test
if __name__ == "__main__":
    sample_qs = get_five_questions()
    for i, q in enumerate(sample_qs, start=1):
        print(f"\nQuestion {i}: {q['question']}")
        print(f"Choices: {q['choices']}")
        print(f"Answer: {q['answer']}")

from features import trivia
import pandas as pd
import random

df = pd.read_csv("weatherdashboard/data/combined_weather_data.csv")
print(df.shape)
print(df.head())

def test_trivia():
    questions = trivia.get_five_questions()
    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {q['question']}")
        print(f"Answer: {q['answer']} ({q['type']})")


if __name__ == "__main__":
    test_trivia()


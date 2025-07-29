import pandas as pd
import os

# Set the base directory (the repo you cloned)
team6 = os.getcwd()  

combined_df = pd.DataFrame()

# Walk through all folders and find CSV files
for root, dirs, files in os.walk(team6):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            try:
                df = pd.read_csv(file_path)
                combined_df = pd.concat([combined_df, df], ignore_index=True)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# Drop duplicates just in case
combined_df.drop_duplicates(inplace=True)

# Save the combined CSV
combined_df.to_csv("combined_weather_data.csv", index=False)
print("✅ Combined CSV saved as 'combined_weather_data.csv'")

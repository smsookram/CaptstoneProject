Section 0: 
Fellow Details
Field	Your Entry
Name	Stephanie Sookram
GitHub Username	: smsookram
Preferred Feature Track:Interactive	
Team Interest: No 

Section 1: Week 11 Reflection
Answer each prompt with 3–5 bullet points:

Key Takeaways: What did you learn about capstone goals and expectations?
I learned about what the requirements are to complete the project.
I learned how to organize my files and folders. 
I learned how to create a planning board for the project to ensure I stay on track. 

Concept Connections: Which Week 1–10 skills feel strongest? Which need more practice?
I feel confident in SQL and performing searches on databases. 
I still need to work on for loops and try/except blocks.

Early Challenges: Any blockers (e.g., API keys, folder setup)?
Not at this time

Support Strategies: Which office hours or resources can help you move forward?
Slack/Fellows/TAs/Videos

🧠 Section 2: Feature Selection Rationale
List three features + one enhancement you plan to build.

#	Feature Name	Difficulty (1–3)	Why You Chose It / Learning Goal
1	City Comparison, Difficulty: 1		
2	Theme Switcher, Difficulty: 2
3   Activity Suggester, Difficulty: 3 

 Section 3: High-Level Architecture Sketch
Add a diagram or a brief outline that shows:

Core modules and folders:
core/weather_api.py	
core/storage.py	
core/error_handling.py	
config/weatherapi.py	
.env	
main.py	

Feature modules:
features/city_comparison.py	Co
features/theme_switcher.py	
features/activity_suggester.py

Data flow between components:
User Input (GUI: main.py)
   ↓
City Name → core.weather_api.get_weather(city)
   ↓
Weather API (OpenWeatherMap)
   ↓
Response JSON → core.weather_api → main.py
   ↓
main.py updates GUI:
   - Shows weather info
   - Saves last searched city via core.storage.save_last_city()
   - Handles errors via core.error_handling

Optional:
 - Features like theme_switcher or activity_suggester are triggered by user interaction
 - All use shared core + config functions

Section 4: Data Model Plan
Fill in your planned data files or tables:

File/Table Name	Format (txt, json, csv, other)	Example Row
weather_history.txt	txt	2025-06-09,New Brunswick,78,Sunny

import streamlit as st  # For creating web interface
import pandas as pd  # For data manipulation
import datetime  # For handling dates
import csv  # For reading and writing CSV file
import os  # For file operations

# Define the file name for storing mood data
MOOD_FILE = "mood_log.csv"

# Function to read mood data from the CSV file
def load_mood_data():
    if not os.path.exists(MOOD_FILE):
        return pd.DataFrame(columns=["Date", "Mood"])  # Empty DataFrame if file doesn't exist
    
    data = pd.read_csv(MOOD_FILE, names=["Date", "Mood"], header=0)
    data.columns = data.columns.str.strip()  # Remove spaces from column names
    
    if "Date" not in data.columns:
        st.error("Error: 'Date' column missing in CSV file!")
        return pd.DataFrame(columns=["Date", "Mood"])
    
    return data

# Function to add new mood entry to CSV file
def save_mood_data(date, mood):
    file_exists = os.path.exists(MOOD_FILE)
    
    with open(MOOD_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Mood"])  # Write header if file is new
        writer.writerow([date, mood])

# Streamlit app title
st.title("Mood Tracker")

# Get today's date
today = datetime.date.today()

# Create subheader for mood input
st.subheader("How are you feeling today?")

# Create dropdown for mood selection
mood = st.selectbox("Select your mood", ["Happy", "Sad", "Angry", "Neutral"])

# Create button to save mood
if st.button("Log Mood"):
    save_mood_data(today, mood)
    st.success("Mood Logged Successfully!")

# Load existing mood data
data = load_mood_data()

# If there is data to display
if not data.empty:
    st.subheader("Mood Trends Over Time")
    
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")  # Convert to datetime safely
    data = data.dropna(subset=["Date"])  # Remove invalid dates
    
    mood_counts = data["Mood"].value_counts()  # Count frequency of each mood
    st.bar_chart(mood_counts)

# Footer
st.write("Built with ❤️ by [Wajeeha Qadir Abbasi](#)")

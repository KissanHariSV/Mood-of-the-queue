import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import plotly.express as px

# --- Google Sheets Authentication using st.secrets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = dict(st.secrets["gcp_service_account"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("MoodLog").sheet1

# --- Streamlit UI ---
st.title("🧠 Mood of the Queue")

mood = st.radio("How's the mood?", ["😊", "😠", "😕", "🎉"], horizontal=True)
note = st.text_input("Optional note")

if st.button("Log Mood"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, mood, note])
    st.success("Mood logged!")

# --- Mood Visualization ---
data = pd.DataFrame(sheet.get_all_records())

if not data.empty:
    data["Timestamp"] = pd.to_datetime(data["Timestamp"])
    today = data[data["Timestamp"].dt.date == datetime.today().date()]

    if not today.empty:
        chart = today["Mood"].value_counts().reset_index()
        chart.columns = ["Mood", "Count"]
        fig = px.bar(chart, x="Mood", y="Count", title="Today's Mood Trend")
        st.plotly_chart(fig)
    else:
        st.info("No moods logged yet today.")
else:
    st.info("No mood entries found yet.")

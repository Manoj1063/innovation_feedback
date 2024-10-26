import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Set up the SQLite database
conn = sqlite3.connect('feedback.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    date TEXT,
    name TEXT,
    email TEXT,
    rating INTEGER,
    ideas TEXT
)
''')
conn.commit()

# Streamlit application with enhanced UI
st.title("💡 Innovation Idea Feedback 💬")

st.markdown("### We value your thoughts! Please provide your feedback below.")
st.markdown("---")

# Input fields with icons
name = st.text_input("👤 Name")
email = st.text_input("📧 Email ID")

# Checkbox options for selecting ideas
st.markdown("### Select the idea(s) you're giving feedback on:")
idea_1 = st.checkbox("Idea 1 - AI Equipped Firmware IDE")
idea_2 = st.checkbox("Idea 2 - Translatable Micro Models in Small Memory Embedded device through Meridian Ecosystem")
idea_3 = st.checkbox("Idea 3 - Method to optimize platform porting pipeline for firmware development using Generative AI")
idea_4 = st.checkbox("Idea 4 - AIFA - AMI Intelligent Firmware Assistant")
idea_5 = st.checkbox("Idea 5 - Smart BMC (Talkthon)")

# Concatenate selected ideas into a string
selected_ideas = ", ".join([idea for idea, selected in [
    ("AI Equipped Firmware IDE", idea_1), 
    ("Translatable Micro Models", idea_2),
    ("Optimize Platform Porting Pipeline", idea_3),
    ("AIFA - Intelligent Firmware Assistant", idea_4),
    ("Smart BMC (Talkthon)", idea_5)
] if selected])

# Rating dropdown
rating = st.selectbox("⭐ Overall Rating", ["5 - Excellent", "4 - Good", "3 - Nice", "2 - Not bad", "1 - Didn't like"])

# Submit feedback button with icon
if st.button("🚀 Submit Feedback"):
    if name and email and rating and selected_ideas:
        # Insert feedback into the database
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO feedback (date, name, email, rating, ideas) VALUES (?, ?, ?, ?, ?)", 
                  (date, name, email, int(rating[0]), selected_ideas))  # Convert rating to an integer
        conn.commit()
        st.success("🎉 Thanks for the feedback, really appreciated!")
    else:
        st.error("⚠️ Please fill in all fields and select at least one idea.")

st.markdown("---")

# Download feedback data button with icon
if st.button("📥 Download Feedback"):
    feedback_data = pd.read_sql("SELECT * FROM feedback", conn)
    if not feedback_data.empty:
        csv = feedback_data.to_csv(index=False)
        st.download_button(
            label="📄 Download feedback data as CSV",
            data=csv,
            file_name="feedback_data.csv",
            mime="text/csv"
        )
    else:
        st.info("ℹ️ No feedback data available to download.")

# Close the database connection when done
conn.close()

import streamlit as st
import random
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URI = "mongodb+srv://himanshugamingyt11:RzR5p5Gjwe5BNFW8@cluster0.32r1vqm.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["love_calculator_db"]
collection = db["results"]

st.title("❤️ Love Calculator with FLAMES 🔥")

# Input fields with unique keys
f_name = st.text_input("Enter Your name:", key="your_name").strip().lower()
s_name = st.text_input("Enter your partner's/Crush's name:", key="partner_name").strip().lower()

# Helper: Check if result already exists
def check_existing_result(name1, name2):
    return collection.find_one({
        "$or": [
            {"name1": name1, "name2": name2},
            {"name1": name2, "name2": name1}
        ]
    })

# Helper: Store result in DB
def store_result(name1, name2, love_percentage, flames_result):
    data = {
        "name1": name1,
        "name2": name2,
        "love_percentage": love_percentage,
        "flames_result": flames_result,
        "timestamp": datetime.now()
    }
    collection.insert_one(data)

# Single button for combined functionality
if st.button("Check Compatibility 💑", key="check_compatibility"):
    if f_name and s_name:
        # Check if result already exists
        existing = check_existing_result(f_name, s_name)
        
        if existing:
            love_percentage = existing["love_percentage"]
            flames_result = existing["flames_result"]
            st.success("✅ Result found in database!")
        else:
            # Generate new results
            love_percentage = random.randint(1, 100)
            flames = ["Friendship", "Love", "Affection", "Marriage", "Enemy", "Siblings"]
            index = (len(f_name) + len(s_name)) % len(flames)
            flames_result = flames[index]
            
            # Store in DB
            store_result(f_name, s_name, love_percentage, flames_result)
            st.success("🎉 New result calculated and saved!")

        # Display results
        st.markdown(f"""
        ### 💘 Compatibility Results
        - **Love Percentage:** `{love_percentage}%` ❤️
        - **FLAMES Result:** `{flames_result}` 🔥
        """)
    else:
        st.error("⚠️ Please enter both names.")

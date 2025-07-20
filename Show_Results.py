import streamlit as st
from pymongo import MongoClient
import pandas as pd
from bson import json_util
import hashlib

# --- MongoDB Configuration ---
MONGO_URI = "mongodb+srv://himanshugamingyt11:RzR5p5Gjwe5BNFW8@cluster0.32r1vqm.mongodb.net/"
DB_NAME = "love_calculator_db"
COLLECTION_NAME = "results"

# --- Security Configuration ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()  # Change this password

# --- Streamlit App Config ---
st.set_page_config(page_title="Love Calculator Results", layout="wide")

# --- Authentication ---
def authenticate(username, password):
    if username == ADMIN_USERNAME:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == ADMIN_PASSWORD_HASH
    return False

# Check if user is logged in
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Login form
if not st.session_state.authenticated:
    st.title("🔒 Admin Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid username or password")
    st.stop()

# --- Main App (only visible after authentication) ---
st.title("💘 Love Calculator Results")

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Get all results
    results = list(collection.find({}))
    
    if not results:
        st.info("No records found in the database.")
    else:
        st.success(f"Found {len(results)} records!")
        
        # Convert to DataFrame for nice display
        df = pd.json_normalize([json_util.loads(json_util.dumps(r)) for r in results])
        
        # Show raw data
        st.subheader("All Records")
        st.dataframe(df)
        
        # Show statistics
        st.subheader("Statistics")
        st.write(df.describe())

except Exception as e:
    st.error(f"Could not connect to database: {e}")

# Logout button
if st.session_state.authenticated:
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
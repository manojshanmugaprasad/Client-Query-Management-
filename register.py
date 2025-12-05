import streamlit as st
import pandas as pd
import pymysql
import hashlib
from datetime import datetime

# DB CONNECTION 
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="shansgan98",
        database="clientquerydb9",
        cursorclass=pymysql.cursors.Cursor
    )

# PASSWORD HASH 
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# PAGE CONFIG 
st.set_page_config(
    page_title="Client Query Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# HEADER 

st.title("Client Query Management System")
st.write("Connecting clients to clarity through smart query management.")
st.header("Admin")
st.image("D:/guvi - project CRM/env/Scripts/7079591.png")


page = st.sidebar.radio("Navigation", ["Register"])

# REGISTER PAGE
if page == "Register":
    st.write("Create your Account Here")

    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    new_role = st.selectbox("Role", ["Client", "Support"])

    if st.button("Create Account"):
        if not new_username or not new_password:
            st.error("Username and password are required.")
        else:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT id FROM users WHERE username=%s", (new_username,))
                if cur.fetchone():
                    st.error("Username already exists. Please choose another one.")
                else:
                    hashed = hash_password(new_password)
                    cur.execute(
                        "INSERT INTO users (username, hashed_password, role) VALUES (%s, %s, %s)",
                        (new_username, hashed, new_role)
                    )
                    conn.commit()
                    st.success("Account created successfully! You can now log in from the Login / Dashboard page.")
                cur.close()
                conn.close()
            except Exception as e:
                st.error(f"Error while creating account: {e}")
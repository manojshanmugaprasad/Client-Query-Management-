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
st.write("Client/Support can login")
st.image("D:/guvi - project CRM/env/Scripts/Arrow-Left-icon.png")

page = st.sidebar.radio("Navigation", ["Login / Dashboard"])

# Session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

# LOGIN + DASHBOARD
if page == "Login / Dashboard":
    st.sidebar.subheader("Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT hashed_password, role FROM users WHERE username=%s",
                (username,)
            )
            result = cur.fetchone()
            if result and hash_password(password) == result[0]:
                st.sidebar.success("Login successful!")
                st.session_state.authenticated = True
                st.session_state.role = result[1]
                st.session_state.username = username
            else:
                st.sidebar.error("Invalid username or password.")
                st.session_state.authenticated = False
            cur.close()
            conn.close()
        except Exception as e:
            st.sidebar.error(f"Database error: {e}")
            st.session_state.authenticated = False

# DASHBOARD CONTENT AFTER LOGIN
    if st.session_state.authenticated:
        role = st.session_state.role
        username = st.session_state.username

        st.write(f"Logged in as: {username} ({role})")

        try:
            conn = get_connection()
            cur = conn.cursor()

            # CLIENT PAGE
            if role == "Client":
                st.header("Submit a New Query")

                with st.form("client_query_form", clear_on_submit=True):
                    email = st.text_input("Email ID")
                    heading = st.text_input("Query Heading")
                    description = st.text_area("Query Description")
                    submitted = st.form_submit_button("Submit Query")

                if submitted:
                    if not email or not heading or not description.strip():
                        st.error("All fields (Email, Heading, Description) are required.")
                    else:
                        cur.execute(
                            """
                            INSERT INTO queries1 (client, email, heading, description, status)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (username, email, heading, description, "Open")
                        )
                        conn.commit()
                        st.success("Your query has been submitted to the support team successfully.")

                st.header("My Submitted Queries")
                cur.execute(
                    """
                    SELECT id, email, heading, description, status, created_at, closed_at
                    FROM queries1
                    WHERE client = %s
                    ORDER BY created_at DESC
                    """,
                    (username,)
                )
                rows = cur.fetchall()
                if rows:
                    df = pd.DataFrame(
                        rows,
                        columns=[
                            "id", "Email", "Heading", "Description",
                            "Status", "Created Time", "Closed Time"
                        ]
                    )
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No queries submitted yet.")

            # SUPPORT PAGE
            elif role == "Support":
                st.header("Support Dashboard - All Client Queries")

                # Live queries from queries1
                cur.execute(
                    """
                    SELECT id, client, email, heading, description, status, created_at, closed_at
                    FROM queries1
                    ORDER BY created_at DESC
                    """
                )
                rows = cur.fetchall()
                if rows:
                    df = pd.DataFrame(
                        rows,
                        columns=[
                            "id", "Client", "Email", "Heading", "Description",
                            "Status", "Created Time", "Closed Time"
                        ]
                    )
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No queries available.")

                st.subheader("Update Query Status")
                query_id = st.number_input("Enter Query ID to update:", min_value=1, step=1)
                new_status = st.selectbox("Update status to:", ["Open", "In Progress", "Closed"])
                if st.button("Update Status"):
                    closed_time = None
                    if new_status == "Closed":
                        closed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        cur.execute(
                            "UPDATE queries1 SET status=%s, closed_at=%s WHERE id=%s",
                            (new_status, closed_time, int(query_id))
                        )
                    else:
                        cur.execute(
                            "UPDATE queries1 SET status=%s WHERE id=%s",
                            (new_status, int(query_id))
                        )
                    conn.commit()
                    st.success("Query status updated.")

 #PAST QUERIES FROM past_queries TABLE
                st.subheader("Past Client Queries")

                cur.execute(
                    """
                    SELECT id,
                        client_email,
                        client_mobile,
                        query_heading,
                        query_description,
                        status,
                        date_raised,
                        date_closed
                    FROM pastqueries
                    ORDER BY date_raised DESC
                    """
                )
                past_rows = cur.fetchall()

                if past_rows:
                    df_past = pd.DataFrame(
                        past_rows,
                        columns=[
                            "id",
                            "email",
                            "mobile",
                            "heading",
                            "description",
                            "status",
                            "date_raised",
                            "date_closed",
                        ],
                    )
                    st.dataframe(df_past, use_container_width=True)
                else:
                    st.info("No historical (past) queries found in database.")


            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Database error: {e}")
    else:
        st.info("Please log in to access the dashboard.")



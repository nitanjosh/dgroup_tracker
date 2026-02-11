import streamlit as st
from tools.db import verify_admin, get_all_dgroup_records
import pandas as pd

#Login Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Show login or dashboard based on login status
if not st.session_state.logged_in:
    # Login Page
    st.title("Admin Login")
    uname = st.text_input("Username:", placeholder="Enter username")
    pwd = st.text_input("Password:", placeholder="Enter Password", type="password")
    st.markdown(" ")

    if st.button("Submit", use_container_width=True):
        if verify_admin(username=uname, password=pwd):
            st.session_state.logged_in = True
            st.rerun()  # Refresh the page to show dashboard
        else:
            st.warning("Incorrect username or password!")

else:
    col1, col2 = st.columns([20,5])
    # Admin Dashboard
    col1.title("Admin Dashboard")
    
    # Logout button
    if col2.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.divider()
    
    records = get_all_dgroup_records()

    if records:
        df = pd.DataFrame(records)
        df = df.drop(columns=["id"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records found in the database.")
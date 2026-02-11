import streamlit as st
from config import PAGE_CONFIG
from tools.db import insert_dgroup_record

st.set_page_config(**PAGE_CONFIG)

st.markdown("""
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='centered'>Exalt Monthly Dgroup Tracker</h1>",
            unsafe_allow_html=True)
st.markdown("<h4 class='centered'>Dgroup Tracking System for Elevate Exalt</h4>",
            unsafe_allow_html=True)

st.divider()

# Dropdown cards explaining dgroup types
col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("**D-Leader**"):
        st.write("Handling 3+ members")

with col2:
    with st.expander("**D-Member**"):
        st.write("Meet with your D-Leader")

with col3:
    with st.expander("**Potential Leader**"):
        st.write("D-Leader handling 1-2 D-members")

st.subheader("Dgroup Meeting Information")

first_name = st.text_input("First Name:", placeholder="(Ex. Juan)")
last_name = st.text_input("Last Name:", placeholder="(Ex. Dela Cruz)")
dgroup_type = st.selectbox("Select Dgroup Type:",
                           ["D-Leader", "D-Member", "Potential Leader"])

# Initialize variables
upline_meet = None
downline_meet = None
leader_name = None

if dgroup_type in ["D-Leader", "Potential Leader"]:
    leader_name = st.text_input("Dgroup Leader Full Name:")
    col1, col2 = st.columns(2)
    upline_meet = col1.date_input("Select most recent UPLINE meeting:")
    downline_meet = col2.date_input("Select most recent DOWNLINE meeting:")
else:  #Member
    upline_meet = st.date_input("Select most recent meet with your leader: ")
    
st.divider()

if st.button("Submit", use_container_width=True):
    # Validate required fields
    if not first_name or not last_name:
        st.error("Please fill in both First Name and Last Name.")
    elif dgroup_type == "D-Member" and not leader_name:
        st.error("Please provide your Dgroup Leader's Full Name.")
    elif dgroup_type == "Leader-Member" and not leader_name:
        st.error("Please provide your Dgroup Leader's Full Name.")
    else:
        # Insert record into database
        success = insert_dgroup_record(
            first_name=first_name,
            last_name=last_name,
            dgroup_type=dgroup_type,
            upline_meet=upline_meet,
            downline_meet=downline_meet,
            leader_name=leader_name
        )
        
        if success:
            st.success("✅ Record submitted successfully!")
            st.balloons()
        else:
            st.error("❌ Failed to submit record. Please try again or contact support.")
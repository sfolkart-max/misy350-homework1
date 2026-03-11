import streamlit as st
import time
import json
import datetime
import uuid
from pathlib import Path

st.set_page_config(
    page_title= 'Course Manager',
    page_icon= '',
    layout= 'centered',
    initial_sidebar_state= 'collapsed',
)

users = {'id':1,
        'email':'admin@school.edu',
        'full_name':'System Admin',
        'password':'admin123',
        'role':'admin',
        'registered_at':'...'


}
json_path = Path("users.json")

if json_path.exists():
    with json_path.open("r", encoding= "utf-8") as f:
        users = json.load(f)

tab1, tab2, = st.tabs(["Login", "Register"])

with tab1:
    with st.container(border=True):
        st.markdown("# Login")
        user_name = st.text_input("Email")
        password = st.text_input("Password", type="password")

    if st.button("Login", type="primary",key="login_button",use_container_width=True):
        with st.spinner("Checking the login..."):
            time.sleep(5)
        
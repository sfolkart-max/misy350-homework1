import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time


st.set_page_config( page_title= "Course Manager",layout="centered")
st.title("Course Manager Application")



users = []
st.subheader("Login")

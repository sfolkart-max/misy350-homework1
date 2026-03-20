import streamlit as st
import json
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="Excuse Absence Management",
    page_icon="📋",
    layout="wide"
)

data_file = Path(__file__).parent / "absence_requests.json"

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


def load_requests():
    if data_file.exists():
        with open(data_file, 'r') as f:
            return json.load(f)
    return []


def save_requests(requests):
    with open(data_file, 'w') as f:
        json.dump(requests, f, indent=2)


def new_request(email, date, excuse_type, explanation):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = date.strftime("%Y-%m-%d")
    request_id = "011" + str(len(load_requests()) + 1)
    
    return {
        "request_id": request_id,
        "status": "Pending",
        "course_id": "011101",
        "student_email": email,
        "absence_date": date_str,
        "submitted_timestamp": timestamp,
        "excuse_type": excuse_type,
        "explanation": explanation,
        "instructor_note": ""
    }



st.sidebar.title("Navigation")
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("Excuse Absence\nDashboard", key="btn_dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
        st.rerun()

with col2:
    if st.button("Excuse Absence\nRequest", key="btn_request", use_container_width=True):
        st.session_state.page = "Request"
        st.rerun()

st.sidebar.divider()



def show_dashboard():
    st.title("Excuse Absences")
    
  
    all_requests = load_requests()
    
    st.subheader("Excused Absences")
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("count", len(all_requests))
    with col2:
        pending_count = 0
        for req in all_requests:
            if req.get("status") == "Pending":
                pending_count = pending_count + 1
        st.metric("Pending", pending_count)
    
    st.divider()
    
    
    if len(all_requests) == 0:
        st.info("No requests yet.")
        return
    
   
    table_data = []
    for req in all_requests:
        row = {
            "ID": req.get("request_id"),
            "Status": req.get("status"),
            "Email": req.get("student_email"),
            "Date": req.get("absence_date"),
            "Type": req.get("excuse_type")
        }
        table_data.append(row)
    
  
    event = st.dataframe(
        table_data,
        on_select="rerun",
        selection_mode="single-row",
        use_container_width=True,
        key="df_reqs"
    )
    
    
    if event.selection.rows:
        selected_index = event.selection.rows[0]
        selected_request = all_requests[selected_index]
        
        st.divider()
        st.subheader("Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Status", selected_request.get("status"))
            st.write(f"**Email:** {selected_request.get('student_email')}")
            st.write(f"**Course:** {selected_request.get('course_id')}")
            st.write(f"**Date:** {selected_request.get('absence_date')}")
        
        with col2:
            st.write(f"**Type:** {selected_request.get('excuse_type')}")
            st.write(f"**Submitted:** {selected_request.get('submitted_timestamp')}")
        
        st.write("**Reason:**")
        st.write(selected_request.get("explanation"))
        
        if selected_request.get("instructor_note"):
            st.write("**Instructor Note:**")
            st.write(selected_request.get("instructor_note"))



def show_request_form():
    st.title("Excuse Absence Request")
    st.write("Submit a new request")
    
    
    with st.form("request_form", clear_on_submit=True):
        email = st.text_input("Email", key="input_email")
        absence_date = st.date_input("Absence Date", key="input_date")
        excuse_type = st.selectbox("Reason", ["Medical", "University Competitions", "Other"], key="input_type")
        explanation = st.text_area("Explanation", key="input_explanation")
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
           
            if not email or not explanation:
                st.error("Please fill in all fields")
            else:
              
                new_req = new_request(email, absence_date, excuse_type, explanation)
                all_requests = load_requests()
                all_requests.append(new_req)
                save_requests(all_requests)
                
                st.success("Request submitted!")
                st.rerun()



if st.session_state.page == "Dashboard":
    show_dashboard()
else:
    show_request_form()


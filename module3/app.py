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
course_id = "011101"

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "selected_request" not in st.session_state:
    st.session_state.selected_request = None


def load_requests():
    if data_file.exists():
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_requests(requests):
    with open(data_file, 'w') as f:
        json.dump(requests, f, indent=2)


def create_request_record(email, absence_date, excuse_type, explanation):
    date_str = absence_date.strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "Status": "Pending",
        "Course ID": course_id,
        "Student Email": email,
        "Absence Date": date_str,
        "Submitted Timestamp": timestamp,
        "Excuse Type": excuse_type,
        "Student Explanation": explanation,
        "Instructor Note": ""
    }


def format_requests_for_display(requests):
    display_data = []
    for idx, req in enumerate(requests):
        display_data.append({
            "ID": idx,
            "Status": req.get("Status", "Pending"),
            "Student Email": req.get("Student Email", ""),
            "Absence Date": req.get("Absence Date", ""),
            "Excuse Type": req.get("Excuse Type", ""),
            "Submitted": req.get("Submitted Timestamp", "")
        })
    return display_data


# Navigation
st.sidebar.title("Navigation")
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("📊 Dashboard", key="btn_dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
        st.session_state.selected_request = None
        st.rerun()

with col2:
    if st.button("📝 Request", key="btn_request", use_container_width=True):
        st.session_state.page = "Request"
        st.session_state.selected_request = None
        st.rerun()

st.sidebar.divider()


def show_dashboard():
    st.title("📊 Excuse Absence Dashboard")
    st.write("Browse all absence requests")
    
    requests = load_requests()
    
    if not requests:
        st.info("No requests yet. Submit one to get started.")
        return
    
    st.subheader("Requests")
    display_data = format_requests_for_display(requests)
    
    event = st.dataframe(
        display_data,
        on_select="rerun",
        selection_mode="single-row",
        use_container_width=True,
        key="dataframe_requests"
    )
    
    if event.selection.rows:
        selected_index = event.selection.rows[0]
        selected_request = requests[selected_index]
        
        st.divider()
        st.subheader("Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Status", selected_request.get("Status", "N/A"))
            st.write(f"**Email:** {selected_request.get('Student Email')}")
            st.write(f"**Course:** {selected_request.get('Course ID')}")
            st.write(f"**Absence Date:** {selected_request.get('Absence Date')}")
        
        with col2:
            st.write(f"**Type:** {selected_request.get('Excuse Type')}")
            st.write(f"**Submitted:** {selected_request.get('Submitted Timestamp')}")
        
        st.write("**Reason:**")
        st.write(selected_request.get("Student Explanation", "—"))
        
        st.write("**Instructor Note:**")
        note = selected_request.get("Instructor Note", "")
        st.write(note if note else "—")


def show_request_form():
    st.title("📝 Request Form")
    st.info("🚧 Coming soon!")



if st.session_state.page == "Dashboard":
    show_dashboard()
else:
    show_request_form()

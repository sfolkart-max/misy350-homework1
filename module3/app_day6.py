import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Course Manager", layout="centered")
st.title("Course Manager Application")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    
if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "role" not in st.session_state:
    st.session_state["role"] = None

users = [
        {
        "id": "1",
        "email": "admin@school.edu",
        "full_name": "System Admin",
        "password": "123ssag@43AE",
        "role": "Admin",
        "registered_at": "..."
    }
]
json_path = Path("users.json")
if json_path.exists():
        with open(json_path, "r") as f:
            users = json.load(f)

assignments = [
    {
        "id" : "HW1",
        "title": "Intro to Database",
        "description" : "basics of database design",
        "points": 100,
        "type" : "homework"
    } ,
    {
        "id" : "HW2",
        "title" : "Normalization",
        "description" : "normalize the table designs",
        "points" : 100,
        "type" : "lab"
    }
]

# Initialize assignment ID number based on existing assignments
next_assignmnet_id_number = 1
for assignment in assignments:
    if assignment["id"].startswith("HW"):
        try:
            num = int(assignment["id"][2:])
            if num >= next_assignmnet_id_number:
                next_assignmnet_id_number = num + 1
        except:
            pass

json_path = Path("assignments.json")
if json_path.exists():
    with open(json_path, "r") as f:
        assignments = json.load(f)

if st.session_state["role"] == "Admin":
    st.markdown("This is the Admin UI- Dashboard")

    if st.button("Log Out"):
        with st.spinner("logging out..."):
            time.sleep(4)
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.rerun()


elif st.session_state["role"] =="Instructor":
    st.markdown("This is the Instructor Dashboard")
    if st.session_state["page"] == "home":
        st.markdown(f"Welcome {st.session_state['user']['email']}")
        if st.button("Go to Dashboard", type="primary",key="view_dash_btn"):
            st.session_state["page"] = "dashboard"
            st.rerun()
    elif st.session_state["page"] == "dashboard":
        st.markdown("Instructor Dashboard")
else:
    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email Address", key = "email_address_login")
        password_input = st.text_input("Password", type="password", key = "password_login")
        
        if st.button("Log In", type="primary",use_container_width=True):
            with st.spinner("Logging in..."):
                time.sleep(2) # Fake backend delay
                
                # Find user
                found_user = None
                for user in users:
                    if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
                        found_user = user
                        break
                
                if found_user:
                    st.success(f"Welcome back, {found_user['email']}!")
                    st.session_state["logged_in"]= True
                    st.session_state["user"] = found_user
                    st.session_state["role"] = found_user['role']
                    st.session_state["page"] = "home"
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid credentials")


tab1, tab2, tab3 = st.tabs(["View Assignments", "Add New Assignment","Update an Assignment"])

with tab1:

    tab_option = st.radio("View/Search", ["View", "Search"], horizontal= True)
    if tab_option == "View":
        st.dataframe(assignments)
    else:
        titles = []
        for assignment in assignments:
            titles.append(assignment["title"])

        selected_title = st.selectbox("Select a title",titles, key="selected_title")

        selected_assignment = {}

        for assignment in assignments:
            if assignment["title"] == selected_title:
                selected_assignment = assignment
                break


        
        st.divider()
        selected_assignment = st.selectbox("Select Title",
                                           options=assignments,
                                           format_func= lambda x: f"{x['title']} ({x['type']})")


        
        if  selected_assignment:
            with st.expander("Assignment Details", expanded=True):
                st.markdown(f"### Title: {selected_assignment['title']}")
                st.markdown(f"**Description**: {selected_assignment['description']}")
                st.markdown(f"Type: **{selected_assignment['type']}**")


with tab2:
    st.markdown("## Add New Assignment")
    #st.markdown("### Add New Assignment")

    title = st.text_input("Title")
    description = st.text_area("Description",placeholder="normalization is covered here",
                            help="Here you are entering the assignment details")
    points = st.number_input("Points")

    #assignmnet_type = st.text_input("Assignmnet Type")
    assignment_type = st.radio("Type", ["Homework","Lab"], horizontal=True)
    st.caption("Homework type")

    assignment_type2 = st.selectbox("Type", ["Select an option","Homework","Lab", "other"])
    if assignment_type2 == "other":
        assignment_type2 = st.text_input("Type", placeholder="Enter the assignmnet Type")

    due_date = st.date_input("Due Date")

    btn_save = st.button("Save",width="stretch",disabled=False)


    if btn_save:
        if not title:
            st.warning("Title needs to be provided!")
        else:
            with st.spinner("Assignment is being recorded...."):
                time.sleep(5)

                new_assignmnet_id = "HW" + str(next_assignmnet_id_number)
                next_assignmnet_id_number += 1

                assignments.append(
                    {
                        "id" : new_assignmnet_id,
                        "title" : title,
                        "description" : description,
                        "points" : points,
                        "type" : assignment_type
                    }
                )

                #record into json file 
                with json_path.open("w",encoding="utf-8") as f:
                    json.dump(assignments,f)

                st.success("New Assignment is recorded!")
                st.info("This is a new assignment")
                time.sleep(4)
                #st.dataframe(assignments)
                st.rerun()

with tab3:
   st.markdown("## Update an Assignment")
   titles = []
   for assignment in assignments:
       titles.append(assignment["title"])
   
   selected_item = st.selectbox("select an assignment", titles, key="selected_title_edit")

   assignment_edit = {}
   for assignment in assignments:
       if assignment['title'] == selected_item:
           assignment_edit = assignment
           break
       

   if assignment_edit:
       edit_title = st.text_input("Title", key=f"edit_title_{assignment_edit['id']}", 
                                  value= assignment_edit['title'])
       edit_description = st.text_area("Description" , key= f"edit_description_{assignment_edit['id']}" , 
                                       value= assignment_edit['description'])

       type_options = ["Homework", "Lab"]
       selected_index = type_options.index(assignment_edit["type"].capitalize())
       
       edit_type = st.radio("Type",type_options, 
                            key=f"edit_type_{assignment_edit['id']}",
                            index= selected_index)        

   
   



    st.subheader("New Instructor Account")
    with st.container(border=True):
        new_email = st.text_input("Email Address", key="email_address_register")
        new_password = st.text_input("Password", type="password" , key = "password_reg")
        
        if st.button("Create Account", type="secondary", use_container_width=True):
            with st.spinner("Creating account..."):
                time.sleep(2) # Fake backend delay
                # ... (Assume validation logic here) ...
                users.append({
                    "id": str(uuid.uuid4()),
                    "email": new_email,
                    "password": new_password,
                    "role": "Instructor"
                })
                with open(json_path, "w") as f:
                    json.dump(users, f, indent=4)
                st.success(f"Account created! {new_email}")
                time.sleep(4)
                st.rerun()

    st.write("---")
    st.dataframe(users)

with st.sidebar:
    if "logged_in" in st.session_state and st.session_state["logged_in"] != False:
        user = st.session_state["user"]
        st.markdown(f"Welcome {user['email']}")
    else:
        st.markdown("Welcome! - Login")
import streamlit as st
import time
import json
from pathlib import Path

st.set_page_config( page_title= "Course Management",
                   page_icon="🎓",
                   layout="centered",
                   initial_sidebar_state="collapsed")


st.title("Course Management App")

st.divider()

next_assignmnet_id_number = 3

#load data
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
        "description" : "normalizing",
        "points" : 100,
        "type" : "homework"
    }
]


json_path = Path("assignmnets.json")

#Load the data from a json file
if json_path.exists():
    with json_path.open("r", encoding= "utf-8") as f:
        assignments = json.load(f)


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

   
   
   
   
   
   btn_update = st.button("Update", key="update_button",type="secondary", use_container_width=True)
   if btn_update:
       with st.spinner("Updating..."):
           time.sleep(5)
           assignment_edit['title'] = edit_title
           assignment_edit['description'] = edit_description

           with json_path.open("w",encoding="utf-8") as f:
               json.dump(assignments,f)

           st.success("Assignment is updated!")
           time.sleep(5)
           st.rerun()


with st.sidebar:
    st.markdown("Sidebar")
    
    
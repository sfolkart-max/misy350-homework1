import streamlit as st

st.title("Course Management App")
st.header("Assignmnet Management")
st.subheader("Dashboard")

next_assignmnet_id_number = 3


st.divider()
st.markdown("---------")

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

#input
#st.markdown("# Add New Assignment")
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

import time
import json
from pathlib import Path

json_path = Path("assignmnets.json")


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
            st.dataframe(assignments)
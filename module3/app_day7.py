
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config("Order Application", layout="wide", initial_sidebar_state="expanded")

inventory = [
    {
        "id": 1,
        "name": "Espresso",
        "price": 2.5,
        "stock": 35
    },
    {
        "id": 2,
        "name": "Latte",
        "price": 4.25,
        "stock": 25
    },
    {
        "id": 3,
        "name": "Cold Brew",
        "price": 3.75,
        "stock": 39
    },
    {
        "id": 4,
        "name": "Mocha",
        "price": 4.5,
        "stock": 20
    },
    {
        "id": 5,
        "name": "Blueberry Muffin",
        "price": 2.95,
        "stock": 18
    }
]

if "page" not in st.session_state:
    st.session_state["page"]="home"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {}
    ]
with st.sidebar:
    if st.button("Home", key="home_btn", type="primary", use_container_width=True):
        st.session_state["page"]="home"
        st.rerun()
        
    if st.button("Orders", key="orders_btn", type="primary", use_container_width=True):
        st.session_state["page"]="orders"
        st.rerun()

json_path_inventory = Path("inventory.json")
if json_path_inventory.exists():
    with open(json_path_inventory, "r") as f:
        inventory = json.load(f)

json_path_orders = Path("orders.json")
if json_path_orders.exists():
    with open(json_path_orders, "r") as f:
        orders = json.load(f)

else:
    orders = []

if st.session_state["page"] == "home":
    col1, col2 = st.columns(2)
    with col1:
        selected_category = st.radio("Select a category", ["Orders", "Inventory"], horizontal=True)

    if selected_category == "Inventory":
        st.markdown("## Inventory")
        if len(inventory) > 0:
            st.dataframe(inventory)
        else:
            st.warning("No item is found.")
    else:
        st.markdown("## Orders")
        if len(orders) > 0:
            st.dataframe(orders)
        else:
            st.warning("No order is found.")


elif st.session_state["page"] == "orders":
    st.markdown("Under Construction")
    tab1, tab2 = st.tabs(["Add New Order", "Cancel an Order"])

    with tab1:
        selected_item = st.selectbox("Items", options=inventory, key= "inventory_selector", format_func=lambda x: f"{x['name']}")
        quantity = st.number_input("Enter the Quantity", min_value=1, step=1)

        if st.button("Create New Order", key="place_order_btn", type="primary", use_container_width=True):
            with st.spinner("Recording your order..."):
                total = quantity * selected_item["item_id"]

                for item in inventory:
                    if item["item_id"] == selected_item["item_id"]:
                        item["stock"] -= quantity
                        break

                orders.append({"id": str(uuid.uuid4()), "item_id": selected_item["item_id"], "quantity": quantity, "Status": "Placed", "total": total})
                

                with open(json_path_inventory, "w") as f:
                    json.dump(inventory, f)

                with open(json_path_orders, "w") as f:
                    json.dump(orders, f)

                st.balloons()
                time.sleep(4)


    with tab2:
        pass

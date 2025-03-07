
# app.py
import streamlit as st
import pandas as pd

# Title
st.title("Motorbike Inventory Management App")

# Sample Data (This could be replaced with a real database or file read)
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = pd.DataFrame({
        "Bike Model": ["Yamaha R1", "Honda CBR500R", "Kawasaki Ninja 400"],
        "Year": [2020, 2019, 2021],
        "Price": [15000, 7000, 6000]
    })

# Show current inventory
st.subheader("Current Inventory")
st.dataframe(st.session_state['inventory'])

# Add new bike
st.subheader("Add New Bike")
with st.form("add_bike_form"):
    model = st.text_input("Bike Model")
    year = st.number_input("Year", min_value=1980, max_value=2025, step=1)
    price = st.number_input("Price", min_value=0, step=100)

    submitted = st.form_submit_button("Add Bike")
    if submitted:
        new_bike = {"Bike Model": model, "Year": year, "Price": price}
        st.session_state['inventory'] = pd.concat(
            [st.session_state['inventory'], pd.DataFrame([new_bike])],
            ignore_index=True
        )
        st.success(f"Added {model} to inventory!")

# Delete bike
st.subheader("Remove Bike")
bike_to_remove = st.selectbox("Select bike to remove", st.session_state['inventory']["Bike Model"])
if st.button("Remove Bike"):
    st.session_state['inventory'] = st.session_state['inventory'][st.session_state['inventory']["Bike Model"] != bike_to_remove]
    st.success(f"Removed {bike_to_remove} from inventory")

# Footer
st.caption("Motorbike Inventory App - Powered by Streamlit")

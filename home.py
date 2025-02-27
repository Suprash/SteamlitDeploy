import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# --- Data Loading and Preprocessing ---

# Load your CSV data; update the path as necessary
df = pd.read_csv('earthquakes.csv', skipinitialspace=True, on_bad_lines='skip')
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
df = df.sort_values('Datetime')
df['DaysGap'] = df['Datetime'].diff().dt.days

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Probability", "Map"])

if page == "Probability":
    st.title("Earthquake Probability Calculator")
    st.write("This section estimates the probability of an earthquake occurring within a specified number of days.")

    # User Input for Probability Calculation
    user_days_gap = st.number_input("Enter the number of days:", min_value=0, value=10, step=1)

    # Probability Calculations
    daysgap_counts = df['DaysGap'].value_counts().sort_index()
    total_counts = daysgap_counts.sum()
    empirical_probability = daysgap_counts[daysgap_counts.index <= user_days_gap].sum() / total_counts

    mean_gap = df['DaysGap'].mean()
    lambda_val = 1 / mean_gap if mean_gap else 0
    exponential_probability = 1 - np.exp(-lambda_val * user_days_gap)

    # Display the Results
    st.subheader("Calculated Probabilities")
    st.write(f"**Empirical Probability** of an earthquake within {user_days_gap} days: **{empirical_probability:.4f}**")
    st.write(f"**Exponential Model Probability** of an earthquake within {user_days_gap} days: **{exponential_probability:.4f}**")
    
    # Large font percentage display
    st.markdown(f"<h1 style='text-align: center; color: red;'>{exponential_probability * 100:.2f}%</h1>", unsafe_allow_html=True)
    st.write("Exponential Model Probability in Percentage")

elif page == "Map":
    st.title("Map of Earthquakes in Nepal")
    st.write("This section displays earthquake locations on a map.")

    # Prepare DataFrame for mapping
    map_df = df[['Latitude', 'Longitude']].dropna().copy()
    map_df.columns = ['lat', 'lon']

    # Create a Pydeck layer for earthquake locations
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position='[lon, lat]',
        get_radius=10000,
        get_fill_color='[255, 0, 0, 140]',
        pickable=True
    )

    # Center the map over Nepal
    view_state = pdk.ViewState(
        latitude=28.3949,
        longitude=84.1240,
        zoom=6,
        pitch=0
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Latitude: {lat}, Longitude: {lon}"}
    )

    st.pydeck_chart(r)

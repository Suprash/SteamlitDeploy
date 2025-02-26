import streamlit as st
import pandas as pd
import numpy as np

# --- Data Loading and Preprocessing ---

# Load your CSV data; update the path as necessary

df = pd.read_csv('earthquakes.csv', skipinitialspace=True, on_bad_lines='skip')

# Clean whitespace from all string columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Create a combined Datetime column and sort the DataFrame
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
df = df.sort_values('Datetime')

# Calculate the gap (in days) between consecutive earthquake events
df['DaysGap'] = df['Datetime'].diff().dt.days

# --- Streamlit App Interface ---

st.title("Earthquake Probability Calculator")
st.write("This app estimates the probability of an earthquake occurring within a specified number of days.")

# Allow user to input the number of days (default is 10)
user_days_gap = st.number_input("Enter the number of days:", min_value=0, value=10, step=1)

# --- Probability Calculations ---

# Empirical Probability
daysgap_counts = df['DaysGap'].value_counts().sort_index()
total_counts = daysgap_counts.sum()
empirical_probability = daysgap_counts[daysgap_counts.index <= user_days_gap].sum() / total_counts

# Exponential Model Probability
mean_gap = df['DaysGap'].mean()
lambda_val = 1 / mean_gap if mean_gap else 0
exponential_probability = 1 - np.exp(-lambda_val * user_days_gap)

# --- Display the Results ---

st.subheader("Calculated Probabilities")
st.write(f"**Empirical Probability** of an earthquake within {user_days_gap} days: **{empirical_probability:.4f}**")
st.write(f"**Exponential Model Probability** of an earthquake within {user_days_gap} days: **{exponential_probability:.4f}**")

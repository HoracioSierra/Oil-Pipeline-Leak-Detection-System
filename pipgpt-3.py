import random
import openai
import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # For plotting the live graph
import time

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI API with your API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure your .env file contains 'OPENAI_API_KEY'

# Function to call GPT-3.5 or GPT-4 to classify vibration, temperature, and pressure data
def analyze_pipeline(vibration, temp, pressure, safe_range_vibration, safe_range_temp):
    prompt = (f"The current vibration level is {vibration:.2f}. The current temperature is {temp:.2f} degrees Celsius. "
              f"The current pressure is {pressure:.2f} psi. "
              f"The safe range for vibration is between {safe_range_vibration[0]:.2f} and {safe_range_vibration[1]:.2f}. "
              f"The safe range for temperature is between {safe_range_temp[0]:.2f} and {safe_range_temp[1]:.2f}. "
              f"Is the pipeline operating within safe conditions? What is your analysis of these readings?")
    
    # Use ChatCompletion API (for GPT-3.5-turbo and GPT-4 models)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" or "gpt-4"
        messages=[
            {"role": "system", "content": "You are a pipeline monitoring assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    # Extract the GPT response
    return response['choices'][0]['message']['content'].strip()

# Simulate sensor data (pressure, vibration, temperature)
def simulate_sensor_data():
    pressure = random.uniform(50, 100)  # Simulate pressure in psi
    vibration = random.uniform(0, 10)   # Simulate vibration levels
    temperature = random.uniform(-10, 50)  # Simulate temperature in Celsius
    return pressure, vibration, temperature

# Streamlit app interface
st.title("Pipeline Integrity Monitoring System with GPT-3.5")

# Set safe ranges for vibration and temperature
safe_range_vibration = [2.0, 7.0]  # Min and max safe vibration level
safe_range_temp = [-5.0, 40.0]     # Min and max safe temperature range
safe_range_pressure = [50.0, 100.0]  # Assuming safe pressure range

# Function to determine if the values are normal or abnormal
def determine_status(value, safe_min, safe_max):
    if safe_min <= value <= safe_max:
        return "normal", "green"
    else:
        return "abnormal", "red"

# Initialize Streamlit session state for start/stop monitoring and data history
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'pressure_history' not in st.session_state:
    st.session_state.pressure_history = []
if 'vibration_history' not in st.session_state:
    st.session_state.vibration_history = []
if 'temperature_history' not in st.session_state:
    st.session_state.temperature_history = []

# Create a row for the Start/Stop buttons
col_start, col_stop = st.columns([1, 1])  # Create two equal-sized columns for buttons

# Place the buttons side by side
with col_start:
    if st.button("Start Monitoring"):
        st.session_state.monitoring = True

with col_stop:
    if st.button("Stop Monitoring"):
        st.session_state.monitoring = False

# Display the monitoring message below the buttons
if st.session_state.monitoring:
    st.write("Monitoring live pressure, vibration, and temperature data...")

# Create columns to display the graph on the left and the metrics on the right
col1, col2 = st.columns([2, 1])  # Set up two columns: larger left column and smaller right column

# Create placeholders for the graph and metrics
graph_placeholder = col1.empty()  # For the live updating graph
gpt_placeholder = st.empty()      # For the GPT analysis
pressure_placeholder = col2.empty()
vibration_placeholder = col2.empty()
temperature_placeholder = col2.empty()

# Monitoring loop
if st.session_state.monitoring:
    while st.session_state.monitoring:
        # Simulate sensor data
        pressure, vibration, temperature = simulate_sensor_data()

        # Append new data to history
        st.session_state.pressure_history.append(pressure)
        st.session_state.vibration_history.append(vibration)
        st.session_state.temperature_history.append(temperature)

        # Determine if the values are normal or abnormal and color them accordingly
        vib_status, vib_color = determine_status(vibration, *safe_range_vibration)
        temp_status, temp_color = determine_status(temperature, *safe_range_temp)
        pressure_status, pressure_color = determine_status(pressure, *safe_range_pressure)

        # Replace old metrics with new values in the placeholders (now in the right column)
        pressure_placeholder.metric(label="Pressure (psi)", value=f"{pressure:.2f}")
        vibration_placeholder.markdown(f"<span style='color:{vib_color};'>Vibration Level: {vibration:.2f} ({vib_status})</span>", unsafe_allow_html=True)
        temperature_placeholder.markdown(f"<span style='color:{temp_color};'>Temperature: {temperature:.2f}°C ({temp_status})</span>", unsafe_allow_html=True)

        # Update the live graph
        with graph_placeholder:
            fig, ax = plt.subplots(figsize=(8, 4))  # Adjust the size to fit the left side
            ax.plot(st.session_state.pressure_history, label='Pressure (psi)', color='blue')
            ax.plot(st.session_state.vibration_history, label='Vibration', color='green')
            ax.plot(st.session_state.temperature_history, label='Temperature (°C)', color='red')

            # Plot safe ranges as dashed lines
            ax.axhline(y=safe_range_pressure[1], color='blue', linestyle='--', label='Safe Max Pressure')
            ax.axhline(y=safe_range_vibration[1], color='green', linestyle='--', label='Safe Max Vibration')
            ax.axhline(y=safe_range_temp[1], color='red', linestyle='--', label='Safe Max Temperature')

            # Set title, labels, and move the legend to the side
            ax.set_title('Live Trendline of Pressure, Vibration, and Temperature')
            ax.set_ylabel('Values')
            ax.set_xlabel('Time (steps)')
            ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

            # Display the live-updating graph
            graph_placeholder.pyplot(fig)

        # Generate GPT-3.5 Analysis dynamically
        gpt_response = analyze_pipeline(vibration, temperature, pressure, safe_range_vibration, safe_range_temp)

        # Display the GPT analysis centered below both the graph and metrics
        gpt_placeholder.markdown(
            f"<div style='text-align: center;'>"
            f"<h3>GPT-3.5 Analysis:</h3>"
            f"<p>{gpt_response}</p>"
            f"</div>", 
            unsafe_allow_html=True
        )

        # Add a 4-second delay before simulating new data
        time.sleep(4)

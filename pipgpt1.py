import random
import openai
import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd  # Added for data handling
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

# Create empty containers for displaying the metrics and GPT analysis
pressure_placeholder = st.empty()
vibration_placeholder = st.empty()
temperature_placeholder = st.empty()
gpt_placeholder = st.empty()

# Initialize Streamlit session state for start/stop monitoring and data history
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'pressure_history' not in st.session_state:
    st.session_state.pressure_history = []
if 'vibration_history' not in st.session_state:
    st.session_state.vibration_history = []
if 'temperature_history' not in st.session_state:
    st.session_state.temperature_history = []

# Start Monitoring Button
if st.button("Start Monitoring"):
    st.session_state.monitoring = True

# Stop Monitoring Button
if st.button("Stop Monitoring"):
    st.session_state.monitoring = False

# Monitoring loop
if st.session_state.monitoring:
    st.write("Monitoring live pressure, vibration, and temperature data...")
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

        # Create columns for layout
        col1, col2 = st.columns([1, 2])

        # Display the simulated pressure with trendline
        with col1:
            pressure_placeholder.metric(label="Pressure (psi)", value=f"{pressure:.2f}")
        with col2:
            pressure_df = pd.DataFrame({
                'Pressure': st.session_state.pressure_history,
                'Safe Min': [safe_range_pressure[0]] * len(st.session_state.pressure_history),
                'Safe Max': [safe_range_pressure[1]] * len(st.session_state.pressure_history)
            })
            pressure_chart = st.line_chart(pressure_df[['Pressure', 'Safe Min', 'Safe Max']])

        # Display the simulated vibration with trendline
        col3, col4 = st.columns([1, 2])
        with col3:
            vibration_placeholder.markdown(
                f"<span style='color:{vib_color};'>Vibration Level: {vibration:.2f} ({vib_status})</span>",
                unsafe_allow_html=True)
        with col4:
            vibration_df = pd.DataFrame({
                'Vibration': st.session_state.vibration_history,
                'Safe Min': [safe_range_vibration[0]] * len(st.session_state.vibration_history),
                'Safe Max': [safe_range_vibration[1]] * len(st.session_state.vibration_history)
            })
            vibration_chart = st.line_chart(vibration_df[['Vibration', 'Safe Min', 'Safe Max']])

        # Display the simulated temperature with trendline
        col5, col6 = st.columns([1, 2])
        with col5:
            temperature_placeholder.markdown(
                f"<span style='color:{temp_color};'>Temperature: {temperature:.2f}°C ({temp_status})</span>",
                unsafe_allow_html=True)
        with col6:
            temperature_df = pd.DataFrame({
                'Temperature': st.session_state.temperature_history,
                'Safe Min': [safe_range_temp[0]] * len(st.session_state.temperature_history),
                'Safe Max': [safe_range_temp[1]] * len(st.session_state.temperature_history)
            })
            temperature_chart = st.line_chart(temperature_df[['Temperature', 'Safe Min', 'Safe Max']])

        # Use GPT-3.5 to analyze the current vibration, temperature, and pressure
        with st.spinner("Analyzing data with GPT-3.5..."):
            try:
                gpt_response = analyze_pipeline(vibration, temperature, pressure, safe_range_vibration, safe_range_temp)
                gpt_placeholder.write(f"**GPT-3.5 Analysis:**\n{gpt_response}")
            except Exception as e:
                gpt_placeholder.error(f"Error analyzing with GPT: {e}")

        # Add a 4-second delay before simulating new data
        time.sleep(4)

        # Clear the placeholders to avoid duplication
        pressure_placeholder.empty()
        vibration_placeholder.empty()
        temperature_placeholder.empty()
        gpt_placeholder.empty()

        # Clear the charts
        pressure_chart.empty()
        vibration_chart.empty()
        temperature_chart.empty()

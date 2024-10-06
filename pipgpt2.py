import random
import openai
import os
import pandas as pd
import streamlit as st
import time
from dotenv import load_dotenv

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

# Set safe vibration and temperature ranges
safe_range_vibration = [2.0, 7.0]  # Min and max safe vibration level
safe_range_temp = [-5.0, 40.0]     # Min and max safe temperature range
safe_pressure = [50, 100]          # For comparison, normal pressure range

# Function to determine if the values are normal or abnormal
def determine_status(value, safe_min, safe_max):
    if safe_min <= value <= safe_max:
        return "normal", "green"
    else:
        return "abnormal", "red"

# Initialize Streamlit session state for start/stop monitoring
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False

# Data history for plotting
if 'data_history' not in st.session_state:
    st.session_state.data_history = {
        "pressure": [],
        "vibration": [],
        "temperature": [],
        "time": []
    }

# Start Monitoring Button
if st.button("Start Monitoring"):
    st.session_state.monitoring = True

# Stop Monitoring Button
if st.button("Stop Monitoring"):
    st.session_state.monitoring = False

# Create line charts for live data
pressure_chart = st.line_chart()
vibration_chart = st.line_chart()
temperature_chart = st.line_chart()

# Monitoring loop
if st.session_state.monitoring:
    st.write("Monitoring live pressure, vibration, and temperature data...")
    while st.session_state.monitoring:
        # Simulate sensor data
        pressure, vibration, temperature = simulate_sensor_data()

        # Track time for x-axis
        current_time = len(st.session_state.data_history["time"])

        # Update data history for plotting
        st.session_state.data_history["pressure"].append(pressure)
        st.session_state.data_history["vibration"].append(vibration)
        st.session_state.data_history["temperature"].append(temperature)
        st.session_state.data_history["time"].append(current_time)

        # Create a DataFrame for plotting
        df = pd.DataFrame({
            "Pressure (psi)": st.session_state.data_history["pressure"],
            "Vibration": st.session_state.data_history["vibration"],
            "Temperature (°C)": st.session_state.data_history["temperature"]
        }, index=st.session_state.data_history["time"])

        # Update the line charts with the new data
        pressure_chart.line_chart(df[["Pressure (psi)"]])
        vibration_chart.line_chart(df[["Vibration"]])
        temperature_chart.line_chart(df[["Temperature (°C)"]])

        # Use GPT-3.5 to analyze the current vibration, temperature, and pressure
        with st.spinner("Analyzing data with GPT-3.5..."):
            try:
                gpt_response = analyze_pipeline(vibration, temperature, pressure, safe_range_vibration, safe_range_temp)
                st.write(f"**GPT-3.5 Analysis:**\n{gpt_response}")
            except Exception as e:
                st.error(f"Error analyzing with GPT: {e}")

        # Create comparison bar chart for pressure, vibration, and temperature
        st.write("### Comparison of Real vs. Normal Ranges")
        
        comparison_data = pd.DataFrame({
            "Real": [pressure, vibration, temperature],
            "Normal": [safe_pressure[1], safe_range_vibration[1], safe_range_temp[1]]
        }, index=["Pressure (psi)", "Vibration", "Temperature (°C)"])

        st.bar_chart(comparison_data)

        # Add a 4-second delay before simulating new data
        time.sleep(4)

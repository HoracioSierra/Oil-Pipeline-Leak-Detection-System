import random
import openai
import os
from dotenv import load_dotenv
import streamlit as st
import matplotlib.pyplot as plt  # For plotting the live graph
import time

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI API with your API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to call GPT-3.5 to classify vibration, temperature, and pressure data
def analyze_pipeline(vibration, temp, pressure, safe_range_vibration, safe_range_temp, safe_range_pressure):
    prompt = (
        f"The current vibration level is {vibration:.2f}. The current temperature is {temp:.2f} degrees Celsius. "
        f"The current pressure is {pressure:.2f} psi. "
        f"The safe range for vibration is between {safe_range_vibration[0]:.2f} and {safe_range_vibration[1]:.2f}. "
        f"The safe range for temperature is between {safe_range_temp[0]:.2f} and {safe_range_temp[1]:.2f}. "
        f"The safe range for pressure is between {safe_range_pressure[0]:.2f} and {safe_range_pressure[1]:.2f}. "
        f"Is the pipeline operating within safe conditions? Provide a brief analysis."
    )

    # Use ChatCompletion API (for GPT-3.5-turbo)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a pipeline monitoring assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150  # Limit the response length to ensure brevity
    )

    # Extract the GPT response
    return response['choices'][0]['message']['content'].strip()

# Simulate sensor data (pressure, vibration, temperature)
def simulate_sensor_data():
    pressure = random.uniform(600, 2000)  # Simulate pressure in psi for oil pipeline
    vibration = random.uniform(0, 10)     # Simulate vibration levels
    temperature = random.uniform(-10, 50)  # Simulate temperature in Celsius
    return pressure, vibration, temperature

# Streamlit app interface
st.title("Pipeline Integrity Monitoring System with GPT-3.5")

# Set safe ranges for vibration, temperature, and oil pipeline pressure
safe_range_vibration = [2.0, 7.0]     # Min and max safe vibration level
safe_range_temp = [-5.0, 50.0]        # Max safe temperature range set to 50°C
safe_range_pressure = [600.0, 2000.0] # Safe pressure range for oil pipelines

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
graph_placeholder = col1.empty()    # For the live updating graph
gpt_placeholder = st.empty()        # For the GPT analysis
pressure_placeholder = col2.empty()
vibration_placeholder = col2.empty()
temperature_placeholder = col2.empty()

# Monitoring loop
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
    pressure_placeholder.markdown(
        f"<h4 style='color:{pressure_color}; font-size:18px;'>Pressure (psi): {pressure:.2f} ({pressure_status})</h4>",
        unsafe_allow_html=True
    )

    vibration_placeholder.markdown(
        f"<h4 style='color:{vib_color}; font-size:18px;'>Vibration Level: {vibration:.2f} ({vib_status})</h4>",
        unsafe_allow_html=True
    )
    temperature_placeholder.markdown(
        f"<h4 style='color:{temp_color}; font-size:18px;'>Temperature: {temperature:.2f}°C ({temp_status})</h4>",
        unsafe_allow_html=True
    )

    # Update the live graph
    with graph_placeholder:
        fig, ax1 = plt.subplots(figsize=(12, 6))  # Increased the graph size to make it more visible

        # Plot pressure on primary y-axis
        ax1.plot(st.session_state.pressure_history, label='Pressure (psi)', color='blue')
        ax1.set_xlabel('Time (steps)')
        ax1.set_ylabel('Pressure (psi)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Create secondary y-axis for temperature and vibration
        ax2 = ax1.twinx()

        # Plot temperature and vibration on secondary y-axis
        ax2.plot(st.session_state.temperature_history, label='Temperature (°C)', color='red')
        ax2.plot(st.session_state.vibration_history, label='Vibration', color='green')
        ax2.set_ylabel('Temperature (°C) / Vibration', color='black')
        ax2.tick_params(axis='y', labelcolor='black')

        # Plot normal ranges as dashed lines
        ax1.axhline(y=safe_range_pressure[1], color='blue', linestyle='--', label='Safe Max Pressure')
        ax2.axhline(y=safe_range_vibration[1], color='green', linestyle='--', label='Safe Max Vibration')
        ax2.axhline(y=safe_range_temp[1] - 15, color='red', linestyle='--', label='Safe Max Temperature')  # Lowered the max temp line by 15 units

        # Combine legends from both axes and move to upper right outside the graph, slightly to the right
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', bbox_to_anchor=(1.35, 1))

        # Set title
        plt.title('Live Trendline of Pressure, Vibration, and Temperature')

        # Display the live-updating graph
        graph_placeholder.pyplot(fig)
        plt.close(fig)  # Close the figure to free memory

    # Generate GPT-3.5 Analysis dynamically
    gpt_response = analyze_pipeline(vibration, temperature, pressure, safe_range_vibration, safe_range_temp, safe_range_pressure)

    # Display the GPT analysis centered below both the graph and metrics, text justified
    gpt_placeholder.markdown(
        f"<div style='text-align: justify;'>"
        f"<h3>GPT-3.5 Analysis:</h3>"
        f"<p>{gpt_response}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Add a 4-second delay before simulating new data
    time.sleep(4)

# After stop, display the final graph
with graph_placeholder:
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot pressure on primary y-axis
    ax1.plot(st.session_state.pressure_history, label='Pressure (psi)', color='blue')
    ax1.set_xlabel('Time (steps)')
    ax1.set_ylabel('Pressure (psi)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create secondary y-axis for temperature and vibration
    ax2 = ax1.twinx()

    # Plot temperature and vibration on secondary y-axis
    ax2.plot(st.session_state.temperature_history, label='Temperature (°C)', color='red')
    ax2.plot(st.session_state.vibration_history, label='Vibration', color='green')
    ax2.set_ylabel('Temperature (°C) / Vibration', color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # Plot normal ranges as dashed lines
    ax1.axhline(y=safe_range_pressure[1], color='blue', linestyle='--', label='Safe Max Pressure')
    ax2.axhline(y=safe_range_vibration[1], color='green', linestyle='--', label='Safe Max Vibration')
    ax2.axhline(y=safe_range_temp[1] - 15, color='red', linestyle='--', label='Safe Max Temperature')

    # Combine legends and move to upper right outside the graph
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', bbox_to_anchor=(1.35, 1))

    plt.title('Final Trendline of Pressure, Vibration, and Temperature')

    # Display the final graph
    graph_placeholder.pyplot(fig)
    plt.close(fig)

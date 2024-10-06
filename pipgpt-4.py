import random
import openai
import os
from dotenv import load_dotenv
import streamlit as st
import matplotlib.pyplot as plt
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
        max_tokens=250  # Increased token limit to prevent cutting off the response
    )

    # Extract the GPT response
    return response['choices'][0]['message']['content'].strip()

# Function to calculate carbon footprint based on energy consumed
def calculate_carbon_footprint(energy_consumed_kWh, carbon_intensity=0.233):
    return energy_consumed_kWh * carbon_intensity

# Function to simulate renewable energy offset (solar + wind)
def simulate_renewable_energy_offset(total_energy_consumed_kWh, solar_power_generation_kWh, wind_power_generation_kWh):
    renewable_energy_generated = solar_power_generation_kWh + wind_power_generation_kWh
    remaining_energy = total_energy_consumed_kWh - renewable_energy_generated
    return max(remaining_energy, 0)

# Simulate sensor data (pressure, vibration, temperature)
def simulate_sensor_data():
    pressure = random.uniform(600, 2000)  # Simulate pressure in psi for oil pipeline
    vibration = random.uniform(0, 10)     # Simulate vibration levels
    temperature = random.uniform(-10, 50)  # Simulate temperature in Celsius
    energy_used_kWh = random.uniform(50, 150)  # Simulate energy consumption in kWh for pumps
    return pressure, vibration, temperature, energy_used_kWh

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
if 'energy_history' not in st.session_state:
    st.session_state.energy_history = []
if 'renewable_energy_history' not in st.session_state:
    st.session_state.renewable_energy_history = []
if 'carbon_footprint_history' not in st.session_state:
    st.session_state.carbon_footprint_history = []

# Create a row for the Start/Stop buttons
col_start, col_stop = st.columns([1, 1])

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
gpt_placeholder = col1.empty()      # For the GPT analysis below the graph
pressure_placeholder = col2.empty()
vibration_placeholder = col2.empty()
temperature_placeholder = col2.empty()
emission_placeholder = col1.empty()  # Placeholder for live emissions report below the graph

# Monitoring loop
while st.session_state.monitoring:
    # Simulate sensor data
    pressure, vibration, temperature, energy_used_kWh = simulate_sensor_data()

    # Simulate renewable energy generation (solar + wind)
    solar_generation_kWh = random.uniform(10, 50)  # Simulate solar energy generation in kWh
    wind_generation_kWh = random.uniform(10, 50)   # Simulate wind energy generation in kWh
    remaining_energy_needed = simulate_renewable_energy_offset(energy_used_kWh, solar_generation_kWh, wind_generation_kWh)

    # Calculate the carbon footprint
    carbon_footprint_kg = calculate_carbon_footprint(remaining_energy_needed)

    # Append new data to history
    st.session_state.pressure_history.append(pressure)
    st.session_state.vibration_history.append(vibration)
    st.session_state.temperature_history.append(temperature)
    st.session_state.energy_history.append(energy_used_kWh)
    st.session_state.renewable_energy_history.append(remaining_energy_needed)
    st.session_state.carbon_footprint_history.append(carbon_footprint_kg)

    # Align metrics and determine if the values are normal or abnormal and color them accordingly
    pressure_placeholder.markdown(
        f"<h4 style='color:{determine_status(pressure, *safe_range_pressure)[1]}; font-size:18px;'>Pressure (psi): {pressure:.2f}</h4>",
        unsafe_allow_html=True
    )
    vibration_placeholder.markdown(
        f"<h4 style='color:{determine_status(vibration, *safe_range_vibration)[1]}; font-size:18px;'>Vibration Level: {vibration:.2f}</h4>",
        unsafe_allow_html=True
    )
    temperature_placeholder.markdown(
        f"<h4 style='color:{determine_status(temperature, *safe_range_temp)[1]}; font-size:18px;'>Temperature: {temperature:.2f}°C</h4>",
        unsafe_allow_html=True
    )

    # Update the live graph
    with graph_placeholder:
        fig, ax1 = plt.subplots(figsize=(14, 7))  # Make the graph larger to fit everything

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
        ax2.axhline(y=safe_range_temp[1], color='red', linestyle='--', label='Safe Max Temperature')

        # Combine legends and move to upper right outside the graph
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', bbox_to_anchor=(1.35, 1))

        plt.title('Live Trendline of Pressure, Vibration, and Temperature')

        # Display the live-updating graph
        graph_placeholder.pyplot(fig)
        plt.close(fig)

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

    # Display live emission report, updated as energy consumption and renewable energy change
    emission_placeholder.markdown(
        f"<div style='text-align: justify; font-size:12px;'>"
        f"<h5>Total Energy Consumed: {sum(st.session_state.energy_history):.2f} kWh</h5>"
        f"<h5>Renewable Energy Offset: {sum(st.session_state.renewable_energy_history):.2f} kWh</h5>"
        f"<h5>Carbon Footprint: {sum(st.session_state.carbon_footprint_history):.2f} kg CO2</h5>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Add a 15-second delay to allow ChatGPT enough time to print the full analysis
    time.sleep(15)

# After stop, display two final graphs: one for pressure, temperature, and vibration; another for renewable energy offset
if not st.session_state.monitoring:
    # First graph: Pressure, Vibration, Temperature trends
    with graph_placeholder:
        fig, ax1 = plt.subplots(figsize=(14, 7))  # Larger graph for better visualization

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
        ax2.axhline(y=safe_range_temp[1], color='red', linestyle='--', label='Safe Max Temperature')

        # Combine legends and move to upper right outside the graph
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', bbox_to_anchor=(1.35, 1))

        plt.title('Final Trendline of Pressure, Vibration, and Temperature')

        # Display the final graph
        graph_placeholder.pyplot(fig)
        plt.close(fig)

    # Second graph: Renewable Energy Offset comparison
    with col1:
        fig, ax3 = plt.subplots(figsize=(14, 7))  # Larger graph for energy consumption vs renewable energy

        # Plot total energy consumption vs renewable offset
        ax3.plot(st.session_state.energy_history, label='Total Energy Used (kWh)', color='orange')
        ax3.plot(st.session_state.renewable_energy_history, label='Remaining Energy After Renewable Offset (kWh)', color='purple')

        ax3.set_xlabel('Time (steps)')
        ax3.set_ylabel('Energy (kWh)')
        ax3.set_title('Final Energy Consumption vs Renewable Offset')

        # Display the renewable energy comparison graph
        ax3.legend(loc='upper right')
        st.pyplot(fig)
        plt.close(fig)

# Final emission report displayed at the end
if not st.session_state.monitoring:
    total_carbon_emissions = sum(st.session_state.carbon_footprint_history)
    emission_placeholder.markdown(
        f"<div style='text-align: justify; font-size:12px;'>"
        f"<h5>Total Energy Consumed: {sum(st.session_state.energy_history):.2f} kWh</h5>"
        f"<h5>Renewable Energy Offset: {sum(st.session_state.renewable_energy_history):.2f} kWh</h5>"
        f"<h5>Total Carbon Footprint: {total_carbon_emissions:.2f} kg CO2</h5>"
        f"</div>",
        unsafe_allow_html=True
    )

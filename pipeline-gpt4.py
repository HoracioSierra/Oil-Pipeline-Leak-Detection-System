import random
import time
import openai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Initialize OpenAI API with your API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure the API key is in your .env file

# Function to call GPT-4 to classify vibration data
def classify_vibrations(vibration, safe_range_low, safe_range_high):
    prompt = f"The current vibration level is {vibration}. The safe range for vibrations is between {safe_range_low} and {safe_range_high}. Is the current vibration abnormal?"

    response = openai.ChatCompletion.create(
        model="gpt-4",  # GPT-4 model
        messages=[
            {"role": "system", "content": "You are an assistant helping to classify vibration levels in a pipeline."},
            {"role": "user", "content": prompt},
        ]
    )

    # Access the message content from the response
    message = response.choices[0].message['content'].strip()
    return message

# Simulate sensor data (pressure and vibration)
def simulate_sensor_data():
    pressure = random.uniform(50, 100)  # Simulate pressure in psi
    vibration = random.uniform(0, 10)   # Simulate vibration levels
    return pressure, vibration

# Streamlit app interface
st.title("Pipeline Monitoring System with GPT-4")

# Set safe vibration range for the pipeline
safe_range_low = st.number_input("Set minimum safe vibration level:", value=2.0, step=0.1)
safe_range_high = st.number_input("Set maximum safe vibration level:", value=7.0, step=0.1)

# Button to start monitoring
if st.button("Start Monitoring"):
    st.write("Monitoring live pressure and vibration data...")
    
    # Simulate sensor data
    pressure, vibration = simulate_sensor_data()

    # Display the simulated pressure
    st.metric(label="Pressure (psi)", value=f"{pressure:.2f}")

    # Display the simulated vibration data
    st.metric(label="Vibration Level", value=f"{vibration:.2f}")

    # Use GPT-4 to classify the vibration as normal or abnormal
    with st.spinner("GPT-4 is analyzing the vibration data..."):
        gpt4_response = classify_vibrations(vibration, safe_range_low, safe_range_high)
        st.write("**GPT-4 Response:**")
        st.success(gpt4_response)

    # Optional: Add a small delay before simulating new data
    time.sleep(2)

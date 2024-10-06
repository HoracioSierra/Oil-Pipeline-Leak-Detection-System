Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import random
import time
import streamlit as st
from twilio.rest import Client

# Simulate sensor data (pressure, flow rate, temperature)
def simulate_sensor_data():
    pressure = random.uniform(50, 100)  # Pressure in psi
    flow_rate = random.uniform(200, 300)  # Flow rate in gallons/min
    temperature = random.uniform(60, 90)  # Temperature in Fahrenheit
    return pressure, flow_rate, temperature

# Detect leaks based on pressure and flow rate
def detect_leak(pressure, flow_rate):
    pressure_threshold = 60  # Set a threshold for pressure
...     flow_rate_threshold = 220  # Set a threshold for flow rate
...     if pressure < pressure_threshold or flow_rate < flow_rate_threshold:
...         send_sms_alert()  # Send an alert if leak detected
...         return True  # Leak detected
...     return False  # No leak
... 
... # Twilio SMS alert function
... def send_sms_alert():
...     # Twilio credentials (replace with your own)
...     account_sid = 'your_account_sid'
...     auth_token = 'your_auth_token'
...     client = Client(account_sid, auth_token)
... 
...     # Send an SMS alert
...     message = client.messages.create(
...         body="Leak Detected in Pipeline! Immediate action required.",
...         from_='your_twilio_phone_number',
...         to='recipient_phone_number'
...     )
...     print(f"SMS sent: {message.sid}")
... 
... # Streamlit app to visualize the sensor data and show leak detection
... st.title('Pipeline Monitoring System')
... 
... # Main loop to simulate sensor data and display it on the dashboard
... while True:
...     pressure, flow_rate, temperature = simulate_sensor_data()
... 
...     # Display the simulated data in Streamlit
...     st.metric(label="Pressure (psi)", value=f"{pressure:.2f}")
...     st.metric(label="Flow Rate (gallons/min)", value=f"{flow_rate:.2f}")
...     st.metric(label="Temperature (°F)", value=f"{temperature:.2f}")
... 
...     # Check for leaks and display the result
...     if detect_leak(pressure, flow_rate):
...         st.error("Leak Detected!")
...     else:
...         st.success("No Leak Detected")
... 

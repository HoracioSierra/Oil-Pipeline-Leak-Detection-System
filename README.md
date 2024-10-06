# Pipeline Integrity Monitoring System with GPT-3.5 and Sustainable Energy Tracking
This project is a **Pipeline Integrity Monitoring System** designed to ensure the safety and efficiency of oil pipelines. Leveraging **GPT-3.5** for real-time analysis, this system monitors vital metrics such as pressure, temperature, and vibration, while also tracking environmental impact through carbon footprint calculations and renewable energy offsets.

## Features

- **Real-time Monitoring of Pressure, Temperature, and Vibration**
  - Tracks vital pipeline statistics to ensure they remain within safe operational ranges.
  - Live-updating graphs provide clear visualization of trends over time.

- **GPT-3.5 Analysis**
  - Utilizes OpenAI's GPT-3.5 to analyze sensor data and provide insightful feedback on pipeline conditions.
  - Generates brief analyses to highlight potential issues or confirm safe operations.

- **Carbon Footprint Calculation**
  - Calculates carbon emissions based on energy consumption.
  - Helps in understanding the environmental impact of pipeline operations.

- **Renewable Energy Offset Simulation**
  - Simulates how much of the pipeline's energy needs can be offset by renewable sources like solar and wind.
  - Displays remaining energy required from non-renewable sources.

- **Emission Report**
  - Provides a live feed of energy consumption, renewable offsets, and carbon footprint.
  - Summarizes total energy consumed and offset upon stopping the monitoring.

- **Dual Graphing System**
  - **Trendline Graph**: Displays pressure, vibration, and temperature over time.
  - **Energy Consumption vs. Renewable Offset Graph**: Compares total energy used with renewable energy offsets.

## Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Web framework for live data visualization and monitoring.
- **OpenAI GPT-3.5**: Provides real-time analysis of pipeline data.
- **Matplotlib**: For creating dynamic, live-updating graphs.
- **dotenv**: Manages environment variables securely.

## How It Works

1. **Start Monitoring**
   - Begin real-time simulation of sensor data for pressure, vibration, temperature, and energy consumption.
   - GPT-3.5 analyzes the data to ensure pipeline integrity and provide actionable insights.

2. **Renewable Energy Simulation**
   - The system simulates energy consumption by the pipeline.
   - Estimates the portion of energy that can be offset by solar and wind energy generation.

3. **Emission Report**
   - Live updates on total energy consumed, renewable energy offset, and carbon footprint.
   - Provides a summary report upon stopping the monitoring.

4. **Stop Monitoring**
   - Final trendline graphs are displayed.
   - Comprehensive emission report is generated.

## Installation

To run this project locally, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/HoracioSierra/Pipeline-Integrity-Monitoring-System.git
   Navigate to the Project Directory

2. **Navigate to the Project Directoy**
   
   - cd Pipeline-Integrity-Monitoring-System
   
3. **Create a Virtual Environment**

   - python3 -m venv env
   - source env/bin/activate   # On Windows use `env\Scripts\activate`
   
4. **Install Dependencies**

   - pip install -r requirements.txt
   
5. **Set Up OpenAI API Key**

   * Create a .env file in the project root directory:
   
     - touch .env
   * Add your OpenAI API key to the .env file:
     
     - OPENAI_API_KEY=your_openai_api_key_here

6. **Run the Application**
    - streamlit run pipgpt-4.py
      
## Usage

1. **Start Monitoring**
   - Click the "Start Monitoring" button to begin real-time data simulation and monitoring.
   - Live graphs and metrics will update every 15 seconds.

2. **Stop Monitoring**
    - Click the "Stop Monitoring" button to end the monitoring session.
    - Final graphs and an emission report will be displayed.
      
3. **Customization**
    - Adjusting the Data Simulation Speed
    - The delay between data updates is currently set to 15 seconds (time.sleep(15)).
    - To make the monitoring faster, you can decrease the delay time. For example, change it to time.sleep(10) for 10-second intervals.
   ##Important Note: Reducing the delay may lead to issues with GPT-3.5 analysis generation, as the model might not have enough time to fully process and return a response before the next update. It is recommended to keep a delay of at least 10 seconds to ensure stable performance.

## File Structure
 - pipeline_monitor.py: Main script for running the real-time monitoring system.
 - .env: Environment file (not pushed to GitHub, used to store API keys).
 - requirements.txt: List of dependencies required to run the project.
 
**LICENSE**: [MIT License](LICENSE) file.

## Contribution
  - Contributions are welcome! Feel free to fork this repository, submit issues, or open pull requests to enhance the project. Whether it's improving the codebase, adding new features, or enhancing documentation, your contributions are highly appreciated.

## License
  - This project is licensed under the MIT License. See the LICENSE file for details.

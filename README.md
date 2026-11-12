# Smart Electrical Energy Meter

### Real-Time Power Quality Monitoring and Harmonic Analysis Using Python

## Project Overview

This project presents a software-based Smart Electrical Energy Meter developed using Python. It simulates electrical signals and performs real-time electrical parameter measurement, energy consumption calculation, harmonic analysis and power quality monitoring through an interactive Streamlit dashboard.

## Features

- AC voltage and current signal generation
- RMS voltage and current measurement
- Active, apparent and reactive power calculation
- Power factor calculation
- Energy consumption in Wh and kWh
- FFT-based harmonic analysis
- Total Harmonic Distortion (THD) calculation
- Voltage sag, swell and interruption simulation
- Automatic voltage event detection
- Interactive power quality dashboard
- Downloadable CSV reports
- Measurement accuracy and theoretical reference comparison

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- Streamlit

## Project Structure

- `app.py` – Main Streamlit dashboard
- `measurements.py` – Electrical parameter calculations
- `power_quality.py` – FFT and THD analysis
- `event_detection.py` – Voltage disturbance detection
- `signal_generator.py` – AC signal generation

## Installation and Execution

Clone the repository:

```bash
git clone https://github.com/harshitha-karne/smart-electrical-energy-meter.git
```

Navigate to the project directory:

```bash
cd smart-electrical-energy-meter
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Project Objective

To develop an interactive software simulation of a smart electrical energy meter capable of measuring electrical parameters and monitoring power quality under different operating conditions.

## Application

This project is developed as a Measurement and Instrumentation academic mini-project using computer-based simulation without physical hardware.

## Author

Harshitha Karne

Electrical Engineering

Indian Institute of Technology Bhubaneswar

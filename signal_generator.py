from measurements import calculate_parameters
from power_quality import calculate_thd
from event_detection import detect_voltage_events

import numpy as np
import matplotlib.pyplot as plt

# 1. Electrical supply parameters

Vrms = 230
Irms = 5
frequency = 50
phase_angle = 30

# 2. Convert RMS values into peak values

Vm = Vrms * np.sqrt(2)
Im = Irms * np.sqrt(2)

# Convert phase angle into radians
phi = np.radians(phase_angle)

# 3. Generate time samples

sampling_frequency = 5000
duration = 0.1

t = np.arange(
    0,
    duration,
    1 / sampling_frequency
)

# 4. Generate voltage waveform

voltage = Vm * (
    np.sin(2 * np.pi * frequency * t)
    + 0.05 * np.sin(2 * np.pi * 3 * frequency * t)
    + 0.03 * np.sin(2 * np.pi * 5 * frequency * t)
)

# 5. Generate current waveform

current = Im * np.sin(
    2 * np.pi * frequency * t - phi
)

# Create a voltage sag condition

voltage_sag = voltage.copy()
sag_condition = (t >= 0.04) & (t < 0.06)
voltage_sag[sag_condition] = voltage_sag[sag_condition] * 0.7


# Create a voltage swell condition

voltage_swell = voltage.copy()
swell_condition = (t >= 0.04) & (t < 0.06)
voltage_swell[swell_condition] = voltage_swell[swell_condition] * 1.3


# Create a voltage interruption condition
voltage_interrupt = voltage.copy()
interrupt_condition = (t >= 0.04) & (t < 0.06)
voltage_interrupt[interrupt_condition] = 0

# Combined Voltage Disturbances

voltage_events = voltage.copy()

# Voltage Sag: 0.02 to 0.04 seconds
sag_condition = (t >= 0.02) & (t < 0.04)
voltage_events[sag_condition] *= 0.7

# Voltage Swell: 0.04 to 0.06 seconds
swell_condition = (t >= 0.04) & (t < 0.06)
voltage_events[swell_condition] *= 1.3

# Voltage Interruption: 0.06 to 0.08 seconds
interrupt_condition = (t >= 0.06) & (t < 0.08)
voltage_events[interrupt_condition] = 0

# 6. Print basic information

print("SMART ENERGY METER")
print("------------------")

print("Peak Voltage:", round(Vm, 2), "V")
print("Peak Current:", round(Im, 2), "A")
print("Frequency:", frequency, "Hz")
print("Phase Angle:", phase_angle, "degrees")

# 7. Plot voltage and current waveforms

plt.figure(figsize=(12, 5))

plt.plot(t, voltage, label="Voltage (V)")
plt.plot(t, current, label="Current (A)")

plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")

plt.title("Simulated AC Voltage and Current Waveforms")

plt.legend()
plt.grid(True)

plt.show()


# Calculate electrical parameters
results = calculate_parameters(voltage, current)

Vrms, Irms, P, S, Q, PF = results

print("\nELECTRICAL MEASUREMENTS")
print("-----------------------")

print(f"RMS Voltage: {Vrms:.2f} V")
print(f"RMS Current: {Irms:.2f} A")
print(f"Active Power: {P:.2f} W")
print(f"Apparent Power: {S:.2f} VA")
print(f"Reactive Power: {Q:.2f} var")
print(f"Power Factor: {PF:.3f}")

# Energy Consumption Calculation

simulation_time = len(voltage) / sampling_frequency

energy_Wh = P * simulation_time / 3600
energy_kWh = energy_Wh / 1000

print("\nENERGY CONSUMPTION")
print("------------------")
print(f"Simulation Time: {simulation_time:.2f} seconds")
print(f"Energy Consumed: {energy_Wh:.6f} Wh")
print(f"Energy Consumed: {energy_kWh:.8f} kWh")


# FFT and THD Analysis

thd, frequencies, amplitudes = calculate_thd(
    voltage,
    sampling_frequency,
    frequency
)

print("\nPOWER QUALITY ANALYSIS")
print("----------------------")

print(f"Voltage THD: {thd:.4f} %")

# Plot FFT Spectrum

plt.figure(figsize=(12, 5))

plt.plot(frequencies, amplitudes)

plt.title("FFT Harmonic Spectrum")

plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (V)")

plt.xlim(0, 550)

plt.grid(True)

plt.show()

# Voltage Event Detection

events = detect_voltage_events(
    voltage_events,
    sampling_frequency
)

print("\nVOLTAGE EVENT DETECTION")
print("-----------------------")

for time, Vrms, status in events:
    print(f"Time: {time:.2f} s | RMS: {Vrms:.2f} V | Status: {status}")
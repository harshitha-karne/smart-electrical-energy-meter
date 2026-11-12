
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from measurements import calculate_parameters
from power_quality import calculate_thd
from event_detection import detect_voltage_events


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Smart Electrical Energy Meter",
    page_icon="⚡",
    layout="wide"
)


# ==================================================
# 2. PROFESSIONAL DASHBOARD THEME
# ==================================================

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0b1220;
    color: #e5e7eb;
}

[data-testid="stHeader"] {
    background-color: #0b1220;
}

.block-container {
    padding: 1rem 1.5rem;
    max-width: 100%;
}

h1 {
    color: #f8fafc !important;
    font-size: 2rem !important;
    font-weight: 750 !important;
}

h2, h3 {
    color: #e2e8f0 !important;
}

p {
    color: #cbd5e1;
}

.section-title {
    color: #38bdf8;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0.5rem 0 0.8rem 0;
}

.metric-card {
    background: linear-gradient(135deg, #172554, #14213d);
    border: 1px solid #2563eb;
    border-radius: 12px;
    padding: 13px 12px;
    min-height: 88px;
    margin-bottom: 8px;
}

.metric-label {
    color: #93c5fd;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 8px;
}

.metric-value {
    color: #ffffff;
    font-size: 1.35rem;
    font-weight: 750;
}

.energy-card {
    background: linear-gradient(135deg, #064e3b, #123c46);
    border: 1px solid #10b981;
    border-radius: 12px;
    padding: 14px;
    min-height: 85px;
}

.energy-label {
    color: #a7f3d0;
    font-size: 0.8rem;
    font-weight: 600;
}

.energy-value {
    color: #ffffff;
    font-size: 1.35rem;
    font-weight: 750;
    margin-top: 8px;
}

.thd-card {
    background: linear-gradient(135deg, #4c1d95, #312e81);
    border: 1px solid #a78bfa;
    border-radius: 12px;
    padding: 14px;
    min-height: 85px;
}

.thd-label {
    color: #ddd6fe;
    font-size: 0.8rem;
    font-weight: 600;
}

.thd-value {
    color: #ffffff;
    font-size: 1.35rem;
    font-weight: 750;
    margin-top: 8px;
}

.event-card {
    border-radius: 9px;
    padding: 10px;
    margin-bottom: 8px;
    font-size: 0.82rem;
    font-weight: 650;
}

.normal {
    background: #064e3b;
    border-left: 4px solid #10b981;
    color: #a7f3d0;
}

.sag, .swell {
    background: #78350f;
    border-left: 4px solid #f59e0b;
    color: #fde68a;
}

.interruption {
    background: #7f1d1d;
    border-left: 4px solid #ef4444;
    color: #fecaca;
}

.assessment-card {
    background: #1e293b;
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 10px;
    color: #e2e8f0;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.75rem;
    padding: 12px;
}

hr {
    border-color: #263449 !important;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. HELPER FUNCTIONS
# ==================================================

def metric_card(label, value):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def energy_card(label, value):
    st.markdown(f"""
        <div class="energy-card">
            <div class="energy-label">{label}</div>
            <div class="energy-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def style_graph(fig, ax):
    fig.patch.set_facecolor("#0B1220")
    ax.set_facecolor("#111C30")

    ax.tick_params(colors="white", labelsize=8)
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")

    ax.grid(
        True,
        color="#475569",
        alpha=0.35,
        linestyle="--"
    )

    for spine in ax.spines.values():
        spine.set_color("#475569")


# ==================================================
# 4. PROJECT TITLE
# ==================================================

st.title("⚡ Smart Electrical Energy Meter")

st.markdown(
    "<p style='color:#94a3b8; font-size:1rem;'>"
    "Real-Time Power Quality Monitoring and Harmonic Analysis"
    "</p>",
    unsafe_allow_html=True
)


# ==================================================
# 5. SIDEBAR - INTERACTIVE CONTROLS
# ==================================================

st.sidebar.title("⚙️ Simulation Controls")
st.sidebar.subheader("Electrical Parameters")

Vrms_input = st.sidebar.slider(
    "Voltage (V)", 180, 260, 230
)

Irms_input = st.sidebar.slider(
    "Current (A)", 1.0, 10.0, 5.0, step=0.5
)

frequency = st.sidebar.slider(
    "Frequency (Hz)", 45, 55, 50
)

phase_angle = st.sidebar.slider(
    "Phase Angle (degrees)", 0, 90, 30
)

st.sidebar.divider()
st.sidebar.subheader("Harmonic Distortion Controls")

third_harmonic = st.sidebar.slider(
    "3rd Harmonic (%)", 0, 20, 5
)

fifth_harmonic = st.sidebar.slider(
    "5th Harmonic (%)", 0, 20, 3
)

st.sidebar.divider()
st.sidebar.subheader("Voltage Disturbance")

disturbance = st.sidebar.selectbox(
    "Select Voltage Event",
    [
        "Normal",
        "Voltage Sag",
        "Voltage Swell",
        "Interruption"
    ]
)


# ==================================================
# 6. GENERATE ELECTRICAL SIGNALS
# ==================================================

Vm = Vrms_input * np.sqrt(2)
Im = Irms_input * np.sqrt(2)

phi = np.radians(phase_angle)

sampling_frequency = 10000
duration = 1.0

t = np.arange(
    0,
    duration,
    1 / sampling_frequency
)

# Voltage containing adjustable harmonics

voltage = Vm * (
    np.sin(2 * np.pi * frequency * t)
    + (third_harmonic / 100)
    * np.sin(2 * np.pi * 3 * frequency * t)
    + (fifth_harmonic / 100)
    * np.sin(2 * np.pi * 5 * frequency * t)
)

# Current with adjustable phase lag

current = Im * np.sin(
    2 * np.pi * frequency * t - phi
)


# ==================================================
# 7. VOLTAGE DISTURBANCE SIMULATION
# ==================================================

voltage_events = voltage.copy()

# Disturbance occurs from the 10th to 20th AC cycle

event_start = 10 / frequency
event_end = 20 / frequency

event_mask = (
    (t >= event_start)
    & (t < event_end)
)

if disturbance == "Voltage Sag":

    # Reduce voltage by 30%
    voltage_events[event_mask] *= 0.70

elif disturbance == "Voltage Swell":

    # Increase voltage by 30%
    voltage_events[event_mask] *= 1.30

elif disturbance == "Interruption":

    # Set voltage to zero
    voltage_events[event_mask] = 0


# ==================================================
# 8. ELECTRICAL PARAMETER CALCULATIONS
# ==================================================

Vrms, Irms, P, S, Q, PF = calculate_parameters(
    voltage_events,
    current
)


# ==================================================
# 9. ENERGY CALCULATION
# ==================================================

simulation_time = len(voltage_events) / sampling_frequency

energy_Wh = P * simulation_time / 3600
energy_kWh = energy_Wh / 1000

# Instantaneous power

instantaneous_power = voltage_events * current

# Cumulative energy in Wh

cumulative_energy_Wh = (
    np.cumsum(instantaneous_power)
    / sampling_frequency
    / 3600
)

energy_mWh = cumulative_energy_Wh * 1000


# ==================================================
# 10. POWER QUALITY ANALYSIS
# ==================================================

# Calculate THD using the steady-state waveform.
# This prevents the temporary voltage disturbance
# from being mistaken for harmonic distortion.

thd, frequencies, amplitudes = calculate_thd(
    voltage,
    sampling_frequency,
    frequency
)


# ==================================================
# 11. VOLTAGE EVENT DETECTION
# ==================================================

events = detect_voltage_events(
    voltage_events,
    sampling_frequency,
    nominal_voltage=Vrms_input,
    frequency=frequency
)


# ==================================================
# 12. ELECTRICAL MEASUREMENTS
# ==================================================

st.divider()

st.markdown(
    '<div class="section-title">⚡ Electrical Measurements</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

with c1:
    metric_card("RMS Voltage", f"{Vrms:.1f} V")

with c2:
    metric_card("RMS Current", f"{Irms:.2f} A")

with c3:
    metric_card("Frequency", f"{frequency} Hz")

with c4:
    metric_card("Active Power", f"{P:.1f} W")

with c5:
    metric_card("Apparent Power", f"{S:.1f} VA")

with c6:
    metric_card("Reactive Power", f"{Q:.1f} var")

with c7:
    metric_card("Power Factor", f"{PF:.3f}")


# ==================================================
# 13. ENERGY AND POWER QUALITY
# ==================================================

st.divider()

st.markdown(
    '<div class="section-title">🔋 Energy & Power Quality</div>',
    unsafe_allow_html=True
)

e1, e2, e3 = st.columns(3)

with e1:
    energy_card(
        "Energy Consumption (Wh)",
        f"{energy_Wh:.5f} Wh"
    )

with e2:
    energy_card(
        "Energy Consumption (kWh)",
        f"{energy_kWh:.8f} kWh"
    )

with e3:
    st.markdown(f"""
        <div class="thd-card">
            <div class="thd-label">
                Voltage Total Harmonic Distortion
            </div>
            <div class="thd-value">
                {thd:.3f} %
            </div>
        </div>
    """, unsafe_allow_html=True)


# ==================================================
# 14. CUMULATIVE ENERGY CONSUMPTION
# ==================================================

st.divider()

st.markdown(
    '<div class="section-title">⚡ Energy Consumption Trend</div>',
    unsafe_allow_html=True
)

fig, ax = plt.subplots(figsize=(6, 1.8))

style_graph(fig, ax)

ax.plot(
    t,
    energy_mWh,
    color="#22D3EE",
    linewidth=2,
    label="Energy (mWh)"
)

ax.fill_between(
    t,
    energy_mWh,
    color="#06B6D4",
    alpha=0.20
)

ax.set_xlabel("Time (s)", fontsize=8)
ax.set_ylabel("Energy (mWh)", fontsize=8)

legend = ax.legend(
    loc="upper left",
    fontsize=7,
    facecolor="#1E293B",
    edgecolor="#475569"
)

for item in legend.get_texts():
    item.set_color("white")

fig.tight_layout(pad=0.8)

st.pyplot(fig, use_container_width=True)

plt.close(fig)


# ==================================================
# 15. SIGNAL ANALYSIS AND MONITORING
# ==================================================

st.divider()

st.markdown(
    '<div class="section-title">📊 Signal Analysis & Monitoring</div>',
    unsafe_allow_html=True
)

left, middle, right = st.columns([1.1, 1.1, 1])


# --------------------------------------------------
# COLUMN 1: AC VOLTAGE AND CURRENT WAVEFORMS
# --------------------------------------------------

with left:

    st.markdown("**AC Voltage & Current Waveforms**")

    # Display first 0.5 seconds so that the
    # simulated disturbance can be seen clearly.

    display_mask = t < 0.5

    t_plot = t[display_mask]
    voltage_plot = voltage_events[display_mask]
    current_plot = current[display_mask]

    fig, ax1 = plt.subplots(figsize=(4.5, 2.5))

    fig.patch.set_facecolor("#111C2E")
    ax1.set_facecolor("#111C2E")

    ax1.plot(
        t_plot,
        voltage_plot,
        color="#38BDF8",
        label="Voltage (V)",
        linewidth=1.7
    )

    ax1.set_xlabel("Time (s)", color="white", fontsize=8)
    ax1.set_ylabel("Voltage (V)", color="#38BDF8", fontsize=8)

    ax1.tick_params(colors="white", labelsize=7)
    ax1.grid(True, color="#475569", alpha=0.35)

    ax2 = ax1.twinx()

    ax2.plot(
        t_plot,
        current_plot,
        color="#F59E0B",
        label="Current (A)",
        linewidth=1.7
    )

    ax2.set_ylabel("Current (A)", color="#F59E0B", fontsize=8)
    ax2.tick_params(colors="white", labelsize=7)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    legend = ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="upper right",
        fontsize=7,
        facecolor="#1E293B",
        edgecolor="#475569"
    )

    for item in legend.get_texts():
        item.set_color("white")

    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


# --------------------------------------------------
# COLUMN 2: FFT HARMONIC SPECTRUM
# --------------------------------------------------

with middle:

    st.markdown("**FFT Harmonic Spectrum**")

    fig, ax = plt.subplots(figsize=(4.5, 2.5))

    style_graph(fig, ax)

    ax.plot(
        frequencies,
        amplitudes,
        color="#A78BFA",
        linewidth=1.8
    )

    ax.fill_between(
        frequencies,
        amplitudes,
        color="#8B5CF6",
        alpha=0.18
    )

    ax.set_xlabel("Frequency (Hz)", fontsize=8)
    ax.set_ylabel("Amplitude (V)", fontsize=8)
    ax.set_xlim(0, min(600, sampling_frequency / 2))

    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


# --------------------------------------------------
# COLUMN 3: VOLTAGE EVENT DETECTION
# --------------------------------------------------

with right:

    st.markdown("**Voltage Event Detection**")

    if not events:
        st.info("No complete voltage cycles available for analysis.")

    for start_time, end_time, rms_value, status in events:

        if status == "NORMAL":
            css_class = "normal"
            icon = "🟢"

        elif status == "VOLTAGE SAG":
            css_class = "sag"
            icon = "🟠"

        elif status == "VOLTAGE SWELL":
            css_class = "swell"
            icon = "🟡"

        elif status == "INTERRUPTION":
            css_class = "interruption"
            icon = "🔴"

        else:
            css_class = "normal"
            icon = "⚪"

        st.markdown(f"""
            <div class="event-card {css_class}">
                {icon} &nbsp; {status}<br>
                <span style="font-weight:400;">
                    Time: {start_time:.2f} – {end_time:.2f} s
                    &nbsp; | &nbsp;
                    RMS: {rms_value:.2f} V
                </span>
            </div>
        """, unsafe_allow_html=True)


# ==================================================
# 16. DOWNLOADABLE REPORTS
# ==================================================

st.divider()

st.markdown(
    '<div class="section-title">📥 Download Simulation Reports</div>',
    unsafe_allow_html=True
)

measurement_data = pd.DataFrame({
    "Parameter": [
        "RMS Voltage (V)",
        "RMS Current (A)",
        "Frequency (Hz)",
        "Active Power (W)",
        "Apparent Power (VA)",
        "Reactive Power (var)",
        "Power Factor",
        "Energy (Wh)",
        "Energy (kWh)",
        "Voltage THD (%)"
    ],
    "Value": [
        Vrms,
        Irms,
        frequency,
        P,
        S,
        Q,
        PF,
        energy_Wh,
        energy_kWh,
        thd
    ]
})

measurement_csv = measurement_data.to_csv(index=False)

event_data = pd.DataFrame(
    events,
    columns=[
        "Start Time (s)",
        "End Time (s)",
        "RMS Voltage (V)",
        "Status"
    ]
)

event_csv = event_data.to_csv(index=False)

d1, d2 = st.columns(2)

with d1:
    st.download_button(
        label="📊 Download Electrical Measurements",
        data=measurement_csv,
        file_name="electrical_measurements.csv",
        mime="text/csv",
        use_container_width=True
    )

with d2:
    st.download_button(
        label="⚡ Download Voltage Event Report",
        data=event_csv,
        file_name="voltage_event_report.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==================================================
# 17. AUTOMATIC POWER QUALITY ANALYSIS
# ==================================================

st.divider()

st.subheader("📋 Automatic Power Quality Analysis")


# Power factor assessment

if PF >= 0.95:
    pf_status = "Good"
    pf_message = "The simulated system has a good power factor."

elif PF >= 0.85:
    pf_status = "Moderate"
    pf_message = "The simulated system has a moderate power factor."

else:
    pf_status = "Low"
    pf_message = "The simulated system has a low power factor."


# Harmonic distortion assessment

if thd < 5:
    thd_status = "Low"
    thd_message = "Low harmonic distortion is observed."

elif thd <= 8:
    thd_status = "Moderate"
    thd_message = "Moderate harmonic distortion is observed."

else:
    thd_status = "High"
    thd_message = "High harmonic distortion is observed."


# Count continuous voltage events

event_counts = {
    "NORMAL": 0,
    "VOLTAGE SAG": 0,
    "VOLTAGE SWELL": 0,
    "INTERRUPTION": 0
}

for event in events:
    status = str(event[3]).strip().upper()

    if status in event_counts:
        event_counts[status] += 1


normal_count = event_counts["NORMAL"]
sag_count = event_counts["VOLTAGE SAG"]
swell_count = event_counts["VOLTAGE SWELL"]
interruption_count = event_counts["INTERRUPTION"]

abnormal_count = (
    sag_count + swell_count + interruption_count
)


# Display summary metrics

a1, a2, a3 = st.columns(3)

a1.metric("Power Factor Status", pf_status)
a2.metric("Harmonic Distortion", thd_status)
a3.metric("Total Event Intervals", len(events))

st.markdown("### Electrical System Assessment")

st.markdown(
    f'<div class="assessment-card">'
    f'<b>Power Factor:</b> {pf_message}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="assessment-card">'
    f'<b>Harmonic Analysis:</b> {thd_message}</div>',
    unsafe_allow_html=True
)

st.markdown("### Voltage Event Summary")

v1, v2, v3, v4 = st.columns(4)

v1.metric("Normal", normal_count)
v2.metric("Voltage Sag", sag_count)
v3.metric("Voltage Swell", swell_count)
v4.metric("Interruption", interruption_count)

st.metric("Total Abnormal Event Intervals", abnormal_count)

if abnormal_count == 0:
    st.success("No abnormal voltage events were detected.")

else:
    st.warning(
        f"{abnormal_count} abnormal voltage event interval(s) detected."
    )


# ==================================================
# 18. FOOTER
# ==================================================

st.markdown("""
<hr>
<div class="footer">
Smart Electrical Energy Meter | Measurement and Instrumentation Project
</div>
""", unsafe_allow_html=True)
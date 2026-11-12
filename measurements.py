
import numpy as np

def calculate_parameters(voltage, current):

    # 1. Calculate RMS Voltage
    Vrms = np.sqrt(np.mean(voltage**2))

    # 2. Calculate RMS Current
    Irms = np.sqrt(np.mean(current**2))

    # 3. Calculate Active Power
    P = np.mean(voltage * current)

    # 4. Calculate Apparent Power
    S = Vrms * Irms

    # 5. Calculate Reactive Power magnitude
    Q = np.sqrt(max(S**2 - P**2, 0))

    # 6. Calculate Power Factor
    PF = P / S if S != 0 else 0

    return Vrms, Irms, P, S, Q, PF


import numpy as np


def detect_voltage_events(
    voltage,
    sampling_frequency,
    nominal_voltage=230,
    frequency=50
):

    if sampling_frequency <= 0 or frequency <= 0:
        raise ValueError("Sampling frequency and supply frequency must be positive.")

    if nominal_voltage <= 0:
        raise ValueError("Nominal voltage must be positive.")

    voltage = np.asarray(voltage, dtype=float)

    if voltage.size == 0:
        return []

    # Determine the number of complete AC cycles
    total_cycles = int(
        len(voltage) * frequency / sampling_frequency
    )

    cycle_results = []

    # Analyse one complete AC cycle at a time
    for cycle_number in range(total_cycles):

        start = round(
            cycle_number * sampling_frequency / frequency
        )

        end = round(
            (cycle_number + 1) * sampling_frequency / frequency
        )

        cycle = voltage[start:end]

        if len(cycle) == 0:
            continue

        # Calculate cycle RMS voltage
        Vrms = np.sqrt(np.mean(cycle ** 2))

        # Classify voltage condition
        if Vrms < 0.1 * nominal_voltage:
            status = "INTERRUPTION"

        elif Vrms < 0.9 * nominal_voltage:
            status = "VOLTAGE SAG"

        elif Vrms > 1.1 * nominal_voltage:
            status = "VOLTAGE SWELL"

        else:
            status = "NORMAL"

        start_time = start / sampling_frequency
        end_time = end / sampling_frequency

        cycle_results.append(
            (start_time, end_time, Vrms, status)
        )

    # Combine consecutive cycles with identical status
    grouped_events = []

    for start_time, end_time, rms_value, status in cycle_results:

        if (
            grouped_events
            and grouped_events[-1][3] == status
        ):

            old_start, _, old_rms, old_status, count = grouped_events[-1]

            new_rms = (
                (old_rms * count + rms_value)
                / (count + 1)
            )

            grouped_events[-1] = (
                old_start,
                end_time,
                new_rms,
                old_status,
                count + 1
            )

        else:

            grouped_events.append(
                (
                    start_time,
                    end_time,
                    rms_value,
                    status,
                    1
                )
            )

    # Return one entry for each continuous event
    results = [
        (start, end, rms, status)
        for start, end, rms, status, count in grouped_events
    ]

    return results


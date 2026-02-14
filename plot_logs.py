#!/usr/bin/env python3
"""
Plot plant monitor sensor data — 3 separate graphs for humidity,
temperature, and moisture vs. timestamp.

Usage:
    python3 plot_logs.py <csv_file>
    python3 plot_logs.py logs/02-14-26.csv
"""

import sys
import re
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def parse_csv(path):
    timestamps, humidity, temperature, moisture = [], [], [], []

    with open(path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    for line in lines[1:]:
        parts = line.split(", ")
        if len(parts) < 2:
            continue

        ts_str = parts[0].strip()
        data_str = ", ".join(parts[1:])

        try:
            ts = datetime.strptime(ts_str, "%H:%M:%S.%f")
        except ValueError:
            continue

        h_match = re.search(r"h=([\d.]+)", data_str)
        t_match = re.search(r"t=([\d.]+)", data_str)
        m_match = re.search(r"moisture0=([\d.]+)", data_str)

        timestamps.append(ts)
        humidity.append(float(h_match.group(1)) if h_match else None)
        temperature.append(float(t_match.group(1)) if t_match else None)
        moisture.append(float(m_match.group(1)) if m_match else None)

    return timestamps, humidity, temperature, moisture


def plot(timestamps, humidity, temperature, moisture, title_date=""):
    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    fig.suptitle(f"Plant Monitor — {title_date}" if title_date else "Plant Monitor",
                 fontsize=14, fontweight="bold")

    ts_h = [t for t, v in zip(timestamps, humidity) if v is not None]
    val_h = [v for v in humidity if v is not None]
    axes[0].plot(ts_h, val_h, color="#1f77b4", linewidth=1)
    axes[0].fill_between(ts_h, val_h, alpha=0.15, color="#1f77b4")
    axes[0].set_ylabel("Humidity (%)")
    axes[0].set_title("Humidity")
    axes[0].grid(True, alpha=0.3)

    ts_t = [t for t, v in zip(timestamps, temperature) if v is not None]
    val_t = [v for v in temperature if v is not None]
    axes[1].plot(ts_t, val_t, color="#e74c3c", linewidth=1)
    axes[1].fill_between(ts_t, val_t, alpha=0.15, color="#e74c3c")
    axes[1].set_ylabel("Temperature (°C)")
    axes[1].set_title("Temperature")
    axes[1].grid(True, alpha=0.3)

    ts_m = [t for t, v in zip(timestamps, moisture) if v is not None]
    val_m = [v for v in moisture if v is not None]
    axes[2].plot(ts_m, val_m, color="#2ecc71", linewidth=1)
    axes[2].fill_between(ts_m, val_m, alpha=0.15, color="#2ecc71")
    axes[2].set_ylabel("Moisture")
    axes[2].set_title("Moisture")
    axes[2].grid(True, alpha=0.3)

    axes[2].set_xlabel("Time")
    axes[2].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    fig.autofmt_xdate(rotation=45)

    plt.tight_layout()
    plt.savefig("logs/02-14-26.png", dpi=150, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <csv_file>")
        sys.exit(1)

    csv_path = sys.argv[1]

    import os
    title_date = os.path.splitext(os.path.basename(csv_path))[0]

    timestamps, humidity, temperature, moisture = parse_csv(csv_path)
    print(f"Loaded {len(timestamps)} data points from {csv_path}")
    plot(timestamps, humidity, temperature, moisture, title_date)

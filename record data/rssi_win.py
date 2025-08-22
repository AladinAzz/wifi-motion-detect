import subprocess
import time
import re
import csv
import random

csv_file = "wifi_signal_m.csv"

# Write header to CSV file if it doesn't exist
try:
    with open(csv_file, 'r') as f:
        pass
except FileNotFoundError:
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "rssi", "label"])

start_time = time.time()
while time.time() - start_time < 600:
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode(errors="ignore")
        match = re.search(r"Signal\s*:\s*(\d+)%", result)
        if match:
            signal_percent = int(match.group(1))
            # Convert percent to RSSI (approximate)
            rssi = int((signal_percent / 2) - 100)
            print("RSSI:", rssi)

            # Simulate motion detection (replace with your actual logic)
            label = "motion" if random.random() < 0.2 else "no_motion"

            # Append timestamp, RSSI, and label to CSV file
            timestamp = int(time.time())
            with open(csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, rssi, label])
    except Exception as e:
        print("Error:", e)
    time.sleep(0.3)
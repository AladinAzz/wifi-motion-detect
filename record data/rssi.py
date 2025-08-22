import subprocess
import time
import re
import csv
import random

iface = "wlp2s0"  # replace with your Wi-Fi interface
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
        result = subprocess.check_output(["sudo", "iwlist", iface, "scan"]).decode()
        match = re.search(r"Signal level=(-\d+)", result)
        if match:
            rssi = int(match.group(1))
            print("RSSI:", rssi)

            # Simulate motion detection (replace with your actual logic)
              # 20% chance of motion
            label = "motion"
            
            # Append timestamp, RSSI, and label to CSV file
            timestamp = int(time.time())  # Unix timestamp
            with open(csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, rssi, label])
    except Exception as e:
        print("Error:", e)
    time.sleep(0.3)
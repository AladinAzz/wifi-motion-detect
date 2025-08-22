import cv2
import numpy as np
import threading
import subprocess
import time
import re
import csv

csv_file = "data.csv"
motion_label = "no_motion"  # Shared variable

def camera_motion_thread():
    global motion_label
    cap = cv2.VideoCapture(0)
    ret, first_frame = cap.read()
    if not ret:
        print("Failed to grab first frame")
        return

    height, width = first_frame.shape[:2]
    line_x = width // 2
    prev_line = cv2.cvtColor(first_frame[:, line_x:line_x+1], cv2.COLOR_BGR2GRAY)
    motion_threshold = 30
    min_changed_pixels = height * 0.05

    last_update_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        current_line = cv2.cvtColor(frame[:, line_x:line_x+1], cv2.COLOR_BGR2GRAY)
        line_delta = cv2.absdiff(prev_line, current_line)
        changed_pixels = np.sum(line_delta > motion_threshold)
        motion_label = "motion" if changed_pixels > min_changed_pixels else "no_motion"

        # Update prev_line every 5 seconds
        if time.time() - last_update_time >= 5 and motion_label == "no_motion":
            prev_line = current_line
            last_update_time = time.time()

        display_frame = frame.copy()
        cv2.line(display_frame, (line_x, 0), (line_x, height), (0, 0, 255), 1)
        status = "Motion Detected" if motion_label == "motion" else "No Motion"
        color = (0, 0, 255) if motion_label == "motion" else (0, 255, 0)
        cv2.putText(display_frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow('Motion Detection', display_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def wifi_rssi_thread():
    global motion_label
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
                rssi = int((signal_percent / 2) - 100)
                print(f"RSSI: {rssi}, Motion: {motion_label}")

                timestamp = int(time.time())
                with open(csv_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, rssi, motion_label])
        except Exception as e:
            print("Error:", e)
        time.sleep(0.3)

if __name__ == "__main__":
    cam_thread = threading.Thread(target=camera_motion_thread)
    wifi_thread = threading.Thread(target=wifi_rssi_thread)
    cam_thread.start()
    wifi_thread.start()
    cam_thread.join()
    wifi_thread.join()
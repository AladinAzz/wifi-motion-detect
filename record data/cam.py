import cv2
import numpy as np

def detect_motion_single_line():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    
    # Get the frame dimensions
    ret, first_frame = cap.read()
    if not ret:
        print("Failed to grab first frame")
        return
    
    height, width = first_frame.shape[:2]
    
    # Define which column to sample (middle of the frame)
    line_x = width // 2
    
    # Initialize previous column
    prev_line = cv2.cvtColor(first_frame[:, line_x:line_x+1], cv2.COLOR_BGR2GRAY)
    
    # Threshold for motion detection
    motion_threshold = 30  # Adjust as needed
    min_changed_pixels = height * 0.05  # At least 5% of pixels should change
    
    print("Motion detection started. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Extract just the middle column from the frame
        current_line = cv2.cvtColor(frame[:, line_x:line_x+1], cv2.COLOR_BGR2GRAY)
        
        # Calculate absolute difference between current and previous column
        line_delta = cv2.absdiff(prev_line, current_line)
        
        # Count pixels with significant change
        changed_pixels = np.sum(line_delta > motion_threshold)
        
        # Determine if motion is detected
        motion_detected = changed_pixels > min_changed_pixels
        
        # Create a visual representation
        display_frame = frame.copy()
        
        # Draw the scan line (vertical)
        cv2.line(display_frame, (line_x, 0), (line_x, height), (0, 0, 255), 1)
        
        # Display motion status
        status = "Motion Detected" if motion_detected else "No Motion"
        color = (0, 0, 255) if motion_detected else (0, 255, 0)
        cv2.putText(display_frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # Visualization of the column delta
        line_delta_visual = np.repeat(line_delta, 50, axis=1)  # Make it 50 pixels wide
        line_delta_visual = cv2.applyColorMap(line_delta_visual, cv2.COLORMAP_JET)
        
        # Show the frames
        cv2.imshow('Motion Detection', display_frame)
        cv2.imshow('Line Delta', line_delta_visual)
        
        # Print motion status to console
        print(f"\r{status}", end="")
        
        # Update previous line
        prev_line = current_line
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    print("\nMotion detection stopped.")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_motion_single_line()
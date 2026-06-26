import cv2
import time

# Set the duration and interval for the timelapse
duration = 10  # Duration in seconds
interval = 0.16  # Interval in seconds

# Open the default webcam
cap = cv2.VideoCapture(1)

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'h264')
out = cv2.VideoWriter('timelapse1.mp4', fourcc, 1 / interval, (int(cap.get(3)), int(cap.get(4))))

start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time > duration:
        break

    # Write the frame to the video file
    out.write(frame)

    # Show the frame (optional)
    cv2.imshow('Timelapse', frame)

    # Wait for the specified interval
    time.sleep(interval)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when done
cap.release()
out.release()
cv2.destroyAllWindows()
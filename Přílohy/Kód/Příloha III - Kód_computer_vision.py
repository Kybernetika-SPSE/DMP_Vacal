import cv2
import numpy as np
from picamera2 import Picamera2
import time
import libcamera

# --- Configuration ---
# Define the range for red color in HSV
# IMPORTANT: Tune these values AFTER confirming color balance and format handling!
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

MIN_RADIUS = 15

# --- Manual Colour Gain Settings ---
# Adjusted gain values based on your findings
red_gain = 1.9  # Multiplier for the Red channel
blue_gain = 1.5 # Multiplier for the Blue channel

# Camera setup
picam2 = Picamera2()
# Request BGR888 format
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)
picam2.configure(config)
print("Requesting BGR888 format from camera.")

print("Starting camera...")
picam2.start()
time.sleep(1.0) # Short sleep just for camera init

# --- Set Manual White Balance (Colour Gains) ---
try:
    print(f"Disabling AWB and setting manual ColourGains (Swapped Order):")
    print(f"  Red Gain Value: {red_gain}")
    print(f"  Blue Gain Value: {blue_gain}")
    # Pass gains in swapped order (blue_gain, red_gain) as needed for this setup
    picam2.set_controls({"AwbEnable": False, "ColourGains": (blue_gain, red_gain)})
    time.sleep(0.5)
    print("Manual ColourGains set.")
except Exception as e:
    print(f"Warning: Could not set manual ColourGains. Error: {e}")
    print("Proceeding with camera defaults.")


print("Camera ready. Looking for red ball...")

# --- Main Loop ---
try:
    while True:
        # Capture frame as a numpy array (in BGR format)
        frame = picam2.capture_array()

        # --- Image Processing ---
        # 1. Blur the frame slightly to reduce noise
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)

        # 2. Convert the frame from BGR to HSV color space
        # *** CORRECTED: Use COLOR_BGR2HSV ***
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # 3. Create masks for the defined red color ranges
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # 4. Perform morphological operations
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # 5. Find contours
        contours, _ = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        center = None
        ball_pos_text = "Ball Position: None"

        # --- Ball Detection Logic ---
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            if radius > MIN_RADIUS:
                M = cv2.moments(c)
                if M["m00"] > 0:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    ball_pos_text = f"Ball Position: ({center[0]}, {center[1]})"
                    print(ball_pos_text)
                    # --- Visualization (Drawing on BGR frame) ---
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) # Yellow (BGR)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1) # Red (BGR)
                else:
                    center = (int(x), int(y))
                    ball_pos_text = f"Ball Position (Approx): ({center[0]}, {center[1]})"
                    print(ball_pos_text)
                    # --- Visualization (Drawing on BGR frame) ---
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)


        # --- Display ---
        # Add text overlay (White in BGR)
        cv2.putText(frame, ball_pos_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 'frame' is already in BGR format, which cv2.imshow expects. Display directly.
        # *** CORRECTED: Display frame directly ***
        cv2.imshow("Frame", frame)
        # Uncomment the line below to see the mask for HSV tuning
        # cv2.imshow("Mask", mask)

        # --- Exit Condition ---
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("Exiting...")
            break

finally:
    # Clean up
    print("Stopping camera and closing windows.")
    cv2.destroyAllWindows()
    picam2.stop()

import cv2
import pytesseract
import time

# Specify the path to tesseract.exe (if not in PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Function to process the image and perform OCR
def process_and_scan_number_plate(frame):
    # Resize the image for better OCR
    resized_image = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to smooth the image
    blurred_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)

    # Perform OCR on the processed image
    ocr_result = pytesseract.image_to_string(blurred_image, lang='eng',
                                             config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    # Clean up the result
    clean_result = "".join(ocr_result.split()).replace(":", "").replace("-", "")

    return clean_result


# Initialize the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    print("Press 'q' to quit.")

# List to store the scanned license plates
scanned_plates = []

# Timing variables
last_scan_time = time.time()  # Record the current time

while True:
    # Capture frame-by-frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Display the live camera feed
    cv2.imshow('Camera - License Plate Scanner', frame)

    # Check if 2 seconds have passed
    current_time = time.time()
    if current_time - last_scan_time >= 2:  # Every 2 seconds
        # Process and scan the number plate
        license_plate_text = process_and_scan_number_plate(frame)

        # Store the scanned result
        scanned_plates.append(license_plate_text)

        print(f"Scanned License Plate Text: {license_plate_text}")





        # Display the scanned result



        # Update last scan time
        last_scan_time = current_time

    # If 'q' is pressed, exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()


# Print and store each scanned plate in a text file
with open("scanned_license_plates.txt", "w") as file:
    # Write the header to the file
    file.write(f"{'Predicted License Plate':<25}\n")
    file.write("-" * 25 + "\n")

    for plate in scanned_plates:
        # Print the result to the console
        print(f"{plate:<25}")
        # Write the result to the file
        file.write(f"{plate:<25}\n")

print("\nResults saved to 'scanned_license_plates.txt'.")

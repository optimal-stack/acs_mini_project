import cv2
import pytesseract
import time


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def process_and_scan_number_plate(frame):
    
    resized_image = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)
    ocr_result = pytesseract.image_to_string(blurred_image, lang='eng',
                                    config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    clean_result = "".join(ocr_result.split()).replace(":", "").replace("-", "")

    return clean_result


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    print("Press 'q' to quit.")

scanned_plates = []


last_scan_time = time.time() 

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break


    cv2.imshow('Camera - License Plate Scanner', frame)

    current_time = time.time()
    if current_time - last_scan_time >= 2: 
        license_plate_text = process_and_scan_number_plate(frame)

    
        scanned_plates.append(license_plate_text)

        print(f"Scanned License Plate Text: {license_plate_text}")





        



        
        last_scan_time = current_time

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()


with open("scanned_license_plates.txt", "w") as file:
    
    file.write(f"{'Predicted License Plate':<25}\n")
    file.write("-" * 25 + "\n")

    for plate in scanned_plates:
        
        print(f"{plate:<25}")
        # Write the result to the file
        file.write(f"{plate:<25}\n")

print("\nResults saved to 'scanned_license_plates.txt'.")

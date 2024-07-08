import cv2
import pytesseract


def process_screenshot(image_path):
    # Path to Tesseract executable (update as per your installation)
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    # Read the image using OpenCV
    image_path = "captcha_screenshot.png"
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply some preprocessing
    # Remove noise
    image = cv2.medianBlur(image, 3)

    # Apply thresholding
    _, image = cv2.threshold(image, 135, 255, cv2.THRESH_BINARY)

    # Dilate the image to make the text thicker
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (1, 1))
    image = cv2.dilate(image, kernel, iterations=1)

    processed_image_path = "processed_image.png"
    cv2.imwrite(processed_image_path, image)

    # Use Tesseract to do OCR on the image
    custom_config = r"--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789+"
    text = pytesseract.image_to_string(image, config=custom_config)

    # Post-processing: replace '4' with '+' if it's likely a misrecognized '+'

    # text = text.replace("4", "+")

    if text[2] == "4":
        text = text[:2] + text[2].replace("4", "+") + text[3:]

    text = text.replace("\n", "")
    calculated = eval(text)

    return text


# Example usage:
if __name__ == "__main__":
    image_path = "captcha_screenshot.png"  # Update with your actual screenshot path
    process_screenshot(image_path)

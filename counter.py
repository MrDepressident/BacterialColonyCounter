import cv2
import numpy as np

# Global variables for storing circle properties
circle_center = (100, 100)  # Initial center of the circle
circle_radius = 50  # Initial radius of the circle


def load_image(file_path):
    """Load an image from the specified file path."""
    img = cv2.imread(file_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {file_path}")
    return img


def preprocess_image(img):
    """Convert image to grayscale and apply binary thresholding."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def count_and_display_colonies(original_img, contours):
    """Count and display the colonies on the original image."""
    # Draw contours on the original image
    output_img = original_img.copy()
    for cnt in contours:
        # Draw each contour in red
        cv2.drawContours(output_img, [cnt], -1, (0, 0, 255), 2)

    # Display the result
    colony_count = len(contours)
    cv2.putText(output_img, f"Colonies Count: {colony_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Colony Counter', output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the output image
    cv2.imwrite('colony_counter_output.png', output_img)
    print(f"Number of colonies detected: {colony_count}")


def on_change(val):
    """Callback function for trackbar changes (does nothing)."""
    pass


def select_circular_area(img):
    """
    Allows the user to select a circular area by adjusting the radius and position.
    Returns the mask of the circular area and the circle parameters.
    """
    global circle_center, circle_radius

    # Create a window
    window_name = 'Adjust Circle'
    cv2.namedWindow(window_name)

    # Trackbars for circle position and radius
    cv2.createTrackbar('Center X', window_name, circle_center[0], img.shape[1], on_change)
    cv2.createTrackbar('Center Y', window_name, circle_center[1], img.shape[0], on_change)
    cv2.createTrackbar('Radius', window_name, circle_radius, min(img.shape[0], img.shape[1]) // 2, on_change)

    while True:
        # Get the current values of the trackbars
        x = cv2.getTrackbarPos('Center X', window_name)
        y = cv2.getTrackbarPos('Center Y', window_name)
        radius = cv2.getTrackbarPos('Radius', window_name)
        circle_center = (x, y)
        circle_radius = radius

        # Create a mask with the circular area
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.circle(mask, circle_center, circle_radius, 255, thickness=-1)

        # Display the image with the selected circular area
        img_copy = img.copy()
        cv2.circle(img_copy, circle_center, circle_radius, (0, 0, 255), 2)
        cv2.imshow(window_name, img_copy)

        # Exit on pressing the ESC key
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    return mask, circle_center, circle_radius


def detect_colonies_in_circle(binary_img, mask):
    """
    Detect colonies inside the circular mask using contour detection.
    """
    # Apply the circular mask to the binary image
    masked_img = cv2.bitwise_and(binary_img, binary_img, mask=mask)

    # Find contours in the masked binary image
    contours, _ = cv2.findContours(masked_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def main():
    # Path to the image file
    image_path = "C:/Users/dimol/Downloads/plate2.jpg"  # Replace with your image file path

    # Load and preprocess the image
    img = load_image(image_path)
    binary_img = preprocess_image(img)

    # Allow user to select a circular area
    mask, center, radius = select_circular_area(img)

    # Detect colonies inside the circular area
    colonies = detect_colonies_in_circle(binary_img, mask)

    # Count and display the results
    count_and_display_colonies(img, colonies)


if __name__ == "__main__":
    main()

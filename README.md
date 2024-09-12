Prerequisites

This project was built on Python 3.11 with the following requirements:

numpy==2.0.0
opencv-python==4.10.0.84

Usage
Once you have a local copy of the repository, place images of the agar plates in the images/ directory

To run the script, you can use the following call to main:

`def main():
    # Path to the image file
    image_path = "images/plate1.jpg"  # Replace with your image file path

    # Load and preprocess the image
    img = load_image(image_path)
    binary_img = preprocess_image(img)

    # Allow user to select a circular area
    mask, center, radius = select_circular_area(img)

    # Detect colonies inside the circular area
    colonies = detect_colonies_in_circle(binary_img, mask)

    # Count and display the results
    count_and_display_colonies(img, colonies)`

Once you have run the script, a window will appear for you to interact with. It will ask you to adjust the coordinates of the circle and its radius.

In order to progress from one "screen" to the next, press the ESC key on your keyboard.


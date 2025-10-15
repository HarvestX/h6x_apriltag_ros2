'''
Resize the original apriltag images to 60x60mm with 300dpi
and add black dots at the corners.
'''
import os
from PIL import Image, ImageDraw


def resize_image(image, new_width_mm, new_height_mm, dpi=300):
    '''
    Resize the image to the specified dimensions in mm at the specified DPI.
    '''
    # Calculate the pixel dimensions
    # 25.4 is the number of mm in an inch
    new_width_px = int(new_width_mm / 25.4 * dpi)
    new_height_px = int(new_height_mm / 25.4 * dpi)

    # Resize the image
    resized_image = image.resize((new_width_px, new_height_px), Image.NEAREST)

    return resized_image


def add_dots_to_image(image, dot_size=3):
    '''
    Add black dots at the corners of the image the visibility of the margin
    '''
    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Get image dimensions
    width, height = image.size

    # Add black dots at the corners
    # Top-left corner
    draw.rectangle([0, 0, dot_size, dot_size], fill="black")
    # Top-right corner
    draw.rectangle([width - dot_size, 0, width, dot_size], fill="black")
    # Bottom-left corner
    draw.rectangle([0, height - dot_size, dot_size, height], fill="black")
    # Bottom-right corner
    draw.rectangle([width - dot_size, height - dot_size,
                   width, height], fill="black")

    return image


def load_image(image_path):
    '''
    Load an image from the specified file path.
    '''
    return Image.open(image_path)


def save_image(image, output_path, dpi=300):
    '''
    Save the image with DPI information
    '''
    image.save(output_path, dpi=(dpi, dpi))


def process_images_in_directory(
        input_directory, output_directory, new_width_mm, new_height_mm, dpi=300, dot_size=3):
    '''
    Process all images in the input directory and save the results in the output directory.
    '''
    os.makedirs(output_directory, exist_ok=True)

    # Loop through all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)

            # Step 1: Load image
            image = load_image(input_path)

            # Step 2: Resize image
            resized_image = resize_image(
                image, new_width_mm, new_height_mm, dpi)

            # Step 3: Add dots to resized image
            final_image = add_dots_to_image(resized_image, dot_size)

            # Save the final image
            save_image(final_image, output_path, dpi)


if __name__ == "__main__":
    INPUT_DIRECTORY = 'tag36h11_in'
    OUTPUT_DIRECTORY = 'tag36h11_out'
    NEW_WIDTH_MM = 60
    NEW_HEIGHT_MM = 60
    DPI = 300
    DOT_SIZE_AROUND_MARGIN = 3

    process_images_in_directory(
        INPUT_DIRECTORY, OUTPUT_DIRECTORY, NEW_WIDTH_MM, NEW_HEIGHT_MM, DPI, DOT_SIZE_AROUND_MARGIN)

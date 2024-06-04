from PIL import Image
import io

def process_image(image):
    # Open the image using PIL
    img = Image.open(image)

    # Perform your image processing here
    # For example, let's just return the image size
    width, height = img.size

    # Return the result as a dictionary
    return {'width': width, 'height': height}

import subprocess
from PIL import Image
from image_preparation import resize_image_to_fit, prepare_image


def get_printer_area(printer_name):
    # Default paper size in points (1/72 inch)
    # Assume 8.5x11 inch paper (letter size)
    paper_width = 612
    paper_height = 792
    return paper_width, paper_height


def print_image_inner(printer_name, image):
    temp_image_path = "/tmp/temp_image_to_print.jpg"
    image.save(temp_image_path)

    subprocess.run(["lp", "-d", printer_name, temp_image_path])


def print_image(image, text):
    printer_name = subprocess.check_output(["lpstat", "-d"]).decode().strip().split(": ")[1]
    print_area = get_printer_area(printer_name)

    img_with_text = prepare_image(image, text)
    resized_image = resize_image_to_fit(img_with_text, *print_area)

    print_image_inner(printer_name, resized_image)

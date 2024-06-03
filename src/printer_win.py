import win32print
import win32ui
from PIL import ImageWin
from image_preparation import resize_image_to_fit, prepare_image


def get_printer_area(printer_name):
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        printer_info = win32print.GetPrinter(hPrinter, 2)
        paper_width = printer_info['pDevMode'].PaperWidth
        paper_length = printer_info['pDevMode'].PaperLength
        return paper_width, paper_length
    finally:
        win32print.ClosePrinter(hPrinter)


def print_image_inner(printer_name, image):
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc("Image Printing")
    hDC.StartPage()

    dib = ImageWin.Dib(image)
    dib.draw(hDC.GetHandleOutput(), (0, 0, image.width, image.height))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()


def print_image(image, text):
    printer_name = win32print.GetDefaultPrinter()
    print_area = get_printer_area(printer_name)

    img_with_text = prepare_image(image, text)
    resized_image = resize_image_to_fit(img_with_text, *print_area)

    print_image_inner(printer_name, resized_image)

from PIL import Image, ImageDraw, ImageFont
import textwrap


def resize_image_to_fit(image, target_width, target_height, dpi=150):
    target_width_pixels = target_width * dpi // 254
    target_height_pixels = target_height * dpi // 254
    img_ratio = image.width / image.height
    target_ratio = target_width_pixels / target_height_pixels

    if target_ratio > img_ratio:
        new_height = target_height_pixels
        new_width = int(new_height * img_ratio)
    else:
        new_width = target_width_pixels
        new_height = int(new_width / img_ratio)

    return image.resize((new_width, new_height), Image.ANTIALIAS)


def add_text_to_image(image, text, position, font_path='arial.ttf', font_size=100, font_color=(0, 0, 0)):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
    draw.text(position, text, font=font, fill=font_color)
    return image


def add_text_below_image(image, text, font_path='arial.ttf', font_size=20, font_color=(0, 0, 0), max_line_length=28):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    wrapped_text = textwrap.fill(text, width=max_line_length)

    draw = ImageDraw.Draw(image)
    lines = wrapped_text.split('\n')
    line_height = draw.textsize('A', font=font)[1]
    total_text_height = line_height * len(lines)

    new_height = image.height + total_text_height + 10
    new_image = Image.new('RGB', (image.width, new_height), 'white')

    new_image.paste(image, (0, 0))

    draw = ImageDraw.Draw(new_image)
    for i, line in enumerate(lines):
        text_width, _ = draw.textsize(line, font=font)
        text_position = ((new_image.width - text_width) // 2, image.height + 5 + i * line_height)
        draw.text(text_position, line, font=font, fill=font_color)

    return new_image


def prepare_image(image, text):
    img_with_text = add_text_below_image(image, text)
    return img_with_text

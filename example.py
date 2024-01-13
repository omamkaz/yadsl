#!/usr/bin/python3

import io
from yadsl import YADSL
from PIL import Image


def print_image_as_ascii(image_path, width=100):
    image = Image.open(image_path)
    image = image.resize((width, int(width * image.height / image.width)))

    # Convert the image to grayscale
    image = image.convert('L')

    # Define ASCII characters from dark to light
    ascii_chars = "@%#*+=-:. "

    # Convert each pixel to an ASCII character
    ascii_image = ""
    for pixel_value in image.getdata():
        ascii_image += ascii_chars[pixel_value // (256 // len(ascii_chars))]

    # Split the ASCII art into lines
    lines = [ascii_image[i:i+width] for i in range(0, len(ascii_image), width)]

    # Print the ASCII art
    for line in lines:
        print(line)


yd = YADSL(
    username="xxxx",
    password="xxxx"
)

yd.login()
print_image_as_ascii(io.BytesIO(yd.fetch_captcha()), 70)
yd.verify(input("? Enter Captcha Number: ").strip())
for k, v in yd.fetch_data().items():
    print(k, v, sep=": ")
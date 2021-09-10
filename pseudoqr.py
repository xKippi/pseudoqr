#!/bin/python3

######################################################
# pseudoqr
# Script to generate a qr code which can't be scanned
#
# Author: Kippi
# Version: 1.0
######################################################

# --- BEGIN IMPORTS (DO NOT EDIT) ---
import argparse
import math
import numpy
import os
import sys
from enum import IntEnum
from PIL import Image
# --- END IMPORTS

# --- BEGIN CONFIG ---

# The size of the modules (points) in px
module_size = 4

# The width of the margin surrounding the qr code in modules
margin = 4

# The qr code symbol version to use. See http://www.qrcode.com/en/about/version.html for details
symbol_version = None

# RGB value to use as foreground
foreground_pixel = [0, 0, 0]

# RGB value to use as background
background_pixel = [255, 255, 255]

# Defines if a fourth edge should be drawn
draw_fourth_edge = False

# Defines the image format. If undefined (None), derive image format from filename
image_format = None

# The output file name
filename = None

# --- END CONFIG ---

# DO NOT EDIT BELOW THIS LINE IF YOU DO NOT KNOW WHAT YOU ARE DOING

EDGE_MODULES = 7
EDGE_SIZE = EDGE_MODULES * module_size

ALIGNMENT_MODULES = 5
ALIGNMENT_SIZE = ALIGNMENT_MODULES * module_size

ALIGNMENT_PADDING = 4
ALIGNMENT_PADDING_SIZE = ALIGNMENT_PADDING * module_size

ALIGNMENT_MAX_SPACE = 23

STDOUT_FILENAME = "-"

class Direction(IntEnum):
    UP = 1
    DOWN = 2
    LEFT = 4
    RIGHT = 8


def parse_color(color, default):
    if color is None:
        return default
    else:
        return [int(color[i:i+2], 16) for i in range(0, len(color), 2)]


def create_image(output, pixels):
    array = numpy.array(pixels, dtype=numpy.uint8)
    new_image = Image.fromarray(array)

    if filename == STDOUT_FILENAME:
        output = sys.stdout

    new_image.save(output, format=image_format)


def draw_module(x, y, pixel, pixels):
    for i in range(0, module_size):
        for j in range(0, module_size):
            pixels[x + i][y + j] = pixel.copy()


def draw_dot(x, y, size, pixels, padding_direction=0):
    if size % 2 == 0 or size < 5:
        raise ValueError("\"size\" must be odd and greater or equal 5")

    for i in range(0, size):
        for j in range(0, size):
            if (j % (size - 3) == 1 and not i % (size - 1) == 0) or (i % (size - 3) == 1 and not j % (size - 1) == 0):
                pixel_to_use = background_pixel
            else:
                pixel_to_use = foreground_pixel
            draw_module(x + i * module_size, y + j * module_size, pixel_to_use, pixels)

    up = padding_direction & Direction.UP == Direction.UP
    down = padding_direction & Direction.DOWN == Direction.DOWN
    left = padding_direction & Direction.LEFT == Direction.LEFT
    right = padding_direction & Direction.RIGHT == Direction.RIGHT

    start_add = 0 if not up else -module_size
    end_add = 0 if not down else module_size

    if up:
        for i in range(0, size * module_size, module_size):
            draw_module(x - module_size, y + i, background_pixel, pixels)
    if down:
        for i in range(0, size * module_size, module_size):
            draw_module(x + size * module_size, y + i, background_pixel, pixels)
    if left:
        for i in range(0 + start_add, size * module_size + end_add, module_size):
            draw_module(x + i, y - module_size, background_pixel, pixels)
    if right:
        for i in range(0 + start_add, size * module_size + end_add, module_size):
            draw_module(x + i, y + size * module_size, background_pixel, pixels)


def main():
    global module_size, margin, symbol_version, foreground_pixel, background_pixel, draw_fourth_edge, image_format, filename
    parser = argparse.ArgumentParser(description='Create a image which looks like a qr code but is unscanable')
    parser.add_argument('-s',
                        '--module-size',
                        type=int,
                        action='store',
                        dest='module_size',
                        default=module_size,
                        required=False,
                        help='Specify module size in dots/pixels (default='+str(module_size)+').')
    parser.add_argument('-m',
                        '--margin',
                        type=float,
                        action='store',
                        dest='margin',
                        default=margin,
                        required=False,
                        help='Specify the width of the margin in modules (default='+str(margin)+').')
    parser.add_argument('-o',
                        '--output-file',
                        type=str,
                        action='store',
                        dest='filename',
                        required=filename is None,
                        default=filename,
                        help='Specify where the image should be saved. If \''+STDOUT_FILENAME+'\' is specified, the image will be written to standard output.')
    parser.add_argument('-v',
                        '--symbol-version',
                        type=int,
                        action='store',
                        dest='symbol_version',
                        required=symbol_version is None,
                        default=symbol_version,
                        help='The QR Code symbol version to use. See https://www.qrcode.com/en/about/version.html for details.')
    parser.add_argument('-d',
                        '--draw-fourth-edge',
                        action='store_true',
                        dest='draw_fourth_edge',
                        required=False,
                        default=draw_fourth_edge,
                        help='Generate a QR Code with 4 position elements ("edges").')
    parser.add_argument('-f',
                        '--format',
                        type=str.upper,
                        action='store',
                        dest='format',
                        required=False,
                        default=image_format,
                        choices=["BMP", "DDS", "DIB", "EPS", "GIF", "ICNS", "ICO", "IM", "JPEG", "JPEG2000", "PCX", "PNG", "PPM", "SGI", "SPIDER", "TGA", "TIFF", "WEBP", "PDF"],
                        help='Specify the format of the resulting image. If omitted, the format is determined from the filename extension.')
    parser.add_argument('--foreground',
                        type=str,
                        action='store',
                        dest='foreground',
                        required=False,
                        default=None,
                        help='Specifies the foreground color in hexadecimal RGB or RGBA notation (default='+("{:02X}" * len(foreground_pixel)).format(*foreground_pixel)+').')
    parser.add_argument('--background',
                        type=str,
                        action='store',
                        dest='background',
                        required=False,
                        default=None,
                        help='Specifies the background color in hexadecimal RGB or RGBA notation (default='+("{:02X}" * len(background_pixel)).format(*background_pixel)+').')

    args = parser.parse_args()
    module_size = args.module_size
    margin = args.margin
    filename = args.filename
    symbol_version = args.symbol_version
    draw_fourth_edge = args.draw_fourth_edge
    image_format = args.format
    foreground_pixel = parse_color(args.foreground, foreground_pixel)
    background_pixel = parse_color(args.background, background_pixel)

    modules = symbol_version * 4 + 17
    margin_size = round(module_size * margin)
    size = margin_size * 2 + module_size * modules
    pixels = []

    row = []
    for i in range(0, size):
        row.append(background_pixel.copy())
    for i in range(0, size):
        pixels.append(row.copy())

    for i in range(0, modules * module_size, module_size):
        for j in range(0, modules * module_size, module_size):
            if int.from_bytes(os.urandom(1), "big") > 127:
                draw_module(i + margin_size, j + margin_size, foreground_pixel, pixels)

    edge_position = size - margin_size - EDGE_SIZE
    draw_dot(margin_size, margin_size, EDGE_MODULES, pixels, Direction.DOWN | Direction.RIGHT)
    draw_dot(margin_size, edge_position, EDGE_MODULES, pixels, Direction.DOWN | Direction.LEFT)
    draw_dot(edge_position, margin_size, EDGE_MODULES, pixels, Direction.UP | Direction.RIGHT)

    if draw_fourth_edge:
        draw_dot(edge_position, edge_position, EDGE_MODULES, pixels, Direction.UP | Direction.LEFT)

    if symbol_version > 1:
        base_alignment_position = size - margin_size - ALIGNMENT_PADDING_SIZE - ALIGNMENT_SIZE

        alignment_count = math.ceil((modules - 2 * ALIGNMENT_PADDING + ALIGNMENT_MAX_SPACE)/(ALIGNMENT_MAX_SPACE + ALIGNMENT_MODULES))
        space = round((modules - 2 * ALIGNMENT_PADDING - alignment_count * ALIGNMENT_MODULES)/(alignment_count-1))
        if space % 2 == 0:
            space += 1

        for i in range(0, alignment_count - 1):
            for j in range(0, alignment_count - 1):
                if not draw_fourth_edge or i + j > 0:
                    draw_dot(base_alignment_position - ((space + ALIGNMENT_MODULES) * i) * module_size, base_alignment_position - ((space + ALIGNMENT_MODULES) * j) * module_size, ALIGNMENT_MODULES, pixels)

        for i in range(1, alignment_count - 1):
            draw_dot(margin_size + ALIGNMENT_PADDING_SIZE, base_alignment_position - ((space + ALIGNMENT_MODULES) * i) * module_size, ALIGNMENT_MODULES, pixels)

        for i in range(1, alignment_count - 1):
            draw_dot(base_alignment_position - ((space + ALIGNMENT_MODULES) * i) * module_size, margin_size + ALIGNMENT_PADDING_SIZE, ALIGNMENT_MODULES, pixels)

    create_image(filename, pixels)


if __name__ == '__main__':
    main()

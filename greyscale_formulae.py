"""Converts colored images to greyscale using the method selected by the user.
Install dependencies:
  pip install pillow docopt
Note: If you do not provide an output path, the generated files will be saved
in a folder named "Converted"
Usage:
  greyscale.py <image_file> <approach2greyscaling>
  greyscale.py -h | --help

Arguments:
  <in_path>   Input directory
  <out_path>  Output directory [default: ./Converted]
  <approach2greyscaling>  which approach to use while greyscaling
Options:
  -h, --help  Show this help screen.
"""
import docopt
from PIL import Image
import sys
import numpy as np
import os


def linear(rgb_img):
    """
    Convert *linear* RGB values to *linear* grayscale values using

    Y = 0.2126*R + 0.7152*G + 0.0722*B

    """
    red = rgb_img[:, :, 0]
    green = rgb_img[:, :, 1]
    blue = rgb_img[:, :, 2]

    gray_img = (
            0.2126 * red
            + 0.7152 * green
            + 0.0722 * blue)

    return gray_img


def linear_approx(rgb_img):
    """
    Convert *linear* RGB values to *linear* grayscale values.

    Y = 0.299*R + 0.587*G + 0.114*B

    """
    red = rgb_img[:, :, 0]
    green = rgb_img[:, :, 1]
    blue = rgb_img[:, :, 2]

    gray_img = (
            0.299 * red
            + 0.587 * green
            + 0.114 * blue)

    return gray_img


def gamma_decompress(img):
    """
    Make pixel values perceptually linear.
    """
    img_lin = ((img + 0.055) / 1.055) ** 2.4
    i_low = np.where(img <= .04045)
    img_lin[i_low] = img[i_low] / 12.92
    return img_lin


def gamma_compress(img_lin):
    """
    Make pixel values display-ready.
    """
    img = 1.055 * img_lin ** (1 / 2.4) - 0.055
    i_low = np.where(img_lin <= .0031308)
    img[i_low] = 12.92 * img_lin[i_low]
    return img


def gamma_decomp(rgb_img):
    """
    rgb_img is a 3-dimensional Numpy array of type float with
    values ranging between 0 and 1.
    Dimension 0 represents image rows, left to right.
    Dimension 1 represents image columns top to bottom.
    Dimension 2 has a size of 3 and
    represents color channels, red, green, and blue.
    Returns a gray_img 2-dimensional Numpy array of type float.
    Values range between 0 and 1.
    """
    return gamma_compress(linear(gamma_decompress(rgb_img)))


def main(image_file, approach):
    # dividing by 255 to get values between 0 and 1
    color_img = np.asarray(Image.open(image_file)) / 255
    # since we have divided by 255, we'll multiply by 255 later to get back same values
    name, ext = os.path.splitext(image_file)
    if approach in ['linear', 'l']:
        grey = Image.fromarray(linear(color_img)*255)
        name = name + "_linear"

    elif approach in ['linear_approx', 'la']:
        grey = Image.fromarray(linear_approx(color_img)*255)
        name = name + "_linearApprox"

    elif approach in ['gamma_decomp', 'gd']:
        grey = Image.fromarray(gamma_decomp(color_img)*255)
        name = name + "_gammaDecompressed"

    else:
        print('Error: Enter a valid approach', file=sys.stderr)
        return
    grey_file = name + ext
    if grey.mode != 'L':
        grey = grey.convert('L')
    grey.save(grey_file)


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args['<image_file>'], args['<approach2greyscaling>'])

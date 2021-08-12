"""Converts colored images to greyscale using the method selected by the user.
Install dependencies:
  pip install pillow docopt

Usage:
  greyscale.py <image_file> 
  greyscale.py -h | --help

Arguments:
  <in_path>   Input directory

Options:
  -h, --help  Show this help screen.
"""
import docopt
from PIL import Image
import sys
import numpy as np
import os
import time
import matplotlib.pyplot as plt


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


def main(image_file):

    x = []  # number of files
    y = []  # time taken to process number if files in x

    # dividing by 255 to get values between 0 and 1
    color_img = np.asarray(Image.open(image_file)) / 255
    # since we have divided by 255, we'll multiply by 255 later to get back same values
    name, ext = os.path.splitext(image_file)

    start_time = time.time()
    grey1 = Image.fromarray(linear(color_img) * 255)
    name1 = name + "_linear"
    grey_file1 = name1 + ext
    if grey1.mode != 'L':
        grey1 = grey1.convert('L')
    grey1.save(grey_file1)
    end_time1 = time.time()
    x.append('linear')
    y.append(end_time1 - start_time)

    grey2 = Image.fromarray(linear_approx(color_img) * 255)
    name2 = name + "_linearApprox"
    grey_file2 = name2 + ext
    if grey2.mode != 'L':
        grey2 = grey2.convert('L')
    grey2.save(grey_file2)
    end_time2 = time.time()
    x.append('linear approx')
    y.append(end_time2 - end_time1)

    grey3 = Image.fromarray(gamma_decomp(color_img) * 255)
    name3 = name + "_gammaDecompressed"
    grey_file3 = name3 + ext
    if grey3.mode != 'L':
        grey3 = grey3.convert('L')
    grey3.save(grey_file3)
    end_time3 = time.time()
    x.append('gamma_decomp')
    y.append(end_time3 - end_time2)

    plt.plot(x, y, 'ko-')
    plt.xlabel('method -> ')
    plt.ylabel('Time taken (s) ->')
    plt.title(label="Time taken by different formulaes", fontsize=15, color="red")
    plt.show()


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args['<image_file>'])

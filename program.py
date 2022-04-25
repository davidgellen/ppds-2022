"""
Lecture 9 : CUDA
Modified codebase from https://www.youtube.com/watch?v=5DFS6Mgh8CU by Mgr. Ing. Matúš Jókay, PhD.
Author: David Gellen
License: GPL 3.0
"""
from __future__ import division
from numba import cuda
import numpy
import math
from PIL import Image


@cuda.jit
def adaptive_thresholding(data_orig, data_result):
    """
    Adaptive thresholding convolves through the image with n x n grid (n being even for the actual pixel to be the
    center of image). We calculate the average pixel value in the current grid. If the value of the pixel is greater
    than the average of the grid surrounding it, we set the value to 255 (white) and if the grid average is smaller than
    the pixel value, we set it to 0 (black). We must not set the pixel values to the original image since this would
    disrupt further grid averages.
    :param data_orig: original image
    :param data_result: output image (copy of image)
    """
    x, y = cuda.grid(2)
    x_max, y_max = data_orig.shape
    if x < x_max and y < y_max:
        sum = 0
        for i in range(15):
            for j in range(15):
                sum += data_orig[x - 7 + i][y - 7 + j]
        average = sum / 225
        if data_orig[x][y] > average:
            data_result[x][y] = 255
        else:
            data_result[x][y] = 0


# host code - loads image, calls the kernel code to get the image threshold and saves the image
image = Image.open('image.png')
data = numpy.asarray(Image.open('image.png'))
data_final = numpy.asarray(Image.open('image.png'))
threads_per_block = (20, 20)
blocks_per_grid_x = math.ceil(data.shape[0] / threads_per_block[0])
blocks_per_grid_y = math.ceil(data.shape[1] / threads_per_block[1])
blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
adaptive_thresholding[blocks_per_grid, threads_per_block](data, data_final)
Image.fromarray(data_final).save("result.png")

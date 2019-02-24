# import the Python Image processing Library

import numpy as np
import matplotlib.pylab as plt
from random import randint
import os

class ImageOptimizer():


    #this is to check if the directory is a file
    def _check_file(dir):
        if os.path.isfile(dir) == True:
            return True
        else:
            return False

    def _return_image(file_dir):
        if ImageOptimizer._check_file(dir):
            im = plt.imread(file_dir)

            return im.shape

        elif not ImageOptimizer._check_file(image_dir):
            raise 'The file is not a directory, must be a file!'

ImageOptimizer._return_image("C:/Users/Noahd/Desktop/images/bitmap.png")
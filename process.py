from PIL import Image
import numpy as np


class Process:

    def __init__(self, image):

        self.image = Image.open(image)

        self.image = self.image.convert('L')

    def get_info(self):

        """
        Get Image size and mode information using the Pillow library.

        Return:
            (size, mode)
        """
        im = self.image
        print(f"Image size: {im.size}")
        print(f"Image mode: {im.mode}")

        return im.size, im.mode

    def get_array(self):

        """
        Get Numpy array for the input image
        """

        self.array = np.array(self.image, dtype='int64')

        return self.array

    def resize_image(self, width, height):

        new_dim = (width, height)
        self.image = self.image.resize(new_dim)

        return 

    def slice_image(self, xi, yi, size):

        self.slice = self.array[xi:(xi + size), yi:(yi + size)]

        return self.slice

    def show_image(self):

        self.image.show()

        return





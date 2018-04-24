import numpy as np
import skimage
import base64


class ImageProcessing:
    """This is a ImageProcessing class.

    __init__ sets the attributes

    Attributes:
        convert_from_64 (string): converts bas64 string image to np.array
        histogram_eq (string, array(int/float)): returns histogram equalization
        contrast_stretching (string, int/float): returns contrast stretching
        log_compression (string, int): returns log compression of image
        reverse_video (string): returns reverse video of image
        convert_to_64 (np.array): converts np.array image to base64 string

    Arguments:
        img (string): base64 image file
        hist_rng (array): 1x2 array of the range for histogram_eq
        cont_rng (int/float): between 0 and 100 indicating amount
        of contrast stretching
        log_rng (int): 0 if standard log compression 1 if inverted
    """

    def __init__(self, img, hist_rng, cont_rng, log_rng):
        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def convert_from_64(img):
        """
        :param img:          base64 image string
        :returns imgData:    np.array image
        :raises ImportError: packages not found
        """

        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            imgData = base64.b64decode(img)
            # code
        except ImportError:
            logging.debug('ImportError: packages not found')
            raise ImportError("Import packages not found.")
        logging.info("Success: image as np array returned.")
        return imgData

    def convert_to_64(imgData):
        """
        :param imgData:      np.array image
        :returns img:        base64 image string
        :raises ImportError: packages not found
        """

        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            img = base64.decodebytes(imgData)
            # code
        except ImportError:
            logging.debug('ImportError: packages not found')
            raise ImportError("Import packages not found.")
        logging.info("Success: image as np array returned.")
        return img

    def histogram_eq(img, hist_rng):
        """
        :param img:          base64 image string
        :param hist_rng      array of ranges for histogram_eq
        :returns imgHist:    np.array histogram equalized image
        :raises ImportError: packages not found
        """

        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            imgData = convert_from_64(img)
            # code
            imgHist = convert_to_64(imgData)
        except ImportError:
            logging.debug('ImportError: packages not found')
            raise ImportError("Import packages not found.")
        logging.info("Success: histogram equalization returned.")
        return imgHist

    def contrast_stretching(img, cont_rng):
        """
        :param img:          base64 image string
        :param cont_rng      array of range for contrast_stretching
        :returns imgHist:    np.array histogram equalized image
        :raises ImportError: packages not found
        """

        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            imgData = convert_from_64(img)
            # code
            imgCont = convert_to_64(imgData)
        except ImportError:
            logging.debug('ImportError: packages not found')
            raise ImportError("Import packages not found.")
        logging.info("Success: histogram equalization returned.")
        return imgCont

    def log_compression(img, log_rng):
        """
        :param img:          base64 image string
        :param cont_rng      array of range for contrast_stretching
        :returns imgHist:    np.array histogram equalized image
        :raises ImportError: packages not found
        """

        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            imgData = convert_from_64(img)
            # code
            imgLog = convert_to_64(imgData)
        except ImportError:
            logging.debug('ImportError: packages not found')
            raise ImportError("Import packages not found.")
        logging.info("Success: histogram equalization returned.")
        return imgLog

    def reverse_video(img):
        """
        :param img:          base64 image string
        :param cont_rng      array of range for contrast_stretching
        :returns imgHist:    np.array histogram equalized image
        :raises ImportError: packages not found
        """

        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            imgData = convert_from_64(img)
            # code
            imgReverse = convert_to_64(imgData)
        except ImportError:
            logging.debug('ImportError: packages not found')
            raise ImportError("Import packages not found.")
        logging.info("Success: histogram equalization returned.")
        return imgReverse

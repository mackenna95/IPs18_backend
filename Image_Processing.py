import numpy as np
from skimage import exposure
import base64
import cv2
import math


class ImageProcessing:
    """This is a ImageProcessing class.

    __init__ sets the attributes

    Attributes:
        convert_from_64 (string): converts bas64 string image to np.array
        histogram_eq (string, int/float): returns histogram equalization
        contrast_stretching (string, array(int/float)): returns
        contrast stretching
        log_compression (string, int): returns log compression of image
        reverse_video (string, bool): returns reverse video of image
        convert_to_64 (np.array): converts np.array image to base64 string

    Arguments:
        img (string): base64 image file
        hist_rng (int/float): num of bins for histogram_eq
        cont_rng (array): between 0 and 100 indicating amount
        of contrast stretching
        log_rng (bool): True if standard log compression False if inverted
    """

    def __init__(self, img, hist_rng, cont_rng, log_rng):
        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def histogram_eq(img, hist_rng):
        """
        :param img:          base64 image string
        :param hist_rng      float of bins for histogram_eq
        :returns img_hist:   base64 string histogram equalized image
        :raises ImportError: packages not found
        """

        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            img_array = convert_from_64(img)

            # Equalization
            hist_rng_exp = hist_rng * img_array.shape[0] * img_array[1]
            img_eq = exposure.equalize_hist(img_array, hist_rng_exp)
            img_eq_exp = img_eq * 255

            img_hist = convert_to_64(img_eq_exp)
        except ImportError:
            logging.debug('ImportError: packages not found')
            raise ImportError("Import packages not found.")
        logging.info("Success: histogram equalization returned.")
        return img_hist

    def contrast_stretching(img, cont_rng):
        """
        :param img:          base64 image string
        :param cont_rng      array of range for contrast_stretching
        :returns img_cont:   base64 string contrast stretched image
        :raises ImportError: packages not found
        """

        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            img_array = convert_from_64(img)

            # Contrast stretching
            p, q = np.percentile(img_array, cont_rng)
            img_rescale = exposure.rescale_intensity(img_array,
                                                     in_range=(p, q))

            img_cont = convert_to_64(img_rescale)
        except ImportError:
            logging.debug('ImportError: packages not found')
            raise ImportError("Import packages not found.")
        logging.info("Success: histogram equalization returned.")
        return img_cont

    def log_compression(img, log_rng):
        """
        :param img:          base64 image string
        :param log_rng       array of range for log compression
        :returns img_log:    base64 string log compressed image
        :raises ImportError: packages not found
        """

        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            img_array = convert_from_64(img)

            # log compression
            if log_rng:
                img_array_log = log_comp(img_array)
            else:
                img_rev = invert(img_array)
                img_rev_log = log_comp(img_rev)
                img_array_log = invert(img_rev_log)

            img_log = convert_to_64(img_array_log)
        except ImportError:
            logging.debug('ImportError: packages not found')
            raise ImportError("Import packages not found.")
        logging.info("Success: histogram equalization returned.")
        return img_log

    def reverse_video(img):
        """
        :param img:           base64 image string
        :returns img_reverse: base64 string inverted image
        :raises ImportError:  packages not found
        """

        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            img_array = convert_from_64(img)

            # Reverse Video
            img_rev = invert(img_array)

            img_reverse = convert_to_64(img_rev)
        except ImportError:
            logging.debug('ImportError: packages not found')
            raise ImportError("Import packages not found.")
        logging.info("Success: histogram equalization returned.")
        return img_reverse


def log_comp(img_array):
    """
    :param img_array:  np.array image
    :returns img_rev:  np.array inverted image
    """
    import logging
    img_array_log = np.zeros((img_array.shape[0], img_array.shape[1]))
    c = 255 / math.log((1 + img_array.max()), 10)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            img_array_log[i][j] = c * math.log((1 + img_array[i][j]), 10)
    logging.info("Success: image as np array returned.")
    return img_array_log


def invert(img_array):
    """
    :param img_array:  np.array image
    :returns img_rev:  np.array inverted image
    """
    import logging
    arr255 = np.full((img_array.shape[0], img_array.shape[1]), 255)
    img_rev = np.subtract(arr255, img_array)
    logging.info("Success: image as np array returned.")
    return img_rev


def convert_from_64(img):
    """
    :param img:          base64 image string
    :returns img_array:  np.array image
    :raises ImportError: packages not found
    """

    import logging
    logging.basicConfig(filename="image_processing_log.txt",
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    try:
        img_data = base64.b64decode(img)
        img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8),
                                 -1)
    except ImportError:
        logging.debug('ImportError: packages not found')
        raise ImportError("Import packages not found.")
    logging.info("Success: image as np array returned.")
    return img_array


def convert_to_64(img_array):
    """
    :param img_array:    np.array image
    :returns img_str:    base64 image string
    :raises ImportError: packages not found
    """

    import logging
    logging.basicConfig(filename="image_processing_log.txt",
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    try:
        img_array.astype('uint8')
        img_data = cv2.imencode(".png", img_array)[1].tostring()
        img_byte_s = base64.b64encode(img_data)
        img_str = img_byte_s.decode("utf-8")
    except ImportError:
        logging.debug('ImportError: packages not found')
        raise ImportError("Import packages not found.")
    logging.info("Success: image as np array returned.")
    return img_str

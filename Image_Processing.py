import numpy as np
from skimage import exposure
import base64
import cv2
import math
import logging


class ImageProcessing:
    """This is a ImageProcessing class.

    __init__ sets the attributes

    Attributes:
        convert_from_64 (dict): converts bas64 string image to np.array
        histogram_eq (dict): returns histogram equalization
        contrast_stretching (dict): returns contrast stretching
        log_compression (dict): returns log compression of image
        reverse_video (dict): returns reverse video of image
        convert_to_64 (np.array): converts np.array image to base64 string
        image_size(dict): Returns image pixel size

    Arguments:
        img_dict = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b', # string
          'img_metadata': {'hist_eq': 20, # int/float
                           'contrast': [10, 80], # list (int/float)
                           'log_comp': False, # boolean
                           'reverse': True, # boolean
                           'format': '.png'}, # string
          'img_orig': tiff_c_text} # string
    """

    def __init__(self, img_dict):
        import logging
        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def histogram_eq(img_dict):
        """
        :param img_dict:     dict containing image metedata and
        base64 converted image
        :returns img_hist:   base64 string histogram equalized image
        """

        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        img_array = convert_from_64(img_dict)
        hist_rng = img_dict['img_metadata']['hist_eq']

        # Equalization
        img_eq = exposure.equalize_hist(img_array)
        img_eq_exp = img_eq * 255

        img_hist = convert_to_64(img_eq_exp, img_dict)
        logging.info("Success: histogram equalization returned.")
        return img_hist

    def contrast_stretching(img_dict):
        """
        :param img_dict:     dict containing image metedata and
        base64 converted image
        :returns img_cont:   base64 string contrast stretched image
        """

        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        img_array = convert_from_64(img_dict)

        # Contrast stretching
        p, q = np.percentile(img_array,
                             img_dict['img_metadata']['contrast'])
        img_rescale = exposure.rescale_intensity(img_array,
                                                 in_range=(p, q))

        img_cont = convert_to_64(img_rescale, img_dict)
        logging.info("Success: contrast stretching returned.")
        return img_cont

    def log_compression(img_dict):
        """
        :param img_dict:     dict containing image metedata and
        base64 converted image
        :returns img_log:    base64 string log compressed image
        """

        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        img_array = convert_from_64(img_dict)

        # log compression
        if img_dict['img_metadata']['log_comp']:
            img_array_log = log_comp(img_array)
        else:
            img_rev = invert(img_array)
            img_rev_log = log_comp(img_rev)
            img_array_log = invert(img_rev_log)

        img_log = convert_to_64(img_array_log, img_dict)
        logging.info("Success: log compression returned.")
        return img_log

    def reverse_video(img_dict):
        """
        :param img_dict:     dict containing image metedata and
        base64 converted image
        :returns img_reverse: base64 string inverted image
        """

        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        img_array = convert_from_64(img_dict)

        # Reverse Video
        img_rev = invert(img_array)

        img_reverse = convert_to_64(img_rev, img_dict)
        logging.info("Success: reverse video returned.")
        return img_reverse

    def image_size(img_dict):
        """
        :param img_dict:    dict containing image metedata and
        base64 converted image
        :returns size_array: np.array of image size
        """

        logging.basicConfig(filename="image_processing_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            img_array = convert_from_64(img_dict)
            size_array = img_array.shape
        except AttributeError:
            logging.debug('AttributeError: Incorrect File Type')
            return AttributeError('Incorrect File Type')
        logging.info("Success: image size as np array returned.")
        return size_array


def log_comp(img_array):
    """
    :param img_array:  np.array image
    :returns img_rev:  np.array inverted image
    """

    img_array_log = np.zeros((img_array.shape[0], img_array.shape[1]))
    c = 255 / math.log((1 + img_array.max()), 10)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            img_array_log[i][j] = c * math.log((1 + img_array[i][j]), 10)
    logging.info("Success: log compression sub returned.")
    return img_array_log


def invert(img_array):
    """
    :param img_array:  np.array image
    :returns img_rev:  np.array inverted image
    """

    arr255 = np.full((img_array.shape[0], img_array.shape[1]), 255)
    img_rev = np.subtract(arr255, img_array)
    logging.info("Success: inverted image returned")
    return img_rev


def convert_from_64(img_dict):
    """
    :param img_dict:    dict containing image metedata and
    base64 converted image
    :returns img_array: np.array image
    :raises TypeError:  Incorrect image type received
    """

    logging.basicConfig(filename="image_processing_log.txt",
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        # data_uri = img_dict['img_orig']
        # img = re.sub(r'.*,', '', data_uri)
        img_data = base64.b64decode(img_dict['img_orig'])
        img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 0)
        if isinstance(img_array, np.ndarray):
            logging.debug('Correct File Type')
        else:
            1 == 2
    except TypeError:
        logging.debug('TypeError: Incorrect File Type')
        raise TypeError('Incorrect File Type')
    logging.info("Success: image as np array returned.")
    return img_array


def convert_to_64(img_array, img_dict):
    """
    :param img_array:    np.array image
    :param img_dict:     dict containing image metedata and
    base64 converted image
    :returns img_str:    base64 image string
    """

    logging.basicConfig(filename="image_processing_log.txt",
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    # ftype = '.'
    # ftype += img_dict['img_metadata']['format']

    img_array.astype('uint8')
    img_data = cv2.imencode(img_dict['img_metadata']['format'],
                            img_array)[1].tostring()
    img_byte_s = base64.b64encode(img_data)
    img_str = img_byte_s.decode("utf-8")

    # img_data_uri = 'data:image/' + img_dict['img_metadata']['format']
    # img_str = img_data_uri + ';base64,' + img_str

    logging.info("Success: image as base64 returned.")
    return img_str

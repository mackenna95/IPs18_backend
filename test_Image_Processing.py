def test_Image_Processing():
    import pytest
    import numpy as np
    import base64
    import cv2
    from skimage import exposure
    from Image_Processing import ImageProcessing
    from Image_Processing import convert_from_64
    from Image_Processing import convert_to_64

    f = open('d.txt', 'r')
    d_text = f.read()
    f = open('d2.txt', 'r')
    d2_text = f.read()
    f = open('d3.txt', 'r')
    d3_text = f.read()

    d = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
         'img_metadata': {'hist_eq': [0, 255],  # histogram equalization
                          'contrast': [2, 98],  # contrast stretching
                          'log_comp': True,
                          'reverse': True},
         'img_orig': d_text}

    d2 = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
          'img_metadata': {'hist_eq': [1, 200],  # histogram equalization
                           'contrast': [2, 98],  # contrast stretching
                           'log_comp': False,
                           'reverse': True},
          'img_orig': d2_text}

    d3 = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
          'img_metadata': {'hist_eq': [1, 200],  # histogram equalization
                           'contrast': [10, 100],  # contrast stretching
                           'log_comp': False,
                           'reverse': True},
          'img_orig': d3_text}

    img_data = base64.b64decode(d2['img_orig'])
    img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), -1)

    output = convert_from_64(d2['img_orig'])
    assert (output == img_array).all()
    # output = ImageProcessing.convert_to_64(img_array)
    # assert output == d2['img_orig']

    # Histogram Equalization
    img_eq = exposure.equalize_hist(img_array)
    img_hist = convert_to_64(img_eq)

    output = ImageProcessing.histogram_eq(d2['img_orig'],
                                          d['img_metadata']['hist_eq'])
    assert output == img_hist

    # Contrast stretching
    p, q = np.percentile(img_array, d2['img_metadata']['contrast'])
    img_rescale = exposure.rescale_intensity(img_array, in_range=(p, q))
    img_cont = convert_to_64(img_rescale)

    out = ImageProcessing.contrast_stretching(d2['img_orig'],
                                              d2['img_metadata']['contrast'])
    assert out == img_cont

    # Reverse Video
    arr255 = np.full((img_array.shape[0], img_array.shape[1]), 255)
    img_rev = np.subtract(arr255, img_array)
    img_reverse = convert_to_64(img_rev)

    output = ImageProcessing.reverse_video(d2['img_orig'])
    assert output == img_reverse

    # Log Compression

    output = ImageProcessing.log_compression(d2['img_orig'],
                                             d2['img_metadata']['log_comp'])
    assert output == 2.5

    pytest.raises(ValueError,
                  ImageProcessing.convert_from_64,
                  d_color['img_orig'])
    return

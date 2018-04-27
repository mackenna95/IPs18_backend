def test_Image_Processing():
    import pytest
    import numpy as np
    import base64
    import cv2
    from skimage import exposure
    from Image_Processing import ImageProcessing
    from Image_Processing import convert_from_64
    from Image_Processing import convert_to_64
    from Image_Processing import log_comp
    from Image_Processing import invert

    f = open('png_g2.txt', 'r')
    png_g_text2 = f.read()
    f = open('png_g.txt', 'r')
    png_g_text = f.read()
    f = open('jpeg_g.txt', 'r')
    jpeg_g_text = f.read()
    f = open('tiff_g.txt', 'r')
    tiff_g_text = f.read()

    f = open('png_c.txt', 'r')
    png_c_text = f.read()
    f = open('jpeg_c.txt', 'r')
    jpeg_c_text = f.read()
    f = open('tiff_c.txt', 'r')
    tiff_c_text = f.read()

    png_g2 = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
              'img_metadata': {'hist_eq': 0,
                               'contrast': [2, 98],
                               'log_comp': True,
                               'reverse': True,
                               'format': '.png'},
              'img_orig': png_g_text2}

    png_g = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
             'img_metadata': {'hist_eq': 40,
                              'contrast': [2, 98],
                              'log_comp': False,
                              'reverse': True,
                              'format': '.tiff'},
             'img_orig': png_g_text}

    jpeg_g = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
              'img_metadata': {'hist_eq': 40,
                               'contrast': [10, 100],
                               'log_comp': False,
                               'reverse': True,
                               'format': '.png'},
              'img_orig': jpeg_g_text}

    tiff_g = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
              'img_metadata': {'hist_eq': 20,
                               'contrast': [10, 80],
                               'log_comp': False,
                               'reverse': True,
                               'format': '.png'},
              'img_orig': tiff_g_text}

    png_c = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
             'img_metadata': {'hist_eq': 20,
                              'contrast': [10, 80],
                              'log_comp': False,
                              'reverse': True,
                              'format': '.png'},
             'img_orig': png_c_text}

    jpeg_c = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
              'img_metadata': {'hist_eq': 40,
                               'contrast': [10, 100],
                               'log_comp': False,
                               'reverse': True,
                               'format': '.png'},
              'img_orig': jpeg_c_text}

    tiff_c = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
              'img_metadata': {'hist_eq': 20,
                               'contrast': [10, 80],
                               'log_comp': False,
                               'reverse': True,
                               'format': '.png'},
              'img_orig': tiff_c_text}

    img_data = base64.b64decode(png_g['img_orig'])
    img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 0)

    output = convert_from_64(png_g['img_orig'])
    assert (output == img_array).all()
    # output = ImageProcessing.convert_to_64(img_array)
    # assert output == png_g['img_orig']

    # Histogram Equalization
    hist = png_g['img_metadata']['hist_eq'] * img_array.shape[0] * img_array[1]
    img_eq = exposure.equalize_hist(img_array, hist)
    img_eq_exp = img_eq * 255

    img_hist = convert_to_64(img_eq_exp, png_g['img_metadata']['format'])

    output = ImageProcessing.histogram_eq(png_g['img_orig'],
                                          png_g['img_metadata']['hist_eq'],
                                          png_g['img_metadata']['format'])
    assert output == img_hist

    # Contrast stretching
    p, q = np.percentile(img_array, png_g['img_metadata']['contrast'])
    img_rescale = exposure.rescale_intensity(img_array, in_range=(p, q))
    img_cont = convert_to_64(img_rescale, png_g['img_metadata']['format'])

    o = ImageProcessing.contrast_stretching(png_g['img_orig'],
                                            png_g['img_metadata']['contrast'],
                                            png_g['img_metadata']['format'])
    assert o == img_cont

    # Reverse Video
    arr255 = np.full((img_array.shape[0], img_array.shape[1]), 255)
    img_rev = np.subtract(arr255, img_array)
    img_reverse = convert_to_64(img_rev, png_g['img_metadata']['format'])

    output = ImageProcessing.reverse_video(png_g['img_orig'],
                                           png_g['img_metadata']['format'])
    assert output == img_reverse

    # Log Compression
    if png_g['img_metadata']['log_comp']:
        img_array_log = log_comp(img_array)
    else:
        img_rev = invert(img_array)
        img_rev_log = log_comp(img_rev)
        img_array_log = invert(img_rev_log)

    img_log = convert_to_64(img_array_log, png_g['img_metadata']['format'])

    output = ImageProcessing.log_compression(png_g['img_orig'],
                                             png_g['img_metadata']['log_comp'],
                                             png_g['img_metadata']['format'])
    assert output == img_log

    # Jpeg file unsupport
    pytest.raises(TypeError, convert_from_64(jpeg_g['img_orig']))
    return

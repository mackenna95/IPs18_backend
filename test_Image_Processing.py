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
    from Image_Processing import image_size

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

    f = open('error_g.txt', 'r')
    error_g_text = f.read()

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

    error_g = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
               'img_metadata': {'hist_eq': 20,
                               'contrast': [10, 80],
                               'log_comp': False,
                               'reverse': True,
                               'format': '.png'},
               'img_orig': error_g_text}

    # testing for png_greyscale
    img_data = base64.b64decode(png_g['img_orig'])
    img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 0)

    output = convert_from_64(png_g)
    assert (output == img_array).all()

    # Histogram Equalization
    hist = png_g['img_metadata']['hist_eq'] * img_array.shape[0] * img_array[1]
    img_eq = exposure.equalize_hist(img_array, hist)
    img_eq_exp = img_eq * 255

    img_hist = convert_to_64(img_eq_exp, png_g)

    output = ImageProcessing.histogram_eq(png_g)
    assert output == img_hist

    # Contrast stretching
    p, q = np.percentile(img_array, png_g['img_metadata']['contrast'])
    img_rescale = exposure.rescale_intensity(img_array, in_range=(p, q))
    img_cont = convert_to_64(img_rescale, png_g)

    o = ImageProcessing.contrast_stretching(png_g)
    assert o == img_cont

    # Reverse Video
    arr255 = np.full((img_array.shape[0], img_array.shape[1]), 255)
    img_rev = np.subtract(arr255, img_array)
    img_reverse = convert_to_64(img_rev, png_g)

    output = ImageProcessing.reverse_video(png_g)
    assert output == img_reverse

    # Log Compression
    if png_g['img_metadata']['log_comp']:
        img_array_log = log_comp(img_array)
    else:
        img_rev = invert(img_array)
        img_rev_log = log_comp(img_rev)
        img_array_log = invert(img_rev_log)

    img_log = convert_to_64(img_array_log, png_g)

    output = ImageProcessing.log_compression(png_g)
    assert output == img_log

    # image size
    output = image_size(png_g)
    assert output == (263, 304)

    # ==============================================================

    # testing for tiff_greyscale
    img_data = base64.b64decode(tiff_g['img_orig'])
    img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 0)

    output = convert_from_64(tiff_g)
    assert (output == img_array).all()

    # Histogram Equalization
    heq = tiff_g['img_metadata']['hist_eq'] * img_array.shape[0] * img_array[1]
    img_eq = exposure.equalize_hist(img_array, heq)
    img_eq_exp = img_eq * 255

    img_hist = convert_to_64(img_eq_exp, tiff_g)

    output = ImageProcessing.histogram_eq(tiff_g)
    assert output == img_hist

    # Contrast stretching
    p, q = np.percentile(img_array, tiff_g['img_metadata']['contrast'])
    img_rescale = exposure.rescale_intensity(img_array, in_range=(p, q))
    img_cont = convert_to_64(img_rescale, tiff_g)

    o = ImageProcessing.contrast_stretching(tiff_g)
    assert o == img_cont

    # Reverse Video
    arr255 = np.full((img_array.shape[0], img_array.shape[1]), 255)
    img_rev = np.subtract(arr255, img_array)
    img_reverse = convert_to_64(img_rev, tiff_g)

    output = ImageProcessing.reverse_video(tiff_g)
    assert output == img_reverse

    # Log Compression
    if tiff_g['img_metadata']['log_comp']:
        img_array_log = log_comp(img_array)
    else:
        img_rev = invert(img_array)
        img_rev_log = log_comp(img_rev)
        img_array_log = invert(img_rev_log)

    img_log = convert_to_64(img_array_log, tiff_g)

    output = ImageProcessing.log_compression(tiff_g)
    assert output == img_log

    # image size
    output = image_size(tiff_g)
    assert output == (263, 304)

    # ==============================================================

    # testing for jpeg_greyscale
    img_data = base64.b64decode(jpeg_g['img_orig'])
    img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 0)

    output = convert_from_64(jpeg_g)
    assert (output == img_array).all()

    # Histogram Equalization
    heq = jpeg_g['img_metadata']['hist_eq'] * img_array.shape[0] * img_array[1]
    img_eq = exposure.equalize_hist(img_array, heq)
    img_eq_exp = img_eq * 255

    img_hist = convert_to_64(img_eq_exp, jpeg_g)

    output = ImageProcessing.histogram_eq(jpeg_g)
    assert output == img_hist

    # Contrast stretching
    p, q = np.percentile(img_array, jpeg_g['img_metadata']['contrast'])
    img_rescale = exposure.rescale_intensity(img_array, in_range=(p, q))
    img_cont = convert_to_64(img_rescale, jpeg_g)

    o = ImageProcessing.contrast_stretching(jpeg_g)
    assert o == img_cont

    # Reverse Video
    arr255 = np.full((img_array.shape[0], img_array.shape[1]), 255)
    img_rev = np.subtract(arr255, img_array)
    img_reverse = convert_to_64(img_rev, jpeg_g)

    output = ImageProcessing.reverse_video(jpeg_g)
    assert output == img_reverse

    # Log Compression
    if jpeg_g['img_metadata']['log_comp']:
        img_array_log = log_comp(img_array)
    else:
        img_rev = invert(img_array)
        img_rev_log = log_comp(img_rev)
        img_array_log = invert(img_rev_log)

    img_log = convert_to_64(img_array_log, jpeg_g)

    output = ImageProcessing.log_compression(jpeg_g)
    assert output == img_log

    # image size
    output = image_size(jpeg_g)
    assert output == (263, 304)

    # ==============================================================

    # testing for png_color
    img_data = base64.b64decode(png_c['img_orig'])
    img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 0)

    output = convert_from_64(png_c)
    assert (output == img_array).all()

    # Histogram Equalization
    hist = png_c['img_metadata']['hist_eq'] * img_array.shape[0] * img_array[1]
    img_eq = exposure.equalize_hist(img_array, hist)
    img_eq_exp = img_eq * 255

    img_hist = convert_to_64(img_eq_exp, png_c)

    output = ImageProcessing.histogram_eq(png_c)
    assert output == img_hist

    # Contrast stretching
    p, q = np.percentile(img_array, png_c['img_metadata']['contrast'])
    img_rescale = exposure.rescale_intensity(img_array, in_range=(p, q))
    img_cont = convert_to_64(img_rescale, png_c)

    o = ImageProcessing.contrast_stretching(png_c)
    assert o == img_cont

    # Reverse Video
    arr255 = np.full((img_array.shape[0], img_array.shape[1]), 255)
    img_rev = np.subtract(arr255, img_array)
    img_reverse = convert_to_64(img_rev, png_c)

    output = ImageProcessing.reverse_video(png_c)
    assert output == img_reverse

    # Log Compression
    if png_c['img_metadata']['log_comp']:
        img_array_log = log_comp(img_array)
    else:
        img_rev = invert(img_array)
        img_rev_log = log_comp(img_rev)
        img_array_log = invert(img_rev_log)

    img_log = convert_to_64(img_array_log, png_c)

    output = ImageProcessing.log_compression(png_c)
    assert output == img_log

    # image size
    output = image_size(png_c)
    assert output == (200, 200)

    # ==============================================================

    # testing for tiff_color
    img_data = base64.b64decode(tiff_c['img_orig'])
    img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 0)

    output = convert_from_64(tiff_c)
    assert (output == img_array).all()

    # Histogram Equalization
    heq = tiff_c['img_metadata']['hist_eq'] * img_array.shape[0] * img_array[1]
    img_eq = exposure.equalize_hist(img_array, heq)
    img_eq_exp = img_eq * 255

    img_hist = convert_to_64(img_eq_exp, tiff_c)

    output = ImageProcessing.histogram_eq(tiff_c)
    assert output == img_hist

    # Contrast stretching
    p, q = np.percentile(img_array, tiff_c['img_metadata']['contrast'])
    img_rescale = exposure.rescale_intensity(img_array, in_range=(p, q))
    img_cont = convert_to_64(img_rescale, tiff_c)

    o = ImageProcessing.contrast_stretching(tiff_c)
    assert o == img_cont

    # Reverse Video
    arr255 = np.full((img_array.shape[0], img_array.shape[1]), 255)
    img_rev = np.subtract(arr255, img_array)
    img_reverse = convert_to_64(img_rev, tiff_c)

    output = ImageProcessing.reverse_video(tiff_c)
    assert output == img_reverse

    # Log Compression
    if tiff_g['img_metadata']['log_comp']:
        img_array_log = log_comp(img_array)
    else:
        img_rev = invert(img_array)
        img_rev_log = log_comp(img_rev)
        img_array_log = invert(img_rev_log)

    img_log = convert_to_64(img_array_log, tiff_c)

    output = ImageProcessing.log_compression(tiff_c)
    assert output == img_log

    # image size
    output = image_size(tiff_c)
    assert output == (200, 200)

    # ==============================================================

    # testing for jpeg_color
    img_data = base64.b64decode(jpeg_c['img_orig'])
    img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 0)

    output = convert_from_64(jpeg_c)
    assert (output == img_array).all()

    # Histogram Equalization
    heq = jpeg_c['img_metadata']['hist_eq'] * img_array.shape[0] * img_array[1]
    img_eq = exposure.equalize_hist(img_array, heq)
    img_eq_exp = img_eq * 255

    img_hist = convert_to_64(img_eq_exp, jpeg_c)

    output = ImageProcessing.histogram_eq(jpeg_c)
    assert output == img_hist

    # Contrast stretching
    p, q = np.percentile(img_array, jpeg_c['img_metadata']['contrast'])
    img_rescale = exposure.rescale_intensity(img_array, in_range=(p, q))
    img_cont = convert_to_64(img_rescale, jpeg_c)

    o = ImageProcessing.contrast_stretching(jpeg_c)
    assert o == img_cont

    # Reverse Video
    arr255 = np.full((img_array.shape[0], img_array.shape[1]), 255)
    img_rev = np.subtract(arr255, img_array)
    img_reverse = convert_to_64(img_rev, jpeg_c)

    output = ImageProcessing.reverse_video(jpeg_c)
    assert output == img_reverse

    # Log Compression
    if jpeg_c['img_metadata']['log_comp']:
        img_array_log = log_comp(img_array)
    else:
        img_rev = invert(img_array)
        img_rev_log = log_comp(img_rev)
        img_array_log = invert(img_rev_log)

    img_log = convert_to_64(img_array_log, jpeg_c)

    output = ImageProcessing.log_compression(jpeg_c)
    assert output == img_log

    # image size
    output = image_size(jpeg_c)
    assert output == (200, 200)

    # ==============================================================

    # Input of single base64 character
    pytest.raises(TypeError, convert_from_64(error_g))

    return

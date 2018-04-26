def test_Image_Processing():
    import pytest
    import numpy as np
    import base64
    import cv2
    from Image_Processing import ImageProcessing

    f = open('d.txt', 'r')
    d_text = f.read()
    f = open('d2.txt', 'r')
    d2_text = f.read()
    f = open('d3.txt', 'r')
    d3_text = f.read()

    d = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
         'img_metadata': {'hist_eq': [0, 255],  # histogram equalization
                          'contrast': 50,  # contrast stretching
                          'log_comp': True,
                          'reverse': True},
         'img_orig': d_text}

    d2 = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
          'img_metadata': {'hist_eq': [1, 200],  # histogram equalization
                           'contrast': 50,  # contrast stretching
                           'log_comp': False,
                           'reverse': True},
          'img_orig': d2_text}

    d3 = {'img_ID': '3e056818-3f45-11e8-b467-0ed5f89f718b',
          'img_metadata': {'hist_eq': [1, 200],  # histogram equalization
                           'contrast': 50,  # contrast stretching
                           'log_comp': False,
                           'reverse': True},
          'img_orig': d3_text}

    img_data = base64.b64decode(d2['img_orig'])
    img_array = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), -1)

    output = ImageProcessing.convert_from_64(d2['img_orig'])
    assert (output == img_array).all()
    # output = ImageProcessing.convert_to_64(img_array)
    # assert output == d2['img_orig']
    output = ImageProcessing.histogram_eq(d2['img_orig'],
                                          d['img_metadata']['hist_eq'])
    assert output == 1
    output = ImageProcessing.contrast_stretching(d2['img_orig'],
                                                 d['img_metadata']['contrast'])
    assert output == 2
    output = ImageProcessing.log_compression(d2['img_orig'],
                                             d['img_metadata']['log_comp'])
    assert output == 1
    output = ImageProcessing.reverse_video(d2['img_orig'])
    assert output == 2.5
    pytest.raises(ValueError,
                  ImageProcessing.convert_from_64,
                  d_color['img_orig'])
    return

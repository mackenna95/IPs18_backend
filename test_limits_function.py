def test_limits_function():
    from number_manipulation import NumberManipulation
    import pytest

    pytest.raises(TypeError, NumberManipulation, (1, 2, 3))
    pytest.raises(ValueError, NumberManipulation, [])
    pytest.raises(TypeError, NumberManipulation, [1, 's'])

    output = NumberManipulation([-1, -3, 4, 0, 2])
    assert output.limits == (-3, 4)

    tolerance = 0.00000001
    output = NumberManipulation([3.3, -5.7, 9, -6.7])
    assert output.limits[0] + 6.7 < tolerance
    assert output.limits[1] - 9 < tolerance

    pass

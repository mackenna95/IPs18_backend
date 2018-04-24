def test_sum_function():
    import pytest
    from number_manipulation import NumberManipulation
    output = NumberManipulation([3, 7, -2])
    assert output.sum == 8
    output = NumberManipulation([-6, -90, -40, 26])
    assert output.sum == -110
    tollerance = 0.00000001
    output = NumberManipulation([6.9, 3.2, -4])
    assert output.sum - 6.1 < tollerance
    output = NumberManipulation([-3.2, -1.8, -9.36, -872])
    assert output.sum + 886.36 < tollerance

    pytest.raises(TypeError, NumberManipulation, (8, "str"))
    pytest.raises(ValueError, NumberManipulation, [])

    pass

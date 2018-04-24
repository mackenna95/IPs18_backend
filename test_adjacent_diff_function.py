def test_max_adjacent():
    import pytest
    from number_manipulation import NumberManipulation
    output = NumberManipulation([1, 2])
    assert output.max_adjacent == 1
    output = NumberManipulation([0, 1, 3, 4, 5, 6, 7, 8, 9, 10])
    assert output.max_adjacent == 2
    output = NumberManipulation([1, 2, 3])
    assert output.max_adjacent == 1
    output = NumberManipulation([1, 2, 2.5, 5])
    assert output.max_adjacent == 2.5
    output = NumberManipulation([-1, 1, -2])
    assert output.max_adjacent == 3
    pytest.raises(TypeError, NumberManipulation, ["str1", "str2"])
    pytest.raises(ValueError, NumberManipulation, [])
    return

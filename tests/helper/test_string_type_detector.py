from tests.helper.string_type_detector import get_string_type

# pylint: disable=missing-docstring


def test_is_str():
    assert get_string_type('foo') is 'str'
    assert get_string_type(u'foo') is 'str'


def test_is_bytes():
    assert get_string_type(b'foo') is 'bytes'


def test_is_neither():
    assert get_string_type(None) is 'neither'
    assert get_string_type(1) is 'neither'
    assert get_string_type(1.5) is 'neither'

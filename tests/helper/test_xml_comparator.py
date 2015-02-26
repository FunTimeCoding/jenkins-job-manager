from lxml import etree
from lxml.etree import Element
from tests.helper.xml_comparator import xml_compare


def test_compare():
    root_a = Element('root')
    root_a.append(Element('element'))

    root_b = Element('root')
    root_b.append(Element('element'))

    assert xml_compare(root_a, root_b) is True

    serialized_a = etree.tostring(root_a,
                                  encoding='unicode',
                                  pretty_print=True)
    serialized_b = etree.tostring(root_b,
                                  encoding='unicode',
                                  pretty_print=True)
    assert serialized_a == serialized_b


def test_compare_negative():
    root_a = Element('root')
    root_a.append(Element('element'))

    root_b = Element('root')
    root_b.append(Element('another'))

    assert xml_compare(root_a, root_b) is False

    serialized_a = etree.tostring(root_a,
                                  encoding='unicode',
                                  pretty_print=True)
    serialized_b = etree.tostring(root_b,
                                  encoding='unicode',
                                  pretty_print=True)
    assert serialized_a != serialized_b

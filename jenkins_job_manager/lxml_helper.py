from lxml import etree
from lxml.etree import Element


def serialize_element(element: Element) -> str:
    return etree.tostring(
        element_or_tree=element,
        encoding='unicode',
        pretty_print=True
    )

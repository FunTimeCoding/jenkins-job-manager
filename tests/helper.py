from lxml import etree
from lxml.etree import Element, XMLParser


def load_fixture(path: str) -> Element:
    return etree.parse(
        source=path,
        parser=XMLParser(remove_blank_text=True)
    ).getroot()

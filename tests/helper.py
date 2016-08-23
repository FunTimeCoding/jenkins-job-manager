from lxml import etree
from lxml.etree import Element, XMLParser


def load_fixture(path: str) -> Element:
    my_parser = XMLParser(remove_blank_text=True)
    fixture_tree = etree.parse(path, parser=my_parser)
    fixture_root_node = fixture_tree.getroot()

    return fixture_root_node

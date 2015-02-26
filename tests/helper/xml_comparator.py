from lxml.etree import Element


def text_compare(text_a, text_b):
    if not text_a and not text_b:
        return True
    if text_a == '*' or text_b == '*':
        return True
    return (text_a or '').strip() == (text_b or '').strip()


def xml_compare(element_a: Element, element_b: Element, reporter=None):
    if element_a.tag != element_b.tag:
        if reporter:
            reporter('Tags do not match: %s and %s' % (element_a.tag,
                                                       element_b.tag))
        return False
    for name, value in element_a.attrib.items():
        if element_b.attrib.get(name) != value:
            if reporter:
                reporter('Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, element_b.attrib.get(name)))
            return False
    for name in element_b.attrib.keys():
        if name not in element_a.attrib:
            if reporter:
                reporter('x2 has an attribute x1 is missing: %s'
                         % name)
            return False
    if not text_compare(element_a.text, element_b.text):
        if reporter:
            reporter('text: %r != %r' % (element_a.text, element_b.text))
        return False
    if not text_compare(element_a.tail, element_b.tail):
        if reporter:
            reporter('tail: %r != %r' % (element_a.tail, element_b.tail))
        return False
    cl1 = element_a.getchildren()
    cl2 = element_b.getchildren()
    if len(cl1) != len(cl2):
        if reporter:
            reporter('children length differs, %i != %i'
                     % (len(cl1), len(cl2)))
        return False
    i = 0
    for child_a, child_b in zip(cl1, cl2):
        i += 1
        if not xml_compare(child_a, child_b, reporter=reporter):
            if reporter:
                reporter('children %i do not match: %s'
                         % (i, child_a.tag))
            return False
    return True

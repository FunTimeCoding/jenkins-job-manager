from lxml.etree import Element


def text_compare(text_a: str, text_b: str) -> bool:
    if not text_a and not text_b:
        result = True
    elif text_a == '*' or text_b == '*':
        result = True
    else:
        result = (text_a or '').strip() == (text_b or '').strip()

    return result


def compare_tags(element_a, element_b, reporter=None) -> bool:
    result = True

    if element_a.tag != element_b.tag:
        result = False

        if reporter:
            reporter.report('Tags do not match: %s and %s' % (element_a.tag,
                                                              element_b.tag))

    return result


def compare_attributes(element_a, element_b, reporter=None) -> bool:
    result = True

    for name, value in element_a.attrib.items():
        if element_b.attrib.get(name) != value:
            result = False

            if reporter:
                reporter.report('Attributes do not match: %s=%r, %s=%r'
                                % (name, value, name,
                                   element_b.attrib.get(name)))

            break

    return result


def compare_missing_attributes(element_a, element_b, reporter=None) -> bool:
    result = True

    for name in element_b.attrib.keys():
        if name not in element_a.attrib:
            result = False

            if reporter:
                reporter.report('x2 has an attribute x1 is missing: %s' % name)

            break

    return result


def compare_text(element_a, element_b, reporter=None) -> bool:
    result = True

    if not text_compare(element_a.text, element_b.text):
        result = False

        if reporter:
            reporter.report(
                'text: %r != %r' % (element_a.text, element_b.text)
            )

    return result


def compare_children_length(cl1, cl2, reporter):
    result = True

    if len(cl1) != len(cl2):
        result = False

        if reporter:
            reporter.report(
                'children length differs, %i != %i' % (len(cl1), len(cl2)))

    return result


def compare_children(cl1, cl2, reporter):
    result = True
    i = 0

    for child_a, child_b in zip(cl1, cl2):
        i += 1

        if not xml_compare(child_a, child_b, reporter=reporter):
            result = False

            if reporter:
                reporter.report('child %i does not match: %s'
                                % (i, child_a.tag))

            break

    return result


def xml_compare(element_a: Element, element_b: Element, reporter=None) -> bool:
    result = True

    if not compare_tags(element_a, element_b, reporter):
        result = False
    elif not compare_attributes(element_a, element_b, reporter):
        result = False
    elif not compare_missing_attributes(element_a, element_b, reporter):
        result = False
    elif not compare_text(element_a, element_b, reporter):
        result = False
    else:
        cl1 = element_a.getchildren()
        cl2 = element_b.getchildren()

        if not compare_children_length(cl1, cl2, reporter):
            result = False
        elif not compare_children(cl1, cl2, reporter):
            result = False

    return result


class Reporter():
    def __init__(self):
        self.count = 0
        self.messages = []

    def report(self, message: str):
        self.count += 1
        self.messages.append(message)
        print(message)

    def get_messages(self):
        return self.messages

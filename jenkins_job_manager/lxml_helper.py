from lxml import etree
from lxml.etree import Element


def serialize_element(element: Element) -> str:
    tags_to_not_shorten = [
        'description',
        'id',
        'name',
        'reportEncoding',
        'sourceCodeEncoding',
        'sourceDirectory',
        'referenceJobName',
        'sourceExclusionPattern',
        'inclusionPattern',
        'exclusionPattern',
    ]

    for node in element.iter():
        if node.tag in tags_to_not_shorten:
            if node.text is None:
                node.text = ''

    return etree.tostring(
        element_or_tree=element,
        encoding='unicode',
        pretty_print=True
    )

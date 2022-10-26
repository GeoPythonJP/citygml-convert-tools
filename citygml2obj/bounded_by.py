#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
from common import nsmap


class BoundedBy:
    """ gml:boundedBy """
    def __init__(self, element):
        if element.tag != "{%s}boundedBy" % nsmap['gml']:
            raise Exception('ERROR: element tag = %s' % element.tag)
        self.element = element

    def get_srid(self):
        envelope = self.element.find('gml:Envelope', namespaces=nsmap)
        # tag = envelope.tag
        # text = envelope.text
        srsName = envelope.attrib["srsName"]
        # srsDimension = envelope.attrib["srsDimension"]
        # 空間参照ID(SRID)
        return srsName.split("/")[-1]

    def get_corner(self):
        envelope = self.element.find('gml:Envelope', namespaces=nsmap)
        lower_corner = envelope.find('gml:lowerCorner', namespaces=nsmap)
        upper_corner = envelope.find('gml:upperCorner', namespaces=nsmap)
        lower_pos = [float(pos) for pos in lower_corner.text.split()]
        upper_pos = [float(pos) for pos in upper_corner.text.split()]
        return [lower_pos, upper_pos]

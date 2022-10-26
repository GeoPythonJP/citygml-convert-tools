#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
from common import nsmap


class Appearance:
    """ app:Appearance """
    def __init__(self, element):
        if element.tag != "{%s}Appearance" % nsmap['app']:
            raise Exception('ERROR: element tag = %s' % element.tag)
        self.element = element

    def execute(self):
        theme = self.element.find('app:theme', namespaces=nsmap).text

        for surface_data_member in self.element.findall('app:surfaceDataMember', namespaces=nsmap):
            parameterized_texture = surface_data_member.find('app:ParameterizedTexture', namespaces=nsmap)
            image_uri = parameterized_texture.find('app:imageURI', namespaces=nsmap).text
            mime_type = parameterized_texture.find('app:mimeType', namespaces=nsmap).text
            for target in parameterized_texture.findall('app:target', namespaces=nsmap):
                uri = target.attrib["uri"]
                for texture_coordinates in target.findall('app:TexCoordList/app:textureCoordinates', namespaces=nsmap):
                    ring = texture_coordinates.attrib["ring"]
                    pos = [float(pos) for pos in texture_coordinates.text.split()]


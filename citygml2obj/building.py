#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
from common import nsmap


class Building:
    """ bldg:Building"""
    def __init__(self, element):
        if element.tag != "{%s}Building" % nsmap['bldg']:
            raise Exception('ERROR: element tag = %s' % element.tag)
        self.element = element

    def execute(self):
        # gml:id
        gml_id = self.element.attrib["{%s}id" % nsmap['gml']]

        # gen:stringAttribute
        for string_attribute in self.element.findall('gen:stringAttribute', namespaces=nsmap):
            name = string_attribute.attrib["name"]
            if name == "建物ID":
                value = string_attribute.find('gen:value', namespaces=nsmap).text
            elif name == "大字・町コード":
                value = string_attribute.find('gen:value', namespaces=nsmap).text
            elif name == "町・丁目コード":
                value = string_attribute.find('gen:value', namespaces=nsmap).text
            elif name == "13_区市町村コード_大字・町コード_町・丁目コード":
                value = string_attribute.find('gen:value', namespaces=nsmap).text

        # bldg:measuredHeight
        measured_height = self.element.find('bldg:measuredHeight', namespaces=nsmap)
        uom = measured_height.attrib["uom"]
        measured_height_value = float(measured_height.text)

        # bldg:lod0RoofEdge
        # bldg:lod0RoofEdge/gml:MultiSurface/gml:surfaceMember/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList
        lod0_roof_edge = self.element.find('bldg:lod0RoofEdge', namespaces=nsmap)
        pos_list = lod0_roof_edge.find('gml:MultiSurface/gml:surfaceMember/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList', namespaces=nsmap)
        pos = [float(pos) for pos in pos_list.text.split()]
        # print(pos)

        # bldg:lod1Solid
        # /bldg:lod1Solid/gml:Solid/gml:exterior/gml:CompositeSurface/gml:surfaceMember/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList
        lod1_solid = self.element.find('bldg:lod1Solid', namespaces=nsmap)
        for surface_member in lod1_solid.findall('gml:Solid/gml:exterior/gml:CompositeSurface/gml:surfaceMember', namespaces=nsmap):
            pos_list = surface_member.find('gml:Polygon/gml:exterior/gml:LinearRing/gml:posList', namespaces=nsmap)
            pos = [float(pos) for pos in pos_list.text.split()]
            # print(pos)

        # bldg:lod2Solid
        # bldg:lod2Solid/gml:Solid/gml:exterior/gml:CompositeSurface
        lod2_solid = self.element.find('bldg:lod2Solid', namespaces=nsmap)
        for surface_member in lod2_solid.findall('gml:Solid/gml:exterior/gml:CompositeSurface/gml:surfaceMember', namespaces=nsmap):
            surface_member_xref = surface_member.attrib["{%s}href" % nsmap['xlink']]
            # print(surface_member_xref)

        # bldg:boundedBy/bldg:GroundSurface
        ground_surface_list = self.get_lod2_surface('bldg:boundedBy/bldg:GroundSurface')

        # bldg:boundedBy/bldg:RoofSurface
        roof_surface_list = self.get_lod2_surface('bldg:boundedBy/bldg:RoofSurface')

        # bldg:boundedBy/bldg:WallSurface
        wall_surface_list = self.get_lod2_surface('bldg:boundedBy/bldg:WallSurface')

        # bldg:address
        address = self.element.find('bldg:address', namespaces=nsmap)
        country = address.find('core:Address/core:xalAddress/xAL:AddressDetails/xAL:Country', namespaces=nsmap)
        country_name = country.find('xAL:CountryName', namespaces=nsmap).text
        locality_name = country.find('xAL:Locality/xAL:LocalityName', namespaces=nsmap)
        locality_name_type = locality_name.attrib["Type"]
        locality_name_value = locality_name.text

        # uro:buildingDetails
        building_details = self.element.find('uro:buildingDetails', namespaces=nsmap)

        # uro:extendedAttribute
        for extended_attribute in self.element.findall('uro:extendedAttribute', namespaces=nsmap):
            pass

    def get_lod2_surface(self, surface_name):
        surface_list = []
        for surface in self.element.findall(surface_name, namespaces=nsmap):
            surface_id = surface.attrib["{%s}id" % nsmap['gml']]
            for lod2_multi_surface in surface.findall('bldg:lod2MultiSurface', namespaces=nsmap):
                for multi_surface in lod2_multi_surface.findall('gml:MultiSurface', namespaces=nsmap):
                    polygon = multi_surface.find("gml:surfaceMember/gml:Polygon", namespaces=nsmap)
                    polygon_id = polygon.attrib["{%s}id" % nsmap['gml']]

                    linear_ring = polygon.find("gml:exterior/gml:LinearRing", namespaces=nsmap)
                    linear_ring_id = linear_ring.attrib["{%s}id" % nsmap['gml']]

                    pos_list = linear_ring.find('gml:posList', namespaces=nsmap)
                    pos = [float(pos) for pos in pos_list.text.split()]
                    # print(pos)

        return surface_list
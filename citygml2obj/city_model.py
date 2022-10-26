#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
from common import nsmap

from bounded_by import BoundedBy
from building import Building
from appearance import Appearance


class CityModel:
    """ core:CityModel """
    def __init__(self, element):
        if element.tag != "{%s}CityModel" % nsmap['core']:
            raise Exception('ERROR: element tag = %s' % element.tag)
        self.element = element

    def execute(self):
        """ child element """
        for child_element in self.element:
            if child_element.tag == "{%s}boundedBy" % nsmap['gml']:
                # print("boundedBy")
                obj_bounded_by = BoundedBy(child_element)
                srid = obj_bounded_by.get_srid()
                corner = obj_bounded_by.get_corner()

                # print(f"srid={srid}")
                # print(f"corner={corner}")

            elif child_element.tag == "{%s}cityObjectMember" % nsmap['core']:
                print("cityObjectMember")
                for building_element in child_element.findall('bldg:Building', namespaces=nsmap):
                    Building(building_element).execute()

            elif child_element.tag == "{%s}appearanceMember" % nsmap['app']:
                print("appearanceMember")
                for appearance_element in child_element.findall('app:Appearance', namespaces=nsmap):
                    Appearance(appearance_element).execute()

            else:
                raise Exception('ERROR: child_element tag = %s' % child_element.tag)



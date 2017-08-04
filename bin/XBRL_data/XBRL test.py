# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:51:22 2015

This file was built to test python-xbrl package. 



@author: ptorre
"""
from xbrl import XBRLParser, GAAP, GAAPSerializer

xbrl_parser = XBRLParser()
xbrl = xbrl_parser.parse(file("rht-20150228.xml"))
#%%
gaap_obj = xbrl_parser.parseGAAP(xbrl, doc_type="10-Q", context="current", ignore_errors=0)
serialized = GAAPSerializer(gaap_obj)
print serialized.data
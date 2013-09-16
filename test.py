#!/usr/bin/env python3
from xml_parsing import XML_Parser
from family_tree_gen import build_tree_from_hf
from attribute_getters import *

def main():

    xml_file = 'test-fixed.xml'
    
    parser = XML_Parser()
    try:
        everything = parser.load_dict(xml_file)
    except Exception as e:
        print(e)
        everything = None
    
    if everything == None:
        new_filename = parser.handle_invalid_file(xml_file)
        everything = parser.load_dict(new_filename)
            
    #build_tree_from_hf(get_element(5461, 'historical_figures', everything), everything, 0)
            
main()

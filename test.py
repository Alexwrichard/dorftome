#!/usr/bin/env python3
from xml_parsing import load_dict, handle_invalid_file
from family_tree_gen import build_tree_from_hf
from attribute_getters import *

def main():

    xml_file = 'test.xml'
    
    try:
        everything = load_dict(xml_file)
    except Exception as e:
        everything = None
    
    if everything == None:
        new_filename = handle_invalid_file(xml_file)
        everything = load_dict(new_filename)
            
    build_tree_from_hf(get_element(5461, 'historical_figures', everything), everything, 0)
            
main()

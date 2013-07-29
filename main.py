#!/usr/bin/env python3
from xml_parsing import load_dict
from family_tree_gen import build_tree_from_hf
from attribute_getters import *

def main():
    everything = load_dict('dwarf.xml')
    build_tree_from_hf(get_element(5461, 'historical_figures', everything), everything, 0)

main()

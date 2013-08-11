#!/usr/bin/env python3
from attribute_getters import *


def create_hf_link(hf_id, everything):
        return "<a href='hf" + hf_id + "' class='entity-link' >" +\
        get_hf_name(hf_id, everything) + "</a>"

def create_entity_link(entity_id, everything):
        return "<a href='en" + entity_id + "' class='entity-link' >" +\
                get_ent_name(entity_id, everything) + "</a>"

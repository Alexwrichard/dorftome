#!/usr/bin/env python3
from attribute_getters import *


def create_hf_link(hf_id, everything):
    return "<a href='hf" + str(hf_id) + "' class='hf-link' >" +\
        get_hf_name(hf_id, everything) + "</a>"

def create_entity_link(entity_id, everything):
    return "<a href='en" + str(entity_id) + "' class='entity-link' >" +\
        get_ent_name(entity_id, everything) + "</a>"
                
def create_site_link(site, everything):
    if 'site_id' in site.keys():
        site_id = site['site_id']
        site_name = get_site_name(site_id, everything)
    elif 'coords' in site.keys():
        site_id, site_name = get_site_data(site['coords'], everything)
        if site_id == -1:
            return ""
    else:
        return ""
        
    return "<a href='si" + str(site_id) + "' class='site-link' >" +\
        "in " + site_name + "</a>"
        


#!/usr/bin/env python3
from attribute_getters import *


link_mapper = {
               '':'',
               'regions': 'reg',
               'underground_regions': 'urg',
               'sites': 'sit',
               'world_constructions': 'woc',
               'artifacts':'art',
               'historical_figures': 'hif',
               'entity_populations': 'enp',
               'entities': 'ent',
               'historical_events': 'evt',
               'historical_event_collections': 'hec',
               'historical_eras':'era'
               }
                        
'''
Given a name of something in the world, will return a properly-
formatted page link.
'''
def create_page_id(name, everything):
    element_type, element_id = get_id_and_type(name, everything)
    return link_mapper[element_type] + str(element_id)
    
'''
Given a page link, return an appropriate page title.
'''
def get_name_from_page_id(page_link, everything):
    element_type = page_link[:3]
    for k in link_mapper:
        if link_mapper[k] == element_type:
            element_type = k
            break
    element_id = int(page_link[3:])
    return get_name(element_id, element_type, everything)
    
'''
Return an HTML link to a historical figure page given a historical
figure ID.
'''
def create_hf_link(hf_id, everything):
    return "<a href='hif" + str(hf_id) + "' class='hf-link' >" +\
        get_hf_name(hf_id, everything) + "</a>"

'''
Return an HTML link to an entity page given an entity ID.
'''
def create_entity_link(entity_id, everything):
    return "<a href='ent" + str(entity_id) + "' class='entity-link' >" +\
        get_ent_name(entity_id, everything) + "</a>"
                
'''
Return an HTML link to a site page given a site ID.
'''
def create_site_link(site, everything):
    if isinstance(site, int):
        site_id = site
        site_name = get_site_name(site_id, everything)
    elif 'site_id' in site.keys():
        site_id = site['site_id']
        site_name = get_site_name(site_id, everything)
    elif 'coords' in site.keys():
        site_id, site_name = get_site_data(site['coords'], everything)
        if site_id == -1:
            return ""
    else:
        return ""
        
    return "<a href='sit" + str(site_id) + "' class='site-link' >" +\
        "in " + site_name + "</a>"
        


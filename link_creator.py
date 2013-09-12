#!/usr/bin/env python3
from attribute_getters import *


link_mapper = {'':'',\
                        'region': 'reg', \
                        'underground_region': 'urg', \
                        'site': 'sit', \
                        'world_construction': 'woc', \
                        'artifact':'art', \
                        'historical_figure': 'hif', \
                        'entity_population': 'enp',\
                        'entity': 'ent',\
                        'historical_event': 'evt',\
                        'historical_event_collection': 'hec',\
                        'historical_era':'era'}
                        
def create_page_id(name, everything):
    element_type, element_id = get_id(name, everything)
    return link_mapper[element_type] + str(element_id)
    
def get_name_from_page_id(page_id, everything):
    element_type = ''.join(c for c in page_id if not c.isdigit())
    for k in link_mapper:
        if link_mapper[k] == element_type:
            element_type = k + 's'
            if element_type == 'entitys':
                element_type = 'entities'
    element_id = ''.join(c for c in page_id if c.isdigit())
    return get_name(int(element_id), element_type, everything)
    
def create_hf_link(hf_id, everything):
    return "<a href='hif" + str(hf_id) + "' class='hf-link' >" +\
        get_hf_name(hf_id, everything) + "</a>"

def create_entity_link(entity_id, everything):
    return "<a href='ent" + str(entity_id) + "' class='entity-link' >" +\
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
        
    return "<a href='sit" + str(site_id) + "' class='site-link' >" +\
        "in " + site_name + "</a>"
        


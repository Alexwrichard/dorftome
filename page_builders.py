#!/usr/bin/env python3
from attribute_getters import *
from event_processing import time_string, event_type_dispatcher
from PySide import QtGui, QtCore

'''
LINK CONVENTIONS:
ent#### = entity
hf#### = historical figure

'''

'''
Given an id, return an HTML string describing that historical figure.
'''
def build_hf_page(an_id, everything, css):
    #event strings is an array of human-readable strings describing events.
    event_strings = []
    hf_name = get_hf_name(an_id, everything)

    #Beginning HTML for the historical figure page.
    page = "<html><head>\
            <link rel='stylesheet' type='text/css' href='format.css'>\
            </head><body>\
            <h1 class='page-title'>" + hf_name + "</h1>\
            <h3 class='page-description'>" + get_hf_gender(an_id, everything) +\
            " " + get_hf_race(an_id, everything) + "</h3><hr>"

    #For each event, we will try to get an event string from the event dispatcher,
    #then put it on the page (TODO hopefully in a more ceremonious manner eventually).
    for event_id in get_hf_events(an_id, everything):
        event_str = event_type_dispatcher(event_id, everything)
        if(event_str is not None):
            event_strings.append(event_str)
            page += event_str

    page += "<div class='page-content'><p><b class='hf-name-occurence'>"\
                   + hf_name + "</b> was born on the " +\
                   time_string(get_hf(an_id, everything)['birth_seconds72']) +\
                   ", Year " + get_hf(an_id, everything)['birth_year'] + ".</p></div>"

    page += "<div class='memberships'>"#<ul>"
    
    #For each entity link, we will add that entity to the membership list.
    for entity_data in get_hf(an_id, everything)['entity_links']:
        page += "<p><a href='ent" + entity_data['entity_id'] + "'>" +\
                get_element(entity_data['entity_id'], 'entities', everything)['name'] +\
                "</a></p>"
    page += "</div>"#"</ul></div>"

    page += "</body></html>"
    print(page)

    return page

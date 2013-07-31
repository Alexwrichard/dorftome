#!/usr/bin/env python3
from attribute_getters import *
from event_processing import time_string, event_type_dispatcher
from PySide import QtGui, QtCore

'''
Given an id, return an HTML string describing that historical figure.
'''
def build_hf_page(an_id, everything, css):
    
    event_strings = []
    hf_name = get_hf_name(an_id, everything)

    page = "<html><head>\
            <link rel='stylesheet' type='text/css' href='format.css'>\
            </head><body>\
            <h1 class='page-title'>" + hf_name + "</h1>\
            <h3 class='page-description'>" + get_hf_gender(an_id, everything) +\
            " " + get_hf_race(an_id, everything) + "</h3><hr>"
    for event_data in get_hf_events(an_id, everything):
        print(event_data)
        event_str = event_type_dispatcher(event_data, everything)
        event_strings.append(event_str)
        print(get_element(event_data, 'historical_events', everything)['type'])
        if(event_str is not None):
            page += event_str

    page += "<p><b class='hf-name-occurence'>" + hf_name + "</b> was born on the " +\
                   time_string(get_hf(an_id, everything)['birth_seconds72']) +\
                   ", Year " + get_hf(an_id, everything)['birth_year'] + ".</p>"
                

    return page

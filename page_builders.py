#!/usr/bin/env python3
from attribute_getters import *
from event_processing import time_string, event_type_dispatcher
from PySide import QtGui, QtCore

CSS_STR = \
        "\
        body {\
            background-color:#555555;\
        }\
        a.entity-link:link {\
            text-decoration:none;\
            color:#448844;\
        }\
        a.entity-link:hover {\
            text-decoration:none;\
            color:#DDDDDD;\
        }\
        .hf-name-occurence {\
            font-family:Helvetica, sans-serif;\
            font-size:14px;\
        }\
        .memberships {\
            font-family:Helvetica, sans-serif;\
            float:right;\
            color:#FF0000;\
            padding:10px;\
            border: 2px solid;\
            border-color: #222222;\
        }\
        .page-content {\
            font-family:Garamond, serif;\
            font-size:13px;\
            float:left;\
        }\
        .page-description {\
            color:#999999;\
            font-family:Helvetica, sans-serif;\
        }\
        .page-title {\
            color:#BBBBBB;\
            font-family:Helvetica, sans-serif;\
        }"

'''
LINK CONVENTIONS:
en#### = entity
hf#### = historical figure
'''
def dispatch_link(page_link, everything):
    code = page_link[:2]
    dispatcher = {
                  'en' : build_entity_page,
                  'hf' : build_hf_page,
                  'sp' : build_splash_page,
                 }
    return dispatcher[code](int(page_link[2:]), everything)

'''
Given an id, return an HTML string describing that historical figure.
'''
def build_hf_page(an_id, everything):
    #event strings is an array of human-readable strings describing events.
    event_strings = []
    hf_name = get_hf_name(an_id, everything)

    #Beginning HTML for the historical figure page.
    page = "<html><head>\
            <style type='text/css'>" + CSS_STR + "</style>\
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
        page += "<p><a href='en" + entity_data['entity_id'] + "' class='entity-link' >" +\
                get_ent_name(entity_data['entity_id'], everything) +\
                "</a></p>"
    page += "</div>"#"</ul></div>"

    page += "</body></html>"

    return page

def build_entity_page(an_id, everything):
    ent_name = get_ent_name(an_id, everything)
    page = "<html><head>\
            <style type='text/css'>" + CSS_STR + "</style>\
            </head><body>\
            <h1 class='page-title'>" + ent_name + "</h1>\
            <hr>\
            </body></html>"
    return page

def build_splash_page(dummy, dummy2):
    string = "<html><head>\
             <style type='text/css'>" + CSS_STR + "</style>\
             </head><body>\
             <h1 class='page-title'> Welcome! </h1>\
             <hr>\
             <p class='plain-text'>To begin browsing, select File > Load XML and locate the correct file.</p>\
             </body></html>"

    return string

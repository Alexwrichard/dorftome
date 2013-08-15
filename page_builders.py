#!/usr/bin/env python3
from attribute_getters import *
from link_creator import *
from event_processing import time_string, event_type_dispatcher

CSS_STR = None

'''
Load the stylesheet from an external file
'''
def load_css():
    global CSS_STR
    f = open("master.css")
    CSS_STR = f.read()
    f.close()

'''
LINK CONVENTIONS:
sp0000 = splash page
en#### = entity
hf#### = historical figure
'''
def dispatch_link(page_link, everything):
    if CSS_STR is None:
        load_css()
    code = page_link[:2]
    dispatcher = {
                  'en' : build_entity_page,
                  'hf' : build_hf_page,
                  'sp' : build_splash_page,
                 }
    return dispatcher[code](int(page_link[2:]), everything)

'''
Return a CSS class name for a given event. All events of the same
type will have the same CSS class. This allows us to grab
all events of a specific type in JavaScript/JQuery, which will in
turn allow for some dynamic page categorization/organization.
'''
def css_classify_event(event_id, everything):
    return get_event_type(event_id, everything).replace(" ","-")

'''
Given an id, return an HTML string describing that historical figure.
'''
def build_hf_page(an_id, everything):
    #event strings is an array of human-readable strings describing events.
    event_strings = []
    hf_name = get_hf_name(an_id, everything)

    #Beginning HTML for the historical figure page.
    page = "<html><head>\
            <style>" + CSS_STR + "</style>\
            </head><body>\
            <h1 class='page-title'>" + hf_name + "</h1>\
            <h3 class='page-description'>" + get_hf_gender(an_id, everything) +\
            " " + get_hf_race(an_id, everything) + "</h3><hr>"

    page += "<div class='page-content'><p><b class='hf-name-occurence'>"\
                   + hf_name + "</b> was born "
    
    birth_year = get_hf(an_id, everything)['birth_year']
    if int(birth_year) >= 0:
         page += "on the " +\
                   time_string(get_hf(an_id, everything)['birth_seconds72']) +\
                   ", Year " + get_hf(an_id, everything)['birth_year'] + ".</p>"
    else:
        page += "at the beginning of the world."
                   
    page += "<hr>"
                   
    #Eventually, it would be cool to find a way to display this as a tree.
    for relationship_data in get_hf(an_id, everything)['hf_links']:
        page += "<p>" + capitalize(relationship_data['link_type']) + ' : ' + create_hf_link(relationship_data['hfid'], everything) + "</p>"
                
    page += "<hr>"
    
    for event_id in get_hf_events(an_id, everything):
        event_class = css_classify_event
        page += "<p>" + event_type_dispatcher(event_id, everything) + "</p>"
                   
    page += "</div>"
    page += "<div class='memberships'>"
    
    #For each entity link, we will add that entity to the membership list.
    for entity_data in get_hf(an_id, everything)['entity_links']:
        page += "<p>" + create_entity_link(entity_data['entity_id'], everything) + "</p>"
    page += "</div>"

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
             <div class='page-content'>\
             <p class='plain-text'>To begin browsing, select File > Load XML and locate the correct file.</p>\
             </div>\
             </body></html>"

    return string

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
Return a CSS class name for a given event. All events of the same
type will have the same CSS class. This allows us to grab
all events of a specific type in JavaScript/JQuery, which will in
turn allow for some dynamic page categorization/organization.
'''
def css_classify_event(event_id, everything):
    return get_event_type(event_id, everything).replace(" ","-")

def get_header():
    return  "<html><head>"\
            "<style>" + CSS_STR + "</style>"\
            "</head><body>"

def get_footer():
    return "</body></html>"

#==============SPLASH PAGE=============
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
    
#==============HF PAGE=============
'''
Given an id, return an HTML string describing that historical figure.
'''
def build_hf_page(an_id, everything):
    #event strings is an array of human-readable strings describing events.
    event_strings = []
    hf_name = get_hf_name(an_id, everything)

    #Beginning HTML for the historical figure page.
    page = get_header()
            
    page += "<h1 class='page-title'>" + hf_name + "</h1>\
            <h3 class='page-description'>" + get_hf_gender(an_id, everything) +\
            " " + get_hf_race(an_id, everything) + "</h3><hr>"

    page += "<div class='page-content' id='pagecontent'><p><b class='hf-name-occurence'>"\
                   + hf_name + "</b> was born "
    try:
        birth_year = get_hf(an_id, everything)['birth_year']
    except Exception:
        birth_year = -1
        
    if birth_year >= 0:
         page += "on the " +\
                   time_string(get_hf(an_id, everything)['birth_seconds72']) +\
                   ", Year " + str(get_hf(an_id, everything)['birth_year']) + ".</p>"
    else:
        page += "at the beginning of the world."
                   
    page += "<hr>"
                   
    #Eventually, it would be cool to find a way to display this as a tree.
    for relationship_data in get_hf(an_id, everything)['hf_links']:
        page += "<p>" + capitalize(relationship_data['type']) + ' : ' + create_hf_link(relationship_data['id'], everything) + "</p>"
                
    page += "<hr>"
    
    for event_id in get_hf_events(an_id, everything):
        event_class = css_classify_event
        page += "<p>" + event_type_dispatcher(event_id, everything) + "</p>"
                   
    page += "</div>"
    page += "<div class='memberships'>"
    
    #For each entity link, we will add that entity to the membership list.
    for entity_data in get_hf(an_id, everything)['entity_links']:
        page += "<p>" + create_entity_link(entity_data['id'], everything) + "</p>"
    page += "</div>"\
             #<script>\
             #    elem = document.getElementById('pagecontent');\
             #    alert(window.getComputedStyle(elem, null).getPropertyValue(\"font-family\"));\
             #</script>\
             #"

    page += get_footer()

    return page

#==============ENTITY PAGE=============
def build_entity_page(an_id, everything):
    ent_name = get_ent_name(an_id, everything)
    page = get_header()
    
    page += " <h1 class='page-title'>" + ent_name + "</h1>\
            <hr>\
            </body></html>"
    return page

#==============REGION PAGE=============
def build_region_page(an_id, everything):
    name = get_name(an_id, 'regions', everything)
    page = get_header()
    
    page += " <h1 class='page-title'>" + name + "</h1>\
            <hr>\
            </body></html>"
    return page

#==============UNDERGROUND REGION PAGE=============
def build_underground_region_page(an_id, everything):
    name = get_name(an_id, 'underground_regions', everything)
    page = get_header()
    
    page += " <h1 class='page-title'>" + name + "</h1>\
            <hr>\
            </body></html>"
    return page    

#==============SITE PAGE=============
def build_site_page(an_id, everything):
    name = get_name(an_id, 'sites', everything)
    page = get_header()
    
    page += " <h1 class='page-title'>" + name + "</h1>\
            <hr>\
            </body></html>"
    return page

#==============WORLD CONSTRUCTION PAGE=============
def build_world_construction_page(an_id, everything):
    name = get_name(an_id, 'world_constructions', everything)
    page = get_header()
    
    page += " <h1 class='page-title'>" + name + "</h1>\
            <hr>\
            </body></html>"
    return page

#==============ARTIFACT PAGE=============
def build_artifact_page(an_id, everything):
    name = get_name(an_id, 'artifacts', everything)
    page = get_header()
    
    page += " <h1 class='page-title'>" + name + "</h1>\
            <hr>\
            </body></html>"
    return page
 
 #==============ENTITY POP PAGE=============
def build_entity_population_page(an_id, everything):
    name = get_name(an_id, 'entity_population', everything)
    page = get_header()
    
    page += " <h1 class='page-title'>" + name + "</h1>\
            <hr>\
            </body></html>"
    return page

#==============HISTORICAL EVENT PAGE=============
def build_historical_event_page(an_id, everything):
    name = get_name(an_id, 'historical_event', everything)
    page = get_header()
    
    page += " <h1 class='page-title'>" + name + "</h1>\
            <hr>\
            </body></html>"
    return page

#==============HEC PAGE=============
def build_historical_event_collection_page(an_id, everything):
    name = get_name(an_id, 'historical_event_collection', everything)
    page = get_header()
    
    page += " <h1 class='page-title'>" + name + "</h1>\
            <hr>\
            </body></html>"
    return page
    
#==============HISTORICAL ERA PAGE=============
def build_historical_era_page(an_id, everything):
    name = get_name(an_id, 'historical_eras', everything)
    page = get_header()
    
    page += " <h1 class='page-title'>" + name + "</h1>\
            <hr>\
            </body></html>"
    return page

'''
Link conventions found in link_creator.py
Some will be removed
'''
dispatcher = {  're' : build_region_page, \
                        'ur' : build_underground_region_page, \
                        'si' : build_site_page, \
                        'wc' : build_world_construction_page, \
                        'ar' : build_artifact_page, \
                        'hf' : build_hf_page, \
                        'ep' : build_entity_population_page, \
                        'en' : build_entity_page, \
                        'he' : build_historical_event_page, \
                        'hec' : build_historical_event_collection_page, \
                        'hera' : build_historical_era_page, \
                        'sp' : build_splash_page,
                 }
           
def dispatch_link(page_link, everything):
    if CSS_STR is None:
        load_css()
    code = page_link[:2]
    
    return dispatcher[code](int(page_link[2:]), everything)

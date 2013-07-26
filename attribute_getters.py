#!/usr/bin/env python3

###################################
#----GENERIC ATTRIBUTE GETTERS----#
###################################

'''
an_id = a string, the id to get
everything = the main dictionary containing everything
a_type = The category, e.g. 'historical_figures'

Given these, will return an element from the database, accounting for the possible offset.
'''
def get_element(an_id, a_type, everything):  
    return everything[a_type][int(an_id) - everything[a_type + '_offset']]

def get_name(an_id, a_type, everything):
    return get_element(an_id, a_type, everything)['name']


####################################
#----SPECIFIC ATTRIBUTE GETTERS----#
####################################

def get_event_type(an_id, everything):
    return everything['events'][int(an_id) - everything['events_offset']]['type']
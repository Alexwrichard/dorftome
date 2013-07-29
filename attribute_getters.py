#!/usr/bin/env python3

def capitalize(string):
    words = string.split(' ')
    for i in range(len(words)):
        if words[i] not in ['the']:
            words[i] = words[i].capitalize()
    
    return ' '.join(words)

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
    return capitalize(get_element(an_id, a_type, everything)['name'])

####################################
#----SPECIFIC ATTRIBUTE GETTERS----#
####################################

def get_event_type(an_id, everything):
    return everything['historical_events'][int(an_id) - everything['historical_events_offset']]['type']

def get_hf_name(an_id, everything):
    return get_name(an_id, 'historical_figures', everything)

def get_hf(an_id, everything):
    return get_element(an_id, 'historical_figures', everything)

from lxml import etree
from lxml.etree import iterparse


def main():
    parser = etree.iterparse('dwarf.xml')
    everything = {}
 
    #There are a handful of "upper-level" tags. This includes historical_figures, sites, entities, etc.
    #Loop through these.
    for item in parser:
        if item[1].tag == 'df_world':
            for element in item[1].getchildren():
                element_data = load_generic_element(element, 'regions')
                everything[element.tag] = element_data[0]
                everything[element.tag + '_offset'] = element_data[1]
            break
    parse_historical_events(everything)

#Given an "upper-level" tag, load the gigantic dictionary with every piece of data in that category.
#This basically goes two levels down, so we have historical_figures -> historical_figure -> data for that historical_figure
#At the end, the dictionary looks like this:

#everything = {'historical_events' : [ {'id' : '57', 'race': 'amphibian man', 'name': 'Urist McAmphibianMan'}, { another historical figure, etc.} ], 'historical_events_offset' : '57'}

#So basically, it's a dictionary that maps strings to lists, where each list is a list of 
#dictionaries that map strings to strings. 

def load_generic_element(element, descriptor):
    elements_xml = element.getchildren()
    elements_list = []
    offset = None
    
    #For each element,
    for element in elements_xml:
        element_dict = {}
        attributes = element.getchildren()
        
        #Add the element attributes to a dictionary representing the element
        for attribute in attributes:
            if((offset is None) and (attribute.tag == 'id')):
                offset = int(attribute.text)
                
            element_dict[attribute.tag] = attribute.text
            
        element_dict['events'] = []
        elements_list.append(element_dict)
        
    return (elements_list, offset)

'''
an_id = a string, the id to get
everything = the main dictionary containing everything
a_type = The category, e.g. 'historical_figures'

Given these, will return an element from the database, accounting for the possible offset.
'''
def get_element_for_id(an_id, a_type, everything):  
    return everything[a_type][int(an_id) - everything[a_type + '_offset']]

def get_name_for_id(an_id, a_type, everything):
    return get_element_for_id(an_id, a_type, everything)['name']

def add_event_link_to_hf(hfid, event_id, everything):
    get_element_for_id(hfid, 'historical_figures', everything)['events'].append(event_id)

def print_event_info(event_id, everything):
    event = get_element_for_id(event_id, 'historical_events', everything)
    print event['type'] + ' in ' + event['year']
    
#Preliminary stuff.
def parse_historical_events(everything):
    for event_data in everything['historical_events']:
        for key in event_data.keys():
            if key in ['hfid', 'slayer_hfid', 'group_hfid', 'group_1_hfid', 'group_2_hfid']:
                if event_data[key] == '-1':
                    event_data[key + '_name'] = 'no one'
                else:
                    add_event_link_to_hf(event_data[key], event_data['id'], everything)
                    event_data[key + '_name'] = get_name_for_id(int(event_data[key]), 'historical_figures', everything)
            
            elif key == 'site_id':
                event_data[key + '_name'] = get_name_for_id(int(event_data[key]), 'sites', everything)

            elif key == 'entity_id':
                event_data[key + '_name'] = get_name_for_id(int(event_data[key]), 'entities', everything)

        '''
        if event_data['type'] == 'hf died':
            if event_data['hfid'] != event_data['slayer_hfid']:
                print '%s was killed by %s at %s.' % ( event_data['hfid_name'], event_data['slayer_hfid_name'], event_data['site_id_name'])
                '''
    for var in range(5500, 6100):
        print get_name_for_id(var, 'historical_figures', everything) + ' events:'
        for i in get_element_for_id(var, 'historical_figures', everything)['events']:
            print_event_info(i, everything)

main()

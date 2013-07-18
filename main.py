from lxml import etree
from lxml.etree import iterparse


def main():
    parser = etree.iterparse('dwarf.xml')
    everything = {}
    
    for item in parser:
        element = item[1]
        if((element.getparent() is not None) and (element.getparent().tag == 'df_world')):
            element_data = load_generic_element(element, 'regions')
            everything[element.tag] = element_data[0]
            everything[element.tag + '_offset'] = element_data[1]
    parse_historical_events(everything)

    
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

def parse_historical_events(everything):
    for event_data in everything['historical_events']:
        for key in event_data.keys():
            if key == 'hfid' or key == 'slayer_hfid':
                if event_data[key] == '-1':
                    event_data[key + '_name'] = 'no one'
                else:
                    event_data[key + '_name'] = everything['historical_figures'][int(event_data[key]) - everything['historical_figures_offset']]['name']
            
            elif key == 'site_id':
                event_data[key + '_name'] = everything['sites'][int(event_data['site_id']) - everything['sites_offset']]['name']

            elif key == 'entity_id':
                event_data[key + '_name'] = everything['entities'][int(event_data['entity_id']) - everything['entities_offset']]['name']

        if event_data['type'] == 'hf died':
            if event_data['hfid'] != event_data['slayer_hfid']:
                print '%s was killed by %s at %s.' % ( event_data['hfid_name'], event_data['slayer_hfid_name'], event_data['site_id_name'])
            
main()

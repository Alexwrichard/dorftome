from lxml import etree
from multiprocessing import Lock, Array
import io
import time
import sys

TAG_MAP = {'region': 'regions', \
           'underground_region': 'underground_regions', \
           'site': 'sites', \
           'world_construction': 'world_constructions', \
           'artifact':'artifacts', \
           'historical_figure': 'historical_figures', \
           'entity_population': 'entity_populations',\
           'entity': 'entities',\
           'historical_event': 'historical_events',\
           'historical_event_collection': 'historical_event_collections',\
           'historical_era':'historical_eras'}
               
'''
Used when not running in multithreaded mode. Parses the 
exported XML file using lxml and loads its data into the 
dictionary.
'''
def parse_file(filename):
    #Dictionary that stores all world information
    everything = {}
    
    element_array = []
    names_dict = {}
    offset = -1
    
    #The tags to search for
    lower_level_tags = TAG_MAP.keys()
    upper_level_tags = TAG_MAP.values()
    
    #Parse the file
    for _, element in etree.iterparse(filename):
        #Look for the lower-level elements
        if element.tag in lower_level_tags:
            if element.tag == 'historical_figure':
                #Smarter loading is needed for the historical figures,
                #as they have nested tags. TODO determine which other
                #elements need smarter loading and make functions for them.
                element_data, element_name, element_id = load_hist_figure_data(element)
            else:
                element_data, element_name, element_id = load_generic_element_data(element)
        
            #If we haven't stored an offset yet, store the first id we see
            if offset == -1:
                offset = element_id
                
            #Store element
            element_array.append(element_data)
            
            #Store the element's name
            if not element_name == "":
                names_dict[element_id] = element_name
            
        elif element.tag in upper_level_tags:
            
            #Store the elements in the everything dict
            everything[element.tag] = element_array
            everything[element.tag + "_names"] = names_dict
            everything[element.tag + "_offset"] = offset
            
            #Close the element
            close_element(element)
            
            #Reset for the next upper level tag
            element_array = []
            names_dict = {}
            offset = -1
            
    return everything
    
'''
Load a given element. This is only called in multithreaded mode.

'''
def load_element(element_string, high_level_tag):
    #Array with all processed elements
    temp_element_array = []

    #Dict mapping element ids to names
    names_dict = {}
    
    #This "offset" is for indexing purposes. So, for example, perhaps the first historical figure in the
    #'historical_figures' section has id=5764. From there, the indices progress one-by-one. So we can
    #set 'historical_figures_offset' to 5764. So then, accessing an element is easy and efficient; we just need to do
    #everything[element_type][id - offset]
    offset = -1
    
    #create a file object around the element
    #for the iterparse
    f = io.BytesIO(element_string)
    #find the lower level tags to look for
    lower_level_tags = TAG_MAP.keys()
    
    #iterparse through the element
    for _, element in etree.iterparse(f):
        #ignore tags within the lower level tag
        if not element.tag in lower_level_tags:
            continue
            
        if element.tag == 'historical_figure':
            element_data, element_name, element_id = load_hist_figure_data(element)
        else:
            element_data, element_name, element_id = load_generic_element_data(element)

        #if we haven't stored an offset yet, store the first id we see
        if offset == -1:
            offset = element_id
                
        #store element
        temp_element_array.append(element_data)
        
        #store the element's name
        if not element_name == "":
            names_dict[element_id] = element_name
    
    #callback to the main thread
    #which will add to main everything dict
    return (high_level_tag, offset, temp_element_array, names_dict)

'''
Returns an element data dictionary with the following structure:
    { 'events': [12521, 3462, 123, 733, 1324...],
      'hf_links': [ {'type':'mother', 'id':12415}, {'type':'father', 'id':1235}...],
      'entity_links' : [ {'type':'something', 'id':12415}, {'type':'somethingelse', 'id':1235}...],
    }
'''
def load_hist_figure_data(element):
    #sys.intern is used to cache strings to save memory
    element_data = {}
    element_data[sys.intern('events')] = []
    element_data[sys.intern('hf_links')] = []
    element_data[sys.intern('entity_links')] = []
    
    for attribute in element:
        #should not be saved
        if attribute.tag in ['hf_skill', 'entity_former_position_link']:
            close_element(attribute)
            continue
        #These tags have tags nested within them, and there are multiple for each historical figure,
        #Here, we parse them separately and store their information in subdictionaries within lists.
        if attribute.tag in ['hf_link', 'entity_link']:
            children = attribute.getchildren()
            
            attribute_dict = {}
            attribute_dict[sys.intern('type')] = sys.intern(children[0].text)
            attribute_dict[sys.intern('id')] = int(children[1].text)
            
            if attribute.tag == 'entity_link' and len(children) > 2:
                attribute_dict[sys.intern('strength')] = int(children[2].text)
                
            element_data[sys.intern(attribute.tag + 's')].append(attribute_dict)
        else: #other hf_fig attribute
        
            #Attributes such as death year for hf_figs still alive
            #or some site coords
            #should not be stored to save space
            if attribute.text == "-1" or attribute.text == "-1,-1":
                close_element(attribute)
                continue
                
            #don't save invalid birth years
            if attribute.tag == "birth_year" and int(attribute.text) < 0:
                close_element(attribute)
                continue
                
            tag = sys.intern(attribute.tag)
            if attribute.text == None:
                element_data[tag] = None
                close_element(attribute)
                continue
                
            #try to store attribute values as int, as they are smaller in memory
            try:
                element_data[tag] = int(attribute.text)
            except (ValueError, TypeError):
                element_data[tag] = sys.intern(attribute.text)
                
        close_element(attribute)
    close_element(element)
        
    #get the figure's name
    try:
        element_name = element_data['name']
    except KeyError:
        element_name = element_data['animated_string']
                
    #find the element's id
    try:
        element_id = int(element_data['id'])
    except KeyError:
        element_id = 0
            
    return element_data, element_name, element_id
     
'''
Returns a processed generic element
'''
def load_generic_element_data(element):
    element_data = {}
    
    #some elements have events
    #TODO: narrow this down
    if element.tag in ['historical_figure', 'site']:
        element_data['events'] = []
    
    #Add the element attributes to a dictionary representing the generic element
    for attribute in element.getchildren():
        
        #Do not store empty attributes
        if attribute.text == "-1":
            close_element(attribute)
            continue
        
        if element.tag == "historical_event":
            #Unimplemented events
            if attribute.tag == 'type' and attribute.text in ['add hf entity link', 'add hf site link', 'create entity position', 'creature devoured', 'hf new pet', 'item stolen', 'remove hf site link', 'remove hf entity link']:
                close_element(attribute)
                element_data = None
                close_element(attribute)
                close_element(element)
                break
            #Unused, do not store
            if attribute.tag == "feature_layer_id":
                close_element(attribute)
                continue
            #Empty coords are useless
            #TODO: maybe subregion ids are not?
            elif attribute.tag == "coords" and attribute.text == "-1,-1":
                close_element(attribute)
                continue

        #sys.intern is used to cache strings to save memory
        tag = sys.intern(attribute.tag)
        
        if attribute.text == None:
            #this is needed for flags like deity
            element_data[tag] = None
            close_element(attribute)
            continue
            
        #try to store attribute values as int, as they are smaller in memory
        try:
            element_data[tag] = int(attribute.text)
        except Exception:
            element_data[tag] = sys.intern(attribute.text)

        close_element(attribute)
    close_element(element)
        
    try:
        element_name = element_data['name']
    except (KeyError, TypeError):
        element_name = ""
        
    #find the element's id
    try:
        element_id = int(element_data['id'])
    except (KeyError, TypeError):
        element_id = 0
                
    return element_data, element_name, element_id
    
'''
Clean up the given lxml element.
'''
def close_element(element):
    element.clear()                 # clean up children
    while element.getprevious() is not None:
        del element.getparent()[0]  # clean up preceding siblings

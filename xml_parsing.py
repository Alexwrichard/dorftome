#!/usr/bin/env python3
from lxml import etree
from lxml.etree import iterparse
from attribute_getters import *
from event_processing import event_type_dispatcher
import os
import codecs
import time

PROFILE_MEMORY = True
PROFILE_TIME = True

try:
    from pympler.asizeof import asizeof
except Exception as e:
    PROFILE_MEMORY = False
    PROFILE_TIME = False

def handle_invalid_file(filename):
    print("Attempting to fix invalid file: " + filename)
    BLOCKSIZE = 1048576 # one megabyte
    
    tempfile = filename.replace(".xml", "-fixed.xml")

    statinfo = os.stat(filename)
    print("File size: " + str(statinfo.st_size) + " bytes")

    counter = 0

    with codecs.open(filename, "r", 'us-ascii', errors='replace') as sourceFile:
        with open(tempfile, "w") as targetFile:
            while True:
                counter += BLOCKSIZE
                percent_done = counter / statinfo.st_size
                if counter % (10 * BLOCKSIZE) < BLOCKSIZE:
                    print("\r" + str(percent_done))
                contents = sourceFile.read(BLOCKSIZE)
                
                if "�" in contents:
                    contents = contents.replace("�", "?")
                    
                if not contents:
                    break
                    
                targetFile.write(contents)

    print("Fixed file")
    return tempfile

def load_dict(filename):
        
    print("Loading file: " + filename)
    parser = etree.iterparse(filename)
        
    everything = {}
    
    tag_mapping = {'region': 'regions', \
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

    lower_level_tags = tag_mapping.keys()
    upper_level_tags = tag_mapping.values()
    
    #PROFILING
    if PROFILE_TIME:
        time_array = []
        start_time = time.clock()
    
    if PROFILE_MEMORY:
        memory_array = []
        memory_array.append(("At beginning : ", asizeof(everything)))
    
    temp_element_array = []
    for _, element in parser:
            
        if element.tag in lower_level_tags:
            if element.tag == 'historical_figure':
                element_data = load_historical_figure(element)
            else:
                element_data = load_generic_element(element)
            
            temp_element_array.append(element_data)
            close_element(element)
            
        elif element.tag in upper_level_tags:
            print("Finishing: " + element.tag)
            
            #This "offset" is for indexing purposes. So, for example, perhaps the first historical figure in the
            #'historical_figures' section has id=5764. From there, the indexes progress one-by-one. So we can
            #set 'historical_figures_offset' to 5764. So then, accessing an element is easy and efficient; we just need to do
            #everything[element_type][id - offset]
            if len(temp_element_array) > 0 and 'id' in temp_element_array[0].keys(): #FIX
                #print("Offset is: " + str(temp_element_array[0]['id']))
                everything[element.tag + "_offset"] = temp_element_array[0]['id']
                
            everything[element.tag] = temp_element_array
            temp_element_array = []
            
            if PROFILE_TIME:
                time_array.append([element.tag, time.clock() - start_time])
                start_time = time.clock() #measure time until next high-level tag is finished
                
            if PROFILE_MEMORY:
                memory_array.append(("Finishing " + element.tag + ": ", asizeof(everything)))
                
            close_element(element)
        
    if PROFILE_TIME:
        start_time = time.clock()
        
    parse_historical_events(everything)
    
    if PROFILE_TIME:
        time_array.append(['parsing historical events', time.clock() - start_time])
    
    if PROFILE_MEMORY:
        memory_array.append(("After parsing historical events: ", asizeof(everything)))
    
    #PRINT PROFILING INFO
    if PROFILE_TIME:
        total_time = 0
        print("\n\nTIMING INFO:")
        for e, t in time_array:
            print("Time taken for " + e + ": " + str(t) + "s")
            total_time += t
        print("Total time: " + str(total_time) + "s")
        
    if PROFILE_MEMORY:
        print("\n\nMEMORY INFO:")
        for i in range(0, len(memory_array)):
            difference = 0
            if (i >= 1):
                difference = memory_array[i][1] - memory_array[i-1][1]
            print(memory_array[i][0] + " : " + str(memory_array[i][1]/1024) + " KB || Difference: " + str(difference/1024) + " KB")
            
    return everything
    
def close_element(element):
    element.clear()                 # clean up children
    while element.getprevious() is not None:
        del element.getparent()[0]  # clean up preceding siblings

def load_generic_element(element):
    generic_element = {}
    generic_element['events'] = []
    
    attributes = element.getchildren()
        
    #Add the element attributes to a dictionary representing the element
    for attribute in attributes:
       try:
            generic_element[attribute.tag] = int(attribute.text)
       except Exception:
            generic_element[attribute.tag] = attribute.text
       
    return generic_element

def load_historical_figure(element):
    hist_fig = {}
    hist_fig['events'] = []
    hist_fig['hf_links'] = []
    hist_fig['entity_links'] = []
    
    attributes = element.getchildren()
    for attribute in element:
        #These tags have tags nested within them, and there are multiple for each historical figure,
        #Here, we parse them separately and store their information in subdictionaries within lists.
        if attribute.tag not in ['hf_link', 'entity_link', 'hf_skill', 'entity_former_position_link']:
            try:
                hist_fig[attribute.tag] = int(attribute.text)
            except Exception:
                hist_fig[attribute.tag] = attribute.text
            
        elif attribute.tag == 'hf_link':
            hf_link_dict = {}
            for link_info in attribute.getchildren():
                try:
                    hf_link_dict[link_info.tag] = int(link_info.text)
                except ValueError:
                    hf_link_dict[link_info.tag] = link_info.text
            hist_fig['hf_links'].append(hf_link_dict)

        elif attribute.tag == 'entity_link':
            entity_link_dict = {}
            for link_info in attribute.getchildren():
                try:
                    entity_link_dict[link_info.tag] = int(link_info.text)
                except ValueError:
                    entity_link_dict[link_info.tag] = link_info.text
            hist_fig['entity_links'].append(entity_link_dict)
        
    return hist_fig
    
def add_event_link_to_hf(hfid, event_id, everything):
    get_element(hfid, 'historical_figures', everything)['events'].append(event_id)

def parse_historical_events(everything):
    if not 'historical_events' in everything:
        return
    
    for event_data in everything['historical_events']:
        for key in event_data.keys():
            if key in set(['hfid', 'slayer_hfid', 'group_hfid', 'group_1_hfid', 'group_2_hfid', 'woundee_hfid',
                           'wounder_hfid', 'trickster_hfid', 'cover_hfid', 'hist_fig_id', 'target_hfid', 
                           'snatcher_hfid', 'changee_hfid', 'changer_hfid', 'hist_figure_id', 'hfid_target',]):
                if event_data[key] != -1:
                    add_event_link_to_hf(event_data[key], event_data['id'], everything)
    '''
    for var in range(5500, 6100):
        print(get_name(var, 'historical_figures', everything) + ' events:')
        for i in get_element(var, 'historical_figures', everything)['events']:
            print_event_info(i, everything)
    '''


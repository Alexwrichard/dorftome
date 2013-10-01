#!/usr/bin/env python3
from lxml import etree
from lxml.etree import iterparse

from attribute_getters import *
from event_processing import event_type_dispatcher
from dict_loading import load_element, parse_file
from connect_elements import parse_historical_events

import functools
import os
import codecs
import time
import configparser

from multiprocessing import Pool

class ProfilerStruct:
    PROFILE_TIME=False
    PROFILE_MEMORY=False
    time_array=[]
    memory_array=[]
    start_time=0

'''
Process an XML file with invalid characters and replace them with 
question marks.
'''
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

'''
Parse the entire XML file 
'''
def load_dict(filename):
    profiler = ProfilerStruct()

    cfg = configparser.ConfigParser()
    cfg.read(os.path.join('..', 'resources', 'legend_reader.cfg'))
    num_parsing_threads = int(cfg.get('default',"num_parsing_threads"))
    
    profiler.PROFILE_TIME = (cfg.get('profiling',"print_parsing_timing") == "True")
    profiler.PROFILE_MEMORY = (cfg.get('profiling',"print_parsing_memory") == "True")

    try:
        from pympler.asizeof import asizeof
    except ImportError:
        profiler.PROFILE_MEMORY = False
        profiler.PROFILE_TIME = False

    everything = {}
    

    print("Loading file: " + filename)
    
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
    if profiler.PROFILE_TIME:
        profiler.time_array = []
        profiler.start_time = time.time()
    
    if profiler.PROFILE_MEMORY:
        profiler.memory_array = []
        profiler.memory_array.append(("At beginning : ", asizeof(everything)))
    
    #set up thread pool
    if num_parsing_threads < 0:
        #create num threads = cpu count
        pool = Pool()
    elif num_parsing_threads > 0:
        #create required size pool
        pool = Pool(num_parsing_threads)
    else:
        pool = None
    
    #using multi-threading to parse file
    if pool:
        for _, element in etree.iterparse(filename):
            if element.tag in upper_level_tags:
                #Use partial from functools to create something we can call back to while
                #passing the everything dict.
                add_elements_callback = functools.partial(add_elements, profiler=profiler, everything=everything)

                #Call parser to process the element
                #The element must be sent as a string
                #Will callback to add elements to actually add to everything dict
                pool.apply_async(load_element, 
                                 args=(etree.tostring(element), element.tag), 
                                 callback = add_elements_callback)
                close_element(element)
        #wait for all threads to stop
        pool.close()
        pool.join()
        
    #using only main thread to parse file
    else:
        #use parser object to parse file
        everything = parse_file(filename)
    
    print("Finished parsing")
    
    if profiler.PROFILE_TIME:
        profiler.time_array.append(['waiting to finish parsing', time.time() - profiler.start_time])
        profiler.start_time = time.time()
        
    parse_historical_events(everything)
    
    if profiler.PROFILE_TIME:
        profiler.time_array.append(['parsing historical events', time.time() - profiler.start_time])
    
    if profiler.PROFILE_MEMORY:
        profiler.memory_array.append(("After parsing historical events: ", asizeof(everything)))
    
    #PRINT PROFILING INFO
    if profiler.PROFILE_TIME:
        total_time = 0
        print("\n\nTIMING INFO:")
        for e, t in profiler.time_array:
            print("Time taken for " + e + ": %.2fs" % t)
            total_time += t
        print("Total time: %.2fs" % total_time)
        
    if profiler.PROFILE_MEMORY:
        print("\n\nMEMORY INFO:")
        for i in range(0, len(profiler.memory_array)):
            difference = 0
            if (i >= 1):
                difference = profiler.memory_array[i][1] - profiler.memory_array[i-1][1]
            print(profiler.memory_array[i][0] + " : " + str(profiler.memory_array[i][1]/1024) + " KB || Difference: " + str(difference/1024) + " KB")
            
    return everything

def close_element(element):
    element.clear()                 # clean up children
    while element.getprevious() is not None:
        del element.getparent()[0]  # clean up preceding siblings
  
  
#add the elements to the everything dict
def add_elements(packed_elements, profiler, everything):
    
    #only one object can be sent in the callback
    #unpack this object
    upper_level_tag, offset, element_array, element_names = packed_elements
    packed_elements = None
    
    everything[upper_level_tag] = element_array
    everything[upper_level_tag + "_names"] = element_names
    everything[upper_level_tag + "_offset"] = offset
    
    if profiler.PROFILE_TIME:
        profiler.time_array.append([upper_level_tag, time.time() - profiler.start_time])
        profiler.start_time = time.time() #measure time until next high-level tag is finished
        
    if profiler.PROFILE_MEMORY:
        profiler.memory_array.append(("Finishing " + upper_level_tag + ": ", asizeof(everything)))

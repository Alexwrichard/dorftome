#!/usr/bin/env python3
from lxml import etree
from lxml.etree import iterparse
from attribute_getters import *
from event_processing import event_type_dispatcher
import os
import codecs
import time

from Parser_Thread import Parser_Thread
from multiprocessing import Pool

class XML_Parser:
    
    def __init__(self):
        
        self.PROFILE_MEMORY = False
        self.PROFILE_TIME = True

        try:
            from pympler.asizeof import asizeof
        except ImportError:
            self.PROFILE_MEMORY = False
            self.PROFILE_TIME = False

        self.everything = {}
    '''
    Process an XML file with invalid characters and replace them with 
    question marks.
    '''
    def handle_invalid_file(self, filename):
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
    def load_dict(self, filename):
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
        if self.PROFILE_TIME:
            self.time_array = []
            self.start_time = time.clock()
        
        if self.PROFILE_MEMORY:
            self.memory_array = []
            self.memory_array.append(("At beginning : ", asizeof(self.everything)))
        
        #set up thread pool
        self.pool = Pool()
        
        #create parser object that handles the element
        self.parser_thread = Parser_Thread()

        for _, element in etree.iterparse(filename):

            if element.tag in upper_level_tags:
                
                #call parser to process the element
                #the element must be sent as a string
                #will callback to add elements to actually add to everything dict
                self.pool.apply_async(self.parser_thread.load_element, args=(etree.tostring(element), element.tag), callback = self.add_elements)
                
                self.close_element(element)
                
        #wait for all threads to stop
        self.pool.close()
        self.pool.join()
        
        print("Finished parsing")
        
        if self.PROFILE_TIME:
            self.time_array.append(['waiting for join', time.clock() - self.start_time])
            self.start_time = time.clock()
            
        self.parse_historical_events()
        
        if self.PROFILE_TIME:
            self.time_array.append(['parsing historical events', time.clock() - self.start_time])
        
        if self.PROFILE_MEMORY:
            self.memory_array.append(("After parsing historical events: ", asizeof(self.everything)))
        
        #PRINT PROFILING INFO
        if self.PROFILE_TIME:
            total_time = 0
            print("\n\nTIMING INFO:")
            for e, t in self.time_array:
                print("Time taken for " + e + ": %.2fs" % t)
                total_time += t
            print("Total time: %.2fs" % total_time)
            
        if self.PROFILE_MEMORY:
            print("\n\nMEMORY INFO:")
            for i in range(0, len(self.memory_array)):
                difference = 0
                if (i >= 1):
                    difference = self.memory_array[i][1] - self.memory_array[i-1][1]
                print(self.memory_array[i][0] + " : " + str(self.memory_array[i][1]/1024) + " KB || Difference: " + str(difference/1024) + " KB")
                
        return self.everything

    def close_element(self, element):
        element.clear()                 # clean up children
        while element.getprevious() is not None:
            del element.getparent()[0]  # clean up preceding siblings
      
      
    #add the elements to the everything dict
    def add_elements(self, packed_elements):
        
        #only one object can be sent in the callback
        #unpack this object
        upper_level_tag, offset, element_array, element_names = packed_elements
        packed_elements = None
        
        print("Adding: " + upper_level_tag + " to everything")
        self.everything[upper_level_tag] = element_array
        self.everything[upper_level_tag + "_names"] = element_names
        self.everything[upper_level_tag + "_offset"] = offset
        
        if self.PROFILE_TIME:
            self.time_array.append([upper_level_tag, time.clock() - self.start_time])
            self.start_time = time.clock() #measure time until next high-level tag is finished
            
        if self.PROFILE_MEMORY:
            self.memory_array.append(("Finishing " + upper_level_tag + ": ", asizeof(self.everything)))
         
    def add_event_link_to_hf(self, hfid, event_id):
        get_element(hfid, 'historical_figures', self.everything)['events'].append(event_id)

    def parse_historical_events(self):
        if not 'historical_events' in self.everything:
            return
        
        hfid_set = ['hfid', 'slayer_hfid', 'group_hfid', 'group_1_hfid', 'group_2_hfid', 'woundee_hfid',
                               'wounder_hfid', 'trickster_hfid', 'cover_hfid', 'hist_fig_id', 'target_hfid', 
                               'snatcher_hfid', 'changee_hfid', 'changer_hfid', 'hist_figure_id', 'hfid_target']
                               
        for event_data in self.everything['historical_events']:
            for key in event_data.keys():
                if key in hfid_set:
                    self.add_event_link_to_hf(event_data[key], event_data['id'])


from lxml import etree

class Parser_Thread():
        
    def load_element(self, element_array, high_level_tag):
        
        #array with all processed elements
        temp_element_array = []
        
        #dict mapping element ids to names
        names_dict = {}
        
        #This "offset" is for indexing purposes. So, for example, perhaps the first historical figure in the
        #'historical_figures' section has id=5764. From there, the indices progress one-by-one. So we can
        #set 'historical_figures_offset' to 5764. So then, accessing an element is easy and efficient; we just need to do
        #everything[element_type][id - offset]
        offset = -1
        
        #print("Parsing " + high_level_tag)
        for ele_string in element_array:
            element = etree.fromstring(ele_string)
            
            if element.tag == 'historical_figure':
                element_data = self.load_hist_figure_data(element)
                try:
                    element_name = element_data['name']
                except KeyError:
                    element_name = element_data['animated_string']
            else: 
                element_data = self.load_generic_element_data(element)
                try:
                    element_name = element_data['name']
                except KeyError:
                    element_name = ""

            try:
                element_id = element_data['id']
            except KeyError:
                element_id = 0
                
            #if we haven't stored an offset yet, store the first id we see
            if offset == -1:
                    offset = element_id
                    
            temp_element_array.append(element_data)
            
            if not element_name == "":
                names_dict[element_id] = element_name
                
            element.clear()
                
        #callback to the main thread to be added to main everything array
        return (high_level_tag, offset, temp_element_array, names_dict)

    '''
    Returns an element data dictionary with the following structure:
        { 'events': [12521, 3462, 123, 733, 1324...],
          'hf_links': [ {'type':'mother', 'id':12415}, {'type':'father', 'id':1235}...],
          'entity_links' : [ {'type':'something', 'id':12415}, {'type':'somethingelse', 'id':1235}...],
        }
    '''
    def load_hist_figure_data(self, element):
        element_data = {}
        element_data['events'] = []
        element_data['hf_links'] = []
        element_data['entity_links'] = []
        
        for attribute in element:
            #should not be saved
            if attribute.tag in ['hf_skill', 'entity_former_position_link']:
                continue
                
            #These tags have tags nested within them, and there are multiple for each historical figure,
            #Here, we parse them separately and store their information in subdictionaries within lists.
            if attribute.tag in ['hf_link', 'entity_link']:
                children = attribute.getchildren()
                
                attribute_dict = {}
                attribute_dict['type'] = children[0].text
                attribute_dict['id'] = int(children[1].text)
                
                if attribute.tag == 'entity_link' and len(children) > 2:
                    attribute_dict['strength'] = int(children[2].text)
                    
                element_data[attribute.tag + 's'].append(attribute_dict)
            else: #other hf_fig attribute
            
                #attributes such as death year for hf_figs still alive
                #or some site coords
                #should not be stored to save space
                if attribute.text == "-1" or attribute.text == "-1,-1":
                    continue
                    
                #try to store attribute values as int, as they are smaller in memory
                try:
                    element_data[attribute.tag] = int(attribute.text)
                except (ValueError, TypeError):
                    element_data[attribute.tag] = attribute.text

        return element_data
         
    '''
    Returns a processed generic element
    '''
    def load_generic_element_data(self, element):
        element_data = {}
        
        #Add the element attributes to a dictionary representing the generic element
        for attribute in element.getchildren():
            
            #do not store empty attributes
            if attribute.text == "-1":
                continue
            
            if element.tag == "historical_event":
                #unimplemented events
                if attribute.tag == 'type' and attribute.text in ['add hf entity link', 'add hf site link', 'create entity position', 'creature devoured', 'hf new pet', 'item stolen', 'remove hf site link', 'remove hf entity link']:
                    continue

            #try to store attribute values as int, as they are smaller in memory
            try:
                element_data[attribute.tag] = int(attribute.text)
            except Exception:
                element_data[attribute.tag] = attribute.text

        return element_data
        
    

import time
from helpers import capitalize

class SearchBar_Worker():
    
    def __init__(self, grace_period):
        self.grace_period = grace_period
        
    def load_name_list(self, name_list):
        self.name_list = name_list
    
    #this is done so that there is a grace period
    #where the user can change their search query
    #before it is sent    
    def wait_for_timeout(self):
        time.sleep(self.grace_period)
        return None
            
    def search(self, text, num, pool_size):
        
        #determine which elements to search
        chunk_size = len(self.name_list)//pool_size
        start = chunk_size * num
        
        if num == pool_size - 1:
            end = len(self.name_list)
        else:
            end = chunk_size * (num + 1)
            
        #word_beginning_results stores results where the search substring occurs
        #at the beginning of a word boundary.
        word_beginning_results = []
        other_results = []
        for name in self.name_list[start:end]:
            substr_index = name.find(text)
            if substr_index is not -1:
                #give precedence when the user's entry matches after a space 
                #or at the beginning of the word.
                if name[substr_index - 1] == " " or substr_index == 0:
                    word_beginning_results.append(capitalize(name))
                else:
                    other_results.append(capitalize(name))
        
        word_beginning_results.sort()
        other_results.sort()
        names_found = word_beginning_results + other_results

        #TODO: These should be returned capitalized
        return names_found

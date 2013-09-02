
class SearchBar_Worker():
    
    def load_name_list(self, name_list):
        self.name_list = name_list
        
    def search(self, text, num, pool_size):
        chunk_size = len(self.name_list)//pool_size
        start = chunk_size * num
        
        if num == pool_size - 1:
            end = len(self.name_list)
        else:
            end = chunk_size * (num + 1)
            
        #print("Process " + str(num) + " is handling " + str(start) + " to " + str(end) + " out of " + str(len(self.name_list)))
        
        names = self.name_list[start:end]
        names_found = []
        for name in names:
            if text in name:
                names_found.append(name.title())
                
        return names_found
        

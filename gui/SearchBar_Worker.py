
class SearchBar_Worker():
    
    def load_name_list(self, name_list):
        self.name_list = name_list
        
    def search(self, text, num, pool_size):
        #determine which elements to search
        chunk_size = len(self.name_list)//pool_size
        start = chunk_size * num
        
        if num == pool_size - 1:
            end = len(self.name_list)
        else:
            end = chunk_size * (num + 1)
            
        names_found = []
        for name in self.name_list[start:end]:
            substr_index = name.find(text)
            if substr_index is not -1:
                names_found.append((name, substr_index))
        
        #I might rewrite this... I've been writing some haskell lately and it's
        #mixing in with my Python. Basically, give precedence when
        #the user's entry matches after a space or at the beginning of the word.
        #Within these blocks, the results are sorted automatically.
        names_found.sort(key=lambda info: 0 if (info[0][info[1] - 1] == " " or info[1] == 0) else 1)
        print(names_found)
        names_found = [i for i in map(lambda x: x[0], names_found)]

        return names_found

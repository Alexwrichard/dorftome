'''
Capitalize a string using common English convention.
'''
def capitalize(string):
    words = string.split(' ')
    for i in range(len(words)):
        if words[i] not in ['the', 'a', 'of'] or i == 0:
            words[i] = words[i].capitalize()
    
    return ' '.join(words)

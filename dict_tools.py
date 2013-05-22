#!/usr/bin/env python
# Requires 2.7+



def dedict(adict, new_key): 
    """ Takes a nested dict structure and turns it into a list of dicts, 
        merging the old highest-level keys into the lower dicts. 
    """
    lst = []
    for k,v in adict.items(): 
        v[new_key] = k
        lst.append(v)
    return lst

def filter_dict(old_dict, keep_keys): 
    """ Make a new dict out of an old dict, removing all but the wanted information. 
    """
    return {k:v for k,v in old_dict.items() if k in keep_keys}


def dictby(dicts, usekey):
    """ Reforges a list of dicts into a dict of dicts, keyed by the value of 'usekey':
        [{'End Date': 'c', 'Start Date': 'b', 'Event': 'a'}
         {'End Date': 'f', 'Start Date': 'e', 'Event': 'd'}
         {'End Date': 'i', 'Start Date': 'h', 'Event': 'g'}] -> 
        {'a': {'End Date': 'c', 'Start Date': 'b'}, 
         'd': {'End Date': 'f', 'Start Date': 'e'}, 
         'g': {'End Date': 'i', 'Start Date': 'h'}} """
    return {adict[usekey]: {k:adict[k] for k in adict if k is not usekey} for adict in dicts}




""" You have a dict but want to map its 'names' to a different set of names,
    without changing the values. 
""" 
def rekey(to_rekey, newmap): 
    """ Where newmap is a dict itself, from old values to new values, or
        a function.
        Keys in to_rekey with no correlate in the map will be preserved. 
    """
    if issubclass(type(newmap), dict): 
        return {(newmap[k] if k in newmap else k):v for k,v in to_rekey.items()}
    else: 
        return {newmap(k):v for k,v in to_rekey.items()}

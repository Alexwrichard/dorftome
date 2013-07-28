#!/usr/bin/env python3
from attribute_getters import *

def event_type_dispatcher(event_id, everything):
    #Probably could have avoided this with string replacing and reflection magic,
    #but I kind of like them all to be right here for reference. This dictionary 
    #maps strings to function names.
    types = { 'add hf entity link' : add_hf_entity_link,
              'add hf hf link' : add_hf_hf_link,
              'add hf site link' : add_hf_site_link,
              'artifact created' : artifact_created,
              'attacked site' : attacked_site,
              'body abused' : body_abused,
              'change hf job' : change_hf_job,
              'change hf state' : change_hf_state,
              'changed creature type' : changed_creature_type,
              'create entity position' : create_entity_position,
              'created site' : created_site,
              'created structure' : created_structure,
              'created world construction' : created_world_construction,
              'creature devoured' : creature_devoured,
              'destroyed site' : destroyed_site,
              'diplomat lost' : diplomat_lost,
              'entity created' : entity_created,
              'field battle' : field_battle,
              'hf abducted' : hf_abducted,
              'hf died' : hf_died,
              'hf new pet' : hf_new_pet,
              'hf razed structure' : hf_razed_structure,
              'hf reunion' : hf_reunion,
              'hf revived' : hf_revived,
              'hf simple battle event' : hf_simple_battle_event,
              'hf travel' : hf_travel,
              'hf wounded' : hf_wounded,
              'impersonate hf' : impersonate_hf,
              'item stolen' : item_stolen,
              'masterpiece arch constructed' : masterpiece_arch_constructed,
              'masterpiece arch design' : masterpiece_arch_design,
              'masterpiece engraving' : masterpiece_engraving,
              'masterpiece food' : masterpiece_food,
              'masterpiece item' : masterpiece_item,
              'masterpiece item improvement' : masterpiece_item_improvement,
              'masterpiece lost' : masterpiece_lost,
              'merchant' : merchant,
              'new site leader' : new_site_leader,
              'peace accepted' : peace_accepted,
              'peace rejected' : peace_rejected,
              'razed structure' : razed_structure,
              'reclaim site' : reclaim_site,
              'remove hf site link' : remove_hf_site_link,
              'remove hf entity link' : remove_hf_entity_link,
              'replaced structure' : replaced_structure,
              'site abandoned' : site_abandoned,
              'site died' : site_died,
              'site taken over' : site_taken_over,
    }
    event_type = get_event_type(event_id, everything)
    if event_type in types.keys():
        event_data = get_element(event_id, 'historical_events', everything)
        types[event_type](event_data, everything)

'''
Historical event occurence is measured in seconds. Here, we will convert
this to a readable date.

Will return a string that looks like:
'15th of Granite'
'2nd of Timber'
etc.
'''
def time_string(seconds):
    seconds = int(seconds)
    #There are 403200 seconds in a DF year.
    yearsec = 403200
    months = ['Granite','Slate','Felsite','Hematite','Malachite','Galena','Limestone','Sandstone','Timber','Moonstone','Opal','Obsidian']
    #33600 = seconds in a DF month (403200 / 12)
    sec_in_month = seconds % 33600
    month = months[int(seconds / 33600)]
    date = int(sec_in_month / 1200) + 1
    
    return '%s of %s' % (suffix_date(date), month)

'''
Return a properly suffix'd date.
'''
def suffix_date(date):
    if str(date)[-1] == '1':
        return str(date) + 'st'
    elif str(date)[-1] == '2':
        return str(date) + 'nd'
    elif str(date)[-1] == '3':
        return str(date) + 'rd'
    else:
        return str(date) + 'th'

# Just for the record, I created the skeleton for the rest of this file in about 2 minutes
# using Vim's q-recording feature, the dictionary above, and about 40 keystrokes.

# Yeah. Vim is that great.

def add_hf_entity_link(data, everything):
    pass

def add_hf_hf_link(data, everything):
    pass

def add_hf_site_link(data, everything):
    pass

def artifact_created(data, everything):
    pass

def attacked_site(data, everything):
    pass

def body_abused(data, everything):
    pass

def change_hf_job(data, everything):
    pass

def change_hf_state(data, everything):
    pass

def changed_creature_type(data, everything):
    print(get_hf_name(data['changer_hfid'], everything) + ' transformed ' + 
          get_hf_name(data['changee_hfid'], everything) + ' from a ' + data['old_caste'] + 
          ' ' + data['old_race'] + ' to a ' + data['new_caste'] + ' ' +
          data['new_race'] + ' on the ' + time_string(data['seconds72']) + ', ' + 
          data['year'] + '.')

def create_entity_position(data, everything):
    pass

def created_site(data, everything):
    pass

def created_structure(data, everything):
    pass

def created_world_construction(data, everything):
    pass

def creature_devoured(data, everything):
    pass

def destroyed_site(data, everything):
    pass

def diplomat_lost(data, everything):
    pass

def entity_created(data, everything):
    pass

def field_battle(data, everything):
    pass

def hf_abducted(data, everything):
    pass

def hf_died(data, everything):
    pass

def hf_new_pet(data, everything):
    pass

def hf_razed_structure(data, everything):
    pass

def hf_reunion(data, everything):
    pass

def hf_revived(data, everything):
    pass

def hf_simple_battle_event(data, everything):
    pass

def hf_travel(data, everything):
    pass

def hf_wounded(data, everything):
    pass

def impersonate_hf(data, everything):
    pass

def item_stolen(data, everything):
    pass

def masterpiece_arch_constructed(data, everything):
    pass

def masterpiece_arch_design(data, everything):
    pass

def masterpiece_engraving(data, everything):
    pass

def masterpiece_food(data, everything):
    pass

def masterpiece_item(data, everything):
    pass

def masterpiece_item_improvement(data, everything):
    pass

def masterpiece_lost(data, everything):
    pass

def merchant(data, everything):
    pass

def new_site_leader(data, everything):
    pass

def peace_accepted(data, everything):
    pass

def peace_rejected(data, everything):
    pass

def razed_structure(data, everything):
    pass

def reclaim_site(data, everything):
    pass

def remove_hf_site_link(data, everything):
    pass

def remove_hf_entity_link(data, everything):
    pass

def replaced_structure(data, everything):
    pass

def site_abandoned(data, everything):
    pass

def site_died(data, everything):
    pass

def site_taken_over(data, everything):
    pass

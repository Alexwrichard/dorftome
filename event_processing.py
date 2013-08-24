#!/usr/bin/env python3
from attribute_getters import *
from link_creator import *

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
        #This might look confusing, but it's just a function call to 
        #whatever function matches up in the above dictionary.
        return date_string(event_data) + " " + types[event_type](event_data, everything)



'''
Format the year and date to be consistent
'''
def date_string(data):
    output = ""
    if 'year' not in data.keys() or data['year'] < 0:
        output += "At the beginning of the world,"
    else:
        output += "In " + str(data['year']) + ","
        if 'seconds72' in data.keys():
            output += " " + time_string(data['seconds72']) + ","
        
    return output

'''
Historical event occurence is measured in seconds. Here, we will convert
this to a readable date.

Will return a string that looks like:
'15th of Granite'
'2nd of Timber'
etc.
'''
def time_string(seconds):
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

#========>--EVENTS--<==========

def add_hf_entity_link(data, everything):
    #NOT IMPLEMENTED
    return "" + str(data)

def add_hf_hf_link(data, everything):
    #TODO: lookup proper relationship
    return(create_hf_link(data['hfid'], everything) + " married/worshipped/imprisoned " + create_hf_link(data['hfid_target'], everything))

def add_hf_site_link(data, everything):
    #NOT IMPLEMENTED
    return "" + str(data)

def artifact_created(data, everything):
    return "" + str(data)

def attacked_site(data, everything):
    return "" + str(data)

def body_abused(data, everything):
    return "" + str(data)

def change_hf_job(data, everything):
    return(create_hf_link(data['hfid'], everything) + " changed their job " + 
            create_site_link(data, everything))

def change_hf_state(data, everything):
    return(create_hf_link(data['hfid'], everything) + " started " + data['state'] + 
            " " +  create_site_link(data, everything))


def changed_creature_type(data, everything):
    return(create_hf_link(data['changer_hfid'], everything) + ' transformed ' + 
          create_hf_link(data['changee_hfid'], everything) + ' from a ' + str(data['old_caste']) + 
          ' ' + str(data['old_race']) + ' to a ' + str(data['new_caste']) + ' ' +
          data['new_race'])

def create_entity_position(data, everything):
    return "" + str(data)

def created_site(data, everything):
    return "" + str(data)

def created_structure(data, everything):
    return "" + str(data)

def created_world_construction(data, everything):
    return "" + str(data)

def creature_devoured(data, everything):
    return "" + str(data)

def destroyed_site(data, everything):
    return "" + str(data)

def diplomat_lost(data, everything):
    return "" + str(data)

def entity_created(data, everything):
    return "" + str(data)

def field_battle(data, everything):
    return "" + str(data)

def hf_abducted(data, everything):
    return create_hf_link(data['snatcher_hfid'], everything) + " abducted " + create_hf_link(data['target_hfid'], everything)+ " " + create_site_link(data, everything)

def hf_died(data, everything):
    #TODO: get proper cause of death
    if 'slayer_hfid' not in data.keys():
        create_hf_link(data['hfid'], everything) + " died of old age " + create_site_link(data, everything)
        return
    return create_hf_link(data['slayer_hfid'], everything) + " " + data['cause'] + " " + create_hf_link(data['hfid'], everything) + " " + create_site_link(data, everything)

def hf_new_pet(data, everything):
    return "" + str(data)

def hf_razed_structure(data, everything):
    return "" + str(data)

def hf_reunion(data, everything):
    return "" + str(data)

def hf_revived(data, everything):
    return "" + str(data)

def hf_simple_battle_event(data, everything):
    return(create_hf_link(data['group_1_hfid'], everything) + " " + 
            grammarify_battle_verb(data['subtype']) + " " + 
            create_hf_link(data['group_2_hfid'], everything) + " " + 
            create_site_link(data, everything))

def hf_travel(data, everything):
    return "" + str(data)

def hf_wounded(data, everything):
        return create_hf_link(data['wounder_hfid'], everything) + " wounded " + create_hf_link(data['woundee_hfid'], everything)+ " " + create_site_link(data, everything)

def impersonate_hf(data, everything):
    return "" + str(data)

def item_stolen(data, everything):
    return "" + str(data)

def masterpiece_arch_constructed(data, everything):
    return "" + str(data)

def masterpiece_arch_design(data, everything):
    return "" + str(data)

def masterpiece_engraving(data, everything):
    return "" + str(data)

def masterpiece_food(data, everything):
    return "" + str(data)

def masterpiece_item(data, everything):
    return "" + str(data)

def masterpiece_item_improvement(data, everything):
    return "" + str(data)

def masterpiece_lost(data, everything):
    return "" + str(data)

def merchant(data, everything):
    return "" + str(data)

def new_site_leader(data, everything):
    return "" + str(data)

def peace_accepted(data, everything):
    return "" + str(data)

def peace_rejected(data, everything):
    return "" + str(data)

def razed_structure(data, everything):
    return "" + str(data)

def reclaim_site(data, everything):
    return "" + str(data)

def remove_hf_site_link(data, everything):
    return "" + str(data)

def remove_hf_entity_link(data, everything):
    return "" + str(data)

def replaced_structure(data, everything):
    return "" + str(data)

def site_abandoned(data, everything):
    return "" + str(data)

def site_died(data, everything):
    return "" + str(data)

def site_taken_over(data, everything):
    return "" + str(data)

#====>--HELPERS--<==== 

'''
Takes a hf simple battle subtype (e.g. "scuffle") and returns
a string like "scuffled with".
'''
def grammarify_battle_verb(subtype):
    corrected = {
                 "scuffle" : "scuffled with",
                 "attacked" : "attacked",
                 #I honestly don't know what some of these things are supposed to mean.
                 "2 lost after receiving wounds" : "retreated after receiving wounds from",
                 "ambushed" : "ambushed",
                 "happen upon" : "happened upon",
                 "confront" : "confronted",
                 }
    return corrected[subtype]

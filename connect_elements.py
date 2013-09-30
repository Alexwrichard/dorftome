from attribute_getters import *

def add_event_link_to_hf(hfid, event_id, everything):
        get_element(hfid, 'historical_figures', everything)['events'].append(event_id)
        
def add_event_link_to_site(event, event_id, everything):
        try:
            #add event based on site_id
            get_element(event['site_id'], 'sites', everything)['events'].append(event_id)
        except KeyError:
            #must use coords instead
            site_data = get_site_data(event['coords'], everything)

def parse_historical_events(everything):
    if not 'historical_events' in everything:
        return

    hfid_set = ['hfid', 'slayer_hfid', 'group_hfid', 'group_1_hfid', 'group_2_hfid', 'woundee_hfid',
                           'wounder_hfid', 'trickster_hfid', 'cover_hfid', 'hist_fig_id', 'target_hfid', 
                           'snatcher_hfid', 'changee_hfid', 'changer_hfid', 'hist_figure_id', 'hfid_target']
    siteid_set = ['site_id', 'coords']
    
    for event_data in everything['historical_events']:
        #We store None for unimplemented events
        #such as creature devoured
        if event_data == None:
            continue
            
        for key in event_data.keys():
            if key in hfid_set:
                add_event_link_to_hf(event_data[key], event_data['id'], everything)
            elif key in siteid_set:
                add_event_link_to_site(event_data, event_data['id'], everything)
                break

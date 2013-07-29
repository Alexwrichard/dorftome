#!/usr/bin/env python3
from attribute_getters import *
import itertools

def recursive_build_tree(hf_data, children, everything, depth):
    max_depth = 2
    hf_links = hf_data['hf_links']
    for hf_link in hf_links:    
        if (hf_link['link_type'] == 'child') and (depth < max_depth):
            child_hf = get_element(hf_link['hfid'], 'historical_figures', everything)
            children.append(recursive_build_tree(child_hf, [], everything, depth + 1))

    if children == []:
        return (int(hf_data['id']), None)

    return (int(hf_data['id']), children)

'''
hf_data is a list of dictionaries, each of which contain data for an hf link.
'''
def build_tree_from_hf(hf_data, everything):
    hf_links = hf_data['hf_links']
    for hf_link in hf_links:
        if hf_link['link_type'] in ['father', 'mother']:
            print('stepping back...')
            build_tree_from_hf(get_element(hf_link['hfid'], 'historical_figures', everything), everything)
            return
    print(hf_data['id'])
    tree = recursive_build_tree(hf_data, [], everything, 0)
    print(display_tree(tree, 0))

'''
These two are helpers for the tree display function.
'''
def block_width(block):
    try:
        return block.index('\n')
    except ValueError:
        return len(block)

def stack_str_blocks(blocks):
    builder = []
    block_lens = [block_width(bl) for bl in blocks]
    split_blocks = [bl.split('\n') for bl in blocks]

    for line_list in itertools.zip_longest(*split_blocks, fillvalue=None):
        for i, line in enumerate(line_list):
            if line is None:
                builder.append(' ' * block_lens[i])
            else:
                builder.append(line)
            if i != len(line_list) - 1:
                builder.append(' ')
        builder.append('\n')

    return ''.join(builder[:-1])

'''
This works as it should, but the tree is too wide for any sane terminal window. Not much I can do about that.
You can take down the depth limit, but then you'll have a boring tree.

stolen from http://stackoverflow.com/questions/15675261/displaying-a-tree-in-ascii
'''
def display_tree(tree, depth):
    max_depth = 1
    tree = (str(tree[0]), tree[1])
    if(tree[1] is None) or depth > max_depth: 
        return tree[0]
    child_strs = [display_tree(child, depth + 1) for child in tree[1]]
    child_widths = [block_width(s) for s in child_strs]

    display_width = max(len(tree[0]), sum(child_widths) + len(child_widths) - 1)
    
    child_midpoints = []
    child_end = 0

    for width in child_widths:
        child_midpoints.append(child_end + (width // 2))
        child_end += width + 1

    brace_builder = []
    for i in range(display_width):
        if i < child_midpoints[0] or i > child_midpoints[-1]:
            brace_builder.append(' ')
        elif i in child_midpoints:
            brace_builder.append('+')
        else:
            brace_builder.append('-')

    brace = ''.join(brace_builder)
    
    name_str = '{:^{}}'.format(tree[0], display_width)
    below = stack_str_blocks(child_strs)

    return name_str + '\n' + brace + '\n' + below

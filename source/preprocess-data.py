#!/usr/bin/env python

''' The script prepares data to a more suitable format and

and save the data in a CSV format.

'''

import sys
import os
import pandas as pd


def convert_color_to_code(color):
    colors_dict = {'green': '#458B00',
                    'yellow': 'FFFF00',
                    'red': 'FF0000',
                    'blue': '0000FF',
                    'cyan': '7FFFD4',
                    'orange': 'FF8C00',
                    'far-red': 'FF0000',
                    'violet': '#A020F0',
                }

    if type(color) == type('color'):
        color = color.lower()
    else:
        return '#FFFFFF'

    if color not in colors_dict:
        return '#FFFFFF'
    else:
        return colors_dict[color]


datafile = 'FPD-Non-Redundant-20Oct2014.csv' # data file in csv format
df = pd.read_csv(os.path.join('data', datafile)
        , delimiter='\t', index_col='FPID')  # read data into a dataframe

''' Preprocess excitations and emissions '''

excitation = df.ix[:, 11].apply(str)
excitation_new = excitation.str.extract(r'(?P<excitation_new>\d+)')
excitation_alt = excitation.str.extract(r'\((?P<excitation_alt>\d+)\)')

emission = df.ix[:, 12].apply(str)
emission_new = emission.str.extract(r'(?P<emission_new>\d+)')
emission_alt = emission.str.extract(r'\((?P<emission_alt>\d+)\)')

new_df = pd.concat([df, excitation_new, excitation_alt,
                    emission_new, emission_alt], axis=1)

''' Preprocess emission colors '''
emission_colors = new_df['Emission Color Class']
emission_colors_new = \
        emission_colors.str.extract(r'(?P<emission_color_new>\w+\s)')
emission_colors_new[emission_colors_new.map(pd.isnull)] = \
                        new_df['Emission Color Class']
emission_colors_new = \
        emission_colors_new.map(convert_color_to_code)
emission_colors_alt = \
        emission_colors.str.extract(r'\((?P<emission_color_alt>\w+)\)')
emission_colors_alt = \
        emission_colors_alt.map(convert_color_to_code)

new_df = pd.concat([new_df, emission_colors_new,
                        emission_colors_alt], axis=1)

''' Preprocess excitation colors '''
excitation_colors = new_df['Excitation Color Class']
excitation_colors_new = \
        excitation_colors.str.extract(r'(?P<excitation_color_new>\w+\s)')
excitation_colors_new[excitation_colors_new.map(pd.isnull)] = \
                        new_df['Excitation Color Class']
excitation_colors_new = \
        excitation_colors_new.map(convert_color_to_code)
excitation_colors_alt = \
        excitation_colors.str.extract(r'\((?P<excitation_color_alt>\w+)\)')
excitation_colors_alt = \
        excitation_colors_alt.map(convert_color_to_code)

new_df = pd.concat([new_df, excitation_colors_new,
                        excitation_colors_alt], axis=1)

''' Write new data to CSV file '''
op = open(os.path.join('data',
        'FPD-non-redundant-processed.csv'), 'w')
op.write(new_df.to_csv(sep='\t'))
op.close()

''' Testing '''
# print(excitation_new.tail())
# print(excitation_alt.tail())

# print('=='*25)
# print(emission_new.tail())
# print(emission_alt.tail())

# print(new_df.head()[['Emission Color Class', 'color_new', 'color_alt']])
# print(new_df.tail()[['Emission Color Class', 'color_new', 'color_alt']])
# print(colors_new.head())
# print(type(colors_new.head()))

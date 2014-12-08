#!/usr/bin/env python

''' The script prepares data to a more suitable format and

and save the data in a CSV format.

'''

import sys
import pandas as pd
import os

def main():
    '''Main function'''

    datafile = 'FPD-Non-Redundant-20Oct2014.csv' # data file in csv format
    df = pd.read_csv(os.path.join('data', datafile)
            , delimiter='\t')  # read data into a dataframe

    ''' Preprocess excitations and emissions '''
    excitation = df.ix[:, 11].apply(str)
    excitation_new = excitation.str.extract(r'(?P<excitation_new>\d+)')
    excitation_alt = excitation.str.extract(r'\((?P<excitation_alt>\d+)\)')

    emission = df.ix[:, 12].apply(str)
    emission_new = emission.str.extract(r'(?P<emission_new>\d+)')
    emission_alt = emission.str.extract(r'\((?P<emission_alt>\d+)\)')

    new_df = pd.concat([df, excitation_new, excitation_alt,
                        emission_new, emission_alt], axis=1)

    del new_df[new_df.columns[11]]  # remove old excitations
    del new_df[new_df.columns[12]]  # remove old emissions

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


if __name__=='__main__':
    main()


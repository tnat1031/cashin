'''
script to clean up data I copy and paste into excel
'''

import pandas as pd
import sys
import argparse as ap
import os



def build_parser():
	''' build and return the argument parser '''
	parser = ap.ArgumentParser(description=__doc__, formatter_class=ap.ArgumentDefaultsHelpFormatter)
	parser.add_argument('infile', help='file to process', type=str, default=None)
	parser.add_argument('--year', help='what year do the stats correspond to', type=int, default=None)

	return parser


if __name__ == '__main__':
	parser = build_parser()
	args = parser.parse_args(sys.argv[1:])

	infile = args.infile
	year = args.year

	d = pd.read_table(infile)

	# make columns lower-case and replace parens
	d.columns = [x.lower().replace('(', '').replace(')', '') for x in d.columns.tolist()]

	# extract position from player name
	d['position'] = pd.Series([x[-1] for x in d.player.str.split(' ')], index=d.index)

	# extract team from player name
	d['team'] = pd.Series([x[-2] for x in d.player.str.split(' ')], index=d.index)

	# extract player name from player
	d['player'] = pd.Series([' '.join(x[:-2]) for x in d.player.str.split(' ')], index=d.index)

	# turn salary bck into float
	d['salary'] = pd.Series([float(x) for x in d.salary.str.replace('$', '')], index=d.index)

	# add year if provided
	if year:
		d['year'] = pd.Series([year]*len(d), index=d.index)

	fname = os.path.splitext(infile)[0] + '_clean.txt'

	d.to_csv(fname, index=False, sep='\t')

'''
script to get data using the myfantasyleague api

api only provides salary info for current year

# get ytd stats across all players
http://football8.myfantasyleague.com/2013/export?TYPE=playerScores&L=47256&JSON=1&W=YTD

# get weekly average scoring
http://football3.myfantasyleague.com/2013/export?TYPE=playerScores&L=47256&JSON=1&W=AVG

this API sucks, I'm just gonna copy and paste stat table from their website

'''

import pandas as pd
import argparse as ap
import json
import urllib2
import sys

def build_parser():
	''' build and return the argument parser '''
	parser = ap.ArgumentParser(description=__doc__, formatter_class=ap.ArgumentDefaultsHelpFormatter)
	parser.add_argument('year', help='what year to pull data for', type=int, default=None)
	parser.add_argument('--league_id', help='your league id', type=int, default=47256)

	return parser


def get_players(year, league_id):
	''' return a dataframe of players and their ids '''
	url = 'http://football3.myfantasyleague.com/{0}/export?TYPE=players&L={1}&W=&JSON=1'.format(str(year), str(league_id))
	data = json.loads(urllib2.urlopen(url).read())
	return pd.DataFrame(data['players']['player'])


def get_rosters(year, league_id):
	''' return a dataframe of players and their ids '''
	url = 'http://football2.myfantasyleague.com/{0}/export?TYPE=rosters&L={1}&JSON=1'.format(str(year), str(league_id))
	data = json.loads(urllib2.urlopen(url).read())
	return pd.concat([pd.DataFrame(x['player']) for x in data['rosters']['franchise']])


def get_ytd_stats(year, league):
	''' return a data frame with player stats for the given year '''
	url = 'http://football8.myfantasyleague.com/{0}/export?TYPE=playerScores&L={1}&JSON=1&W=YTD'.format(str(year), str(league_id))
	data = json.loads(urllib2.urlopen(url).read())
	return pd.concat([pd.DataFrame(x['player']) for x in data['rosters']['franchise']])


if __name__ == '__main__':
	parser = build_parser()
	args = parser.parse_args(sys.argv[1:])


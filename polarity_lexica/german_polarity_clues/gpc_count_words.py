# This should read the input and dump
# 1) A file with all the unique strings
# 2) A file with all the unique (string, POS) pairs
#
# Of course, in the case of this datset, both files will have the same size.
# The goal of using this format is compatibility (and comparability) with
# the output of the other tools.
#
# Both files should be sorted. The goal is to be able to compare the output
# of this with the output of similar scripts for other datsets.
#
# This will work for the German Polarity Clues version 0.1 (March 2011). It
# will also work for the German Senti Spin that comes bundled with that.
#

import argparse
import csv

def main(args):
	words, descriptions = parse_german_polarity_clues(args.in_file)

	with open(args.out_file, 'w', encoding='utf-8') as f:
		for i in words.keys():
			row = [i]

			if args.include_pos:
				row.append(get_pos(words[i]))

			if args.include_polarity:
				row.append(get_polarity(words[i]))

			f.write(','.join(row) + '\n')

	#with open('gpc_string_and_pos.txt', 'w', encoding='utf-8') as f:
	#	for i in words.keys():
	#		string = i
	#		pos = get_pos(words[i])
	#		f.write(string + ',' + pos + '\n')

def get_polarity(description):
	positivity = float(description[6]) if description[6] != '-' else None
	negativity = float(description[7]) if description[7] != '-' else None

	polarity = '-'
	if (positivity is not None and negativity is not None):
		polarity = positivity - negativity

	return str(polarity)

def get_pos(description):
	pos = description[2]
	if pos in ['ADJA', 'ADJD']:
		# This is for compatibility with SentiWS
		pos = 'ADJX'
	return pos

def parse_german_polarity_clues(in_file):
	words = {}
	descriptions = []
	with open(args.in_file, 'r', encoding='utf-8') as f:
		csv_reader = csv.reader(f, delimiter='\t', quotechar=None)
		for row in csv_reader:
			parse_row(row, words, descriptions)
	return words, descriptions

def parse_row(row, words, descriptions):
	word, lemma, pos, is_positive, is_negative, is_neutral, \
			positivity, negativity, neutrality = row

	descriptions.append(tuple(row))
	words[word] = descriptions[-1]


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('in_file', metavar='in_file', type=str,
			help='The file whose words are to be counted')
	parser.add_argument('out_file', metavar='out_file', type=str,
			help='The file whose words are to be counted')
	parser.add_argument("--include_pos", action="store_true", default=False)
	parser.add_argument("--include_polarity", action="store_true", default=False)
	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()
	main(args)


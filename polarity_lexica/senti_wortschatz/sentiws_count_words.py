# This should read the input file and dump
# 1) A file with all the unique strings
# 2) A file with all the unique (string, POS) pairs
#
# Both files should be sorted. The goal is to be able to compare the output
# of this with the output of similar scripts for other datsets.
#
# The expected input file is the result of concatenating both the Positive
# and the Negative files:
# $ cat SentiWS_v1.8c_Negative.txt SentiWS_v1.8c_Positive.txt > in_file.txt
#

import argparse
import csv

def main(args):
	words, descriptions = parse_sentiws(args.in_file)

	# Dumps the output
	#with open('sentiws_strings.txt', 'w', encoding='utf-8') as f:
	#	for i in words.keys():
	#		f.write(i + '\n')

	with open(args.out_file, 'w', encoding='utf-8') as f:
		for i in words.keys():
			for j in words[i]:
				row = [i]

				if args.include_pos:
					row.append(get_pos(descriptions[j]))

				if args.include_polarity:
					row.append(get_polarity(descriptions[j]))

				f.write(','.join(row) + '\n')

def get_polarity(description):
	return description[2]

def get_pos(description):
	return description[1]

def parse_sentiws(in_file):
	words = {}
	descriptions = []
	with open(args.in_file, 'r', encoding='utf-8') as f:
		csv_reader = csv.reader(f, delimiter='\t')
		for row in csv_reader:
			parse_row(row, words, descriptions)
	return words, descriptions


def parse_row(row, words, descriptions):
	word, pos = row[0].split('|')
	polarity = row[1]

	inflections = []
	if len(row) == 3:
		inflections = row[2].split(',')
	inflections.append(word)

	descriptions.append((word, pos, polarity, inflections))

	for i in inflections:
		if i in words:
			words[i].append(len(descriptions)-1)
		else:
			words[i] = [len(descriptions)-1]


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


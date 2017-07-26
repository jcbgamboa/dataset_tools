import argparse
import csv

import senti_wortschatz.sentiws_count_words
import german_polarity_clues.gpc_count_words

def main(args):
	file1 = read_file(args.file1)
	file2 = read_file(args.file2)

	intersection = [val for val in file1 if val in file2]
	with open('intersection.txt', 'w', encoding='utf-8') as f:
		for i in intersection:
			f.write(str(i) + '\n')

def read_file(file_name):
	ret = []
	with open(file_name, 'r', encoding='utf-8') as f:
		csv_reader = csv.reader(f, delimiter=',', quotechar=None)
		for row in csv_reader:
			ret.append(row)
	return ret

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('file1', metavar='file1', type=str,
			help='First input file.')
	parser.add_argument('file2', metavar='file2', type=str,
			help='Second input file.')
	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()
	main(args)


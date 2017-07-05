import sys
import argparse

from collections import Counter

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('in_file', metavar='in_file', type=str,
			    help='The file whose words are to be counted')
	parser.add_argument('--min_count', type=int, default=1,
			    help='If defined, only words that appear at least' +
				' `min_count` times in `in_file` will be ' +
				'considered.')
	return parser.parse_args()

def main():
	args = parse_args()

	all_words = []
	with open(args.in_file, 'r') as f:
		#print("will read file")
		lines = f.readlines()
		for i in lines:
			curr_line = i.strip()
			curr_line = curr_line.split(' ')
			all_words += curr_line

	#print("Removing repeated words")
	#print(all_words)

	unique_words = Counter(all_words)
	for word in unique_words:
		if unique_words[word] >= args.min_count:
			print(str(word))

if __name__ == "__main__":
	main()


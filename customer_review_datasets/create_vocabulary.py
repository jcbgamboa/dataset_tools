import sys
import argparse

from itertools import islice
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

	batch_size = 8192
	unique_words = Counter()
	with open(args.in_file, 'r') as f:
		while True:
			next_n_lines = list(islice(f, batch_size))
			if not next_n_lines:
				break

			for i in next_n_lines:
				curr_line = i.strip()
				curr_line = curr_line.split(' ')
				for j in curr_line:
					unique_words[j] += 1

	#print("Removing repeated words")
	#print(all_words)

	for word in unique_words.most_common():
		if word[1] >= args.min_count:
			print(str(word[0]))

if __name__ == "__main__":
	main()

# Command line to just count words in a file:
#
# Taken from:
# https://unix.stackexchange.com/questions/39039/get-text-file-word-occurrence-count-of-all-words-print-output-sorted
#
# cat $1 | tr '[:space:]' '[\n*]' | grep -v "^\s*$" | sort | uniq -c | sort -bnr
#

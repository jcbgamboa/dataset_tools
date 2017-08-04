from itertools import islice
import json

import argparse
import re

import spacy

# Code taken from
# http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
def find_ngrams(input_list, n):
	return zip(*[input_list[i:] for i in range(n)])


def generate_n_grams(review_text, out_src, out_tgt, nlp,
			n_min, n_max, capitalize):
	doc = nlp(review_text)
	doc_sentences = (doc.sents)

	sentences = []
	for i in doc_sentences:
		s = re.sub("'", '', i.text)
		s = re.sub('[^a-zA-Z0-9]', ' ', s)
		s = re.sub('\s+', ' ', s).strip()

		if (capitalize == 'lowercase'):
			s = s.lower()
		elif (capitalize == 'title'):
			s = s.title()

		sentences.append(s)

	if len(sentences) == 1:
		pass

	for i in sentences:
		doc = nlp(i)
		words = list(doc)
		for j in range(n_min, n_max+1):
			n_grams_generator = find_ngrams(words, j)
			for k in n_grams_generator:
				texts = [k.text for k in k]
				out_src.write(re.sub('\s+', ' ', ' '.join(' '.join(texts))) + '\n')
				out_tgt.write(' '.join(texts) + '\n')

def run_generate_n_grams(in_file, out_file, nlp, capitalize, batch_size=8192,
			n_min=2, n_max=6):
	curr_batch = 0

	with open(in_file, 'r') as f, open(out_file + '.src', 'w') as g, \
					open(out_file + '.tgt', 'w') as h:
		while True:
			print("Parsing batch {}".format(curr_batch))
			curr_batch += 1

			next_n_lines = list(islice(f, batch_size))
			if not next_n_lines:
				break

			for line in next_n_lines:
				data = json.loads(line)
				review_text = data['reviewText']

				generate_n_grams(review_text, g, h,
						nlp, n_min, n_max,
						capitalize)

				del review_text, data
			del next_n_lines

			if curr_batch % 100 == 0:
				print("Processing batch {}".format(curr_batch))


def parse_command_line():
	parser = argparse.ArgumentParser()
	parser.add_argument("in_file", help="input file name.")
	parser.add_argument("out_file", help="input file name.")
	parser.add_argument("language", help="input language ('en' or 'de').")

	parser.add_argument("--capitalize",
		help="Change capitalization of the first letter of each " +
			"word in the n-gram. If 'lowercase', then all words in " +
			"each n-gram are lowercased; if 'title', then each word" +
			"in each n-gram has its first letter capital",
		default='none')
	return parser.parse_args()

def main():
	args = parse_command_line()

	nlp = spacy.load(args.language)
	run_generate_n_grams(args.in_file, args.out_file, nlp,
				args.capitalize)

if __name__ == '__main__':
	main()


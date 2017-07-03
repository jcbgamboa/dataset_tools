# Code for preprocessing the dataset available in
# https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
# containing annotated customer reviews (5 products).
#
# The dataset is composed of lines that look like:
# <list of aspects>##<sentence>
#
# However, it has problems. For example, sometimes, instead of "##" it
# has "#". The list of aspects also contains some tags (see dataset's
# Readme.txt file), which we ignore.
#

import sys, os, re
import argparse
import get_parse_trees

# Useful for tokenizing the sentences
import spacy

nlp = spacy.load('en')


def get_sentence_and_aspects(line):
	aspects = []

	# Some lines have only one "#" instead of two "##"
	if '##' not in line:
		line = re.sub('#', '##', line)

	aspect_information, sentence = line.split('##')

	aspects_information = aspect_information.split(',')
	for i in aspects_information:
		curr_aspect = re.sub('\[.*\]', '', i)
		aspects.append(curr_aspect)

	return sentence, aspects

def is_title(sentence):
	if '[t]' in sentence:
		return True
	return False

def is_second_word(word, aspect_doc):
	for k, i in enumerate(aspect_doc):
		if k == 0:
			continue
		if i.lemma_ == word.lemma_:
			return True
	return False

def get_ground_truth_tag(word, aspects):
	#if re.match('[%&"~;]', word):
	#	return 'O'

	print("Word: ", word)
	#word_doc = nlp(word)
	for i in aspects:
		aspect_doc = nlp(i.strip())
		print((word, aspect_doc))
		if len(aspect_doc) == 0:
			return 'O'
		elif word.lemma_ == aspect_doc[0].lemma_:
			return 'B-A'
		elif is_second_word(word, aspect_doc):
			return 'I-A'
	return 'O'

def generate_ground_truth_sequence(sentence, aspects):
	ground_truth = []

	# We simply split the sentence by "-" and " "
	#doc = re.split('[ -]', sentence)
	doc = nlp(sentence)
	for i in doc:
		if len(i) == 0:
			continue
		curr_ground_truth_tag = get_ground_truth_tag(i, aspects)
		ground_truth.append(curr_ground_truth_tag)

	return ' '.join(ground_truth)

def parse_file(f):
	file_sentences = []
	file_aspects = []
	for i in f:
		# `i` is a line from the file `f`
		if i.startswith('*') or i.startswith('\n'):
			# This is to skip the useless header in the dataset
			continue

		if is_title(i):
			# Titles don't have aspect annotation =/
			continue

		sentence, aspects = get_sentence_and_aspects(i)
		file_sentences.append(sentence)
		file_aspects.append(aspects)

	return file_aspects, file_sentences

def main(in_file, out_file, generate_parse_trees=False, use_senticnet=False):
	# Open file
	with open(in_file, 'r') as f:
		aspects, sentences = parse_file(f)

	#sentences = []
	#ground_truths = []
	sentences_file = os.path.basename(out_file) + '.in'
	ground_truths_file = os.path.basename(out_file) + '.gt'
	with open(sentences_file, 'w') as fi, open(ground_truths_file, 'w') as fo:
		for i in zip(aspects, sentences):
			aspects_list = i[0]
			sentence = i[1].strip()
			print("Sentence: ", sentence)
			curr_ground_truth = generate_ground_truth_sequence(sentence, aspects_list)
			#sentences.append(sentence)
			#ground_truths.append(curr_ground_truth)
			if generate_parse_trees:
				doc = nlp(sentence)
				print('"' + str(doc) + '"')
				parse_tree_list = get_parse_trees.parse(doc)
				sentence = ' '.join(parse_tree_list)
			fi.write(sentence + '\n')
			fo.write(curr_ground_truth + '\n')


if __name__ == "__main__":
	#in_file = sys.argv[1]
	#out_file = sys.argv[2]
	parser = argparse.ArgumentParser()
	parser.add_argument('in_file', metavar='in_file', type=str,
			    help='an integer for the accumulator')
	parser.add_argument('out_file', metavar='out_file', type=str,
			    help='an integer for the accumulator')
	parser.add_argument("--generate_parse_trees", action="store_true", default=False)
	parser.add_argument("--use_senticnet", action="store_true", default=False)
	args = parser.parse_args()

	main(args.in_file, args.out_file, args.generate_parse_trees, args.use_senticnet)

	#text = get_sentence_and_aspects("remote control[-2]##one bad thing though , i find the remote-control a bit flimsy and i predict it will most probably ' die ' before the player does .")
	#text = generate_ground_truth_sequence('The remote control is bad', ['remote control'])
	#print(text)
	#text = generate_ground_truth_sequence('The remote control is bad', ['remote-control'])
	#print(text)


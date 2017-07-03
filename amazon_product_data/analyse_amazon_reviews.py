# Counts the occurrences of certains words in the dataset available in
# http://jmcauley.ucsd.edu/data/amazon/
# containing amazon reviews.
#
# The dataset is a JSON file containing one review per line.
#
# The code iterates through all reviews, counting the occurence of
# intensifying words such as "very" or "really", as well as their
# cooccurrence with along with "positive" and "negative" words.
# To know if a word is positive or negative, the code uses the
# `sentiment_analyser` module.
#
# (currently, the `sentiment_analyser` module always returns 0, so
# the code is not specially useful; but one can use it as a
# boilerplate for defining any function.

from itertools import islice
import json

import argparse

import numpy as np
import matplotlib.pyplot as plt

import spacy

import glob
import os
import sys
sys.path.append('.')
import sentiment_analyser.sentiment_analyser as sa

output_file_name = 'statistics.json'

# List of intensifiers based on "Degree modifiers of adjectives in spoken
# British English" (Carita Paradis, 1997)
# https://lup.lub.lu.se/search/ws/files/4923802/1590143.pdf
#
# That work already presents a list of collocations between these and other
# adjectives
#
# The first element of the tuple represents the total count
statistics = {
	"n_sentences": 0,
	"n_reviews": 0,
	"n_positive_reviews": 0,
	"n_negative_reviews": 0,

	# English words
	# Maximizers
	"absolutely": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"completely": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"perfectly": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"totally": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"entirely": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"utterly": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],

	# Approximator
	"almost": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],

	# Booster
	"very": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"terribly": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"extremely": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"most": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"awfully": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"jolly": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"highly": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"frightfully": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],

	# Moderator
	"quite": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"rather": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"pretty": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"fairly": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],

	# Diminisher
	"little": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"slightly": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"somewhat": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],

	# Added by me
	"really": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"super": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"surprisingly": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],


	# German words
	"sehr" : [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"wirklich" : [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"ziemlich" : [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"absolut" : [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"extrem" : [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"komplett" : [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"total" : [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"etwas" : [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"kaum" : [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
	"zu" : [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

}

def generate_statistics(file_name, nlp, input_several_files=False, batch_size=8192):
	curr_batch = 0

	# This works for the English dataset, but doesn't work for the
	# German reviews (which are separated in files).
	if not input_several_files:
		with open(file_name, 'r') as f:
			while True:
				print("Parsing batch {}".format(curr_batch))
				curr_batch += 1

				next_n_lines = list(islice(f, batch_size))
				if not next_n_lines:
					break

				for line in next_n_lines:
					data = json.loads(line)
					review_text = data['reviewText']
					review_polarity = data['overall']
					statistics['n_reviews'] += 1
					if review_polarity in [4, 5]:
						statistics['n_positive_reviews'] += 1
					elif review_polarity in [1, 2]:
						statistics['n_negative_reviews'] += 1

					calculate_statistics(review_text, nlp,
								review_polarity)

					del review_text, review_polarity, data
				del next_n_lines

				if curr_batch % 100 == 0:
					with open(output_file_name, 'w') as fp:
						json.dump(statistics, fp)
	else:
		for i in glob.glob(os.path.join(file_name, "*.json")):
			print ("Parsing file {}".format(i))
			curr_batch += 1
			if curr_batch % 100 == 0:
				with open(output_file_name, 'w') as fp:
					json.dump(statistics, fp)

			with open(i, 'r', encoding='utf-8') as f:
				json_str = f.read()
				data = json.loads(json_str)
				for j in data:
					review_text = j['review_text']
					review_polarity = int(j['review_rating'])
					statistics['n_reviews'] += 1
					if review_polarity in [4, 5]:
						statistics['n_positive_reviews'] += 1
					elif review_polarity in [1, 2]:
						statistics['n_negative_reviews'] += 1

					calculate_statistics(review_text, nlp,
								review_polarity)

					del review_text, review_polarity

				del json_str, data

def calculate_statistics(sentence, nlp, review_polarity):
	doc = nlp(sentence)
	doc = sa.add_sentiment_hook(doc, nlp.lang, consider_modifiers=False)
	for sentence in doc.sents:
		statistics['n_sentences'] += 1
		for token in sentence:
			if token.lemma_ in statistics and \
				token.lemma_ != "n_sentences":
				get_curr_token_statistics(token, review_polarity)
	del doc


def get_left_token(token):
	if token.i == 0:
		return None

	doc = token.doc
	curr_idx = token.i
	return doc[curr_idx-1]

def get_right_token(token):
	if token.i == len(token.doc)-1:
		return None
	doc = token.doc
	curr_idx = token.i
	return doc[curr_idx+1]

def is_positive(token):
	return token.sentiment > 0

def is_negative(token):
	return token.sentiment < 0

def get_curr_token_statistics(token, review_polarity):
	polarity_index = None
	if review_polarity in [4, 5]:
		polarity_index = 1
	elif review_polarity in [1, 2]:
		polarity_index = 2

	next_token = get_right_token(token)
	if (next_token is not None):
		if is_positive(next_token):
			statistics[token.lemma_][0][0] += 1
		elif is_negative(next_token):
			statistics[token.lemma_][0][1] += 1

		if polarity_index is not None:
			if is_positive(next_token):
				statistics[token.lemma_][polarity_index][0] += 1
			elif is_negative(next_token):
				statistics[token.lemma_][polarity_index][1] += 1


	head_token = token.head
	if (head_token is not None):
		if is_positive(head_token):
			statistics[token.lemma_][0][2] += 1
		elif is_negative(head_token):
			statistics[token.lemma_][0][3] += 1

		if polarity_index is not None:
			if is_positive(head_token):
				statistics[token.lemma_][polarity_index][2] += 1
			elif is_negative(head_token):
				statistics[token.lemma_][polarity_index][3] += 1

	#print("Analysing: {}, next_token: {}, head_token: {}, in: {}\n".format(
	#	token, next_token, head_token, token.doc))

def format_data_to_plot(data, order, plot_type=0):
	pos_next = []
	neg_next = []
	pos_head = []
	neg_head = []
	for i in order:
		counts = data[i][plot_type]
		pos_next.append(counts[0])
		neg_next.append(counts[1])
		pos_head.append(counts[2])
		neg_head.append(counts[3])

	return (pos_next, neg_next, pos_head, neg_head)

def produce_graphics(data, plot_type_str='all', language='en'):
	plot_type_map = {
		'all': 0,
		'positive': 1,
		'negative': 2
	}
	plot_type = plot_type_map[plot_type_str]

	if language == 'en':
		order = ('absolutely',
			 'completely',
			 'perfectly',
			 'totally',
			 'entirely',
			 'utterly',
			 'almost',
			 'very',
			 'terribly',
			 'extremely',
			 'most',
			 'awfully',
			 'jolly',
			 'highly',
			 'frightfully',
			 'quite',
			 'rather',
			 'pretty',
			 'fairly',
			 'little',
			 'slightly',
			 'somewhat',
			 'really',
			 'super',
			 'surprisingly',
			)
		n_groups = 25
	elif language == 'de':
		order = (
			 'absolut',
			 'etwas',
			 'extrem',
			 'kaum',
			 'komplett',
			 'sehr',
			 'total',
			 'wirklich',
			 'ziemlich',
			 'zu',
			)
		n_groups = 10

	positive_next, negative_next, positive_head, negative_head = \
				format_data_to_plot(data, order, plot_type)

	# data to plot
	 
	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.2
	opacity = 0.8
	 
	rects1 = plt.bar(index, positive_next, bar_width,
			 alpha=opacity,
			 color='b',
			 label='Next word is Positive')
	 
	rects2 = plt.bar(index + bar_width, negative_next, bar_width,
			 alpha=opacity,
			 color='g',
			 label='Next word is Negative')

	rects3 = plt.bar(index + 2*bar_width, positive_head, bar_width,
			 alpha=opacity,
			 color='b',
			 label='Head is Positive')

	rects4 = plt.bar(index + 3*bar_width, negative_head, bar_width,
			 alpha=opacity,
			 color='y',
			 label='Head is Negative')
	 
	plt.xlabel('Intensifier')
	plt.ylabel('Count')
	plt.xticks(index + bar_width, order, rotation=70)
	plt.legend()
	plt.tight_layout()

	
	plt.title('Coocurrences with Intensifiers in ' + plot_type_str + ' reviews')

	#plt.show()
	plt.savefig('plotted_results_{}.pdf'.format(plot_type_str),
			format='pdf')

def parse_command_line():
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help="input file name.")
	parser.add_argument("language", help="input language ('en' or 'de').")
	parser.add_argument("--only_plot",
		help="If false, then `input` contains the dataset. The " +
			"statistics will be calculated and stored in " +
			"`statistics.json`. Additionally, a plot of the " +
			"counts will be stored in `plotted_results.pdf`. "+
			"If true, then the input contains " +
			"the file with values already counted. In that case, " +
			"only `plotted_results.pdf` will be created. ",
		default=False, action="store_true")
	parser.add_argument("--input_several_files",
		help="If true, then the input is a folder and the program " +
			" will read all files in the folder.",
		default=False, action="store_true")

	return parser.parse_args()

def main():
	args = parse_command_line()

	global statistics
	if not args.only_plot:
		print("Loading spacy...")
		nlp = spacy.load(args.language)
		print("Parsing file...")
		generate_statistics(args.input, nlp, args.input_several_files)

		with open(output_file_name, 'w') as fp:
			json.dump(statistics, fp)
	else:
		with open(args.input, 'r') as fp:
			statistics = json.load(fp)

	produce_graphics(statistics, 'all', language=args.language)
	produce_graphics(statistics, 'positive', language=args.language)
	produce_graphics(statistics, 'negative', language=args.language)

if __name__ == '__main__':
	main()


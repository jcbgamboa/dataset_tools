import argparse
import json

intensifiers = [
	# English
	'absolutely',
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

	# German
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
	]

def parse_command_line():
	parser = argparse.ArgumentParser()
	parser.add_argument("in_file", help="input file name.")
	parser.add_argument("out_file", help="output file name.")
	#parser.add_argument("--only_plot",
	#	help="If false, then `input` contains the dataset. The " +
	#		"only `plotted_results.pdf` will be created. ",
	#	default=False, action="store_true")
	#parser.add_argument("--input_several_files",
	#	help="If true, then the input is a folder and the program " +
	#		" will read all files in the folder.",
	#	default=False, action="store_true")

	return parser.parse_args()

def main():
	args = parse_command_line()

	statistics = {}
	with open(args.in_file, 'r') as fp:
		statistics = json.load(fp)

	n_positive_reviews = statistics['n_positive_reviews']
	n_negative_reviews = statistics['n_negative_reviews']

	if n_positive_reviews <= 0:
		print("ERROR: No positive reviews")
	if n_negative_reviews <= 0:
		print("ERROR: No negative reviews")

	for i in intensifiers:
		if not statistics.has_key(i):
			print("WARNING: {} not found in input file".format(i))
			continue

		positive_counts = statistics[i][1]
		for j in range(len(positive_counts)):
			statistics[i][1][j] /= n_positive_reviews

		negative_counts = statistics[i][2]
		for j in range(len(negative_counts)):
			statistics[i][2][j] /= n_negative_reviews

	with open(args.out_file, 'w') as fp:
		json.dump(statistics, fp)

if __name__ == "__main__":
	main()


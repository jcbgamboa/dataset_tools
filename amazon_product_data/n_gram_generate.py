


def generate_n_grams(review_text, out_file, nlp, n_min, n_max):
	pass


def run_generate_n_grams(in_file, out_file, nlp, batch_size=8192, n_min=2, n_max=6):
	curr_batch = 0

	with open(in_file, 'r') as f, open(out_file) as g:
		while True:
			print("Parsing batch {}".format(curr_batch))
			curr_batch += 1

			next_n_lines = list(islice(f, batch_size))
			if not next_n_lines:
				break

			for line in next_n_lines:
				data = json.loads(line)
				review_text = data['reviewText']

				generate_n_grams(review_text, out_file,
						nlp, n_min, n_max)

				del review_text, data
			del next_n_lines

			if curr_batch % 100 == 0:
				print("Processing batch {}".format(curr_batch))


def parse_command_line():
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help="input file name.")
	parser.add_argument("language", help="input language ('en' or 'de').")
	return parser.parse_args()

def main():
	args = parse_command_line()

	nlp = spacy.load(args.language)
	run_generate_n_grams(args.in_file, args.out_file nlp)

if __name__ == '__main__':
	main()


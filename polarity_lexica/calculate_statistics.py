import argparse
import csv

import intersect

import numpy as np
import matplotlib.pyplot as plt

def main(args):
	rows = intersect.read_file(args.infile)
	columns = list(zip(*rows))
	polarities = np.array(columns[2]).astype(np.float32)

	create_histogram(polarities, args.dataset_name, args.outfile)
	dump_mean(polarities, args.outfile)

def create_histogram(polarities, dataset_name, outfile):
	plt.hist(polarities, bins=20)

	plt.title('Histogram{}{}'.format(
		'' if dataset_name == '' else ': ',
		dataset_name))

	plt.savefig('{}.pdf'.format(outfile), format='pdf')

def dump_mean(polarities, outfile):
	with open('{}.txt'.format(outfile), 'w', encoding='utf-8') as f:
		f.write(str(polarities.mean()) + '\n')
		f.write(str(polarities.std()) + '\n')

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', metavar='infile', type=str,
			help='First input file.')
	parser.add_argument('outfile', metavar='outfile', type=str,
			help='Name of output file.')
	parser.add_argument("--dataset_name", default='', type=str)
	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()
	main(args)


import argparse
import csv

def main(args):
	infile1 = read_file(args.infile1)
	infile2 = read_file(args.infile2)

	intersection = [val for val in infile1 if val in infile2]
	with open(args.outfile, 'w', encoding='utf-8') as f:
		for i in intersection:
			f.write(','.join(i) + '\n')

def read_file(file_name):
	ret = []
	with open(file_name, 'r', encoding='utf-8') as f:
		csv_reader = csv.reader(f, delimiter=',', quotechar=None)
		for row in csv_reader:
			ret.append(row)
	return ret

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('infile1', metavar='infile1', type=str,
			help='First input file.')
	parser.add_argument('infile2', metavar='infile2', type=str,
			help='Second input file.')
	parser.add_argument('outfile', metavar='outfile', type=str,
			help='Name of output file.')
	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()
	main(args)


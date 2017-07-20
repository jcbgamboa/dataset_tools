# This should read the two files and dump
# 1) A file with all the unique strings
# 2) A file with all the unique (string, POS) pairs
#
# Both files should be ordered. The goal is to be able to compare the output
# of this with the output of similar scripts for other datsets.
#

import argparse
import sys
import csv

def main(args):
    # Reads the file
    words = {}
    descriptions = []
    with open(args.in_file, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for row in csv_reader:
            parse_row(row, words, descriptions)

    # Dumps the output
    with open('sentiws_strings.txt', 'w', encoding='utf-8') as f:
        for i in words.keys():
            f.write(i + '\n')

    with open('sentiws_string_and_pos.txt', 'w', encoding='utf-8') as f:
        for i in words.keys():
            for j in words[i]:
                string = i
                pos = descriptions[j][1]
                f.write(string + ',' + pos + '\n')



def parse_row(row, words, descriptions):
    word, pos = row[0].split('|')
    polarity = row[1]

    inflections = []
    if len(row) == 3:
        inflections = row[2].split(',')
    inflections.append(word)
    print (inflections)

    descriptions.append((word, pos, polarity, inflections))

    for i in inflections:
        if i in words:
            words[i].append(len(descriptions)-1)
        else:
            words[i] = [len(descriptions)-1]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file', metavar='in_file', type=str,
            help='The file whose words are to be counted')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)

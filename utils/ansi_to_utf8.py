import argparse
import codecs
import glob

# Totally based on
# https://stackoverflow.com/questions/191359/how-to-convert-a-file-to-utf-8-in-python

BLOCKSIZE = 1048576 # or some other, desired size in bytes

def convert_encoding(in_file, out_file, in_encoding, out_encoding):
    with codecs.open(in_file, "r", in_encoding) as sourceFile:
        with codecs.open(out_file, "w", out_encoding) as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)

def convert_ansi_to_utf8(ansi_file, utf8_file):
    convert_encoding(ansi_file, utf8_file, 'windows-1252', 'utf-8')

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('in_files', nargs='*')
    return p.parse_args()

def main(args):
    for i in args.in_files:
        convert_ansi_to_utf8(i, i + '.utf8')

if __name__ == '__main__':
    args = parse_args()
    main(args)


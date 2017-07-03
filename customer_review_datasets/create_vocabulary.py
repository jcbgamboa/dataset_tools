import sys

def main():
	in_file = sys.argv[1]

	all_words = []
	with open(in_file, 'r') as f:
		#print("will read file")
		lines = f.readlines()
		for i in lines:
			curr_line = i.strip()
			curr_line = curr_line.split(' ')
			all_words += curr_line

	#print("Removing repeated words")
	#print(all_words)

	unique_words = set(all_words)
	for word in unique_words:
		print(str(word))

if __name__ == "__main__":
	main()


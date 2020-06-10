import nltk
import csv
import urllib.request

WAR_AND_PEACE = "http://www.gutenberg.org/files/2600/2600-0.txt"
ULYSSES = "http://www.gutenberg.org/files/4300/4300-0.txt"
SHAKESPEARE = "http://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt"

def parse(text):
	print("Parsing text...")
	raw_text = urllib.request.urlopen(text).read()
	raw_text = raw_text.decode('utf-8')
	tokens = nltk.word_tokenize(raw_text)
	print(str(len(tokens)) + " tokens read.")
	return tokens

def main():
	texts = [WAR_AND_PEACE, ULYSSES, SHAKESPEARE]

	for text in texts: 
		tokens = parse(text)
		to_csv(tokens, text)

def to_csv(tokens, name):
	FILENAME = ''
	
	if name == WAR_AND_PEACE:
		FILENAME = 'war_and_peace.csv'
	elif name == ULYSSES:
		FILENAME = 'ulysses.csv'
	elif name == SHAKESPEARE:
		FILENAME = 'shakespeare.csv'

	with open(FILENAME, 'w', newline='') as csvfile:
		csvwriter=csv.writer(csvfile, delimiter = ' ') 
		for token in tokens:
			csvwriter.writerow([token])

if __name__ == '__main__':
	main()
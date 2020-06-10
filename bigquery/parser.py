import nltk

import urllib

WAR_AND_PEACE = "http://www.gutenberg.org/files/2600/2600-0.txt"

def parse(text):
	print("Parsing text...")
	raw_text = urllib.request.urlopen(text).read()
	raw_text = raw_text.decode('utf-8')
	tokens = nltk.word_tokenize(raw_text)
	print(str(len(set(tokens))) + " tokens read.")
	
	for j in sorted(list(set(tokens))):
		print(j)

	return tokens

if __name__ == '__main__':
	parse(WAR_AND_PEACE)

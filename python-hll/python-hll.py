from python_hll.hll import HLL
import mmh3
import nltk
import urllib
from tqdm import tqdm
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

WAR_AND_PEACE = "http://www.gutenberg.org/files/2600/2600-0.txt"
ULYSSES = "http://www.gutenberg.org/files/4300/4300-0.txt"
SHAKESPEARE = "http://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt"

texts = [WAR_AND_PEACE, ULYSSES, SHAKESPEARE]

LOG2M = 13 # The log-base-2 of the number of registers used in the HyperLogLog algorithm. Must be at least 4 and at most 31.
REG_WIDTH = 5 # The number of bits used per register in the HyperLogLog algorithm. Must be at least 1 and at most 8.

LOG2M_MIN = 4
LOG2M_MAX = 30
REG_WIDTH_MIN = 1
REG_WIDTH_MAX = 8

def main():
	# for text in texts:
	# 	hll = HLL(LOG2M, REG_WIDTH)
	# 	tokens = download_and_tokenize(text)
	# 	for token in tqdm(tokens):
	# 		hashed_value = mmh3.hash(token)
	# 		hll.add_raw(hashed_value)
	# 	cardinality = hll.cardinality()
	# 	print(cardinality


	tokens = download_and_tokenize(SHAKESPEARE)
	run_one_test(tokens)


def run_one_test(tokens):
	log2m_list = []
	reg_width_list = []
	cardinality_list = []
	num_trials = (LOG2M_MAX - LOG2M_MIN + 1) * (REG_WIDTH_MAX - REG_WIDTH_MIN + 1)
	trial = 1
	for log2m in range(LOG2M_MIN, LOG2M_MAX + 1):
		for reg_width in range(REG_WIDTH_MIN, REG_WIDTH_MAX + 1):
			print("Trial" + " " + str(trial) + " / " + str(num_trials))
			print(reg_width)
			hll = HLL(log2m, reg_width)
			for token in tokens:
				hashed_value = mmh3.hash(token)
				hll.add_raw(hashed_value)
			cardinality = hll.cardinality()
			log2m_list.append(log2m)
			reg_width_list.append(reg_width)
			cardinality_list.append(cardinality)
			trial += 1
	plot(log2m_list, reg_width_list, cardinality_list)


def plot(log2m_list, reg_width_list, cardinality_list):
	ax = plt.axes(projection='3d')
	log2m_list = np.array(log2m_list)
	reg_width_list = np.array(reg_width_list)
	cardinality_list = np.array(cardinality_list)
	ax.plot_trisurf(log2m_list, reg_width_list, cardinality_list, cmap=plt.cm.GnBu, shade = False)
	# ax.scatter(log2m_list, reg_width_list, cardinality_list, cmap=plt.cm.Spectral)
	ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
	ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
	ax.zaxis.set_major_locator(plt.MaxNLocator(integer=True))
	ax.set_xlabel('LOG2M')
	ax.set_ylabel('REG_WIDTH')
	ax.set_zlabel('Cardinality Estimate')
	plt.title("HLL Cardinality Estimates: Shakespeare's Plays")
	plt.show()

def download_and_tokenize(text_url):
	print("Parsing text...")
	raw_text = urllib.request.urlopen(text_url).read()
	raw_text = raw_text.decode('utf-8')
	tokens = nltk.word_tokenize(raw_text)
	print(str(len(tokens)) + " tokens read.")
	return tokens



if __name__ == '__main__':
	main()
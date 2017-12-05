
import sys
import csv
from functools import reduce

def read_data(filename, limit=1000):
	"""Yields a generator with the data
	Only consider columns for:
		'BORO'
		'ZIPCODE'
		'CUISINE DESCRIPTION'
		'INSPECTION DATE'
		'VIOLATION DESCRIPTION'
		'CRITICAL FLAG'
		'GRADE'
		'INSPECTION TYPE'
	
	We do not consider columns for:
		['CAMIS', 'DBA', 'BUILDING', 'STREET', 'PHONE', 'ACTION', 'VIOLATION CODE', 'SCORE', 'GRADE DATE', 'RECORD DATE']

	:Input:
	 - filename (string) Filename of data to read
	 - limit (int) number of rows to read

	:Output:
	 - (generator) generator of lists containing data.
	"""
	with open(filename, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=",", quotechar='"')
		i = 0
		for row in reader:
			i += 1
			if i == 1:
				continue
			elif (i > limit + 1):
				break
			if row[-4] == '' or row[-4] == 'Not Yet Graded':
				i -= 1
				continue
			yield [row[i] for i in (2,5,7,8,11,12,14,17)]

def createC1(data):
	"""Generates the first candidate set.

	:Input:
	 - data (list) A list of sets, where each set is a transaction. Candidate
	 	set will be created using this data.

	:Output:
	 - (dict) A candidate set generated from the data
	 	Key: frozenset(candidate set)
	 	Value: number of occurences in data
	"""
	C1 = {}
	for transaction in data:
		for item in transaction:
			item = frozenset([item])
			if item not in C1:
				C1[item] = 1
			else:
				C1[item] += 1
	return C1


def createL(Ck, min_sup):
	"""Creates a frequest itemset using a given candidate set Ck

	:Input:
	 - Ck (dict) The candidate set. Keys are the candidates and values are
	 	the frequency count.
	 - min_sup (float) Minimum support

	:Output:
	 - (list) list of frequent itemsets. Each item is a frozenset.
	"""
	L = []
	# Prune candidate set based on miniumum support
	for can in Ck:
		if Ck[can] >= min_sup:
			L.append(can)
	return L


def apriori_gen(data, Lk, k):
	"""Generate a new candidate set for apriori algorithm
	
	:Input:
	 - data (list)
	 - Lk (list) previous iteration's frequent itemset
	 - k (int) number of items to include in the itemset

	:Output:
	 - (dict) A candidate set generated from the data
	 	Key: frozenset(candidate set)
	 	Value: number of occurences in data
	"""
	Ck = {}
	itemset = reduce(lambda x,y: x.union(y), Lk)
	for l in Lk:
		for i in itemset - l:
			candidate = frozenset(l.union(i))
			if len(candidate) == k:
				Ck[candidate] = 0

	for candidate in Ck:
		for transaction in data:
			if candidate <= transaction:
				Ck[candidate] += 1

	return Ck

def _supp(x, data):
	# calculate the support
	support = 0
	for transaction in data:
		if x <= transaction:
			support += 1
	return support

def confidence(x, y, data):
	# calculate the confidence and support of association rule
	supp = _supp({x, y}, data)
	return supp, supp / _supp({x}, data)


def apriori(data, min_sup, min_conf, size):
	"""Creates a frequest itemset using a given candidate set Ck

	:Input:
	 - Ck (dict) The candidate set. Keys are the candidates and values are
	 	the frequency count.
	 - min_sup (float) Minimum support
	 - min_conf (float) Minimum confidence for association rules
	 - size (int) Number of data points

	:Output:
	 - (list) list of frequent itemsets. Each item is a frozenset.
	"""
	L = {}
	Ck = createC1(data)
	L[1] = createL(Ck, min_sup)
	k = 1

	while Ck and L[k]:
		Ck = apriori_gen(data, L[k], k + 1)
		L[k + 1] = createL(Ck, min_sup)
		k += 1

	# calculate association rules
	rules = []
	for l in L:
		for s in L[l]:
			print(list(s), ", %.3f" % (_supp(s, data) / size))
			for x in s:
				# calculate the association with all other elements in set
				for y in s - {x}:
					supp, conf = confidence(x, y, data)
					if conf >= min_conf:
						rules.append((x,y,conf, supp / size))
	return rules, L

if __name__ == "__main__":
	try:
		_, filename, min_sup, min_conf = sys.argv
		min_sup = float(min_sup)
		min_conf = float(min_conf)
	except Exception as e:
		print(e)
		# print("Usage:\n\tpython <filename> <min_sup> <min_conf>")
		sys.exit("Usage:\n\t./run <filename> <min_sup> <min_conf>")

	# find size of dataset. do not include row for column titles
	with open(filename) as f:
		size=sum(1 for _ in f)
	limit = size - 1

	print("==Frequent itemsets (min_sup=%.3f%%)" % (min_sup * 100))

	# Read data and execute apriori algorithm
	data = read_data(filename, limit=limit)
	data = list(map(set, data))
	rules, L = apriori(data, min_sup * limit, min_conf, size - 1)
	
	# Print the confidence for each rule
	print("==High-confidence association rules (min_conf=%.3f%%)" % (min_conf * 100))
	for rule in rules:
		print("[%s] => [%s] (Conf: %.3f, Supp: %.3f)" % rule)

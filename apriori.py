
import sys
import csv
from functools import reduce

def read_data(filename, limit=1000):
	"""
	Yields a generator with the data
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
	L = []
	for can in Ck:
		if Ck[can] >= min_sup:
			L.append(can)
	return L


def apriori_gen(data, Lk, k):
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
	support = 0
	for transaction in data:
		if x <= transaction:
			support += 1
	return support

def confidence(x, y, data):
	return _supp({x, y}, data) / _supp({x}, data)


def apriori(data, min_sup, min_conf):
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
			print(list(s), ", %.3f" % (_supp(s, data) / 395672))
			for x in s:
				for y in s - {x}:
					conf = confidence(x, y, data)
					if conf >= min_conf:
						rules.append((x,y,conf))
	return rules, L

if __name__ == "__main__":
	try:
		_, filename, min_sup, min_conf = sys.argv
		min_sup = float(min_sup)
		min_conf = float(min_conf)
	except Exception as e:
		print(e)
		print("Usage:\n\tpython <filename> <min_sup> <min_conf>")
		sys.exit('System will exit')

	# there are 395672 rows not inlcuding the title
	print("Filename:", filename)
	print("Min support:", min_sup)
	print("Min confidence:", min_conf)

	limit = 395672
	print("==Frequent itemsets (min_sup=%.2f%%)" % (min_sup * 100))
	data = read_data(filename, limit=limit)
	data = list(map(set, data))
	rules, L = apriori(data, min_sup * limit, min_conf)
	
	print("==High-confidence association rules (min_conf=%.2f%%)" % (min_conf * 100))
	for rule in rules:
		print(rule[0],"=>",rule[1], "\nConfidence:", rule[2])

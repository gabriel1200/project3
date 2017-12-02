
import sys
import csv

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
			yield row

def apriori():
	pass

if __name__ == "__main__":
	try:
		_, filename, min_sup, min_conf = sys.argv
	except Exception as e:
		print(e)
		print("Usage:\n\tpython <filename> <min_sup> <min_conf>")
		sys.exit('System will exit')

	data = read_data(filename, limit=1000)

	for d in data:
		pass

	print("Filename:", filename)
	print("Min support:", min_sup)
	print("Min confidence:", min_conf)

The files submitted are, apriori.py, example-run.txt, rows.csv, README.txt and run.
apriori.py:
This is file contains python code that
-imports data from rows.csv 
-uses the a-priori algorithm as defined in Section 2.1 of the Agrawal and Srikant paper in VLDB 1994 to generate a list of association rules between different items in the data set. Differs from a-priori algorithm in that it uses count to determine frequency, we compensate for this by multiplying min_sup by the number of rows at the beginning of the algorithm. The columns considered in our implementations are specified in the columns. 
-formats and prints said list of associations and writes this information to output.txt
-The usage format is as follows:
python <filename> <min_sup> <min_conf>
filename refers to the name of the chosen csv fil
min_sup referring to the minimum (percentage value from 0 to 1) support threshold, ie the frequency with which an item needs to appear in the data set to be added to the current iteration of the frequency item set
min_conf refers to the minimum confidence (percentage value from 0 to 1) in a rule needed for a rule to be included in the list of associations. Any association rule with confidence less than min_conf will not be included.
example-run.txt:
A sample run of this program as detailed in the instructions.
rows.csv:
Csv file used in apriori algorithm. Contains a list of NYC restaurants and their health “grade”, along with a number of other variables. To retrieve the data set, use wget with the following link.
wget https://data.cityofnewyork.us/api/views/xx67-kt59/rows.csv
This creates the rows.csv file with the relevant data.
run
A shell script that runs apriori.py. follows the same pattern of usage
./run <filename> <min_sup> <min_conf>


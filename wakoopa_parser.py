#!/usr/bin/python

'''
	//MSH XM8_P
	
	Nikhil Vyas
'''

import sys
import re

def dict_val(x):
	'''
		used as key for sorting the op_dict dict by usage time
	'''
	return x[1];

def parse(filename, unit="hours"):
	f = open(filename, "r")
	op = open("output.txt", "w")
	op_csv = open(filename + "_Parsed.csv", "w")
	op_dict = {}

	div = 3600
	
	if unit=="seconds":
		div = 1
	elif unit=="minutes":
		div = 60
	
	total_usage = 0
	f.readline() #Skipping the first line.
	
	for line in f:
		mtch = re.search('([\w\s\W]+)(\\t)([\w\s\W]+)(\\t)([\w\s\W]+)(\\t)([\s\w\W]+)(\\t)([\w\s\W]+)(\\t)([\w\s\W]+)(\\t)([\w\s\W]+)(\\t)([\w\W\s]+)',line)
		if mtch:
			s_name = mtch.group(1)
			s_used_sec = mtch.group(7)
			
			if s_name in op_dict:
				op_dict[s_name] += float(s_used_sec) / div
			else:
				op_dict[s_name] = float(s_used_sec) / div
			
			total_usage += float(s_used_sec) / div
		else:
			print "Things went south"
	
	op_list = sorted(op_dict.items(), key=dict_val, reverse=True)
	
	op.writelines("Total software usage tracked: " + str(round(total_usage,2)) + " " + unit + "s\n\n\n")
	
	for itm in op_list:
		op.writelines(itm[0] + " used for " + str(round(itm[1], 2)) + " " + unit + "s\n")
		op_csv.writelines(itm[0] + "\t" + str(round(itm[1], 2)) + "\n")

	
	f.close()
	op.close()
	op_csv.close()

def main():
	if len(sys.argv) > 2:
		filename=sys.argv[1]
		unit = sys.argv[2][2:]
		parse(filename, unit)
	else:
		print 'Usage: ./wakoopa_parser.py <filename> --hours||--minutes||--seconds'

if __name__ == '__main__':
	main()
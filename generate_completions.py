#!/usr/bin/env python
# encoding: utf-8

"""
Generate sublime-completions file from Pebble header file.
Usage : python generate.py /path/to/pebble.h /path/to/pebble.sublime-completions
"""

import sys
import argparse
import re

def generate(header, output):
	pattern = r'^\w+\*?\s+\*?(\w+)\(([^\\/\(\)]*)\);'
	regex = re.compile(pattern, re.MULTILINE)

	f = open(header,'r')
	procs = [(i.group(1), i.group(2)) for i in regex.finditer(f.read())]
	f.close()
	
	content = ''
	content += '{\n'
	content += '\t"scope": "source",\n'
	content += '\t"completions": [\n'
	
	for i, proc in enumerate(procs): 
		content += '\t\t{"trigger": "' + proc[0] + '", "contents": "' + proc[0] + '('

		varnames = proc[1].split(',')
		for j, varname in enumerate(varnames):
			varname = varname.split()[-1].split('*')[-1]
			if not (varname == 'void') :
				content += '${' + str(j+1) + ':' + varname + '}'
				if j < len(varnames) - 1: content += ','

		content += ')"}'
		if i < len(procs) - 1: content += ','
		content += '\n'

	content += '\t]\n'
	content += '}\n'
	
	f = open(output,"w")
	f.write(content)
	f.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate sublime-completions file from Pebble header file.')
	parser.add_argument('header', action="store", help="Pebble header file")
	parser.add_argument('output', action="store", help="sublime-completions output file")
	result = parser.parse_args()

	generate(result.header, result.output)

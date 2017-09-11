# Author: Amanda House (aeh247@cornell.edu)

import csv, graphviz as gv, sys, os

fname = sys.argv[1]
oname = os.path.splitext(fname)[0]

with open(fname, 'rb') as file:
    form = list(csv.reader(file))

form = form[1:]

tree = gv.Digraph(format='pdf')

for row in form:
    parent = row[0]
    yes = row[1]
    no = row[2]
    if yes != '':
        tree.edge(parent, yes, 'Yes')
    if no != '':
        tree.edge(parent, no, 'No')

tree.render('out/' + oname)

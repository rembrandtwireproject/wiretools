# Author: Amanda House (aeh247@cornell.edu)

import csv
import graphviz as gv

with open('tree.csv', 'rb') as file:
    reader = csv.reader(file)
    flat_tree = list(reader)

flat_tree = flat_tree[1:]

tree = gv.Digraph(format='svg')

for row in flat_tree:
    parent = row[0]
    child1 = row[1]
    child2 = row[2]
    if child1 != '':
        tree.edge(parent, child1, row[3])
    if child2 != '':
        tree.edge(parent, child2, row[4])

tree.render('out/tree')

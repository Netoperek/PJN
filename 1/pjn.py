from graphviz import Digraph
import csv

EDGE_SIZE = 100
#ENGINE = 'circo'
ENGINE = 'fdp'
#ENGINE = 'neato'

def attach_to_graph(graph, keyword, filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            graph.node(row['name'].decode('utf-8'))
            length = str((1 / float(row['weight'])) * EDGE_SIZE)
            edge = graph.edge(keyword, row['name'].decode('utf-8'), label=row['weight'], len=length)

A = Digraph(comment='My Graph', engine=ENGINE)
attach_to_graph(A, 'mleko', 'mleko.csv')
attach_to_graph(A, 'ser', 'ser.csv')
attach_to_graph(A, 'woda', 'woda.csv')
attach_to_graph(A, 'bialy', 'bialy.csv')

A.render('test-output/round-table.gv', view=True)
#A.view()

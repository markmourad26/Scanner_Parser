import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QLabel, QTextEdit, QWidget
from scanner import Scanner
from Parser import Parser
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")


class TINYParserWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl = QLabel('Enter TINY Language Code', self)
        self.input_code = QTextEdit()
        self.add_initial_code()
        submit_button = QPushButton('Parse')
        submit_button.clicked.connect(self.submitted)
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lbl, 1, 0)
        grid.addWidget(self.input_code, 1, 1)
        grid.addWidget(submit_button, 2, 1)
        self.setLayout(grid)
        self.setGeometry(40, 40, 500, 900)
        self.setWindowTitle('TINY Parser')
        self.show()

    def add_initial_code(self):
        self.input_code.append("read x;")
        self.input_code.append("if 0<x then")
        self.input_code.append("    fact:=1;")
        self.input_code.append("    repeat")
        self.input_code.append("        fact:=fact*x;")
        self.input_code.append("        x:=x-1")
        self.input_code.append("    until x=0;")
        self.input_code.append("    write fact")
        self.input_code.append("end")

    def pygraphviz_layout_with_rank(self, G, prog="dot", root=None, sameRank=[], args=""):
        try:
            import pygraphviz
        except ImportError:
            raise ImportError('requires pygraphviz ',
                              'http://networkx.lanl.gov/pygraphviz ',
                              '(not available for Python3)')
        if root is not None:
            args += "-Groot=%s" % root
        A = nx.nx_agraph.to_agraph(G)
        for sameNodeHeight in sameRank:
            if type(sameNodeHeight) == str:
                print("node \"%s\" has no peers in its rank group" %
                      sameNodeHeight)
            A.add_subgraph(sameNodeHeight, rank="same")
        A.layout(prog=prog, args=args)
        node_pos = {}
        for n in G:
            node = pygraphviz.Node(A, n)
            try:
                xx, yy = node.attr["pos"].split(',')
                node_pos[n] = (float(xx), float(yy))
            except:
                print("no position for node", n)
                node_pos[n] = (0.0, 0.0)
        return node_pos

    def draw(self, same_rank_nodes):
        graph = self.G
        # pos = nx.get_node_attributes(graph, 'pos')
        # pos = self.pygraphviz_layout_with_rank(
        #     graph, prog='dot', sameRank=same_rank_nodes)
        # pos = nx.nx_pydot.graphviz_layout(graph, prog='dot')
        # pos = nx.spring_layout(graph)
        labels = dict((n, d['value']) for n, d in graph.nodes(data=True))
        f = plt.figure(1, figsize=(13, 8.65))
        for shape in ['s', 'o']:
            nx.draw_networkx_nodes(graph, pos, node_color='y', node_size=1300, node_shape=shape, labels=labels, nodelist=[
                sNode[0] for sNode in filter(lambda x: x[1]["shape"] == shape, graph.nodes(data=True))])
        nx.draw_networkx_edges(graph, pos, arrows=False)
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8)
        f.canvas.manager.window.wm_geometry("+%d+%d" % (600, 0))
        print(graph)
        plt.show()

    def submitted(self):
        scanned_code = Scanner(self.input_code.toPlainText() + ' ')
        parse_code = Parser(scanned_code.get_tokens())
        parse_code.parse()
        nodes_list = parse_code.get_nodes()
        edges_list = parse_code.get_edges()
        self.G = nx.DiGraph()
        for node_number, node in nodes_list.items():
            self.G.add_node(
                node_number, value=node[0] + '\n' + node[1], shape=node[2])
        self.G.add_edges_from(edges_list)
        parse_code.clear_tables()
        self.draw(parse_code.get_rank())


app = QApplication(sys.argv)
w = TINYParserWidget()
sys.exit(app.exec_())
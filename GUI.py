from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
import sys
from scanner import Scanner
from Parser import Parser
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("TINY language parser")
        MainWindow.resize(791, 531)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(791, 531))
        MainWindow.setMaximumSize(QtCore.QSize(791, 531))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 791, 531))
        self.tabWidget.setObjectName("tabWidget")
        self.Code = QtWidgets.QWidget()
        self.Code.setObjectName("Code")
        self.code_plainText = QtWidgets.QPlainTextEdit(self.Code)
        self.code_plainText.setGeometry(QtCore.QRect(0, 30, 791, 421))
        self.code_plainText.setObjectName("code_plainText")

        self.code_plainText.setFont(QFont('Consolas', 12))
        self.add_initial_code()

        self.code_parse = QtWidgets.QPushButton(self.Code)
        self.code_parse.setGeometry(QtCore.QRect(660, 460, 121, 41))
        self.code_parse.setAutoFillBackground(False)
        self.code_parse.setObjectName("code_parse")
        self.code_export = QtWidgets.QPushButton(self.Code)
        self.code_export.setGeometry(QtCore.QRect(540, 460, 121, 41))
        self.code_export.setObjectName("code_export")
        self.code_import = QtWidgets.QPushButton(self.Code)
        self.code_import.setGeometry(QtCore.QRect(420, 460, 121, 41))
        self.code_import.setObjectName("code_import")
        self.label = QtWidgets.QLabel(self.Code)
        self.label.setGeometry(QtCore.QRect(10, 0, 251, 31))
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.Code, "")
        self.Tokens = QtWidgets.QWidget()
        self.Tokens.setObjectName("Tokens")
        self.token_plainText = QtWidgets.QPlainTextEdit(self.Tokens)
        self.token_plainText.setGeometry(QtCore.QRect(0, 30, 791, 421))
        self.token_plainText.setObjectName("token_plainText")

        self.token_plainText.setFont(QFont('Consolas', 12))
        self.add_initial_token()

        self.token_parse = QtWidgets.QPushButton(self.Tokens)
        self.token_parse.setGeometry(QtCore.QRect(660, 460, 121, 41))
        self.token_parse.setObjectName("token_parse")
        self.token_export = QtWidgets.QPushButton(self.Tokens)
        self.token_export.setGeometry(QtCore.QRect(540, 460, 121, 41))
        self.token_export.setObjectName("token_export")
        self.label_2 = QtWidgets.QLabel(self.Tokens)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 251, 31))
        self.label_2.setObjectName("label_2")
        self.token_import = QtWidgets.QPushButton(self.Tokens)
        self.token_import.setGeometry(QtCore.QRect(420, 460, 121, 41))
        self.token_import.setObjectName("token_import")
        self.tabWidget.addTab(self.Tokens, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.code_parse.clicked.connect(self.submitted)
        self.code_export.clicked.connect(self.c_export)
        self.code_import.clicked.connect(self.c_import)

        self.token_parse.clicked.connect(self.t_submitted)
        self.token_export.clicked.connect(self.t_export)
        self.token_import.clicked.connect(self.t_import)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("TINY language parser", "TINY language parser"))
        self.code_parse.setText(_translate("MainWindow", "Parse"))
        self.code_parse.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.code_export.setText(_translate("MainWindow", "Export"))
        self.code_export.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.code_import.setText(_translate("MainWindow", "Import"))
        self.code_import.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.label.setText(_translate("MainWindow", "Enter TINY language code:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Code), _translate("MainWindow", "Code"))
        self.token_parse.setText(_translate("MainWindow", "Parse"))
        self.token_parse.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.token_export.setText(_translate("MainWindow", "Export"))
        self.token_export.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.label_2.setText(_translate("MainWindow", "Enter list of tokens:"))
        self.token_import.setText(_translate("MainWindow", "Import"))
        self.token_import.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tokens), _translate("MainWindow", "Tokens"))

    def add_initial_code(self):
        self.code_plainText.setPlainText('''read x;
if 0<x then
    fact:=1;
    repeat
        fact:=fact*x;
        x:=x-1
    until x=0;
    write fact
end''')

    def add_initial_token(self):
        self.token_plainText.setPlainText('''read, keyword
x, identifier
;, special_character
if, keyword
0, number
<, operator
x, identifier
then, keyword
fact, identifier
:=, assign
1, number
;, special_character
repeat, keyword
fact, identifier
:=, assign
fact, identifier
*, operator
x, identifier
;, special_character
x, identifier
:=, assign
x, identifier
-, operator
1, number
until, keyword
x, identifier
=, operator
0, number
;, special_character
write, keyword
fact, identifier
end, keyword''')

    def pygraphviz_layout_with_rank(self, G, prog="dot", sameRank=[], args=""):
        try:
            import pygraphviz
        except ImportError:
            raise ImportError('requires pygraphviz ',
                              'http://networkx.lanl.gov/pygraphviz ',
                              '(not available for Python3)')
        A = nx.nx_agraph.to_agraph(G)
        sameRank = sorted([sorted(x) for x in sameRank])
        
        for sameNodeHeight in sameRank:
            A.add_subgraph(sameNodeHeight, rank="same")
        A.layout(prog=prog, args=args)
        node_pos = {}
        for n in G:
            node = pygraphviz.Node(A, n)
            try:
                xx, yy = node.attr["pos"].split(',')
                node_pos[n] = [float(xx), float(yy)]
            except:
                node_pos[n] = [0.0, 0.0]
        return node_pos

    def show_msg(self, pos):
        msg = QMessageBox()
        msg.setWindowTitle("Wrong grammer")
        msg.setText(f"Error in line {pos[0]}, {pos[1]}")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

    def show_msg2(self, l):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(f"Please enter valid {l}.")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()


    def draw(self, same_rank_nodes, shape_s, shape_o, extra_edges):
        graph = self.G
        pos = self.pygraphviz_layout_with_rank(
            graph, prog='dot', sameRank=same_rank_nodes)
        labels = dict((n, '\n'+d['value']) for n, d in graph.nodes(data=True))
        f = plt.figure(1, figsize=(13, 8.65))
        nx.draw_networkx_nodes(graph, pos, node_color='#2F9191', linewidths=2, edgecolors='#247070', node_size=1700, node_shape='s', nodelist=shape_s)
        nx.draw_networkx_nodes(graph, pos, node_color='#2F9191', linewidths=2, edgecolors='#247070', node_size=2200, node_shape='o', nodelist=shape_o)
        for edge in extra_edges:
            graph.remove_edge(edge[0], edge[1])
        nx.draw_networkx_edges(graph, pos, arrows=False)
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=7, font_color='#D3FFFF', font_weight='bold')
        f.canvas.manager.window.wm_geometry("+%d+%d" % (600, 0))
        plt.show()

    def submitted(self):
        try:
            scanned_code = Scanner(self.code_plainText.toPlainText() + ' ') 
            parse_code = Parser(scanned_code.get_tokens(), scanned_code.get_token_pos())
            try:
                parse_code.parse()
                nodes_list = parse_code.get_nodes()
                edges_list = parse_code.get_edges()
                shape_s=[]
                shape_o=[]
                self.G = nx.DiGraph()
                for node_number, node in nodes_list.items():
                    self.G.add_node(
                        node_number, value=node[0] + '\n' + node[1], shape=node[2])
                    if node[2] == 's':
                        shape_s.append(node_number)
                    elif node[2] == 'o':
                        shape_o.append(node_number)
                children = parse_code.get_children()
                sameRank = parse_code.get_rank()
                sameRank+=children
                extra_edges = []
                for child_list in children:
                    for i in range(len(child_list)-1):
                        extra_edges.append((child_list[i],child_list[i+1]))
                edges_list+=extra_edges
                self.G.add_edges_from(edges_list)
                parse_code.clear_tables()
                self.draw(sameRank, shape_s, shape_o, extra_edges)
            except:
                error_line = parse_code.get_error()
                self.show_msg(error_line)
        except:
            self.show_msg2('code')

    def t_submitted(self):
        try:
            tokens = self.convert_tokens()
            pos = [x for x in range(1, len(tokens) + 1)]
            parse_code = Parser(tokens, pos)
            try:
                parse_code.parse()
                nodes_list = parse_code.get_nodes()
                edges_list = parse_code.get_edges()
                shape_s=[]
                shape_o=[]
                self.G = nx.DiGraph()
                for node_number, node in nodes_list.items():
                    self.G.add_node(
                        node_number, value=node[0] + '\n' + node[1], shape=node[2])
                    if node[2] == 's':
                        shape_s.append(node_number)
                    elif node[2] == 'o':
                        shape_o.append(node_number)
                children = parse_code.get_children()
                sameRank = parse_code.get_rank()
                sameRank+=children
                extra_edges = []
                for child_list in children:
                    for i in range(len(child_list)-1):
                        extra_edges.append((child_list[i],child_list[i+1]))
                edges_list+=extra_edges
                self.G.add_edges_from(edges_list)
                parse_code.clear_tables()
                self.draw(sameRank, shape_s, shape_o, extra_edges)
            except:
                error_line = parse_code.get_error()
                self.show_msg(error_line)
        except:
            self.show_msg2('tokens')

    def convert_tokens(self):
        list_of_tokens = self.token_plainText.toPlainText().split('\n')
        list_of_tokens = [x.replace(" ", "").split(',') for x in list_of_tokens]
        return list_of_tokens

    def c_export(self):
        data = self.code_plainText.toPlainText()
        filename = QFileDialog.getSaveFileName(filter='*.txt')
        if filename[0]:
            with open(filename[0], 'w+') as out:
                out.write(data)

    def c_import(self):
        filename = QFileDialog.getOpenFileName(filter='*.txt')
        if filename[0]:
            f = open(filename[0],'r')
            with f:
                data = f.read()
                self.code_plainText.setPlainText(data)

    def t_export(self):
        data = self.token_plainText.toPlainText()
        filename = QFileDialog.getSaveFileName(filter='*.txt')
        if filename[0]:
            with open(filename[0], 'w+') as out:
                out.write(data)

    def t_import(self):
        filename = QFileDialog.getOpenFileName(filter='*.txt')
        if filename[0]:
            f = open(filename[0],'r')
            with f:
                data = f.read()
                self.token_plainText.setPlainText(data)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

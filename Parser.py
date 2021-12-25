from scanner import *


class Node:
    def __init__(self, token, shape):
        self.token_value = token
        self.shape = shape
        self.children = []
        self.sibling = None
        self.index = None

    def set_children(self, y):
        try:
            assert isinstance(y, list)
            for i in y:
                self.children.append(i)
        except:
            self.children.append(y)

    def set_sibling(self, y):
        self.sibling = y


class Parser:
    counter = 0
    def __init__(self, tokens, pos):
        self.tokens = tokens
        self.token_pos = pos
        self.error = None
        self.count_tokens = len(self.tokens)
        self.curr_index = 0
        self.curr_token = self.tokens[self.curr_index]
        self.tree = None
        self.nodes = {}
        self.edges = []
        self.rank = []
        self.children = []

    def get_nodes(self):
        return self.nodes
    def get_edges(self):
        return self.edges
    def get_rank(self):
        return self.rank
    def get_children(self):
        return self.children
    def get_error(self):
        return self.error

    def set_tokens(self, tokens):
        self.tokens = tokens
        self.curr_index = 0
        self.curr_token = self.tokens[self.curr_index]

    def match(self, x):
        if self.curr_token[0] == x:
            if self.curr_index == self.count_tokens - 1:
                return False
            self.curr_index += 1
            self.curr_token = self.tokens[self.curr_index]
            return True
        else:
            if self.token_pos[self.curr_index] == self.token_pos[self.curr_index-1]:
                self.error = self.token_pos[self.curr_index],x+' is missing.'
            else:
                self.error = self.token_pos[self.curr_index-1],x+' is missing.'
            raise ValueError('Token Mismatch', self.tokens)

    def factor(self):
        if self.curr_token[0] == '(':
            self.match('(')
            tree = self.exp()
            self.match(')')
        elif self.curr_token[1] == 'number':
            tree = Node(('CONSTANT', '(' + str(self.curr_token[0]) + ')'), 'o')
            self.match(self.curr_token[0])
        elif self.curr_token[1] == 'identifier':
            tree = Node(('IDENTIFIER', '(' + str(self.curr_token[0]) + ')'), 'o')
            self.match(self.curr_token[0])
        else:
            if self.token_pos[self.curr_index] == self.token_pos[self.curr_index-1]:
                self.error = self.token_pos[self.curr_index],'factor'+' is missing.'
            else:
                self.error = self.token_pos[self.curr_index-1],'factor'+' is missing.'
            raise ValueError('SyntaxError', self.tokens)
        return tree

    def mulop(self):
        if self.curr_token[0] == '*' or self.curr_token[0] == '/':
            self.match(self.curr_token[0])

    def addop(self):
        if self.curr_token[0] == '+' or self.curr_token[0] == '-':
            self.match(self.curr_token[0])

    def comparison_op(self):
        if self.curr_token[0] in ['<', '>', '>=', '<=', '=']:
            self.match(self.curr_token[0])

    def term(self):
        tree = self.factor()
        while self.curr_token[0] == '*' or self.curr_token[0] == '/':
            parent = Node(('OPERATOR', '(' + str(self.curr_token[0]) + ')'), 'o')
            parent.set_children(tree)
            tree = parent
            self.mulop()
            tree.set_children(self.factor())
        return tree

    def simple_exp(self):
        tree = self.term()
        while self.curr_token[0] == '+' or self.curr_token[0] == '-':
            parent = Node(('OPERATOR', '(' + str(self.curr_token[0]) + ')'), 'o')
            parent.set_children(tree)
            tree = parent
            self.addop()
            tree.set_children(self.term())
        return tree

    def exp(self):
        tree = self.simple_exp()
        if self.curr_token[0] in ['<', '>', '>=', '<=', '=']:
            parent = Node(('OPERATOR', '(' + str(self.curr_token[0]) + ')'), 'o')
            parent.set_children(tree)
            tree = parent
            self.comparison_op()
            tree.set_children(self.simple_exp())
        return tree

    def write_stmt(self):
        tree = Node(('WRTIE', ''), 's')
        self.match('write')
        tree.set_children(self.exp())
        return tree

    def read_stmt(self):
        tree = Node(('READ', '(' + str(self.tokens[self.curr_index+1][0]) + ')'), 's')
        self.match('read')
        if self.curr_token[1] == 'identifier':
            self.match(self.curr_token[0])
        else:
            if self.token_pos[self.curr_index] == self.token_pos[self.curr_index-1]:
                self.error = self.token_pos[self.curr_index],'identifier'+' is missing.'
            else:
                self.error = self.token_pos[self.curr_index-1],'identifier'+' is missing.'
            raise ValueError('Token Mismatch', self.tokens)
        return tree

    def assign_stmt(self):
        tree = Node(('ASSIGN', '(' + str(self.curr_token[0]) + ')'), 's')
        self.match(self.curr_token[0])
        self.match(':=')
        tree.set_children(self.exp())
        return tree

    def repeat_stmt(self):
        tree = Node(('REPEAT', ''), 's')
        self.match('repeat')
        tree.set_children(self.stmt_sequence())
        self.match('until')
        tree.set_children(self.exp())
        return tree

    def if_stmt(self):
        tree = Node(('IF', ''), 's')
        self.match('if')
        tree.set_children(self.exp())
        self.match('then')
        tree.set_children(self.stmt_sequence())
        if self.curr_token[0] == 'else':
            self.match('else')
            tree.set_children(self.stmt_sequence())
        self.match('end')
        return tree


    def statement(self):
        if self.curr_token[0] == 'if':
            tree = self.if_stmt()
        elif self.curr_token[0] == 'repeat':
            tree = self.repeat_stmt()
        elif self.curr_token[1] == 'identifier':
            tree = self.assign_stmt()
        elif self.curr_token[0] == 'read':
            tree = self.read_stmt()
        elif self.curr_token[0] == 'write':
            tree = self.write_stmt()
        else:
            if self.token_pos[self.curr_index] == self.token_pos[self.curr_index-1]:
                self.error = self.token_pos[self.curr_index],'Incomplete statment'
            else:
                self.error = self.token_pos[self.curr_index-1],'Incomplete statment'
            raise ValueError('SyntaxError', self.tokens)
        return tree

    def stmt_sequence(self):
        tree = self.statement()
        parent = tree
        while self.curr_token[0] == ';':
            s = Node((None, None), None)
            self.match(';')
            s = self.statement()
            if s == None:
                break
            else:
                if tree == None:
                    tree = parent = s
                else:
                    parent.set_sibling(s)
                    parent = s
        return tree


    def create_data_tables(self, tree, index):
        tree.index = index
        self.nodes.update(
            {index: [tree.token_value[0], tree.token_value[1], tree.shape]})
        Parser.counter+=1
        if len(tree.children) != 0:
            l = []
            for i in tree.children:
                self.create_data_tables(i, Parser.counter)
                self.edges.append((tree.index, i.index))
                l.append(i.index)
            self.children.append(l)

        if tree.sibling != None:
            self.create_data_tables(tree.sibling, Parser.counter)
            self.edges.append((tree.index, tree.sibling.index))
            self.rank.append([tree.index, tree.sibling.index])

    def parse(self):
        self.tree = self.stmt_sequence()
        self.create_data_tables(self.tree, 0)
        if self.curr_index == len(self.tokens) - 1:
            pass
        elif self.curr_index < len(self.tokens):
            if self.token_pos[self.curr_index] == self.token_pos[self.curr_index-1]:
                self.error = self.token_pos[self.curr_index],"SyntaxError"
            else:
                self.error = self.token_pos[self.curr_index-1],"SyntaxError"
            raise ValueError('SyntaxError', self.tokens)

    def clear_tables(self):
        self.nodes.clear()
        Parser.counter = 0
        self.edges.clear()
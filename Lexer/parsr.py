

class Parser:
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = []
        self.current_token = None
        self.parse_tree = []
        self.last = None

    def next_token(self):
        self.current_token = self.lexer.token()

    def match(self, type):
        if type == self.current_token.type:
            self.last = self.current_token
            self.next_token()
            return True
        return False

    def ttype(self):
        return self.current_token.type

    def error(self, msg):
        self.errors.append(msg)

    def expect(self, symbol):
        if self.match(symbol):
            return True
        self.error(f'Syntax Error: line[{self.current_token.lineno}] Expected {symbol}')
        return False

    def factor(self, parent):
        if self.match('ID'):
            parent.append(['ID', self.last.value])
        elif self.match('NUMBER'):
            parent.append(['NUMBER', self.last.value])
        elif self.match('LPAREN'):
            parent.append('LPAREN')
            child = ['EXPRESSION']
            parent.append(child)
            self.expression(child)
            self.expect('RPAREN')
            parent.append('RPAREN')
        else:
            self.error(f'Syntax Error:line[{self.current_token.lineno}] invalid factor')
            self.last = self.current_token
            self.next_token()

    def term(self, parent):
        child = ['FACTOR']
        parent.append(child)
        self.factor(child)
        while self.ttype() == 'MUL' or self.ttype() == 'DIV':
            parent.append(self.ttype())
            self.last = self.current_token
            self.next_token()
            child = ['FACTOR']
            parent.append(child)
            self.factor(child)

    def expression(self, parent):
        if self.ttype() == 'ADD' or self.ttype() == 'SUB':
            parent.append(self.ttype())
            self.last = self.current_token
            self.next_token()
        child = ['TERM']
        parent.append(child)
        self.term(child)
        while self.ttype() == 'ADD' or self.ttype() == 'SUB':
            parent.append(self.ttype())
            self.last = self.current_token
            self.next_token()
            child = ['TERM']
            parent.append(child)
            self.term(child)

    def condition(self, parent):
        if self.match('ODD'):
            child = ['EXPRESSION']
            parent.append(child)
            self.expression(child)
        else:
            child = ['EXPRESSION']
            parent.append(child)
            self.expression(child)
            if self.ttype() == 'GE' or self.ttype() == 'LE' or self.ttype() == 'GT' or self.ttype() == 'LT' or self.ttype() == 'EQ' or self.ttype() == 'NEQ':
                parent.append(self.ttype())
                self.last = self.current_token
                self.next_token()
                child = ['EXPRESSION']
                parent.append(child)
                self.expression(child)
            else:
                self.error(f'Syntax Error:line[{self.current_token.lineno}] invalid operator')
                self.last = self.current_token
                self.next_token()
    
    def statement(self, parent):
        if self.match('ID'):
            parent.append(['ID', self.last.value])
            self.expect('ASSIGN')
            parent.append('ASSIGN')
            child = ['EXPRESSION']
            parent.append(child) 
            self.expression(child)
        elif self.match('CALL'):
            parent.append('CALL')
            self.expect('ID')
            parent.append(['ID', self.last.value])
        elif self.match('BEGIN'):
            parent.append('BEGIN')
            child = ['STATEMENT']
            parent.append(child)
            self.statement(child)
            while self.match('SEMIC'):
                parent.append('SEMICOLON')
                child = ['STATEMENT']
                parent.append(child)
                self.statement(child)
            self.expect('END')
            parent.append('END')
        elif self.match('IF'):
            parent.append('IF')
            child = ['CONDITION']
            parent.append(child)
            self.condition(child)
            self.expect('THEN')
            parent.append('THEN')
            child = ['STATEMENT']
            parent.append(child)
            self.statement(child)
        elif self.match('WHILE'):
            parent.append('WHILE')
            child = ['CONDITION']
            parent.append(child)
            self.condition(child)
            self.expect('DO')
            parent.append('DO')
            child = ['STATEMENT']
            parent.append(child)
            self.statement(child)
        elif len(self.lexer.tokens) == 0:
            pass
        else:
            self.error(f'Syntax Error:line[{self.current_token.lineno}] invalid statement {self.current_token}')

    def block(self, parent):
        if self.match('CONST'):
            parent.append('CONST')
            self.expect('ID')
            parent.append(['ID', self.last.value])
            self.expect('EQ')
            parent.append('EQ')
            self.expect('NUMBER')
            parent.append(['NUMBER', self.last.value])
            while self.match('COMMA'):
                parent.append('COMMA')
                self.expect('ID')
                parent.append(['ID', self.last.value])
                self.expect('EQ')
                parent.append('EQ')
                self.expect('NUMBER')
                parent.append(['NUMBER', self.last.value])
            self.expect('SEMIC')
            parent.append('SEMICOLON')
        if self.match('VAR'):
            parent.append('VAR')
            self.expect('ID')
            parent.append(['ID', self.last.value])
            while self.match('COMMA'):
                parent.append('COMMA')
                self.expect('ID')
                parent.append(['ID', self.last.value])
            self.expect('SEMIC')
            parent.append('SEMICOLON')
        while self.match('PROCEDURE'):
            parent.append('PROCEDURE')
            self.expect('ID')
            parent.append(['ID', self.last.value])
            self.expect('SEMIC')
            parent.append('SEMICOLON')
            child = ['BLOCK']
            parent.append(child)
            self.block(child)
            self.expect('SEMIC')
            parent.append('SEMICOLON')
        child = ['STATEMENT']
        parent.append(child) 
        self.statement(child)

    def begin(self):
        self.next_token()
        parent = self.parse_tree
        parent.append('BLOCK')
        self.block(parent)
        self.expect('DOT')
        parent.append('DOT')
    
    def remove_single(self, curr):
        remove = []
        for i, element in enumerate(curr):
            if type(element) == list:
                if len(element) == 1:
                    remove.append(i)
        for element in remove:
            curr.pop(element)

    def print_subtree(self, tree, space, last):
        self.remove_single(tree)
        sep = '├─'
        for i in range(len(tree)):
            if i == (len(tree) - 1):
                sep = '└─'
            print('│')
            if type(tree[i]) == list:
                print(' '*space, sep, '─'*(last-1),tree[i][0], sep='')
                self.print_subtree(tree[i][1:], space+last+1, len(tree[i][0]))
            else:
                print(' '*space, sep, '─'*(last-1),tree[i], sep='')

    def print_tree(self):
        print(self.parse_tree[0])
        self.print_subtree(self.parse_tree[1:], 0, len(self.parse_tree[0]))
            



    def parse(self):
        self.begin()

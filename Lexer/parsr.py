

class Parser:
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = []
        self.current_token = None
        self.parse_tree = []

    def next_token(self):
        self.current_token = self.lexer.token()

    def match(self, type):
        if type == self.current_token.type:
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

    def factor(self):
        if self.match('ID'):
            pass #add
        elif self.match('NUMBER'):
            pass #add
        elif self.match('LPAREN'):
            self.expression()
            self.expect('RPAREN')
        else:
            self.error(f'Syntax Error:line[{self.current_token.lineno}] invalid factor')
            self.next_token()

    def term(self):
        self.factor()
        while self.ttype() == 'MUL' or self.ttype() == 'DIV':
            self.next_token()
            self.factor()

    def expression(self):
        if self.ttype() == 'ADD' or self.ttype() == 'SUB':
            self.next_token()
        self.term()
        while self.ttype() == 'ADD' or self.ttype() == 'SUB':
            self.next_token()
            self.term()

    def condition(self):
        if self.match('ODD'):
            self.expression()
        else:
            self.expression()
            if self.ttype() == 'GE' or self.ttype() == 'LE' or self.ttype() == 'GT' or self.ttype() == 'LT' or self.ttype() == 'EQ' or self.ttype() == 'NEQ':
                self.next_token()
                self.expression()
            else:
                self.error(f'Syntax Error:line[{self.current_token.lineno}] invalid operator')
                self.next_token()
    
    def statement(self):
        if self.match('ID'):
            self.expect('ASSIGN')
            self.expression()
        elif self.match('CALL'):
            self.expect('ID')
        elif self.match('BEGIN'):
            self.statement()
            while self.match('SEMIC'):
                self.statement()
            self.expect('END')
        elif self.match('IF'):
            self.condition()
            self.expect('THEN')
            self.statement()
        elif self.match('WHILE'):
            self.condition()
            self.expect('DO')
            self.statement()
        else:
            self.error(f'Syntax Error:line[{self.current_token.lineno}] invalid statement {self.current_token}')

    def block(self):
        if self.match('CONST'):
            self.expect('ID')
            self.expect('EQ')
            self.expect('NUMBER')
            while self.match('COMMA'):
                self.expect('ID')
                self.expect('EQ')
                self.expect('NUMBER')
            self.expect('SEMIC')
        if self.match('VAR'):
            self.expect('ID')
            while self.match('COMMA'):
                self.expect('ID')
            self.expect('SEMIC')
        while self.match('PROCEDURE'):
            self.expect('ID')
            self.expect('SEMIC')
            self.block()
            self.expect('SEMIC')
        self.statement()

    def begin(self):
        self.next_token()
        self.block()
        self.expect('DOT')

    def parse(self):
        self.begin()

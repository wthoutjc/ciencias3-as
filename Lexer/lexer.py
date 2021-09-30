import re
from Lexer.token import Token
from Lexer.keywords import *

# for data in lex.tokens: #Usa este for para que visualizes mejor como funciona ahora por tupla
#             print(data.category)
#             print(data.position)
#             print(data.symbol)
#             print(data.value)

class Lexer:
    def __init__(self, source_file):
        self.tokens = []
        self.source = source_file
        self.curr_idx = 0
        self.next_idx = 1
        self.col = 1
        #self.errors = []

    #Returns 
    def next_Token(self):
        if self.tokens:
            return self.tokens.pop(0)

    #Increments the indexes
    def go_on(self, delta=1):
        self.curr_idx += delta
        self.next_idx += delta
        self.col += delta

    #Returns Current character
    def cchar(self):
        if self.curr_idx < len(self.source):
            return self.source[self.curr_idx]
        return ''

    #Returns Next character
    def nchar(self):
        if self.next_idx < len(self.source):
            return self.source[self.next_idx]
        return ''

    def scan(self):
        line = 1
        while self.cchar():
            if self.cchar() == ' ' or self.cchar() == '\t':   #Ignore blanks
                self.go_on()
                continue
            if self.cchar() == '\n':    #Count new line
                line += 1
                self.col = 1
            elif self.cchar() == '/' and self.nchar() == '/':   #Ignore single-line comments
                while self.cchar() and self.nchar() != '\n':
                    self.go_on()
            elif self.cchar() and (self.cchar() == '/' and self.nchar() == '*'):   #Ignore multi-line comments
                while self.cchar() and (self.cchar() != '*' or self.nchar() != '/'):
                    if self.cchar() == '\n':
                        line += 1
                        self.col = 1
                    self.go_on()
                self.go_on()
            elif self.cchar().isalpha():    #Begins with a letter
                col = self.col
                category, value, symbol = self.classify_alpha(self.curr_idx)
                self.tokens.append(Token(category, value, symbol, line, col))
            elif self.cchar().isdigit():    #Begins with a number
                col = self.col
                category, value, symbol = self.classify_number(self.curr_idx)
                self.tokens.append(Token(category, value, symbol, line, col))
            else:   #Begins with a symbol
                col = self.col
                category, value, symbol = self.classify_symbol(self.curr_idx)
                self.tokens.append(Token(category, value, symbol, line, col))
            self.go_on()

    def classify_alpha(self, begin):
        while self.cchar() and (self.nchar().isalpha() or self.nchar().isdigit() or self.nchar() in '_$'):
            self.go_on()
        word = self.source[begin:self.next_idx]
        if word in RESERVED:
            if word == 'false' or word == 'true':
                return 'Reserved Literal', bool(word), word
            if word == 'null':
                return 'Reserved Literal', None, word
            return 'Reserved', RESERVED[word], word
        else:
            return 'Identifier', word, word
    
    def classify_number(self, begin):
        value = 'Unknown'
        category = 'Unknown'
        word = ''
        if self.cchar() == '0':
            if self.nchar() == '.':
                self.go_on()
                while self.cchar() and self.nchar().isdigit():
                    self.go_on()
                word = self.source[begin:self.next_idx]
                value = float(word)
                category = 'Literal REAL'
            elif self.nchar() == 'x':
                self.go_on()
                while self.cchar() and (self.nchar().isdigit() or self.nchar() in 'abcdefABCDEF'):
                    self.go_on()
                word = self.source[begin:self.next_idx]
                value = int(word, 16)
                category = 'Literal NUMBER'
            elif self.nchar().isdigit():
                self.go_on()
                while self.cchar() and self.nchar().isdigit():
                    self.go_on()
                word = self.source[begin:self.next_idx]
                value = int('0o' + word, 8)
                category = 'Literal NUMBER'
            else:
                value = 0
                category = 'Literal NUMBER'
        elif self.nchar() == '.':
            self.go_on()
            while self.cchar() and self.nchar().isdigit():
                self.go_on()
            word = self.source[begin:self.next_idx]
            value = float(word)
            category = 'Literal REAL'
        elif self.nchar().isdigit():
            while self.cchar() and self.nchar().isdigit():
                self.go_on()
            word = self.source[begin:self.next_idx]
            value = int(word)
            category = 'Literal NUMBER'
        else:
            word = self.source[begin:self.next_idx]
            value = int(word)
            category = 'Literal NUMBER'

        return category, value, word
        

    def classify_symbol(self, begin):
        value = 'Unknown'
        category = 'Unknown'
        key = self.cchar()
        if key in PUNCTUATORS:
            category = 'Punctuation'
            value = PUNCTUATORS[key]
        elif self.cchar() == '"':
            while self.nchar() != '"' and self.cchar():
                self.go_on()
            category = 'Literal String'
            value = self.source[begin:self.next_idx]
            self.go_on()
        else:
            while (key + self.nchar()) in OPERATOR and self.cchar():
                self.go_on()
        if key in OPERATOR:
            value = OPERATOR[key][0]
            category =OPERATOR[key][1]

        return category, value, self.source[begin:self.next_idx]
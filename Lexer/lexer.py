import re
from tokn import Token
from keywords import *

class Lexer:
    def __init__(self, source_file):
        self.tokens = []
        self.source = source_file
        self.curr_idx = 0
        self.next_idx = 1
        self.col = 1
        #self.errors = []

    #Returns the next token in the list structure
    def token(self):
        if self.tokens:
            return self.tokens.pop(0)
        else:
            return None

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
            elif self.cchar() == '#':   #Ignore single-line comments
                while self.cchar() and self.nchar() != '\n':
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
            return 'Reserved', word, word
        else:
            return 'Identifier', word, 'ID'
    
    def classify_number(self, begin):
        value = int(self.cchar())
        category = 'INT'
        word = ''
        if self.nchar().isdigit():
            while self.cchar() and self.nchar().isdigit():
                self.go_on()
            word = self.source[begin:self.next_idx]
            value = int(word)
        elif self.nchar() == '.':
            self.go_on()
            while self.cchar() and self.nchar().isdigit():
                self.go_on()
            word = self.source[begin:self.next_idx]
            value = float(word)
            category = 'FLOAT'
            

        return category, value, category
        

    def classify_symbol(self, begin):
        value = 'Unknown'
        category = 'Unknown'
        key = self.cchar()
        while (key + self.nchar()) in OPERATOR and self.cchar():
                self.go_on()
                key += self.cchar()
        if key in OPERATOR:
            value = OPERATOR[key][0]
            category =OPERATOR[key][1]
        if key in PUNCTUATORS:
            category = 'Punctuation'
            value = PUNCTUATORS[key]
            

        return category, key, value
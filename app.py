from Lexer.lexer import Lexer
from Parser.parser import Parser

with open('lexer/Test.java','r') as f:  
        lex = Lexer(f.read())
        lex.scan()
        parser = Parser(lex.tokens)
        
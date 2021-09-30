from parsr import Parser
from lexer import Lexer


with open('lexer/Test','r') as f: 
        lex = Lexer(f.read())
        lex.scan()
        for token in lex.tokens:
           print(token)
        par = Parser(lex)
        par.parse()
        for error in par.errors:
                print(error)
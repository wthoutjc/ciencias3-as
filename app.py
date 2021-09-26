from Lexer.lexer import Lexer
from Parser.parser import Parser

with open('lexer/Test.java','r') as f:  
        lex = Lexer(f.read())
        lex.scan()
        Parser(lex.tokens)
        parser = Parser(lex.tokens)
        parser.decompose_lexer()
        # for data in lex.tokens: #Usa este for para que visualizes mejor como funciona ahora por tupla
        #     print(data.category)
        #     print(data.position)
        #     print(data.symbol)
        #     print(data.value)
            
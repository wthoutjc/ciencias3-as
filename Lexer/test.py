from semantics import Semantics
from parsr import Parser
from lexer import Lexer


with open("lexer/Test", "r") as f:
    lex = Lexer(f.read())
    lex.scan()
    print(f'\n{"-"*40} ANÁLISIS LÉXICO {"-"*40}')
    for token in lex.tokens:
        print(token.ptoken())
    print(f'\n{"-"*40} ANÁLISIS SINTÁCTICO {"-"*40}')
    par = Parser(lex)
    par.parse()
    print(f'\n{"-"*40} ERRORES SINTÁCTICOS {"-"*40}')
    for error in par.errors:
        print(error)
    print(f'\n{"-"*41} ÁRBOL DE SINTAXIS {"-"*41}')
    print(par.parse_tree)
    par.print_tree()
    print(f'\n{"-"*40} ANÁLISIS SEMÁNTICO {"-"*40}')
    asem = Semantics(par)
    asem.analyze()
    print(f'\n{"-"*40} ERRORES SEMÁNTICOS {"-"*40}')
    for error in sorted(asem.errors):
        print(error)

from Parser.syntax import SYNTAX

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens #Acá actua como tokens: Símbolos terminales. (?)
        self.invalid_tokens = []
        self.valid_tokens = []
        self.parse_tree = None

    def decompose_lexer(self): #Acá actua como producciones de una grámatica
        categories = []
        for data_tokens in self.tokens:
            categories.append(data_tokens.category)
        for number in range(len(self.tokens)):
            print('Categoria del Lexer: ' + categories[number])
            print('Categoria del SYNTAX: ' + categories[number])

    def top_down(self, token):
        '''
        Aca asigna una categoria, si el token cumple SYNTAX (Estructura no definida),
        se asigna a valid_token, si no, a invalid_token
        '''
        #If token in SYNTAX:
        self.invalid_tokens.append(0)
        self.valid_tokens.append(1)
        pass
    
    def LRParser(self):
        pass
    
    def parse_table(self):
        '''
        este método genera el parse tree
        '''
        pass

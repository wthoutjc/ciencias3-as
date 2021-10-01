#Actuán como no terminales (V)
SYNTAX = [
    ('Reserved', 'Identifier', 'Punctuation'), #Imports, Declaraciones
    ('Reserved', 'Reserved', 'Identifier', 'Punctuation', 'Punctuation'), #public class Lexer {}
    ('Reserved', 'Reserved', 'Reserved', 'Identifier', 'Punctuation', 'Identifier', 'Punctuation', 'Punctuation', 'Identifier', 'Punctuation', 'Punctuation', 'Punctuation'), #public static void main(String[] args) {}
]

SYNTAX_TOP_DOWN = {
    "Reserved" : ['Identifier'], #Estructura de derivación, Reserved puede derivar en un identifier o en...
    "Identifier" : ['deriva_0','deriva_1','deriva_2','deriva_3'], #Estructura de derivación, Identifier puede derivar en un identifier o en...
}
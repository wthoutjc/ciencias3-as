RESERVED = ['ODD',
            'CALL', 
            'BEGIN', 
            'END', 
            'IF', 
            'THEN', 
            'WHILE', 
            'DO', 
            'CONST', 
            'VAR', 
            'PROCEDURE',
            'INT',
            'FLOAT']
    

OPERATOR = {'+': ("ADD", 'Arithmetic Operator'),
            '-': ("SUB", 'Arithmetic Operator'),
            '*': ("MUL", 'Arithmetic Operator'),
            '/': ("DIV", 'Arithmetic Operator'), 
            ':=': ("ASSIGN", 'Assign operator'),
            "<": ("LT", 'Relational Operator'),
            ">": ("GT", 'Relational Operator'),
            "<=": ("LE", 'Relational Operator'),
            ">=": ("GE", 'Relational Operator'),
            "=": ("EQ", 'Relational Operator'),
            "!=": ("NEQ", 'Relational Operator')}

OPINV = {'ADD': '+',
         'SUB': '-',
         'MUL': '*',
         'DIV': '/', 
         'ASSIGN': ':=',
         'LT': '<',
         'GT': '>',
         'LE': '<=',
         'GE': '>=',
         'EQ': '=',
         'NEQ': '!='}

PUNCTUATORS = {',': 'COMMA',
               '(': 'LPAREN',
               ')': 'RPAREN',
               '.': 'DOT',
               ';': 'SEMIC',
               ':': 'COLON'}

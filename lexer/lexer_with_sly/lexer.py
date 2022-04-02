# Test code. If the python intepretor tells you that :     src_file = open("Test.c")
# FileNotFoundError: [Errno 2] No such file or directory: 'Test.c'
# >> then go to your file explorer, look for lexer.py, run it, go back and try to run code again


from sly import Lexer

class CalcLexer(Lexer):
    tokens = { IDENTIFIER, RETURN, VOID, BOOL, INT, CHAR, IF, ELSE, WHILE, FLOAT_CONSTANT, NUMBER,
               PLUS, MINUS, TIMES, MODULUS,DIVIDE, EQUIVALENCE, ASSIGN, LE, LT, GE,
               GT, NE, LPAREN, RPAREN, LSQUARE, RSQUARE, LCURLY, RCURLY, SCOLON, COMMA}

    # String containing ignored characters between tokens
    ignore = '\t'
    ignore_whitespace = '\s+'

    # Regular expression rules for tokens
    FLOAT_CONSTANT = r'\d*\.{1}\d+'
    NUMBER  = r'\d+'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    MODULUS = r'%'
    DIVIDE  = r'/'
    EQUIVALENCE = r'=='
    ASSIGN  = r'='
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='
    LPAREN  = r'\('
    RPAREN  = r'\)'
    LSQUARE = r'\['
    RSQUARE = r'\]'
    LCURLY = r'\{'
    RCURLY = r'\}'
    SCOLON = ';'
    COMMA = ','

    # Tokens for keywords
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENTIFIER['return'] = RETURN
    IDENTIFIER['void'] = VOID
    IDENTIFIER['bool'] = BOOL
    IDENTIFIER['int'] = INT
    IDENTIFIER['char'] = CHAR
    IDENTIFIER['if'] = IF
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['while'] = WHILE

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
        return t

if __name__ == '__main__':
    src_file = open("Test.c")
    out_file = open("Lexer_Output.txt","w")
    lexer = CalcLexer()

    # count = 1
    for line in src_file:
        for tok in lexer.tokenize(line):
            # print('type=%r, value=%r' % (tok.type, tok.value))
            out_file.write('<%r> --> %r\t' %(tok.type, tok.value))
        out_file.write("\n")

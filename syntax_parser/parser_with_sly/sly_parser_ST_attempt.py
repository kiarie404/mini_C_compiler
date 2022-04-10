# -----------------------------------------------------------------------------
# calc.py
# Ok, team ... people
# Am having a hard time seperating the lexer and Parser into different files.
# I have tried using json files to transfer data between the 2 modules, And I ended
# up shooting myself in the foot--- a couple of times --- deliberately ----
#
# As much as modularity == good design  , We have to take this shot.
# At least the code structure is modest
#
# Good luck people, in modifying the file.
# Hope the code structure is clear
# -----      kiarie404
# -----------------------------------------------------------------------------

from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { NAME, NUMBER, PLUS, TIMES, MINUS, DIVIDE, ASSIGN, LPAREN, RPAREN }
    ignore = ' \t'

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    # time to get the tokens from the parser.
    # why ?? why are we not scaning the BNF
    # why ?? where will we get the non_terminals?
    tokens = CalcLexer.tokens

    # declaring the precedence
    # you declare asscociativity, and then tokens that have the same precedence
    # As the list goes down, the precedence goes higher. eg
    # Minus has a lower precedence that TIMES
    precedence = (
        ('left', PLUS, MINUS), # plus and minus have the same precedence level, apply left asscociatuvity in case of conflict
        ('left', TIMES, DIVIDE),
        )

    def __init__(self):
        self.names = { }

    # incase of SHIFT/REDUCE error , sly by default opts to shift.
    # To resolve ambiguity, especially in expression grammars,
    # SLY allows individual tokens to be assigned a precedence level and associativity as shown above... problem solved... How?
    # If the current token has higher precedence than the rule on the stack, it is shifted.
    # If the grammar rule on the stack has higher precedence, the rule is reduced.
    # If the current token and the grammar rule have the same precedence, the rule is reduced for left associativity, whereas the token is shifted for right associativity.
    # If nothing is known about the precedence, shift/reduce conflicts are resolved in favor of shifting (the default).




    # for example , the function below can be re-witten as the BNF production - statement : NAME ASSIGN expr
    # the @_() encloses the right side of a production
    # the function name ie "statement" is the left side of the BNF
    # this function gets triggered whenever the contents enclosed by the @_() get detected
    # the function receives a sequence of grammar symbol values in p
    # for Tokens, the value of the coresponding p.symbol is the same as the p.value attribute assigned to tokens in the lexer module
    # For non-terminals, the value is whatever was returned by the methods defined for that rule
    # If a grammar rule includes the same symbol name more than once,
    # you need to append a numeric suffix to disambiguate the symbol name when you’re accessing values. For example:
    # @_('expr PLUS expr')
    # def expr(self, p):
    #   return p.expr0 + p.expr1
    @_('NAME ASSIGN expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1


    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)



    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print("Undefined name '%s'" % p.NAME)
            return 0

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))

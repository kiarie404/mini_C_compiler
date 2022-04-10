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

import json
from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { IDENTIFIER, RETURN_KEYWORD, VOID_KEYWORD, BOOL_KEYWORD, FLOAT_KEYWORD, INT_KEYWORD,
               IF, ELSE, WHILE, BREAK,
               FLOAT_CONSTANT, INT_CONSTANT, BOOL_CONSTANT,
               PLUS, MINUS, TIMES, MODULUS, DIVIDE, ASSIGN,
               EQUIVALENT_TO, LESS_OR_EQUAL, LESS_THAN, GREATER_OR_EQUAL, GREATER_THAN, INEQUIVALENT_TO,
               LOGICAL_NOT, LOGICAL_OR, LOGICAL_AND,
               LPAREN, RPAREN, LCURLY, RCURLY, SCOLON, COMMA}

    # String containing ignored characters between tokens
    ignore = '\t'
    ignore_whitespace = '\s+'
    ignore_comment = r'\/\/.*'  # meant to ignore comments

    # Regular expression rules for tokens
    FLOAT_CONSTANT = r'\d*\.{1}\d+'
    INT_CONSTANT  = r'\d+'
    BOOL_CONSTANT = r'(true|TRUE|false|FALSE)'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    MODULUS = r'%'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    EQUIVALENT_TO = r'=='
    LESS_OR_EQUAL = r'<='
    LESS_THAN = r'<'
    GREATER_OR_EQUAL = r'>='
    GREATER_THAN = r'>'
    INEQUIVALENT_TO = r'!='
    LOGICAL_NOT = r'!'
    LOGICAL_OR = r'\|\|'
    LOGICAL_AND = r'&&'
    LPAREN  = r'\('
    RPAREN  = r'\)'
    LCURLY = r'\{'
    RCURLY = r'\}'
    SCOLON = ';'
    COMMA = ','

    # Tokens for keywords
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENTIFIER['return'] = RETURN_KEYWORD
    IDENTIFIER['void'] = VOID_KEYWORD
    IDENTIFIER['bool'] = BOOL_KEYWORD
    IDENTIFIER['float'] = FLOAT_KEYWORD
    IDENTIFIER['int'] = INT_KEYWORD
    IDENTIFIER['if'] = IF
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['while'] = WHILE
    IDENTIFIER['break'] = BREAK

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
        return t


class CalcParser(Parser):
    # time to get the tokens from the parser.
    tokens = CalcLexer.tokens

    # declaring the precedence
    # you declare asscociativity, and then tokens that have the same precedence
    # As the list goes down, the precedence goes higher. eg
    # Minus has a lower precedence that TIMES
    precedence = (
        ('left', PLUS, MINUS), # plus and minus have the same precedence level, apply left asscociatuvity in case of conflict
        ('left', TIMES, DIVIDE, MODULUS),
        )

    def __init__(self):
        self.names = { }  # this is where we store variables in the form "variable_name" : "2" where 2 can be a NUMBer or an expression

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
        self.names[p.NAME] = p.expr  # create a new instance of "name" : expr in the class CalcParser
                                     # this function returns nothing, because it has no-one to report to

    @_('expr')
    def statement(self, p):
        print(p.expr)            # prints expr part of the statement.
                                 # it ignores the NAME even if the name was defined
                                 # this function returns nothing, because it has no-one to report to
        # test : we print the json file...
        json_pretty_output = json.dumps(p.expr, indent=2)
        print(json_pretty_output)
        # now we write that tree as a json file.
        with open("syntax_tree_representation.json", "w") as output_file:
            json.dump(p.expr, output_file)

    @_('expr PLUS expr')
    def expr(self, p):
        return { 'addition_expression' : (p.expr0, p[1], p.expr1)}

    @_('expr MINUS expr')
    def expr(self, p):
        return { 'subtraction_expression' : (p.expr0, p[1], p.expr1)}


    @_('expr TIMES expr')
    def expr(self, p):
        return { 'multiplication_expression' : (p.expr0, p[1], p.expr1)}

    @_('expr DIVIDE expr')
    def expr(self, p):
        return { 'division_expression' : (p.expr0, p[1], p.expr1)}

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return { 'group_expression' : (p[1])}

    @_('NUMBER')
    def expr(self, p):
        return { 'number_value' : p.NUMBER}



    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]  # makes it that, the value represented by the NAME variable is returned.
                                       # for example : if NAME = 2, then 2 will be returned
                                       # from here on , the expr -> NAME is same as expr = 2
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

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
    # you need to append a numeric suffix to disambiguate the symbol name when you???re accessing values. For example:
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

        # print(self.names)  # test case to check stored variables

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

    # time to execute ...
    try:
        # take input from the sample code
        with open("sample_test_code.c", "r") as source_file:
            data = source_file.read()
    except EOFError:
        pass
    if data:  # if data was read from source file successfully...
        parser.parse(lexer.tokenize(data))

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
    tokens = { IDENTIFIER_CONST, RETURN_KEYWORD, VOID_KEYWORD, BOOL_KEYWORD, FLOAT_KEYWORD, INT_KEYWORD,
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
    IDENTIFIER_CONST = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENTIFIER_CONST['return'] = RETURN_KEYWORD
    IDENTIFIER_CONST['void'] = VOID_KEYWORD
    IDENTIFIER_CONST['bool'] = BOOL_KEYWORD
    IDENTIFIER_CONST['float'] = FLOAT_KEYWORD
    IDENTIFIER_CONST['int'] = INT_KEYWORD
    IDENTIFIER_CONST['if'] = IF
    IDENTIFIER_CONST['else'] = ELSE
    IDENTIFIER_CONST['while'] = WHILE
    IDENTIFIER_CONST['break'] = BREAK

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
        self.identifiers = { }  # this is where we store variables in the form "variable_name" : "2" where 2 can be a NUMBer or an expression
        self.local_identifiers = { }
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
    #
    @_('command_list')
    def program(self, p):
        print(p.command_list)            # prints command_list part of the statement.
                                         # this function returns nothing, because it has no-one to report to
        # test : we print the json file...
        json_pretty_output = json.dumps(p.command_list, indent=2)
        print(json_pretty_output)
        # now we write that tree as a json file.
        with open("syntax_tree_representation.json", "w") as output_file:
            json.dump(p.command_list, output_file)

    @_('command command_list')
    def command_list(self, p):
        return { 'global declarations' : (p.command, p.command_list)}

    @_('command')
    def command_list(self, p):
        return { 'global declaration' : (p.command)}

    @_('variable_declaration')
    def command(self, p):
        return { 'global variable declaration' : (p.variable_declaration)}

    @_('function_definition')
    def command(self, p):
        return { 'function definition' : (p.function_definition)}

    @_('type_specifier IDENTIFIER_CONST SCOLON')
    def variable_declaration(self, p):
        # store the undefined variable in our variable store.
        # But with a NULL value associated with it
        self.identifiers[p.IDENTIFIER_CONST] = None
        return { 'global variable declaration' : (p.type_specifier, p.IDENTIFIER_CONST, p.SCOLON)}

    @_('type_specifier IDENTIFIER_CONST ASSIGN expression SCOLON')
    def variable_declaration(self, p):
        self.identifiers[p.IDENTIFIER_CONST] = p.expression  # create a new instance of "name" : expr in the class CalcParser
        return { 'variable definition' : (p.type_specifier, p.IDENTIFIER_CONST, p.ASSIGN, p.expression, p.SCOLON)}

    @_('VOID_KEYWORD',
       'BOOL_KEYWORD',
       'INT_KEYWORD',
       'FLOAT_KEYWORD')
    def type_specifier(self, p):
        return { 'type' : p[0]}

    @_('type_specifier IDENTIFIER_CONST LPAREN function_parameters RPAREN compound_statement')
    def function_definition(self, p):
        return { 'function_definition' : (p.type_specifier, p.IDENTIFIER_CONST, p.LPAREN, p.function_parameters, p.RPAREN, p.compound_statement)}

    @_('type_specifier IDENTIFIER_CONST LPAREN RPAREN compound_statement')
    def function_definition(self, p):
        return { 'function_definition' : (p.type_specifier, p.IDENTIFIER_CONST, p.LPAREN, p.RPAREN, p.compound_statement)}

    @_('parameter_list')
    def function_parameters(self, p):
        return { 'function_parameters' : (p.parameter_list)}

    @_('parameter COMMA parameter_list')
    def parameter_list(self, p):
        return { 'parameter_list' : (p.parameter, p.COMMA, p.parameter_list)}

    @_('parameter')
    def parameter_list(self, p):
        return { 'parameter' : (p.parameter)}

    @_('type_specifier IDENTIFIER_CONST')
    def parameter(self, p):
        return { type_specifier['type'] : p.IDENTIFIER_CONST }  # smth like { int : x }

    @_('stmt stmt_list')
    def stmt_list(self, p):
        return { 'statements' : (p.stmt, p.stmt_list)}

    @_('stmt')
    def stmt_list(self, p):
        return { 'statement' : p.stmt }

    @_('if_else_variant_stmt')
    def stmt(self, p):
        return { 'conditional statement' : p.if_else_variant_stmt }

    @_('non_if_else_variant_stmt')
    def stmt(self, p):
        return { 'non conditional statement' : p.non_if_else_variant_stmt }

    @_('expression_statement')
    def non_if_else_variant_stmt(self, p):
        return { 'full expression statement' : p.expression_statement }

    @_('compound_statement')
    def non_if_else_variant_stmt(self, p):
        return { 'compound_statement' : p.compound_statement }

    @_('iteration_statement')
    def non_if_else_variant_stmt(self, p):
        return { 'iteration_statement' : p.iteration_statement }

    @_('jump_statement')
    def non_if_else_variant_stmt(self, p):
        return { 'jump_statement' : p.jump_statement }

    @_('local_decl')
    def non_if_else_variant_stmt(self, p):
        return { 'local_decl' : p.local_decl }

    @_('expression SCOLON')
    def expression_statement(self, p):
        return (p.expression, p.SCOLON)   # careful

    @_('SCOLON')
    def expression_statement(self, p):
        return (p.SCOLON)   # careful

    @_('WHILE LPAREN boolean_expression RPAREN compound_statement')
    def iteration_statement(self, p):
        return { 'iteration_statement' : (p.WHILE, p.LPAREN, p.boolean_expression, p.RPAREN, p.compound_statement)}

    @_('LCURLY stmt_list RCURLY')
    def compound_statement(self, p):
        return { 'compound_statement' : (p.LCURLY, p.stmt_list, p.RCURLY)}

    @_('type_specifier IDENTIFIER_CONST SCOLON')
    def local_decl(self, p):
        # store the undefined variable in our variable store for local declarations.
        # But with a NULL value associated with it
        self.local_identifiers[p.IDENTIFIER_CONST] = None
        return { 'local_variable_declaration' : (p.type_specifier, p.IDENTIFIER_CONST, p.SCOLON)}

    @_('type_specifier IDENTIFIER_CONST ASSIGN expression SCOLON')
    def local_decl(self, p):
        self.local_identifiers[p.IDENTIFIER_CONST] = p.expression  # create a new instance of "name" : expr in the class CalcParser
        return { 'local_variable_definition' : (p.type_specifier, p.IDENTIFIER_CONST, p.ASSIGN, p.expression, p.SCOLON)}

    @_('return_stmt')
    def jump_statement(self, p):
        return { 'return_stmt' : p.return_stmt}

    @_('break_stmt')
    def jump_statement(self, p):
        return { 'break_stmt' : p.break_stmt}

    @_('RETURN_KEYWORD SCOLON')
    def return_stmt(self, p):
        return (p.RETURN_KEYWORD, p.SCOLON)

    @_('RETURN_KEYWORD expression SCOLON')
    def return_stmt(self, p):
        return (p.RETURN_KEYWORD, p.expression, p.SCOLON)

    @_('BREAK SCOLON')
    def break_stmt(self, p):
        return (p.BREAK, p.SCOLON)

    @_('IF LPAREN boolean_expression RPAREN compound_statement')
    def if_else_variant_stmt(self, p):
        return (p.IF, p.LPAREN, p.boolean_expression, p.RPAREN, p.compound_statement)

    @_('IF LPAREN boolean_expression RPAREN compound_statement ELSE compound_statement')
    def if_else_variant_stmt(self, p):
        return (p.IF, p.LPAREN, p.boolean_expression, p.RPAREN, p.compound_statement, p.ELSE, p.compound_statement)

    @_('arithmetic_expression')
    def expression(self, p):
        return {"arithmetic_expression" : p[0] }

    @_('boolean_expression')
    def expression(self, p):
        return {"boolean_expression" : p[0] }

    @_('relational_boolean_expression')
    def boolean_expression(self, p):
        return {"relational_boolean_expression" : p[0] }

    @_('logical_boolean_expression')
    def boolean_expression(self, p):
        return {"logical_boolean_expression" : p[0] }

    @_('IDENTIFIER_CONST ASSIGN arithmetic_expression')
    def arithmetic_expression(self, p):
        if p.IDENTIFIER_CONST in self.local_identifiers:
            self.local_identifiers['IDENTIFIER_CONST'] = p.arithmetic_expression
            return (p.IDENTIFIER_CONST, p.ASSIGN, p.arithmetic_expression)

        else :
            self.identifiers['IDENTIFIER_CONST'] = p.arithmetic_expression
            return (p.IDENTIFIER_CONST, p.ASSIGN, p.arithmetic_expression)

    @_('meta_term')
    def arithmetic_expression(self, p):
        return { "meta_term" : p.meta_term}

    @_('meta_term PLUS term',
       'meta_term MINUS term')
    def meta_term(self, p):
        return (p.meta_term, p[0], p.term)

    @_('term')
    def meta_term(self, p):
        return p.term      # careful...

    @_('term TIMES factor',
       'term DIVIDE factor',
       'term MODULUS factor')
    def term(self, p):
        return (p.term, p[1], p.factor)

    @_('factor')
    def term(self, p):
        return p.factor      # careful...

    @_('LPAREN arithmetic_expression RPAREN')
    def factor(self, p):
        return (p.LPAREN, p.arithmetic_expression, p.RPAREN)      # careful...

    @_('IDENTIFIER_CONST')
    def factor(self, p):
        return {p.IDENTIFIER_CONST : self.identifiers['p.IDENTIFIER_CONST']  }  #careful...

    @_('number')
    def factor(self, p):
        return (p.number)

    @_('INT_CONSTANT')
    def number(self, p):
        return {"Integer" : p.INT_CONSTANT}

    @_('FLOAT_CONSTANT')
    def number(self, p):
        return {"Float" : p.FLOAT_CONSTANT}







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

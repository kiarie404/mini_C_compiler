
from sly import Lexer
import json

class CalcLexer(Lexer):
    tokens = { NON_TERMINAL, TERMINAL, ARROW, OR}

    # String containing ignored characters between tokens
    ignore = '\t'
    ignore_whitespace = '\s+'
    ignore_comments = '\#.'

    # Regular expression rules for tokens
    NON_TERMINAL = r'<[a-zA-Z_][a-zA-Z0-9_]*>'
    TERMINAL = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ARROW = '::='
    OR = '\|'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
        return t

if __name__ == '__main__':
    src_file = open("original_BNF.txt")
    # json_out_file = open("extracted_json_BNF.json","w")   # it is in json in order to facilitate transfer of data
    txt_out_file = open("extracted_txt_BNF.txt","w")   # it is in txt in order to facilitate readability, writing pretty json is not a park walk
    lexer = CalcLexer()

    # count = 1
    indent = 4  # spacing in the extracted BNF
    class Terminal_object:
        def __init__(self, name):
            self.name = name

    class Non_terminal_object:
        def __init__(self, name):
            self.name = name


    # every BNF has productions.
    # all productions have a left_portion and right_portion
    # the left_portion contains a non-terminal
    # the right_portion contains one or more statements that contain both terminals and non-terminals.
    class Production:
        #instance attribute.
        def __init__(self, a_unit):
            self.left_non_terminal = a_unit  # which is of class unit
            self.statements = []     # comprises of objects of type STMT

        # how to convert Production into class 'dict', useful for json serialization
        def as_dict(self):
            # self.statements comprises of objects of type STMT
            # objects of type STMT are arrays that contain Unit class objects
            # else we wont be able to print self.statements as a whole
            # so we crete a copy array.
            copy_of_self_statements = self.statements
            # we convert each of the arrays components into dicts, since the compiler cant do this implicitly.
            for element in copy_of_self_statements:
                element = element.as_dict()

            return { "first_non_terminal" : self.left_non_terminal.as_dict(),
                      "statements" : copy_of_self_statements
                }

    class Unit:                # a unit can either be a terminal or nonterminal token
        #instance attribute.
        def __init__(self, type, name):
            self.type = type        # each token has a type eg "Terminal"
            self.name = name      # each token has a value eg "add_sign"

        # how to convert Unit into class 'dict', useful for json serialization
        def as_dict(self):
            return { self.type : self.name }


    class STMT:                #
        #instance attribute.
        def __init__(self):
            self.string_of_units = []

        # how to convert STMT into class 'dict', useful for json serialization
        def as_dict(self):
            return { "STMT" : self.string_of_units }

        def append(self, some_unit):
            self.string_of_units.append(some_unit)

    array_of_productions = [] # an empty array of productions.
    current_production_index = -1 # this value will increment the moment we detect a new production.
                                  # a new production is detected if a line begins with a non_terminal instead if the "|" sign
    current_STMT_index = -1
    current_statement_index = -1

    for line in src_file:                             # parse the source file line by line.
        # we will navigate the file line by line.
        # we will tokenize each line as follows
        for count, token in enumerate(lexer.tokenize(line)):
            # each line can begin with either a non_terminal or the "|" sign.
            # hence we have the if ... else stmt below
            if (count == 0 and token.type == "NON_TERMINAL"):
                # if the first term is a nonterminal, then that means we are handling a new production.
                current_production_index = current_production_index + 1
                print(current_production_index)
                # create a new instance of the class "Unit" to store the first non-terminal.
                first_non_terminal = Unit(token.type, token.value)
                # create a new instance of the class "Production"
                # then add that first non-terminal to the current productions left_portion
                temporary_production = Production(first_non_terminal)
                # add our new production to the array of productions
                array_of_productions.append(temporary_production)


            elif (count == 1 and token.type == "ARROW"):
                # if we meet the arrow, we just ignore it
                # this also means that , we are meeting our first statement for our production.
                # so we create an empthy statement in our production
                current_statement_list = [] # it should contain STMTs but it is currently empty...
                array_of_productions[current_production_index].statements.append(current_statement_list)
                current_statement_index = current_statement_index + 1



            elif (count > 1 ):
                # under this option , we will find both terminals and non_terminals
                # crete an instance of the 'Unit' class
                temporary_unit = Unit(token.type, token.value)
                # append it to the current STMT of the current production.
                array_of_productions[current_production_index].statements.append(temporary_unit)

            elif (count == 0 and token.type == "OR"):
                # if the first term is an OR sign, It means that we are handling the same old production.
                # It also means that we are dealing with another STMT variation of the current production
                current_STMT_index = current_STMT_index + 1

    # print(current_production_index)  #test
    for production in array_of_productions:
        print(production.as_dict())

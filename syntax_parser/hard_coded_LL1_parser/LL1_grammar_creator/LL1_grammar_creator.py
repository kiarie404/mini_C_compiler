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
    #class attribute
        # no class attributes

    #instance attribute.
    def __init__(self, left_portion, right_portion):
        self.left_portion = left_portion
        self.right_portion = right_portion

# a production has a right side.
# that right side might contain several mini-stmts seperated by OR operands
# hence we store these many productions in a list.
class Production_right_portion:
    # class attributes
        # no class attributes at the moment.

    # instance attributes
    def __init__(self):
        self.statements = []  # we store the statements . items in this array are of Statement class

    #methods
    def add_element(self, some_statement):
        self.statements.append(some_statement)

# a statement is found as part of the right side of a production
# for example : in the production S --> Ab || c
# there are 2 statements : (Ab)  and c
# as seen, a statement is made uo of terminals and nonterminals
class Statement:
    def __init__(self):
        self.string_of_terminals_and_non_terminals = [] # items in this array are of Terminal_object class and Non_terminal_object class

    #methods
    def add_element(self, some_term):
        self.string_of_terminals_and_non_terminals.append(some_term)




##########################  testing if we can safely store productions ####################

# tesing the production :  <identifier> ::= constant_identifier
NT1 = Non_terminal_object("identifier")
T1  = Terminal_object("constant_identifier")

stmt_1 = Statement()
stmt_1.string_of_terminals_and_non_terminals.append(T1)

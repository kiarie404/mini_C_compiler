# rule_index = 0
statement ::= NAME ASSIGN expr  # index = 0.1
           |  expr # index = 0.2

# rule_index = 1
expr      ::= expr PLUS expr    # index = 1.1
           |  expr MINUS expr   # index = 1.2
           |  expr TIMES expr   # index = 1.3
           |  expr DIVIDE expr  # index = 1.4
           |  LPAREN expr RPAREN    # index = 1.5
           |  NUMBER    # index = 1.6
           |  NAME      # index = 1.7

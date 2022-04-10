statement ::= NAME ASSIGN expr
           |  expr

expr      ::= expr PLUS expr
           |  expr MINUS expr
           |  expr TIMES expr
           |  expr DIVIDE expr
           |  LPAREN expr RPAREN
           |  NUMBER
           |  NAME

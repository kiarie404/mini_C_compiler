document is stored as an array

let us use the BNF below :
    S ::= Ab
       |  Cb

    A ::= aA
    C ::= cC

This will be stored as :
[
    { S : [ [A, b], [C, b] ]  },
    { A : [ [a, A] ]  },
    { C : [ [a, C] ]  }
]

where terminals and nonterminals are stored as objects of the form :

   {  'status' : 'value' }   or "value"

For example   A == { "non_terminal" : 'A'}  ***** this rule applies to any non_terminal that appears on the right side of a production statement
              b == { "terminal" : "b" }
              S == "S"    ***** this rule applies to any non_terminal that appears on the left side of a production statement

Now the difference with yours here is that we avoid having a dict within a dict, this way we can use same intuitive keys without getting errors.
For example , the dict below will give an error in json
    {"non_terminal": "s" {"non_terminal": "W"} }

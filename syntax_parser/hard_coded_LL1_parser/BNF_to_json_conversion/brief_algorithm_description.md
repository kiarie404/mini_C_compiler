The main goal of the algorithm is to convert an BNF grammar into a json object.
In future, I hope This algorithm will convert a BNF to a yaml file , A .yaml is more readable.
We are converting the BNF into serialized data formats, so that we can easily hack the BNF through code
Hacking means to : remove left recursion and left factoring in a program

For example :

  If we have the BNF :
    <S> ::= <A>b
         |  <A>c

    <A> ::= a

  The resulting json file will be:
  {"productions": [
      {
        "left_non_terminal" : {"type" : "non_terminal", "value" : "S"},
        "right_side_stmts"  : [
          [{"type" : "non_terminal", "value" : "A"}, {"type" : "terminal", "value" : "b"}],
          [{"type" : "non_terminal", "value" : "A"}, {"type" : "terminal", "value" : "c"}]
        ]
      },

      {
        "left_non_terminal" : {"type" : "non_terminal", "value" : "A"},
        "right_side_stmts"  : [
          [{"type" : "terminal", "value" : "a"}]
        ]
      }
    ]
  }

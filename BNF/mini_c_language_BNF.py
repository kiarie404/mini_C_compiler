
------------------------- part 1 : BNF (productions only) -------------------------------

<program> ::= <command_list>

<command_list> ::= <command> <command_list>
       	           | <command>

<command> ::=  <variable_declaration>
  	            | <function_definition>

<variable_declaration> ::= <type_specifier> <identifier> semi_colon_delimiter
           	 | <type_specifier> <identifier> assignment_operator <expression> semi_colon_delimiter

<identifier> ::= constant_identifier

<type_specifier> ::=      key_word_void
      	                | key_word_bool
      	                | key_word_int
      	                | key_word_float

<function_definition> ::= <type_specifier> <identifier> left_rounded_bracket <function_parameters> right_rounded_bracket <compound_statement>
                        | <type_specifier> <identifier> left_rounded_bracket  right_rounded_bracket <compound_statement>   # made function accept NULL as a parameter safely

<function_parameters> ::= <parameter_list>

<parameter_list> ::= <parameter> comma_delimiter <parameter_list>
        	| <parameter>

<parameter> ::= <type_specifier> <identifier>

<stmt_list> ::= <stmt> <stmt_list>
       	| <stmt>

<stmt>   ::= <if_else_variant_stmt>
          |  <non_if_else_variant_stmt>


<non_if_else_variant_stmt> ::= <expression_statement>
  	            | <compound_statement>
                | <iteration_statement>
  	            | <jump_statement>
                | <local_decls>


<expression_statement> ::= <expression> semi_colon_delimiter
       	| semi_colon_delimiter



<iteration_statement> ::= key_word_while  left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement>


<compound_statement> ::= left_curly_bracket <stmt_list> right_curly_bracket


<local_decls> ::= <local_decl> <local_decls>
         	| <local_decl>

<local_decl> ::= <type_specifier> <identifier> semi_colon_delimiter
               | <type_specifier> <identifier> assignment_operator <expression> semi_colon_delimiter

<jump_statement> ::= <return_stmt>
        	         | <break_stmt>

<return_stmt> ::= key_word_return semi_colon_delimiter
                | key_word_return <expression> semi_colon_delimiter

<break_stmt>  ::= key_word_break semi_colon_delimiter

<if_else_variant_stmt>  ::= key_word_if left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement>
                         |  key_word_if left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement> key_word_else <compound_statement>

<expression> ::= <arithmetic_expression>  # includes both floats and int operations . A number is a number! ... whether a float or int.
              |  <boolean_expression>     # logical operations


<boolean_expression> ::= <relational_boolean_expression>   # A relational expression is an expression used to compare two operands. eg 2 < 3
                      |  <logical_boolean_expression>      # that make decisions  eg (sunny && windy) || !(rainy)


<arithmetic_expression> ::=  <identifier> assignment_operator <arithmetic_expression>  # to suppors an expression like x = y = z = 2+3(2*4)
                         |   <meta_term>    # smth like 2+3(2*4)

<meta_term>    ::=  <meta_term> addition_operator <term>
                  | <meta_term> subtraction_operator <term>
                  | <term>

<term>          ::=  <term> multiplication_operator <factor>
                  | <term> division_operator <factor>
                  | <term> modulus_operator <factor>
                  | <factor>

<factor>        ::=  right_rounded_bracket arithmetic_expression left_rounded_bracket
                  | subtraction_operator <factor>
                  | addition_operator <factor>
                  | <identifier>
                  | <number>

<number>  ::= constant_int
           |  constant_float

<relational_boolean_expression>  ::= <arithmetic_expression> <comparison_sign> <arithmetic_expression>

<comparison_sign>       ::= less_than_sign
                         |  greater_than_sign
                         |  equivalent_to_sign
                         |  inequivalent_to_sign
                         |  greater_than_or_equal_to_sign
                         |  less_than_or_equal_to_sign

<logical_boolean_expression>  ::=  <identifier> assignment_operator <logical_boolean_expression>  # to support smth like bool x = y = z = !(2<3) && (1==0)
                               |   <intermediate_logic_term>    #smth like !(rainy )

<intermediate_logic_term>   ::= left_rounded_bracket <basic_logic_term> <logical_sign> <basic_logic_term> right_rounded_bracket

<basic_logic_term>  ::=  left_rounded_bracket <relational_boolean_expression>  right_rounded_bracket
                      |   logical_NOT_sign left_rounded_bracket <relational_boolean_expression>  right_rounded_bracket
                      |   constant_bool
                      |   left_rounded_bracket   <intermediate_logic_term>  right_rounded_bracket

------------------------- part 1 : end of BNF (productions only) ------------------------
------------------------- part 2 : Terminals used and their regex -------------------------------
#tokens for keywords
  key_word_int = "^int$"
  key_word_float = "^float$"
  key_word_bool = "^bool$"
  key_word_void = "^void$"
  key_word_return = "^return$"
  key_word_while = "^while$"
  key_word_if = "^if$"
  key_word_else = "^else$"
  key_word_break = "^break$"


#tokens for constants
  constant_int = "^[\+\-]{0,1}\d+$"             # integers can be signed or unsigned
  constant_float = "^[\+\-]{0,1}\d+\.{1}\d+$"   # floats can be signed or unsigned
  constant_bool = "^(true|false|TRUE|FALSE)$"
  constant_identifier ="^[a-zA-Z_][a-zA-Z0-9_]*"


#tokens for logical signs
  equivalent_to_sign = "^==$"
  inequivalent_to_sign = "^!=$"
  less_than_sign = "^<$"
  greater_than_sign = "^>$"
  greater_than_or_equal_to_sign = "^>=$"
  less_than_or_equal_to_sign = "^<=$"
  logical_NOT_sign = "^!$"
  logical_OR_sign = "^\|\|$"
  logical_AND_sign = "^&&$"

#tokens for delimiters
  semi_colon_delimiter = "^;$"
  comma_delimiter      = "^,$"
  right_rounded_bracket = "^\)$"
  left_rounded_bracket = "^\($"
  left_curly_bracket = "^\{$"
  right_curly_bracket = "^\}$"

#tokens for mathematical operators
  addition_operator = "^\+$"
  subtraction_operator = "^-$"
  division_operator = "^\/$"
  multiplication_operator = "\*$"
  modulus_operator = "^%$"
  assignment_operator= "^=$"

------------------------- end of part 2 : Terminals used and their regex  ------------------------

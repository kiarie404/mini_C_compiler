

This module aims to convert the token stream generated from the lexer into a json file.
In other words, it consumes the token_stream.txt file and outputs token_stream.json file.

The reason why we need to convert files into json files is so that we allow easy transfer of parsable data between different compiler modules

*************** folders ************
READ_ME
token_stream.txt
token_stream.json
BNF_to_json_convertion.py



***************  How the json file is structured ********************8

Take for example The following snippet of a token stream....

<'INT_KEYWORD'> --> 'int' <'IDENTIFIER'> --> 'an_int' <'ASSIGN'> --> '='  <'INT_CONSTANT'> --> '34' <'SCOLON'> --> ';'
<'FLOAT_KEYWORD'> --> 'float' <'IDENTIFIER'> --> 'a_float'  <'ASSIGN'> --> '='  <'FLOAT_CONSTANT'> --> '34.78'  <'SCOLON'> --> ';'

#How a token is defined

{0:["INT_KEYWORD","int"]}
#This is the structure of our tokens;
#The key of the dictionary is an index of type int,
#This index indicates the position of that particular token in that particular line.
#The token name and its value are stored in an array where the first element is the token name and the second value is the lexeme/Constant value
{1:["IDENTIFIER","an_int"]}
{2:["ASSIGN","="]}

#How a line is defined
[{0:["INT_KEYWORD","int"]},{1:["IDENTIFIER","an_int"]},{2:["ASSIGN","="]}]


#How a document is defined
#The document is made up of many lines
#Each line is stored as an element of a dictionary where the key is index of type int and its value is a line
{
    0:[{0:["INT_KEYWORD","int"]},{1:["IDENTIFIER","an_int"]},{2:["ASSIGN","="]}],
    1:[{0:["FLOAT_KEYWORD","float"]},{1:["IDENTIFIER","a_float"]},{2:["ASSIGN","="]}]
 }

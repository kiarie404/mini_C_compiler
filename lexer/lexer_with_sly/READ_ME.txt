This is the lexer.
The lexer scans the sample code and tokenizes the elements of that sample code.
It outputs a token stream .
The token stream is produced in two forms, for the sake of document compatibility :
  1. token_stream.txt
  2. token_stream.json


  
The reason why we need to convert files into json files is so that we allow easy transfer of parsable data between different compiler modules

**************  How to manipulate elements of the json file **********
  think of the example program :
    int main(){
      int num = 10 ;
    }

  The json document is imported as an array (list or tuple)
     like this in python :
       with open("token_stream.json", 'r') as source:
           a_list = json.load(source)

  To access the first line :  a_list[0]    ---> returns  [{"0": ["INT_KEYWORD", "int"]}, {"1": ["IDENTIFIER", "main"]}, {"2": ["LPAREN", "("]}, {"3": ["RPAREN", ")"]}, {"4": ["LCURLY", "{"]}]
  to access the second line : a_list[1]    ---> returns  [{"0": ["INT_KEYWORD", "int"]}, {"1": ["IDENTIFIER", "num"]}, {"2": ["ASSIGN", "="]}, {"3": ["INT_CONSTANT", "10"]}, {"4": ["SCOLON", ";"]}]

  To access the first token ie. int token                    : a_list[0][0]      ----> [INT_KEYWORD, int]
  To access the name of the first token as used in the BNF   : a_list[0][0][0]    ---> INT_KEYWORD
  To access the lexeme of the first token as used in the BNF : a_list[0][0][1]    ---> int



***************  How the output json file is structured ********************8

Take for example The following snippet of a token stream....

<'INT_KEYWORD'> --> 'int' <'IDENTIFIER'> --> 'an_int' <'ASSIGN'> --> '='  <'INT_CONSTANT'> --> '34' <'SCOLON'> --> ';'
<'FLOAT_KEYWORD'> --> 'float' <'IDENTIFIER'> --> 'a_float'  <'ASSIGN'> --> '='  <'FLOAT_CONSTANT'> --> '34.78'  <'SCOLON'> --> ';'

#How a token is defined

["INT_KEYWORD","int"]
#This is the structure of our tokens;
#The key of the dictionary is an index of type int,
#This index indicates the position of that particular token in that particular line.
#The token name and its value are stored in an array where the first element is the token name and the second value is the lexeme/Constant value
{1:["IDENTIFIER","an_int"]}
{2:["ASSIGN","="]}

#How a line is defined
[["INT_KEYWORD","int"],["IDENTIFIER","an_int"],["ASSIGN","="]]


#How a document is defined
#The document is made up of many lines
#Each line is stored as an element of a dictionary where the key is index of type int and its value is a line
[
    [[["INT_KEYWORD","int"],["IDENTIFIER","an_int"],["ASSIGN","="]]],
    [["FLOAT_KEYWORD","float"], ["IDENTIFIER","a_float"], ["ASSIGN","="] ]
 ]

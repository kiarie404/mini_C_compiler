#this is the pseudocode for

define a class called token_blueprint that has :
  a name;
  a regex;

define a class called token_instance that has :
  a name;
  lexeme;

define all token_blueprints and store them in an array.
run a test on the validity of the token_blueprints using the test cases provided.

If all the tests have passed , then continue.

######### order of precedence ###################
define a new array called ; order_of_precedence[] and statically store the token_blueprints in it in their order of precedence.

 #########  extraction of input ##################
 define an array of words.
 a word is anything seperated by \n or \t.

 read the test.c file and extract words from it.
 Store the extracted words in a 2d array called - words.
 The number of rows in words array == the number of lines in the test.c file.
 ######## end of extracting input ################

######### maximal munch algorithm ################
create a 2d array for token_instances.
traverse all the words one by one and
    run them against DFAs in the order of precedence.
        if a DFA turns true, create the respective token_instance, and store it in the 2d token_instance array
        if all DFAs turn false, create a token_instance with the name "ERROR".
 ######### end of maximal munch algorithm ################

 ######## print out the output file ######################
 print the token_instance 2d array to a file
 ######## end of print out the output file ######################

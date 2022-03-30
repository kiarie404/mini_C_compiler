The custom_bnf.txt file contains the CFG for the Mini-C language in Backus Naur form.

The file has been divided into 2 parts for the sake of modularity:
  1. Terminals used and their regex - plainly states the terminals used. defines the regular expression for each terminal term..
  2. BNF part - outline the production rules. the regular expressions for the terminals are not included in this section.

The custom_bnf will be used to make the lexer.

##### for the group ####
I will base my creation of the BNF based on this page; This is in regards to which expressions our Language has. : https://www.javatpoint.com/c-expressions

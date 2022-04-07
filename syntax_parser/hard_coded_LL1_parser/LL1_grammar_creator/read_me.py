This module consumes a BNF and produces an LL1 grammar :
  The LL1 grammar is a grammar that does not have :
    - Left factoring.
    - Left recursion.

The files in this module are :
    - LL1_grammar_creator.py - consumes a BNF and produces an equivalent LL1-grammar (no left factoring or left recursion)
    - LL1_grammar_checker.py - checks if the output from the LL1_grammar_creator.py is okay.

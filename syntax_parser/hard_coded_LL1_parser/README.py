# proposition of module arrangement by kiarie404
*** maybe we should use yaml instead of json in order to allow comments within the passed json text ***
*** but this can esily be solved by unanimously agreeing on the json format of various files *****

Let the LL1 parser have the following modules :
  
  - Input files
      - BNF.txt
      - token_stream.txt
      
  - Preparation_module
      - BNF_to_JSON_converter.py ---- > converts BNF.txt into a  BNF.json file
      - token_stream_to_JSON_converter.py ---- > converts token_stream.txt into a token_stream.json file
          
       output files of the Preparation module
          - BNF.json
          - token_stream.json
  - LL1_grammar_creator
      - Left_recursion_remover.py ----> consumes BNF.json and outputs BNF_without_left_recursion.json
      - left_factoring_remover.py ----> consumes BNF_without_left_recursion.json and outputs full_LL1_grammar_BNF.json
      
  - LL1_table_creator
      - generate_first_sets.py ---> consumes the full_LL1_grammar_BNF.json and outputs first_sets.json
      - generate_follow_sets.py ---> consumes the first_sets.json + full_LL1_grammar_BNF.json  and outputs full_LL1_symbol_table.json
      
  - parser
      - parser.py - consumes the token_stream.json + full_LL1_symbol_table.json and outputs syntax_tree.json
      - tree_generator.py ---> consumes the syntax_tree.json and displays a visual tree structure : (optional...since we can use online tree generators )
  

# proposition by : <insert your name here>


  

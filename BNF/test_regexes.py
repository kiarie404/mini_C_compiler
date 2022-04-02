# You can use this template to test the Regular expressions defined in the BNF

import re

pattern = "^-$"
test_string = '-'
result = re.match(pattern, test_string)

if result:
  print("Search successful.")
else:
  print("Search unsuccessful.")

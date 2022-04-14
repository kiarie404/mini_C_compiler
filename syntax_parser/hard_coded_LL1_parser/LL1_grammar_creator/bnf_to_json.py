def stringify_array(arr,start_num):
    txt = ""
    for item in range(start_num,len(arr)):
        txt += arr[item]
    return txt

def remove_newline(txt):
    new_txt = ""
    for ch in txt:
        if ch != '\n':
            new_txt += ch
    return new_txt

def is_last(arr,item):
    if arr.index(item) == (len(arr) - 1):
        return True
    else:
        return False

def prod_rule(arr):
    prod_rule = ""
    prod_rule += "\t\"productions\":{\n"
    txt = ""
    new_arr = []
    if len(arr) == 0:
        return None
    else:
        txt += stringify_array(arr,1)
    new_arr = txt.split(" ")
    for item in new_arr:
        if is_last(new_arr,item):
            if len(find_non_terminal(item)) != 0:
                prod_rule += "\t\t\"non_terminal\":\"{}\"\n".format(find_non_terminal(item))
            else:
                prod_rule += "\t\t\"terminal\":\"{}\"\n".format(remove_newline(item))
        else:
            if len(find_non_terminal(item)) != 0:
                prod_rule += "\t\t\"non_terminal\":\"{}\",\n".format(find_non_terminal(item))
            else:
                prod_rule += "\t\t\"terminal\":\"{}\",\n".format(remove_newline(item))
    
    prod_rule += "\t}\n"

    return prod_rule

def find_non_terminal(line):
    count = 0
    non_terminal = ""
    for ch in line:
        if count != 0 and ch != '>':
            non_terminal += ch
        if ch == '<':
            count = count + 1
        if ch == '>':
            count = count - 1
    return non_terminal

def bnf_json(line,out_file):
    json_str = ""
    prod = []
    prod = line.split(" ::= ")
    if(prod[0] != '\n'):
        json_str += "{\n"
        json_str += "\t\"non_terminal\":\"{}\",\n".format(find_non_terminal(prod[0])) 
        json_str += prod_rule(prod)
        json_str += "}\n"
        out_file.write(json_str)

in_file = open("bnf.txt","r")
out_file = open("bnf.json","w")

for line in in_file:
    bnf_json(line,out_file)

in_file.close()
out_file.close()
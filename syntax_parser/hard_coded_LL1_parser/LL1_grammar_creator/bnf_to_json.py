from sly import Lexer

def stringify_nt(nt):
    txt = ""
    for ch in nt:
        if ch != '<' and ch != '>':
            txt += ch
    return txt

def is_last(arr,item):
    if arr.index(item) == (len(arr) - 1):
        return True
    else:
        return False

def tok_type(val):
    if val == "NON_TERMINAL":
        return "non_terminal"
    else:
        return "terminal"

def check(val,arr):
    for item in arr:
        if item == val:
            return True
    return False

def get_rules(in_file):
    class CalcLexer(Lexer):
        tokens = { TERMINAL, NON_TERMINAL }

        ignore = ' \t'
        ignore_rule = '::='
        ignore_newline = '\n'

        TERMINAL      = r'[a-zA-Z_]+'
        NON_TERMINAL  = r'(<\w+>)+'
    lexer = CalcLexer()
    rules = []
    for line in in_file:
        rule = []
        for tok in lexer.tokenize(line):
            my_dict = {"token_type":tok.type,"token_value":tok.value}
            rule.append(my_dict)
        rules.append(rule)
    return rules

def prod(val,rules):
    arr_1 = []
    for rule in rules:
        arr_2 = []
        if len(rule) != 0:
            my_dict = rule[0]
            if my_dict["token_value"] == val:
                for i in range(1,len(rule)):
                    arr_2.append(rule[i])
                arr_1.append(arr_2)
    return arr_1

def jsonify(nt,prod_list):
    string = ""
    string += "\t\t{\n"
    string += "\t\t\t\"token_value\": \"{}\",\n".format(stringify_nt(nt))
    string += "\t\t\t\"productions\": [\n"
    for prod in prod_list:
        if is_last(prod_list,prod) and len(prod) != 0:
            string += "\t\t\t\t[\n"
            for item in prod:
                string += "\t\t\t\t\t{\n\t\t\t\t\t\t\"token_type\": \"%s\",\n"%(tok_type(item["token_type"]))
                string += "\t\t\t\t\t\t\"token_value\": \"%s\"\n"%(stringify_nt(item["token_value"]))
                if is_last(prod,item):
                    string += "\t\t\t\t\t}\n"
                else:
                    string += "\t\t\t\t\t},\n"
            string += "\t\t\t\t]\n"
        else:
            string += "\t\t\t\t[\n"
            for item in prod:
                string += "\t\t\t\t\t{\n\t\t\t\t\t\t\"token_type\": \"%s\",\n"%(tok_type(item["token_type"]))
                string += "\t\t\t\t\t\t\"token_value\": \"%s\"\n"%(stringify_nt(item["token_value"]))
                if is_last(prod,item):
                    string += "\t\t\t\t\t}\n"
                else:
                    string += "\t\t\t\t\t},\n"
            string += "\t\t\t\t],\n"
    string += "\t\t\t]\n\t\t},\n"
    return string

def left(rules):
    txt = ""
    arr = []
    lst = False
    for rule in rules:
        if len(rule) != 0:
            my_dict = rule[0]
            if not check(my_dict["token_value"],arr):
                arr.append(my_dict["token_value"])
                prods = prod(my_dict["token_value"],rules)
                txt += jsonify(my_dict["token_value"],prods)
    return txt

def bnf_json(rules,out_file):
    out = ""
    out += "{\n\t\"bnf\": [\n"
    out += left(rules)
    out += "\t]\n}"
    out_file.write(out)

if __name__ == '__main__':
    in_file = open("bnf.txt","r")
    out_file = open("bnf_test.json","w")

    bnf_json(get_rules(in_file),out_file)

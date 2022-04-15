import json

# Reading the bnf.json file
def getBNFJSON(Hardcoded_LL1BNFjson):
    with open('Hardcoded_LL1\BNF.json', 'r') as fp:
        return json.load(fp)

def removeLeftRecursion(rulesDict):
    # to store the new rules to be added in the file
    store = {}
    # traverse over rules
    #divide the rules into two the ones that have left recursion and the ones without
    for lhs in rulesDict:
        alphaRules = []
        betaRules = []
        # get righthandside for current lefthandside
        allrhs = rulesDict[lhs]
        for subrhs in allrhs:
            if subrhs[0] == lhs:
                alphaRules.append(subrhs[1:])
            else:
                betaRules.append(subrhs)
        # now form two new rules
        if len(alphaRules) != 0:
            # to generate new unique symbol
            lhs_ = lhs + "'"
            while (lhs_ in rulesDict.keys()) \
                    or (lhs_ in store.keys()):
                lhs_ += "'"
            # make beta rule and alpha rule
            for b in range(0, len(betaRules)):
                betaRules[b].append(lhs_)
            rulesDict[lhs] = betaRules

            for a in range(0, len(alphaRules)):
                alphaRules[a].append(lhs_)
            alphaRules.append(['#'])
            # store in temp
            store[lhs_] = alphaRules
    # - after removing left recursion
    for left in store:
        rulesDict[left] = store[left]
    return rulesDict
#Writing on the BNF.json(updating it)
def pasteBNFJSON(Hardcoded_LL1BNFjson):
    with open('Hardcoded_LL1\BNF.json', 'w') as f:
        return json.dump(store,f,ensure_ascii=False)
        f.close()
#so basically here is where the problem is,I want to convert it into a new json file called BNF_without_recursion.json
# instead on writing on the old one (bnf.json) so we can have two files 

import tree_generator

width = 10

CodeOp = [ 'cd_LABEL', 'cd_UMINUS', 'cd_ASSIGN',
           'cd_ADD', 'cd_SUB', 'cd_MULT', 'cd_DIVIDE',
           'cd_DIV', 'cd_MOD', 'cd_OR', 'cd_AND', 'cd_NOT',
           'cd_LT', 'cd_LE', 'cd_GT', 'cd_GE', 'cd_EQ', 'cd_NE',
		   'cd_GOTO', 'cd_CALL', 'cd_APARAM', 'cd_FPARAM', 'cd_VAR',
           'cd_RETURN', 'cd_NOOP']

class Quadruple:
	def __init__(self, operation, arg1='', arg2='', result=''):
		self.operation = operation
		self.arg1 = arg1
		self.arg2 = arg2
		self.result = result

class Quint:
    # A class to hold a quintdruple (labels in front)
    def __init__(self,name=' ',operation=' ',arg1=' ',arg2=' ',result=' '):
        self.name = name
        self.operation = operation
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        global width
        if self.name == None: name = ''
        else: name = str(self.name).lower()
        if self.operation == None: operation = ''
        else:
            if self.operation == 'PLUS': operation = 'ADD'
            elif self.operation == 'MINUS': operation = 'SUB'
            else:
                operation = self.operation[3:]
        if self.arg1 == None:  arg1= ''
        else:  arg1= str(self.arg1).lower()
        if self.arg2 == None: arg2= ''
        else:  arg2 = str(self.arg2).lower()
        if self.result == None:  result= ''
        else:  result = str(self.result).lower()
        return name.rjust(8)+operation.rjust(10)+arg1.rjust(15)+arg2.rjust(15)+result.rjust(15)

class ThreeAddressCode:
	def __init__(self):
		# self.symbolTable = None
		self.allCode = []
        self.__quintList = []
		self.tempVarCount = 0
        self.__labels = 0

	def generateCode(self, operation, arg1, arg2, result):
		code = Quadruple(operation, arg1, arg2, result)
		self.allCode.append(code)

    def generateCall(self,entry,eList):
        # GenerateCall takes a list of variables as a parameters
        # and creates a line in the list for each variable in the list.
        # Finally it creates the call line where.

        for variable in eList:
            code = Quadruple('cd_APARAM',None,None,variable)
            self.allCode.append(code)

        code = Quadruple('cd_CALL',entry,None,None)
        self.allCode.append(code)

    def generateVariables(self,eList):
        for variable in eList:
            code = Quadruple('cd_VAR',None,None,variable)
            self.allCode.append(code)

    def generateFParams(self,eList):
        for variable in eList:
            code = Quadruple('cd_FPARAM',None,None,variable)
            self.allCode.append(code)

    def generateAParams(self,eList):
        for variable in eList:
            code = Quadruple('cd_APARAM',None,None,variable)
            self.allCode.append(code)

    def newLabel(self):
        self.__labels += 1
        labelName = 'lab'+str(self.__labels)
        return labelName

    def newTemp(self):
        self.tempVarCount += 1
        varName = 't'+str(self.tempVarCount)
        return varName

    def print_code(self):
        global width
        label = ''
        for code in self.allCode:
            if code.operation == 'cd_LABEL':
                label = '%s:'%code.result
            else:
                quint = Quint(label,code.op,code.arg1,code.arg2,code.result)
                self.__quintList.append(quint)
                label = ''
    print_code ()

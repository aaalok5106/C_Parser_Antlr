from gen.CVisitor import CVisitor


class MyCVisitor(CVisitor):
    def __init__(self):
        self.nodeCounter = 1
        self.crude_cfg = ""
        self.dataInNodesDict = dict()



    # def visitTranslationUnit(self, ctx):    # functions
    #     if(ctx.getChildCount() > 1):
    #         print("***")
    #         self.crude_cfg = self.crude_cfg + "[ " + str(ctx.children[1].children[0].children[1].children[0].children[0].getText())
    #         print(ctx.children[1].children[0].children[1].children[0].children[0].getText())    # function name
    #         if(ctx.children[1].children[0].children[1].children[0].getChildCount() > 3):
    #             print(self.nodeCounter, "\n", ctx.children[1].children[0].children[1].children[0].children[2].getText())  # function params     <------node
    #             self.crude_cfg = self.crude_cfg + "_" + str(self.nodeCounter)
    #             self.nodeCounter = self.nodeCounter + 1
    #         else:
    #             self.crude_cfg = self.crude_cfg + "_0"
    #         #print("***", ctx.children[1].children[0].children[1].getText())
    #         print("***")
    #         self.crude_cfg = self.crude_cfg + " [ "
    #         self.visit(ctx.children[1])
    #         self.crude_cfg = self.crude_cfg + " ]"
    #         self.crude_cfg = self.crude_cfg + " ]\n"
    #     else:
    #         print("***")
    #         self.crude_cfg = self.crude_cfg + "[ " + str(ctx.children[0].children[0].children[1].children[0].children[0].getText())
    #         print(ctx.children[0].children[0].children[1].children[0].children[0].getText())  # function name
    #         if (ctx.children[0].children[0].children[1].children[0].getChildCount() > 3):
    #             print(self.nodeCounter, "\n", ctx.children[0].children[0].children[1].children[0].children[2].getText())  # function params     <------node
    #             self.crude_cfg = self.crude_cfg + "_" + str(self.nodeCounter)
    #             self.nodeCounter = self.nodeCounter + 1
    #         else:
    #             self.crude_cfg = self.crude_cfg + "_0"
    #         #print("***", ctx.children[0].children[0].children[1].getText())
    #         print("***")
    #     self.crude_cfg = self.crude_cfg + " [ "
    #     self.visit(ctx.children[0])
    #     self.crude_cfg = self.crude_cfg + " ]"
    #     self.crude_cfg = self.crude_cfg + " ]\n"

    def visitFunctionDefinition(self, ctx):         # a particular function...
        self.crude_cfg = self.crude_cfg + "[ "
        for i in range(ctx.getChildCount()):
            self.visit(ctx.children[i])
        self.crude_cfg = self.crude_cfg + " ]" + "\n"

    def visitIterationStatement(self, ctx):     # dowhile, for, while
        if (str(ctx.children[0]) == "while"):
            print("----while_cond")
            self.crude_cfg = self.crude_cfg + "[ while_"
            self.visit(ctx.children[2])
            print("--while_true")
            self.crude_cfg = self.crude_cfg + "[ "
            self.visit(ctx.children[4])
            self.crude_cfg = self.crude_cfg + " ] "
            self.crude_cfg = self.crude_cfg + " ] "
        elif(str(ctx.children[0]) == "for"):
            print("----for_cond")
            self.crude_cfg = self.crude_cfg + "[ for_"
            self.visit(ctx.children[2].children[0])
            self.crude_cfg = self.crude_cfg.rstrip()
            self.crude_cfg = self.crude_cfg + "_"
            self.visit(ctx.children[2].children[2])
            self.crude_cfg = self.crude_cfg.rstrip()
            self.crude_cfg = self.crude_cfg + "_"
            self.visit(ctx.children[2].children[4])
            print("--for_true")
            self.crude_cfg = self.crude_cfg + "[ "
            self.visit(ctx.children[4])
            self.crude_cfg = self.crude_cfg + " ] "
            self.crude_cfg = self.crude_cfg + " ] "
        elif(str(ctx.children[0]) == "do"):
            print("----dowhile_cond")
            self.crude_cfg = self.crude_cfg + "[ while_"
            self.visit(ctx.children[4])
            print("--dowhile_true")
            self.crude_cfg = self.crude_cfg + "[ "
            self.visit(ctx.children[1])
            self.crude_cfg = self.crude_cfg + " ] "
            self.crude_cfg = self.crude_cfg + " ] "

    def visitSelectionStatement(self, ctx):     # switch, if
        if (str(ctx.children[0]) == "if"):
            print("----if_cond")
            self.crude_cfg = self.crude_cfg + "[ if_"
            self.visit(ctx.children[2])
            print("---if_true")
            self.crude_cfg = self.crude_cfg + "[ "
            self.visit(ctx.children[4])
            self.crude_cfg = self.crude_cfg + " ] "
            self.crude_cfg = self.crude_cfg + "[ "
            if (ctx.getChildCount()>5 and str(ctx.children[5]) == "else"):
                print("---if_false")
                self.visit(ctx.children[6])
            self.crude_cfg = self.crude_cfg + " ] "
            self.crude_cfg = self.crude_cfg + " ] "
        if (str(ctx.children[0]) == "switch"):
            print("----switch_cond")
            self.visit(ctx.children[2])
            print("---switch_cases:")
            self.visit(ctx.children[4])

    def visitDeclaration(self, ctx):
        if ctx.getChildCount() > 1:
            print(self.nodeCounter, "\n", self.getTerminals(ctx))                        # <------node
            self.crude_cfg = self.crude_cfg + str(self.nodeCounter) + " "
            self.dataInNodesDict[self.nodeCounter] = str(self.nodeCounter) + ".\n" + self.getTerminals(ctx)
            self.nodeCounter = self.nodeCounter+1

    def visitForDeclaration(self, ctx):
        if ctx.getChildCount() > 1:
            print(self.nodeCounter, "\n", self.getTerminals(ctx))                        # <------node
            self.crude_cfg = self.crude_cfg + str(self.nodeCounter) + " "
            self.dataInNodesDict[self.nodeCounter] = str(self.nodeCounter) + ".\n" + self.getTerminals(ctx)
            self.nodeCounter = self.nodeCounter + 1

    def visitAssignmentExpression(self, ctx):
        if ctx.getChildCount() > 1:
            print(self.nodeCounter, "\n", self.getTerminals(ctx))                        # <------node
            self.crude_cfg = self.crude_cfg + str(self.nodeCounter) + " "
            self.dataInNodesDict[self.nodeCounter] = str(self.nodeCounter) + ".\n" + self.getTerminals(ctx)
            self.nodeCounter = self.nodeCounter + 1

    def visitExpression(self, ctx):
        #if ctx.getChildCount() > 1:
        print(self.nodeCounter, "\n", self.getTerminals(ctx))                        # <------node
        self.crude_cfg = self.crude_cfg + str(self.nodeCounter) + " "
        self.dataInNodesDict[self.nodeCounter] = str(self.nodeCounter) + ".\n" + self.getTerminals(ctx)
        self.nodeCounter = self.nodeCounter + 1

    def visitForExpression(self, ctx):
        #if ctx.getChildCount() > 1:
        print(self.nodeCounter, "\n", self.getTerminals(ctx))                        # <------node
        self.crude_cfg = self.crude_cfg + str(self.nodeCounter) + " "
        self.dataInNodesDict[self.nodeCounter] = str(self.nodeCounter) + ".\n" + self.getTerminals(ctx)
        self.nodeCounter = self.nodeCounter + 1

    def visitJumpStatement(self, ctx):
        if ctx.getChildCount() > 1:
            print(self.nodeCounter, "\n", self.getTerminals(ctx))                        # <------node
            self.crude_cfg = self.crude_cfg + str(self.nodeCounter) + " "
            self.dataInNodesDict[self.nodeCounter] = str(self.nodeCounter) + ".\n" + self.getTerminals(ctx)
            self.nodeCounter = self.nodeCounter + 1

    def visitLabeledStatement(self, ctx):
        if str(ctx.children[0]) == "case":
            print("--case : ", self.getTerminals(ctx.children[1]))
            print(self.nodeCounter, "\n", self.getTerminals(ctx.children[1]))                        # <------node
            self.dataInNodesDict[self.nodeCounter] = str(self.nodeCounter) + ".\n" + self.getTerminals(ctx.children[1])
            self.nodeCounter = self.nodeCounter + 1
            self.visit(ctx.children[3])
        if str(ctx.children[0]) == "default":
            print("--default : ")
            self.visit(ctx.children[2])




    def getTerminals(self, ctx):
        if ctx==None:
            return ""
        c = ctx.getChildCount()
        if c==0:
            return str(ctx) + " "
        else:
            res = ""
            for i in range(c):
                res = res + self.getTerminals(ctx.children[i])
            return res
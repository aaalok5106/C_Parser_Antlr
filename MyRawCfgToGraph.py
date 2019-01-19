
class MyRawCfgToGraph():

    def __init__(self):
        self.j_counter = 1  #jump nodes = 1  # jump nodes
        self.dot_str = ""	#string for dot file

    def execute(self, rawCfg):
        rawCfg = rawCfg.replace("  ", " ")
        rawCfg = rawCfg.strip()
        tokens = rawCfg.split(" ")

        f, l = self.cfgReader(tokens, 0, len(tokens) - 1)
        self.dot_str = "\n\tstart -> " + f + ";" + self.dot_str + "\n\t" + l + " -> exit;"
        self.dot_str = "# dot file created at runtime\n" + "\ndigraph G {" + self.dot_str
        self.dot_str = self.dot_str + "\n\n\tstart [shape=Msquare, color=green];\n\texit [shape=Msquare, color=red];\n}"

    def getDescriptedGraph(self, rawCfg, dataInNodesDict):
        rawCfg = rawCfg.replace("  ", " ")
        rawCfg = rawCfg.strip()
        tokens = rawCfg.split(" ")

        f, l = self.cfgReader(tokens, 0, len(tokens) - 1)
        self.dot_str = "\n\tstart -> " + f + ";" + self.dot_str + "\n\t" + l + " -> exit;"
        self.dot_str = "# dot file created at runtime\n" + "\ndigraph G {" + self.dot_str
        for i in dataInNodesDict.keys():
            self.dot_str = self.dot_str + "\n\t" + str(i) + "[ label=\"" + str(dataInNodesDict[i]) + "\" ]"
        self.dot_str = self.dot_str + "\n\n\tstart [shape=Msquare, color=green];\n\texit [shape=Msquare, color=red];\n}"


    def cfgReader(self, tokens, s, e):
        # assumming : we get string of form [---] here, strictly
        s = s + 1  # start
        e = e - 1  # end
        current = s
        a = "-1"  # maintain parent
        re = "-1"  # maintain return_end
        rs = "-1"  # maintain return_start
        while current <= e:
            # case_0
            if tokens[current] == "[":
                curr2 = self.utilBracketMatcher(tokens, current)
                f, l = self.cfgReader(tokens, current, curr2)  # returns (first, last)
                current = curr2 + 1
                # connecting parent
                if (a != "-1"):
                    self.connect(a, f)
                # a
                a = l
                # rs
                if (rs == "-1"):
                    rs = f
                # re
                re = l
            # case_1
            elif tokens[current].isdigit() == True:
                # rs
                if (rs == "-1"):
                    rs = tokens[current]
                # connecting parent
                if (a != "-1"):
                    self.connect(a, tokens[current])
                while tokens[current + 1].isdigit() == True and current + 1 <= e:
                    self.connect(tokens[current], tokens[current + 1])
                    current = current + 1
                current = current + 1
                # a
                a = tokens[current - 1]
                # re
                re = a
            # print (" rs = ", rs, " , re = ", re)
            # case_2
            elif tokens[current].split("_")[0] == "if":
                temp = tokens[current].split("_")[1]
                self.reshapeNodeStyle(temp, "diamond", "orange")
                # connecting parent
                if (a != "-1"):
                    self.connect(a, temp)
                current = current + 1
                curr2 = self.utilBracketMatcher(tokens, current)
                f1, l1 = self.cfgReader(tokens, current, curr2)
                current = curr2 + 1
                curr2 = self.utilBracketMatcher(tokens, current)
                f2, l2 = self.cfgReader(tokens, current, curr2)
                # print (" rs = ", rs, " , re = ", re, " , a = ", a)
                # print (" f1 = ", f1, " , l1 = ", l1, ", f2 = ", f2, ", l2 = ", l2)
                current = curr2 + 2  # <<---note : [ if_XX [ ][ ] ]
                self.connect(temp, f1, "if_true")  # green
                # handle empty else...
                if (f2 != "-1"):
                    self.connect(temp, f2, "if_false")  # red
                # rs
                if (rs == "-1"):
                    rs = temp
                # re & j
                re = "J" + str(self.j_counter)  # self.j_counter=1 GLOBALLY
                self.j_counter = self.j_counter + 1
                self.reshapeNodeStyle(re, "square", "grey")
                self.connect(l1, re)
                # handle empty else...
                if (l2 != "-1"):
                    self.connect(l2, re)
                else:
                    self.connect(temp, re, "if_false")
                # a
                a = re
            # case_3
            elif tokens[current].split("_")[0] == "while":
                temp = tokens[current].split("_")[1]
                self.reshapeNodeStyle(temp, "diamond", "orange")
                current = current + 1
                curr2 = self.utilBracketMatcher(tokens, current)
                f, l = self.cfgReader(tokens, current, curr2)
                current = curr2 + 2  # <<---note : [ while_XX [ ][ ] ]
                self.connect(temp, f, "while_true")
                # print (" rs = ", rs, " , re = ", re, " , a = ", a)
                # j
                j_temp = "J" + str(self.j_counter)
                self.j_counter = self.j_counter + 1
                # if(a != "-1"):		# a always remains "-1" here
                #	self.connect(a, j_temp)
                self.connect(j_temp, temp)
                self.reshapeNodeStyle(j_temp, "square", "grey")
                self.connect(l, j_temp)
                # rs
                if (rs == "-1"):
                    rs = j_temp
                # re
                re = temp
                # a
                a = temp

        # return
        # print (" rs = ", rs, " , re = ", re)
        return rs, re



    def connect(self, x, y, param=""):
        self.dot_str = self.dot_str + "\n\t" + x + " -> " + y + " "
        if (param == "if_true" or param == "while_true"):
            self.dot_str = self.dot_str + "[color=green] ;"
        elif param == "if_false" or param == "while_false":
            self.dot_str = self.dot_str + "[color=red] ;"
        else:
            self.dot_str = self.dot_str + ";"


    def reshapeNodeStyle(self, node, shape, color):
        self.dot_str = self.dot_str + "\n\t" + node + " [shape=" + shape + ", color=" + color + "] ;"


    def utilBracketMatcher(self, tokens, i):
        c = 1
        while True:
            i = i + 1
            if (tokens[i] == "]"):
                c = c - 1
            if (tokens[i] == "["):
                c = c + 1
            if (c == 0):
                return i


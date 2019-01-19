import sys
from inspect import signature
from subprocess import call

from antlr4 import *

from MyCVisitor import MyCVisitor
from MyRawCfgToGraph import MyRawCfgToGraph
from gen.CLexer import CLexer
from gen.CParser import CParser


def main(argv):
    c_fileName = "gen/inputdata/"+argv[1]
    input = FileStream(c_fileName)
    lexer = CLexer(input)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.compilationUnit()
    #ast = tree.toStringTree(recog=parser)
    #print("\n\n", signature(tree.toStringTree), "\n")
    #print(ast, "\n\n")

    # file = open('ggg.md', 'w')
    # file.write(ast)
    # file.close()

    # listener
    #listener = MyCListener(parser)
    #walker = ParseTreeWalker()
    #walker.walk(listener, tree)
    #print(listener.getData(tree))

    v = MyCVisitor()
    v.visit(tree)

    print("\n\n\n", v.crude_cfg)

    d = MyRawCfgToGraph()
    #d.execute(v.crude_cfg)
    d.getDescriptedGraph(v.crude_cfg, v.dataInNodesDict)

    filename = "cprogram.dot"
    file = open(filename, 'w')
    file.write(d.dot_str)
    file.close()

    call(["dot", "-Tpng", "-o", filename + ".png", filename])
    call(["eog", filename + ".png"])




if __name__ == '__main__':
    main(sys.argv)


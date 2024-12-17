from select import select

class NodeIdent:
    def __init__(self , variable):
        self.var = variable

class NodeInt:
    def __init__(self , Constant):
        self.constant = Constant

class NodeExpr:
    def __init__(self , Int):
        self.NodeInt = Int

class NodeStmt:
    def __init__(self , Expr):
        self.NodeExpr = Expr

class NodeFunc:
    def __init__(self, Ident , Stmt):
        self.NodeIdent = Ident
        self.NodeStmt = Stmt

class NodeProg:
    def __init__(self , Func):
        self.NodeFunc = Func

class Parser :

    def __init__(self , tokens):
        self.tokens = tokens
        self.cur_idx = 0

    def parseInt(self):
        nodeInt = NodeInt(self.peek())
        return nodeInt

    def parseIdent(self):
        nodeIdent = NodeIdent(self.peek())
        return nodeIdent

    def parseExpr(self):
        nodeInt = self.parseInt()
        return NodeExpr(nodeInt)


    def parseStmt(self):
        #Experession is : 'return'  <expr>  ';'

        ##check return token
        token = self.peek()
        if (token == None or token[0] != "KEYWORD" or token[1] != "return") :
            raise SyntaxError(f"Enta ya ema nasi elreturn ya ema katebha 8lt ;)")
        self.consume()

        ##check <expr> token
        token = self.peek()
        if (token == None or token[0] != "CONSTANT") :
            raise SyntaxError(f"Yasta y5rebet elde7k ent nsit digit b3d el return stmt fe {self.cur_idx}")
        nodeExpr = self.parseExpr()
        nodeStmt = NodeStmt(nodeExpr)
        self.consume()

        ##check ';' token
        token = self.peek()
        if (token == None or token[0] != 'SEMICOLON') :
            raise SyntaxError(f"pls yasta rkz myn34 tensa el ';' abadn fe {self.cur_idx}")
        self.consume()

        return nodeStmt


    def parseFunc(self):
        ## Function is : 'int' <identifier> '(' 'void' ')' '{' <statement> '}'

        #check int keyword token
        token = self.peek()
        if (token == None or token[0] != "KEYWORD" or token[1] != "int") :
            raise SyntaxError("fel el function parsing lazem tbd2 be int keyword")
        self.consume()

        #check identefier token
        token = self.peek()
        if (token == None or token[0] != "IDENTEFIER") :
            raise SyntaxError("T3reef ay function lazem b3d eldata type ykon fe esm leha")
        nodeIdent = self.parseIdent()
        self.consume()

        # check '(' token
        token = self.peek()
        if (token == None or token[0] != "OPEN_PARANTHESE") :
            raise SyntaxError("Mtensa4 el '(' fel function parser")
        self.consume()

        # check 'void' token
        token = self.peek()
        if (token == None or token[0] != "KEYWORD" or token[1] != "void"):
            raise SyntaxError("Mtensa4 el void fel function parser")
        self.consume()

        # check ')' token
        token = self.peek()
        if (token == None or token[0] != "CLOSE_PARANTHESE"):
            raise SyntaxError("Mtensa4 el ')' fel function parser")
        self.consume()

        # check '{' token
        token = self.peek()
        if (token == None or token[0] != "OPEN_BRACE"):
            raise SyntaxError("Mtensa4 el '{' fel function parser")
        self.consume()


        # check Stmt token
        nodeStmt = self.parseStmt()

        # check '}' token
        token = self.peek()
        if (token == None or token[0] != "CLOSE_BRACE") :
            raise SyntaxError("Mtensa4 el '}' fel function parser")
        self.consume()

        ##Double check for junk data
        token = self.peek()
        if (token != None and token[0] != "KEYWORD"):
            raise SyntaxError("Enta kateb 7agat zeyada yasta!!")

        #return the node of function
        nodeFunc = NodeFunc(nodeIdent , nodeStmt)
        return nodeFunc

    def parseProg(self):
        nodeFunc = self.parseFunc()
        return NodeProg(nodeFunc)

    def peek(self , offset = 0):
        if (self.cur_idx + offset < len(self.tokens)) :
            return self.tokens[self.cur_idx + offset]
        return None

    def consume(self):
        token = self.tokens[self.cur_idx]
        self.cur_idx += 1
        return token

    def debugAST(self , node , ident=0):
        prefix = " " * ident

        if (isinstance(node, NodeProg)):
            print(f"{prefix}NodeProg:")
            self.debugAST(node.NodeFunc, ident + 2)

        if (isinstance(node, NodeFunc)):
            print(f"{prefix}NodeFunc:")
            print(f"{prefix}  Identifier: {node.NodeIdent.var[1]} ")
            self.debugAST(node.NodeStmt, ident + 2)

        if (isinstance(node, NodeStmt)):
            print(f"{prefix}NodeStmt:")
            self.debugAST(node.NodeExpr, ident + 2)

        if (isinstance(node, NodeExpr)):
            print(f"{prefix} return {node.NodeInt.constant[1]} ")
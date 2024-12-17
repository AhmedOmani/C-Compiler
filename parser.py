class IdentNode:
    def __init__(self , identifier):
        self.identifier = identifier

class IntNode:
    def __init__(self , constant):
        self.constant = constant

class ExprNode:
    def __init__(self , Int):
        self.int_node = Int

class StmtNode:
    def __init__(self , Expr):
        self.expr_node = Expr

class FuncNode:
    def __init__(self, Ident , Stmt):
        self.ident_node = Ident
        self.stmt_node = Stmt

class ProgNode:
    def __init__(self , Func):
        self.fucn_node = Func

class Parser :

    def __init__(self , tokens):
        self.tokens = tokens
        self.cur_idx = 0

    def parseIntNode(self):
        node_int = IntNode(self.peek())
        return node_int

    def parseIdentNode(self):
        node_ident = IdentNode(self.peek())
        return node_ident

    def parseExprNode(self):
        node_int = self.parseIntNode()
        return ExprNode(node_int)

    def parseStmtNode(self):
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
        node_expr = self.parseExprNode()
        node_stmt = StmtNode(node_expr)
        self.consume()

        ##check ';' token
        token = self.peek()
        if (token == None or token[0] != 'SEMICOLON') :
            raise SyntaxError(f"pls yasta rkz myn34 tensa el ';' abadn fe {self.cur_idx}")
        self.consume()

        return node_stmt

    def parseFuncNode(self):
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
        node_ident = self.parseIdentNode()
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
        node_stmt = self.parseStmtNode()

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
        fucn_node = FuncNode(node_ident , node_stmt)
        return fucn_node

    def parseProgNode(self):
        fucn_node = self.parseFuncNode()
        return ProgNode(fucn_node)

    def peek(self , offset = 0):
        if (self.cur_idx + offset < len(self.tokens)) :
            return self.tokens[self.cur_idx + offset]
        return None

    def consume(self):
        token = self.tokens[self.cur_idx]
        self.cur_idx += 1
        return token

    def print_AST(self , node , ident=0):
        prefix = " " * ident

        if (isinstance(node, ProgNode)):
            print(f"{prefix}ProgNode:")
            self.print_AST(node.fucn_node, ident + 2)

        if (isinstance(node, FuncNode)):
            print(f"{prefix}FuncNode:")
            print(f"{prefix}  Identifier: {node.ident_node.identifier[1]} ")
            self.print_AST(node.stmt_node, ident + 2)

        if (isinstance(node, StmtNode)):
            print(f"{prefix}StmtNode:")
            self.print_AST(node.expr_node, ident + 2)

        if (isinstance(node, ExprNode)):
            print(f"{prefix} return {node.int_node.constant[1]} ")
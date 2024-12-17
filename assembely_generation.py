from parser import *

class AssemblyNode:
    """Base class for all assembly nodes. (inheretince) """
    pass

class AssemblyProgramNode(AssemblyNode):
    """Root node representing the whole program."""
    def __init__(self , functions):
        self.functions = functions

class AssemblyFunctionNode(AssemblyNode):
    """Node representing a function definition."""
    def __init__(self , name , instructions):
        self.name = name
        self.instructions = instructions

class AssemblyInstructionNode(AssemblyNode):
    def __init__(self , operation , src = None , dst = None):
        self.operation = operation # Operation (e.g., 'mov', 'ret')
        self.src = src
        self.dst = dst

class AssemblyImmediateNode(AssemblyNode):
    """Node representing an immediate value."""
    def __init__(self , value):
        self.value = value # Immediate value (e.g., 42)

class AssemblyRegisterNode(AssemblyNode):
    """Node representing a register."""
    def __init__(self , register):
        self.register = register

# visitor desing pattern for more instruction in future
class InstructionVisitor:
    def visit_mov (self , src , dst):
        return AssemblyInstructionNode(operation = "movl" , src = src , dst = dst)

    def visit_ret(self):
        return AssemblyInstructionNode(operation = "ret")

class AssemblyGenerator :

    def __init__(self, root):
        self.root = root

    #start generating from here
    def generate(self):
        if (isinstance(self.root , ProgNode)) :
            return self.visit_prog(self.root)
        raise ValueError("Expected NodeProgram from parser")

    def visit_prog(self , node):
        funcion_node = self.visit_function(node.fucn_node)
        return AssemblyProgramNode(functions = [funcion_node])

    def visit_function(self , node):
        function_name = node.ident_node.identifier[1]
        function_instructions = self.visit_instruction(node.stmt_node)
        return AssemblyFunctionNode(name = function_name , instructions = function_instructions)

    def visit_instruction(self , node):
        visitor = InstructionVisitor()
        stmt_expr = self.visit_expr(node.expr_node)

        mov_instrucion = visitor.visit_mov(src = stmt_expr , dst = AssemblyRegisterNode("eax"))
        ret_instruction = visitor.visit_ret()

        return [mov_instrucion , ret_instruction]

    def visit_expr(self , node):
        return AssemblyImmediateNode(value = node.int_node.constant[1])

    def print_AAST(self , node , ident = 0):
        prefix = " " * ident
        if (isinstance(node , AssemblyProgramNode)):
            print(f"{prefix}AssemblyProgramNode:")
            for func in node.functions:
                self.print_AAST(func , ident + 2)

        if (isinstance(node, AssemblyFunctionNode)):
            print(f"{prefix}AssemblyFunctionNode: {node.name}")
            for instruction in node.instructions:
                self.print_AAST(instruction , ident + 2)

        if (isinstance(node , AssemblyInstructionNode)):
            print(f"{prefix}AssemblyInstructionNode: {node.operation}")
            if (node.src != None):
                print(f"{prefix}  Source:")
                self.print_AAST(node.src , ident + 4)
            if (node.dst != None):
                print(f"{prefix}  Destination:")
                self.print_AAST(node.dst , ident + 4)

        if (isinstance(node , AssemblyImmediateNode)):
            print(f"{prefix}AssemblyImmediateNode: {node.value}")

        if (isinstance(node , AssemblyRegisterNode)):
            print(f"{prefix}AssemblyRegisterNode: {node.register}")
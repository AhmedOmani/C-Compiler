from assembely_generation import *

class CodeEmitter :
    def __init__(self, file):
        self.file = file

    def emit_assembly(self , node):
        if (isinstance(node , AssemblyProgramNode)):
            self.file.write("    .section .note.GNU-stack," + '""' + ",@progbits\n\n\n")
            self.file.write("    .text\n")
            for function in node.functions :
                self.emit_assembly(function)

        if (isinstance(node , AssemblyFunctionNode)) :
            self.file.write(f"    .globl {node.name}\n\n\n")
            self.file.write(f"{node.name}:\n")
            for instruction in node.instructions :
                self.emit_assembly(instruction) ;

        if (isinstance(node , AssemblyInstructionNode)) :
            if node.dst != None :
                self.file.write(f"    {node.operation}    ${node.src.value}, %{node.dst.register}\n")
            else :
                self.file.write(f"    {node.operation}\n")

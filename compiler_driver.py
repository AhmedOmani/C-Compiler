import argparse
import os
import subprocess
import sys
from lexer import *
from code_emission import *

def LexicalAnalysis(preprocessed_file) :
    print("\nLexical analysis is processing..\n")
    with open(preprocessed_file , "r") as file:
        source_code = file.read()
    lexer = LEXER(source_code)
    try:
        tokens = lexer.tokenize()
        for token in tokens :
            print(token)
        return tokens
    except SyntaxError as e:
        print(f"Lexer error: {e}")
    finally:
        os.remove(preprocessed_file)

def Parsing(tokens) :
    print("\nParsing is processing...\n")
    parser = Parser(tokens)
    root = parser.parseProgNode()
    parser.print_AST(root)
    return root

def Assembling(root) :
    print("\nAssembling the code is processing...\n")
    assembler = AssemblyGenerator(root)
    assembly_root = assembler.generate()
    assembler.print_AAST(assembly_root)
    return assembly_root

def CodeGenerating(assembly_root):
    print("\nRunning full compilation up to code generation...\n")
    with open("out.s", "w") as asm_file:
        generator = CodeEmitter(asm_file)
        generator.emit_assembly(assembly_root)

def main():
    #Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Compiler Driver")
    parser.add_argument("source_file" , help = "Path to the C source file.")
    parser.add_argument("--lex" , action = "store_true" , help = "Run lexer only.")
    parser.add_argument("--parse" , action = "store_true" , help = "Run lexer and parser.")
    parser.add_argument("--codegen" , action = "store_true" , help = "Run lexer , parser and code generation.")

    args = parser.parse_args()
    source_file = args.source_file

    #Step 1: Preprocess the source file as book mentioned in Chapter1-page7
    preprocessed_file = source_file.replace(".c" , ".i")
    try:
        subprocess.run(["gcc" , "-E" , "-P"  , source_file , "-o" , preprocessed_file])
        #print(f"Preprocessed {source_file} to {preprocessed_file}")
    except subprocess.CalledProcessError:
        print("Error during preprocessing")
        sys.exit(1)

    ##lets build the lexer

    # Handle --lex flag: Run the lexer and stop
    if args.lex:
        LexicalAnalysis(preprocessed_file)
        sys.exit(0) ##Delete this line when you go further

    # Handle --parse flag: Run the lexer and parser, but stop before assembly generation
    if args.parse:
        Parsing(LexicalAnalysis(preprocessed_file))
        sys.exit(0)

    # Handle --codgen flag : run the excutable code
    if args.codegen:
        CodeGenerating(Assembling(Parsing(LexicalAnalysis(preprocessed_file))))
        sys.exit(0)

    #Step 2 : Compiled preprocessed file to assembly
    assembly_file = source_file.replace(".c" , ".s")
    try:
        subprocess.run(["gcc" , "-S" , preprocessed_file , "-o" , assembly_file])
        print(f"Compiled {preprocessed_file} to {assembly_file}")
    except subprocess.CalledProcessError:
        print("Error during compiling to assembly")
        sys.exit(1)
    finally:
        os.remove(preprocessed_file)

    #Step 3 : assembl & link the assembly file to create executable
    output_file = source_file.replace(".c" , "")
    try:
        subprocess.run(["gcc" , assembly_file , "-o" , output_file])
        print(f"Executable has been created")
    except subprocess.CalledProcessError:
        print("Error during assembly and linking!")
        sys.exit(1)
    finally:
        os.remove(assembly_file)



if __name__ == "__main__":
    main()

## Run the code by this command :
## $ python3 compiler_driver.py language.c --parse
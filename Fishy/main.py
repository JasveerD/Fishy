from lexer import *
from emitter import *
from parse import *
import sys

if (__name__ == "__main__"):

    print("Fishy Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")

    if not(sys.argv[1].endswith(".fishy")):
        sys.exit("Error: Input file with wrong format")

    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    # Initialize the lexer and parser.
    lexer = Lexer(source)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()       # start the parser.
    emitter.writeFile()    # writing the output to the .c file
    print("Parsing completed.")

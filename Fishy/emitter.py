"""
Emitter object will keep track of the generated code and output.
In each function of the parser, we will call the emitter to produce the appropriate C code.
The emitter is effectively just appending a bunch of strings together while following along the parse tree.
For each grammar rule of Fishy, we will figure out how it should map to C code.
"""

class Emitter:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.header = ""
        self.code = ""

    def emit(self, code):
        self.code += code

    def emitLine(self, code):
        self.code += code + '\n'

    def headerLine(self, code):
        self.header += code + '\n'

    def writeFile(self):
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code)

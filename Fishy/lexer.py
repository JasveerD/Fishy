"""
The lexer will take the source code of the FISHY programming language and iterate over the
characters. It'll decide where each token start and stops and the tokens type. If the lexer
encounters an invalid token, it'll also raise an error
"""

import sys
import enum

class Lexer:
    def __init__(self, source):
        self.source = source + "\n"    # source code sent to lexer as string; add \n for ease
        self.curChar = ''   # current char in processing
        self.curPos = -1    # current pointer position
        self.nextChar()

    # to process the next char
    def nextChar(self):
        '''
        increments lexer's current pos and updates curChar. If we reach the end, sets the
        cur char to end of file. This is the only func where we will update curPos and curChar
        directly.
        '''
        self.curPos += 1

        if (self.curPos >= len(self.source)):
            self.curChar = '\0'    # end of file char '\0' is null char
        else:
            self.curChar = self.source[self.curPos]

    # returns the lookahead char
    def peek(self):
        '''
        Sometimes it is useful to "look" at the next char without updating
        the curPos and curChar, so we use peek
        '''
        if (self.curPos + 1 >= len(self.source)):
            return '\0'
        return self.source[self.curPos+1]

    # invalid token, will print error message and exit
    def abort(self, message):
        sys.exit("Lexing error. " + message)

    # skips whitespaces except '\n' chars, which will be used to detect end of statements
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    # skip processing comments
    def skipComments(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # returns the next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComments()

        token = None

        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)

        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)

        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)

        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)

        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)

        elif self.curChar == '\0':
            token = Token(self.curChar, TokenType.EOF)

        elif self.curChar == '=':
            # checking if the token is '=' or '=='
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar+self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)

        elif self.curChar == '>':
            # checking if the token is '>' or '>='
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar+self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)

        elif self.curChar == '<':
            # checking if the token is '<' or '<='
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)

        elif self.curChar == '!':
            # checking if the token is '!='
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !"+self.peek())

        # for processing strings
        elif self.curChar == '\"':
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # not allowing special chars in string: escape, newline, tab, %
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            # getting the string and returning it as a token
            tokText = self.source[startPos:self.curPos]
            token = Token(tokText, TokenType.STRING)

        elif self.curChar.isdigit():
            # processing numbers
            # getting all the digit chars in the number

            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()

            if self.peek() == '.':  # Decimal number
                self.nextChar()

                # there should be a number after the decimal
                # handling the above condition
                if not self.peek().isdigit():
                    self.abort("Illegal char in number.")

                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos:self.curPos+1]
            token = Token(tokText, TokenType.NUMBER)

        elif self.curChar.isalpha():
            # processing identifiers
            # getting all the alphanumeric chars in the identifier
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            tokText = self.source[startPos:self.curPos+1]

            # checking if the identifier is not a keyword defined in our language
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None: # if None then it is a identifier
                token = Token(tokText, TokenType.IDENT)
            else:
                token = Token(tokText, keyword)

        else:
            self.abort('Unknown token: ' + self.curChar)

        self.nextChar()
        return token


class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # Token's actual text; used for: identifiers, strings & numbers
        self.kind = tokenKind   # classification of token

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # all keyword enums values have to be in the form 1XX
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211




















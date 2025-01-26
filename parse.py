"""
The parser will keep track of the current token and check
is the source code matches the grammar

GRAMMAR OF THE LANG:

program ::= {statement}
statement ::= "PRINT" (expression | string) nl
    | "IF" comparison "THEN" nl {statement} "ENDIF" nl
    | "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
    | "LABEL" ident nl
    | "GOTO" ident nl
    | "LET" ident "=" expression nl
    | "INPUT" ident nl
comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
expression ::= term {( "-" | "+" ) term}
term ::= unary {( "/" | "*" ) unary}
unary ::= ["+" | "-"] primary
primary ::= number | ident
nl ::= '\n'+
"""

import sys
from lexer import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.curToken = None
        self.peekToken = None

        # calling the func twice to inti both cur and peek token
        self.nextToken(); self.nextToken()

    # returns True if the current token is valid
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # returns True if the next token is valid with the current token
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # tries to match the current token, If not, error
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + " ,got " + self.curToken.kind.name)
        self.nextToken()

    # advances the current token
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error. " + message)

    # Return true if the current token is a comparison operator.
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    # PRODUCTION RULES

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # allow new lines at the start of the input
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # parse all the statements in the program
        while not self.checkToken(TokenType.EOF):
            self.statement()

    def statement(self):
        # check the first token to see what type of statement this is

        # "PRINT" (expression | string)
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                # it is a simple string
                self.nextToken()
            else:
                # expect an expression
                self.expression()   # will add later

        # "IF" comparison "THEN" nl {statement} "ENDIF" nl
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()   # will add later

            self.match(TokenType.THEN)
            self.nl()

            # zero or more statements allowed in the body
            while not self.checkToken(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            # zero or more statements allowed in the loop body
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)

        # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()
            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.match(TokenType.IDENT)

        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            print("STATEMENT-LET")
            self.nextToken()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()
            self.match(TokenType.IDENT)

        # invalid statement, raise error
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        # newline, applied to all statements
        self.nl()

    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("COMPARISON")

        self.expression()

        # Must be at least one comparison and another expression
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()

        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)

        # can have 0 or more comparison operator and expression
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

    """
    to implement precedence we'll parse the operators with the highest precedence last
    hence, they'll be closer to the leaves of the tree
    which will lead them to get evaluated first
    """
    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")

        self.term()
        # Can have 0 or more +/- expressions
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    def term(self):
        print("TERM")

        self.unary()
        # can have 0 or more * | / and expressions
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        # optional +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()


    """
    primary is either a token or an identifier like a variable name
    """
    # primary ::= number | ident
    def primary(self):
        print("PRIMARY (" + self.curToken.text + ')')

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            self.nextToken()
        else:
            # Error!
            self.abort("Unexpected token at " + self.curToken.text)


    # nl ::= '\n'+
    def nl(self):
        """
        handles newlines. will call this at the end of statement since it applies to all
        statements. works by expecting at least one nl char but allows more
        """
        print("NEWLINE")
        # at least one nl char expected
        self.match(TokenType.NEWLINE)
        # more nl chars allowed
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()





















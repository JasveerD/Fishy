from lexer import *

if (__name__ == "__main__"):

    source =  "IF+-123 foo*THEN/"
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()

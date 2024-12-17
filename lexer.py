import re

class LEXER :

    TOKENS = [ ("KEYWORD" , r"\b(printf|scanf|int|void|return)\b") ,
               ("IDENTEFIER" , r"[a-zA-Z_][\w]*\b") ,
               ("STRING", r'"[^"\n]*"'),
               ("COMMA", r","),
               ("CONSTANT" , r"\b[0-9]+\b"),
               ("OPEN_PARANTHESE" , r"\("),
               ("CLOSE_PARANTHESE" , r"\)") ,
               ("OPEN_BRACE" , r"\{") ,
               ("CLOSE_BRACE" , r"\}") ,
               ("SEMICOLON" , r";")
             ]

    def __init__(self , source_code):
        self.source_code = source_code
        self.tokens = []
        self.curIdx = 0

    def tokenize(self):
        while(self.curIdx < len(self.source_code)):

            if self.source_code[self.curIdx].isspace():
                self.curIdx += 1
                continue

            match = None

            for token_type , regex in self.TOKENS :
                pattern = re.compile(regex)
                match = pattern.match(self.source_code , self.curIdx)
                if match :
                    lexem = match.group(0)
                    self.tokens.append((token_type , lexem))
                    self.curIdx += len(lexem)
                    break

            if not match :
                raise SyntaxError(f"Lexem is not defined at index {self.curIdx} , the lexem is {self.source_code[self.curIdx]}")

        return self.tokens
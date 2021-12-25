class Scanner:
    line_count = 1
    def __init__(self, tiny_code = ""):
        self.tiny_code = tiny_code
        self.tokens = []
        self.token_pos = []

    def set_tiny_code(self, tiny_code):
        self.tiny_code = tiny_code

    def get_token_pos(self):
        return self.token_pos


    def scan(self):
        self.tokens = []
        special_chars = ['(', ')', ';']
        operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=']
        key_words = ["if", "then", "else", "end", "repeat", "until", "read", "write"]
        token_value = ""
        token_type = ""
        state = "start"
        i = 0
        line_inc = False
        while i < len(self.tiny_code):
            if self.tiny_code[i] == '\n':
                Scanner.line_count += 1
                line_inc = True
            if state == "start":
                if self.tiny_code[i] == ' ':
                    i+=1
                    continue
                elif self.tiny_code[i] == '{':
                    state = "in_comment"
                elif self.tiny_code[i].isdigit():
                    state = "in_num"
                    token_type = "number"
                    token_value += self.tiny_code[i]
                elif self.tiny_code[i].isalpha():
                    state = "in_id"
                    token_type = "identifier"
                    token_value += self.tiny_code[i]
                elif self.tiny_code[i] == ':':
                    state = "in_assign"
                    token_type = "assign"
                    token_value += self.tiny_code[i]
                elif self.tiny_code[i] in special_chars:
                    state = "done"
                    token_type = "special_character"
                    token_value += self.tiny_code[i]
                elif self.tiny_code[i] in operators:
                    state = "operator"
                    token_type = "operator"
                    token_value += self.tiny_code[i]
                else:
                    pass
            elif state == "in_comment":
                if self.tiny_code[i] == '}':
                    state = "start"

            elif state == "in_num":
                if self.tiny_code[i].isdigit():
                    token_value += self.tiny_code[i]
                else:
                    state = "done"

            elif state == "in_id":
                if self.tiny_code[i].isalpha() or self.tiny_code[i].isdigit():
                    token_value += self.tiny_code[i]
                else:
                    state = "done"

            elif state == "in_assign":
                if self.tiny_code[i] == '=':
                    token_value += self.tiny_code[i]
                else:
                    state = "done"

            elif state == "operator":
                if self.tiny_code[i] == "=":
                    token_value += self.tiny_code[i]
                else:
                    state = "done"

            if state == "done":
                if token_type == "identifier":
                    if token_value in key_words:
                        token_type = "keyword"
                self.tokens.append((token_value, token_type))
                if token_type != "special_character":
                    i-=1
                    if line_inc:
                        Scanner.line_count-=1
                self.token_pos.append(Scanner.line_count)
                token_value = ""
                token_type = ""
                state = "start"
            i+=1
            line_inc = False

    def get_tokens(self):
        self.token_pos = []
        Scanner.line_count = 1
        self.scan()
        Scanner.line_count = 1
        return self.tokens

    def export_tokens(self, filename):
        self.token_pos = []
        Scanner.line_count = 1
        self.scan()
        with open(filename, 'w+') as out:
            for token in self.tokens:
                out.write(token[0] + ", " + token[1] + '\n')


'''scan = Scanner("""{ Sample program in TINY language – computes factorial}
                    read x;   {input an integer }
                    if  0 < x   then     {  don’t compute if x <= 0 }
                    fact  := 1;
                    repeat
                    fact  := fact *  x;
                    x  := x  -  1
                    until  x  =  0;
                    write  fact   {  output  factorial of x }
 
                    end""")'''
# while True:
#     scan = ""
#     print("Please enter the Tiny language code: ")
#     while True:
#         line = input()
#         if line:
#             scan = scan + line + ' '
#             line = ''
#         else:
#             break
#
#     scan = Scanner(scan)
#     tokens = scan.get_tokens()
#     scan.export_tokens("tokens.txt")
#     print("Tokens have been generated successfully.")
#     print("To exit enter 0, else to continue")
#     if input() == '0':
#         break;
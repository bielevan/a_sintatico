# Representa a tabela de simbolos ja definidos pela linguagem inicialmente
# Possui uma estrutura de dados em tabela hash, onde as colisões são resolvidas
# Implementando uma lista para cada posição. Assim, se houver dois elementos
# para a mesma posição, então eles estaram inseridos em formato de lista na 
# mesma posição

# Para buscar a posição, foi implementado uma função de hash, na qual calcula-se
# a posição devida do token através da soma dos valores inteiros de cada caracter 
# e aplicando a função de resto, com um valor já pré-definido no inicio da compilação (LEN = 37).  

class Table:
    len = 0
    table_token = list()

    # Método construtor
    def __init__(self, len):
        self.len = len 
        i = 0
        while i < len:
            self.table_token.append(list())
            i += 1

        self.add("var", "simb_var")
        self.add("integer", "simb_integer")
        self.add("real", "simb_real")
        self.add("char", "simb_char")
        self.add("begin", "simb_begin")
        self.add("end", "simb_end")
        self.add("while", "simb_while")
        self.add("do", "simb_do")
        self.add("if", "simb_if")
        self.add("then", "simb_then")
        self.add("else", "simb_else")
        self.add("for", "simb_for")
        self.add("to", "simb_to")
        self.add("read", "simb_read")
        self.add("write", "simb_write")
        self.add("program", "simb_program")
        self.add("const", "simb_const")
        self.add("procedure", "simb_procedure")
        self.add(";", "simb_pv")
        self.add(":", "simb_dp")
        self.add(":=", "simb_atrib")
        self.add("=", "simb_igual")
        self.add("(", "simb_apar")
        self.add(")", "simb_fpar")
        self.add("<", "simb_menor")
        self.add(">", "simb_maior")
        self.add("+", "simb_mais")
        self.add("*", "simb_multi")
        self.add("-", "simb_menos")
        self.add("+", "simb_mais")
        self.add("/", "simb_div")
        self.add(".", "simb_p")
        self.add("<>", "simb_dif")
        self.add(">=", "simb_maior_igual")
        self.add("<=", "simb_menor_igual")
        self.add(".", "simb_pf")
        self.add(",", "simb_virgula")
        self.add("'", "simb_aspas")

    # Printa toda a tabela
    def show(self):
        for pos, value in enumerate(self.table_token):
            if (len(self.table_token[pos]) is not 0):
                print(value)

    # Retorna a posição de um elemento
    def pos(self, cad):
        tam = 0
        aux = list(cad)
        for i in aux:
            tam += ord(i)
        return tam % self.len

    # Insere elemento na tabela hash
    def add(self, cad, token):
        self.table_token[self.pos(cad)].append((cad, token))

    # Obter um token
    def getToken(self, cad):
        aux = self.pos(cad)
        for i in self.table_token[aux]:
            if i[0] == cad:
                return i[1]
        return None
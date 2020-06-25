#Importa todas as classes necessárias para realizar a analise léxica
from table import *
from ident import *
from number import *
from chr import *

class Pair:
    _cadeia = ''
    _token = ''
    _row = 0
    _error = False
    pass

class AL:
    
    # Construtor
    def __init__(self, len):
        self.table = Table(len)
        self.ident = Ident(self.table)
        self.number = Number(self.table)
        self.chr = Chr(self.table)
    
    # Classifica o caracterer e o direciona para o leitor correto
    def readToken(self, pair, file, c):
        # Consumir caracteres vazios
        while ((ord(c) == 32) or (ord(c) == 10) or (ord(c) == 9)):
            # Verifica se é uma quebra de linha
            if (ord(c) == 10):
                pair._row += 1
            c = file.read(1)
            # Verifica se acabou
            if (len(c) == 0):
                return False

        # Consumir comentários
        if (ord(c) == 123):
            # Consomi todos os caracteres até encontrar um final de chaves ou fim do arquivo
            c = file.read(1)
            while (ord(c) != 125):
                # Verifica se possui quebra de linha
                if (ord(c) == 10):
                    pair._row += 1
                c = file.read(1)
            
            # Verifica se chegou no final do comentário
            if (ord(c) == 125):
                c = file.read(1)
            
            # Se chegou no final do arquivo, então aconteceu um erros
            elif (len(c) == 0):
                pair._cadeia = ""
                pair._token = "error_comment"
                pair._error = True
                return False

        # Consumir caracteres vazios
        while (ord(c) == 32) or (ord(c) == 10) or (ord(c) == 9):
            # Verifica se é uma quebra de linha
            if (ord(c) == 10):
                pair._row += 1
            c = file.read(1)
            # Verifica se acabou
            if (len(c) == 0):
                return False

        # Verifica se existe caracteres ainda para ler
        if (len(c)> 0):   
            aux = ord(c)
            # Chama o autômato responsável por ler números
            if (aux >= 47 and aux <= 57):
                self.number.readToken(pair, file, c)

            # Chama o automato responsavel por ler identificadores
            elif ((aux >= 65 and aux <= 90) or (aux >= 97 and aux <= 122)):
                self.ident.readToken(pair, file, c)
            
            # Chama o automato responsavel por ler caracteres especiais
            else:
                self.chr.readToken(pair, file, c)
        
        return True



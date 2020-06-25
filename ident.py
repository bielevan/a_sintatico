# Classe responsavel por identificar e classificar identificadores
class Ident:
    tb = None

    # Construtor
    def __init__(self, table):
        self.tb = table

    # Ler e retornar par cadeia token
    def readToken(self, pair, file, c):
        # Identificador
        word = c
        c = file.read(1)

        # Continua lendo enquanto não terminar o identificador
        while c:
            # Verifica se não é uma letra ou dígito
            aux = ord(c)
            if ((aux < 48 or aux > 57) and (aux < 65 or aux > 122)):
                # Consumir caracteres não imprimiveis
                if ((aux == 32) or (aux == 9)):
                    break

                # Verifica se quebrou a linha
                if (aux == 10):
                    pair._row += 1
                    break
                     
                # Verifica se é um caracter que não está na tabela, logo não pertence a linguagem
                # Portanto, identificador foi mal construído
                if (self.tb.getToken(c) == None):
                    pair._error = True
                    word = word + c
                    break

                # Caracter é um final, logo fim do identificador
                else:
                    # Retorna uma posição no arquivo
                    pos = file.tell()-1
                    file.seek(pos)
                    break
                    
            # Adiciona ao identificador
            word = word + c
            c = file.read(1)

        # Verifica se a cadeia é demasiadamente grande
        if (len(word) > 20):
            pair._error = True
            pair._token = "error_invalid_token (identificador muito grande)"
            pair._cadeia = word
        
        # Identificador mal construído
        elif (pair._error):
            pair._token = "error_invalid_token (identificador mal construído)"
            pair._cadeia = word
    
        # Verifica se é um identificador ou uma palavra reservada
        else:
            pair._token = self.tb.getToken(word)
            if (pair._token == None):
                pair._token = "ident"
            pair._cadeia = word
         
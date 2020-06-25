# Classe responsavel por identificar e classificar números
class Number:
    tb = None

    # Construtor
    def __init__(self, table):
        self.tb = table

    # Ler número e retorna par cadeia-token
    def readToken(self, pair, file, c):
        # Add number
        pair._cadeia = c
        c = file.read(1)
        ponto = False

        # Continua leitura até finalizar o número
        while c:
            aux = ord(c)

            # Verifica se não é um digito
            if ((aux < 47) or (aux > 57)):
            
                # Verifica se é um comentário ou caracter nao imprimivel
                if ((aux == 32) or (aux == 9)):
                    break
                
                # Verifica se é um quebra de linha
                if (aux == 10):
                    pair._row += 1
                    break

                # Verifica se é um numero real
                if (c == "."):
                    if (ponto is True):
                        pair._error = True
                    else:
                        ponto = True
                
                # Se for um caracter nao final, então o número está escrito de forma inválida
                elif (self.tb.getToken(c) is None):
                    pair._error = True

                # Caracter é um final, logo o número acabou
                else:
                    # Retorna uma posição do controlador de arquivo
                    pos = file.tell()-1
                    file.seek(pos)
                    break

            pair._cadeia = pair._cadeia + c
            c = file.read(1)
        
        # Verifica se o número está mal construído
        if (pair._error):
            pair._token = "error_invalid_number (Número mal construído)"
            return
        
        # Verifica se o número é demasiado grande
        elif (len(pair._cadeia) > 15):
            pair._error = True
            pair._token = "error_max_size_number (Número muito grande)"
            return
        
        # Verifica se é um número real ou inteiro
        if (ponto is True):
            pair._token = "simb_real"
        else:
            pair._token = "simb_integer"
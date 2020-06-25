# Classe responsavel por identificar e classificar caracteres especiais
class Chr:
    tb = None 

    # Construtor
    def __init__(self, table):
        self.tb = table
    
    # Ler caracter e retorna par cadeia-token
    def readToken(self, pair, file, c):
        """
        # Ler todos os espaçamentos
        while (len(c) > 0 and ((ord(c) == 32) or (ord(c) == 10) or (ord(c) == 9))):
            # Verifica se é uma quebra de linha
            if (ord(c) == 10):
                pair._row += 1
            c = file.read(1)

        # Verifica se acabou
        if (len(c) == 0):
            return
        """

        chr = c
        token = self.tb.getToken(chr) 

        # Caracter final
        if (token is not None):
            c = file.read(1)

            # Verifica se chegou no final do arquivo
            if (len(c) == 0):
                pair._cadeia = chr
                pair._token = token
                return

            # Obtem o valor asc do caracter obtido no arquivo   
            aux = ord(c)

            # Verifica se é um caracter nao imprimivel
            if ((aux == 32) or (aux == 9)):
                pair._cadeia = chr
                pair._token = token
                return
            
            # Verifica se é uma quera de linha
            if (aux == 10):
                pair._cadeia = chr
                pair._token = token
                pair._row += 1
                return

            # Verifica se é um dígito ou número
            if (((aux >= 48) and (aux <= 57)) or ((aux >= 65) and (aux <= 122))):
                # Retorna uma posição do controlador de arquivo
                pos = file.tell()-1
                file.seek(pos)
                pair._cadeia = chr
                pair._token = token
                return
            
            chr = chr + c
            token_aux = self.tb.getToken(chr)

            # Verifica se é um caracter inválido
            if (token_aux == None):
                # Retorna uma posição do controlador de arquivo
                pos = file.tell()-1
                file.seek(pos)
                pair._cadeia = chr[0]
                pair._token = token
                return

            # Caracter pertence a linguagem
            else:
                pair._token = token_aux
                pair._cadeia = chr
                return
        
        # Não é um caracter válido
        pair._error = True
        pair._token = "error_char_invalid"
        pair._cadeia = chr
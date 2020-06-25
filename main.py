from al import AL
from al import Pair

# Gabriel Ribeiro Evangelista
# NUSP: 9771334

# Função principal
# Funciona com analisador sintático para cada entrada chama o analisador léxico

file = None
pair = None
row = None
la = None

def main():
    al = AL(37)

    global file
    global pair
    global la

    # Arquivo
    try:
        print("Informe o nome do arquivo: ", end='')
        name = str(input())
        with open('./arquivo_entrada/' + name + '.txt') as file:
            # Caracter lookhead
            la = ''
            pair = Pair()
            pair._row = 1
            pair._error = False

            # Ler todo o arquivo
            la = file.read(1)
            while la:
                # Obtem par cadeia-token
                al.readToken(pair, file, la)

                # Verifica se houve algum erro
                if (pair._error):
                    print("Erro léxico na linha", pair._row, ":", pair._cadeia, pair._token)
                else:
                    print(":", pair._cadeia, pair._token, pair._row)

                # Reajusta parametros
                la = file.read(1)
                pair._token = ""
                pair._cadeia = ""
                pair._error = False

    except IOError:
        print("Arquivo não encontrado ou impossível de ser aberto")

main()
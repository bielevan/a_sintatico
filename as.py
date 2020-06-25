from al import AL
from al import Pair

# Função principal
# Analisador sintático
class AS:
    
    al = None           # Analisador léxico
    pair = Pair()       # Obtém par cadeia-token
    la =  None          # Caracter lookahead
    qnt_erros = 0       # Qnt de erros

    # Construtor
    def __init__(self):
        self.al = AL(37)

    # Obter par cadeia-token
    def getToken(self, file):
        self.pair._error = False
        self.la = file.read(1)
        if (self.al.readToken(self.pair, file, self.la) is False):
            fim()

        # Verifica se houve erro léxico
        if (self.pair._error):
            print("Erro léxico na linha {} : {} {}".format(
                self.pair._row, self.pair._cadeia, self.pair._token))
            self.qnt_erros += 1

    # Função para escrever erro na saída padrão
    def error(self, txt):
        # Se não ocorreu um erro léxico
        if (self.pair._error is False):
            print("Error sintático na linha", self.pair._row, ": " + txt)
            self.qnt_erros += 1

    # Função que realiza a leitura de tokens ate encontrar um ponto e virgula
    def pv(self, file):
        while len(self.pair._token) > 0 and self.pair._token is not "simb_pv":
            self.getToken(file)
        
        if (self.pair._token == "simb_pv"):
            self.getToken(file)
            return True
        return False

    # Fim do programa
    def fim(self):
        exit(0)

    # Função Principal, inicia o processo de análise sintática
    def ASD(self):
        # Abre arquivo
        try:
            name = "meu_programa"
            with open("./arquivo_entrada/" + name + ".txt") as file:
                # Obtem par cadeia-token
                self.getToken(file)
                
                # Chama função program
                self.program(file)

                # Verifica se cadeia de entrada acabou
                if self.la:
                    print("Quantidade de erros:", self.qnt_erros)
                else:
                    print("Erro: programa acabou de forma inesperada!")
        except IOError:
            print('Arquivo impossível de abrir ou localizar no diretório informado')

    # Função recursiva para inicializar programa
    def program(self, file):
        # Verifica palavra program
        if (self.pair._token is not "simb_program"):
            self.error("palavra reservada 'program' era esperado no início do programa.")
        
        # Verifica nome do programa
        self.getToken(file)
        if (self.pair._token is not "ident"):
            self.error("identificador esperado para nomear programa.")
        
        # Verifica ponto-virgula
        self.getToken(file)
        if (self.pair._token is not "simb_pv"):
            self.error("ponto e vírgula esperado no final da definição do programa.")
        
        # Chama o corpo da função
        self.getToken(file)
        self.corpo(file)

    # Função recursiva do corpo principal do programa
    def corpo(self, file):
        # Chama função para verificar propriedades e definições do programa
        self.dc(file)
        if (self.pair._token is not 'simb_begin'):
            self.error("palavra reservada 'begin' era esperada no início do programa")

        # Chama função de comandos do corpo principal
        self.getToken(file)
        self.comandos(file)
        if (self.pair._token is not'simb_end'):
            self.error("palavra reservada 'end' era esperada no final do programa.")
        
        # Fim do programa
        self.getToken(file)
        if (self.pair._token is not 'simb_p'):  
            self.error("símbolo de ponto final era esperado no final do programa.")

        # Se nao tiver 
        print("Fim da compilação !!")

    # Função recursiva para as propriedades e definições do programa  
    def dc(self, file):
        # Chama a função de constantes
        self.dc_c(file)
        
        # Chama a função de variaveis
        self.dc_v(file)
        
        # Chama a função de procedimento
        self.dc_p(file)
    
    # Função recursiva para as constantes do programa
    def dc_c(self, file):
        while(self.pair._token == "simb_const"):
            # Verifica nome da constante
            self.getToken(file)
            if (self.pair._token is not "ident"):
                self.error("idenfificador para constante não encontrado.")
            
            # Verifica simbolo de igual
            self.getToken(file)
            if (self.pair._token is not "simb_igual"):
                self.error("símbolo de atribuição era esperado.")

            # Testa valor
            self.getToken(file)
            self.numero(file)
            if (self.pair._token == "simb_pv"):
                self.error("ponto e vírgula era esperado no final da definição.")            
            
            # Obtem token e retorna função
            self.getToken(file)
    
    # Função recursiva para as variaveis do programa
    def dc_v(self, file):
        # Verifica a presença da palavra reservada var
        if (self.pair._token is not 'simb_var'):
            self.error("palavra reservada 'var' era esperado no início das declarações.")
        else:
            # Enquanto tiver variaveis a declarar
            while self.pair._token is 'simb_var':
                # Chama a função que ler variaveis
                self.getToken(file)
                self.variaveis(file)
                if (self.pair._token is not 'simb_dp'):
                    self.error("símbolo de dois pontos era esperado.")
                
                # Chama a função para definir o tipo de variavel
                self.getToken(file) 
                self.tipo_var(file)
                
                # Verifica ponto e vírgula
                if (self.pair._token is not 'simb_pv'):
                    self.error("símbolo de ponto e vírgula era esperado.")                
                
                #Obtem proximo token
                self.getToken(file)

    # Função recursiva para definir o tipo de variavel
    def tipo_var(self, file):
        if ((self.pair._token is not 'simb_real') and (self.pair._token is not 'simb_integer')):
            self.error("era esperado a definição de tipo para a variável")

        # Obtem proximo token e retorna
        self.getToken(file)

    # Função recursiva para definir os nomes das variaveis
    def variaveis(self, file):
        # verifica a presença do nome da variavel
        if (self.pair._token is not 'ident'):
            self.error("idenficador da variável era esperado.")

        # Verifica se possui mais variaveis a declarar
        self.getToken(file)
        self.mais_var(file)
            
    # Função recursiva para criar mais de uma variável
    def mais_var(self, file):
        if (self.pair._token is 'simb_virgula'):
            while self.pair._token is 'simb_virgula':
                # Cria identificadores
                self.getToken(file)
                if (self.pair._token is not 'ident'):
                    self.error("identificador da variável era esperado.")
                
                # Verifica se tem mais nomes de variaveis a declarar
                self.getToken(file)
                
    # Função recursiva para criar procedimentos
    def dc_p(self, file):
        while (self.pair._token == "simb_procedure"):
            # Verifica nome do identificador
            self.getToken(file)
            if (self.pair._token is not "ident"):
                self.error("identificador do procedimento era esperado.")
            
            # Verifica parametros
            self.getToken(file)
            self.parametros(file)
            
            # verifica ponto e virgula
            if (self.pair._token is not "simb_pv"):
                self.error("símbolo de ponto e vírgula era esperado.")
            
            # Lê o corpo do procedimento
            self.getToken(file)
            self.corpo_p(file)
            
    # Função recursiva para criar parametros para o procedimento
    def parametros(self, file):
        if (self.pair._token is not "simb_ap"):    
            self.error("símbolo de abre parenteses era esperado.")

        # Obtem lista de parametros
        self.getToken(file)
        self.lista_par(file)

        # Verifica se fechou parenteses
        if (self.pair._token is not "simb_fp"):
            self.error("símbolo de fecha parenteses era esperado.")

        # Ontem token e retorna
        self.getToken(file)

    # Função recursiva para listar todos os parametros de um procedimento 
    def lista_par(self, file):
        self.variaveis(file)
        if (self.pair._token is not "simb_dp"):
            self.error("símbolo : era esperado para determinar o tipo de paramêtro.")

        self.getToken(file)
        self.tipo_var(file)
        self.mais_par(file)

    # Função recursiva para adicionar parametros
    def mais_par(self, file):
        while (self.pair._token is not "simb_pv"):
            self.getToken(file)
            self.variaveis(file)

            # Busca simbulo de atribuição para paremetro
            if (self.pair._token is not "simb_dp"):
                self.error("símbolo : era esperado para determinar o tipo de parametro.")
            
            # Ler token e obtem o tipo de parametro
            self.getToken(file)
            self.tipo_var(file)
                
    # Função recursiva para determinar o corpo do procedimento criado
    def corpo_p(self, file):
        self.dc_loc(file)

        # Verifica begin
        if (self.pair._token is not "simb_begin"):
            self.error("palavra reservada 'begin' era esperada para inicializar o procedimento")

        # Chama corpo do procesimento
        self.getToken(file)
        self.comandos(file)
        
        # Verifica se finalizou
        if (self.pair._token is not "simb_end"):
            self.error("palavra reservada 'end' era esperada para finalizar o procedimento.")        
        
        # Verifica ponto e virgula
        self.getToken(file)
        if (self.pair._token is not "simb_pv"):
            self.error("simbolo de ponto e vírgula era esperado.")
        
        # Obtem tolen e retorna
        self.getToken(file)
        
        # Função recursiva para determinar as variáveis do procedimento
    
    # Função recursiva para determinar as variaveis do procedimento
    def dc_loc(self, file):
        self.dc_v(file)

    # Função recursiva para criar uma Lista de argumentos
    def lista_arg(self, file):
        if (self.pair._token == "simb_ap"):
            self.getToken(file)
            self.argumentos(file)
            
            # Simbolo de fecha parenteses
            if (self.pair._token is not "simb_fp"):
                self.error("símbolo de fecha parenteses era esperado.")    
            
            # Obtem token e retorna
            self.getToken(file)
                
    # Função recursiva para determinar os argumentos de uma função
    def argumentos(self, file):
        if (self.pair._token == "ident"):
            self.getToken(file)
            self.mais_ident(file)
    
    # Função recursiva para criar uma lista de argumentos
    def mais_ident(self, file):
        # Enquanto tiver ponto e virgula
        while (self.pair._token == "simb_pv"):
            self.getToken(file)
            if (self.pair._token is not "ident"):
                self.error("identificador do argumento era esperado.")
            
            # Obtem token e retorna
            self.getToken(file)
            
    # Função recursiva para criar novos else
    def p_falsa(self, file):
        if (self.pair._token is 'simb_else'):
            self.getToken(file)
            self.cmd(file)

    # Função recursiva repetidora de funções do corpo principal
    def comandos(self, file):
        # Chama corpo do programa
        self.cmd(file)

        # Se o programa não finalizou
        while self.pair._token is not 'simb_end':
            self.comandos(file)
    
    # Função recursiva que chama método no corpo principal
    def cmd(self, file):
        # Verifica qual função deve chamar
        # Função read
        if (self.pair._token is 'simb_read'):
            self.getToken(file) 
            if (self.pair._token is not 'simb_apar'):
                self.error("simbolo de abre parênteses era esperado.")
            self.getToken(file)
            self.variaveis(file)
            if (self.pair._token is not 'simb_fpar'):
                self.error("simbolo de fecha parênteses era esperado.")
            self.getToken(file)
            
            # Verifica se ponto e virgula foi encontrado
            if (self.pair._token is not 'simb_pv'):
                self.error("simbolo de ponto-vírgula era esperado.")

            # Obtem token e retorna
            self.getToken(file)

        # Função write
        elif (self.pair._token is 'simb_write'):
            # VErifica abre parenteses
            self.getToken(file)
            if (self.pair._token is not 'simb_apar'):
                self.error("simbolo de abre parênteses era esperado.")
            
            # verifica fecha parenteses
            self.getToken(file)
            self.variaveis(file)
            if (self.pair._token is not 'simb_fpar'):
                self.error("simbolo de fecha parênteses era esperado.")
            
            self.getToken(file)
            # Verifica se ponto e virgula foi encontrado
            if (self.pair._token is not 'simb_pv'):
                self.error("simbolo de ponto-vírgula era esperado.")

            # Obtem token e retorna
            self.getToken(file)

        # Função while
        elif (self.pair._token is 'simb_while'):
            self.getToken(file)
            
            # Verifica abre parenteses
            if (self.pair._token is not 'simb_apar'):
                self.error("simbolo de abre parênteses era esperado.")

            # Verifica condição de parada   
            self.getToken(file)
            self.condicao(file)
            if (self.pair._token is not 'simb_fpar'):
                self.error("simbolo de fecha parênteses era esperado.")
            
            # Verifica palavra reservada do
            self.getToken(file)
            if (self.pair._token is not 'simb_do'):
                self.error("palavra reservada 'do' era esperada.")
            
            # Chama corpo do while
            self.getToken(file)
            self.comandos(file)
            if (self.pair._token is not 'simb_end'):
                self.error("palavra reservada 'end' era esperado para finalizar comando while.")
            
            self.getToken(file)
            # Verifica se ponto e virgula foi encontrado
            if (self.pair._token is not 'simb_pv'):
                self.error("simbolo de ponto-vírgula era esperado.")
            
            # Obtem token e retorna
            self.getToken(file)

        # Função For
        elif (self.pair._token is 'simb_for'):
            self.getToken(file)
            if (self.pair._token is 'ident'):
                self.getToken(file)
                if (self.pair._token is 'simb_atrib'):
                    self.getToken(file)
                    if (self.pair._token is 'integer'):
                        self.getToken(file)
                        if (self.pair._token is 'simb_to'):
                            self.getToken(file)
                            if (self.pair._token is 'integer' ):
                                self.getToken(file)
                                if (self.pair._token is 'simb_do'):
                                    self.getToken(file)
                                    self.cmd(file)
                                else:
                                    self.error("palavra reservada 'do' era esperada.")
                            else:
                                self.error("range era esperado para for.")
                        else:
                            self.error("palavra reservada 'to' era esperado.")
                    else:
                        self.error("valor inicial era esperado para função for.")
                else:
                    self.error("simbolo de atribuição era esperado.")
            else:
                self.error("identificador era esperado na função for.")

        # Função If
        elif (self.pair._token is 'simb_if'):
            # Verifica condição
            self.getToken(file)
            self.condicao(file)

            # Verifica palavra reservada then
            if (self.pair._token is not 'simb_then'):
                self.error("palavra reservada 'then' era esperada.")
            self.getToken(file)
            self.cmd(file)
            self.p_falsa(file)
            
            # Verifica se ponto e virgula foi encontrado
            if (self.pair._token is not 'simb_pv'):
                self.error("simbolo de ponto-vírgula era esperado.")

            # Obtem token e retorna
            self.getToken(file)

        # Função Identificador
        elif (self.pair._token is 'ident'):
            self.getToken(file)

            # Verifica qual função chamar para o identificador
            if (self.pair._token is 'simb_atrib'):
                self.getToken(file)
                self.expressao(file)
            else:
                self.lista_arg(file)
            
            # Verifica se ponto e virgula foi encontrado
            if (self.pair._token is not 'simb_pv'):
                self.error("simbolo de ponto-vírgula era esperado.")

            # Obtem token e retorna
            self.getToken(file)

        # Inicia begin
        elif (self.pair._token is 'simb_begin'):
            self.getToken(file)
            self.comandos(file)
            if (self.pair._token is not 'simb_end'):
                self.error("palavra reservada 'end' era esperada.")
            self.getToken(file)

            # Verifica se ponto e virgula foi encontrado
            if (self.pair._token is not 'simb_pv'):
                self.error("simbolo de ponto-vírgula era esperado.")

            # Obtem token e retorna
            self.getToken(file)

    # Função recursiva para condições decisórias
    def condicao(self, file):
        self.expressao(file)
        self.relacao(file)
        self.expressao(file)

    # Função recursiva que determina relações entre elementos
    def relacao(self, file):
        if (self.pair._token is 'simb_igual'):
            self.getToken(file)
        elif (self.pair._token is 'simb_dif'):
            self.getToken(file)
        elif (self.pair._token is 'simb_maior_igual'):
            self.getToken(file)
        elif (self.pair._token is 'simb_menor_igual'):
            self.getToken(file)
        elif (self.pair._token is 'simb_maior'):
            self.getToken(file)
        elif (self.pair._token is 'simb_menor'):
            self.getToken(file)
        else:
            self.error("simbolo de relação era esperado.")
            
    # Função recursiva para criar uma expressão
    def expressao(self, file):
        self.termo(file)
        # Enquanto encontrar sinal de mais ou menos, continua adicionando termos a expressão
        while self.pair._token is 'simb_mais' or self.pair._token is 'simb_menos':
            self.op_ad(file)
            self.termo(file)

    # Função recursiva 
    def op_un(self, file):
        if (self.pair._token is 'simb_mais' or self.pair._token is 'simb_menos'):
            self.getToken(file)

    # Função recursiva para adicionar símbolo de mais ou menos à expressão
    def op_ad(self, file):
        if (self.pair._token is not 'simb_mais' and self.pair._token is not 'simb_menos'):
            self.error("simbolo de adição ou subtração era esperado.")
        self.getToken(file)

    # Função recursiva para acrescimo de termos na expressão
    def termo(self, file):
        self.op_un(file)
        self.fator(file)
        while self.pair._token is 'simb_mult' or self.pair._token is 'simb_div':
            self.getToken(file)
            self.fator(file)

    # Função recursiva para determinar fator
    def fator(self, file):
        # Identificador
        if (self.pair._token is 'ident'):
            self.getToken(file)
        # Expressão
        elif (self.pair._token is 'simb_apar'):
            self.getToken(file)
            self.expressao(file)

            if (self.pair._token is not 'simb_fpar'):
                self.error("símbolo de fecha parenteses era esperado.")
            
            self.getToken(file)
        # Número
        else:
            self.numero(file)

    # Função recursiva para expressar o tipo númerico
    def numero(self, file):
        if (self.pair._token is not 'simb_integer' and self.pair._token is not 'simb_real'):
            self.error("valor numérico era esperado na expressão")
        self.getToken(file)

a_s = AS()
a_s.ASD()
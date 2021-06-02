import operator
from collections import OrderedDict

# PORTO ALEGRE, RS
# 11465373,11465953,40845451,40846031
# '20210517', '20210518', '20210519', '20210520', '20210521', '20210522', '20210523','20210524'

class No:
     
     def __init__(self, key, dir, esq):
          self.item = key
          self.dir = dir
          self.esq = esq

class Tree:

    def __init__(self):
        self.root = No(None,None,None)
        self.root = None

    def inserir(self, v):
        novo = No(v,None,None) # cria um novo Nó
        if self.root == None:
            self.root = novo
        else: # se nao for a raiz
            atual = self.root
            while True:
                anterior = atual
                if v <= atual.item: # ir para esquerda
                    atual = atual.esq
                    if atual == None:
                        anterior.esq = novo
                        return
                    # fim da condição ir a esquerda
                    else: # ir para direita
                        atual = atual.dir
                        if atual == None:
                            anterior.dir = novo
                            return
                    # fim da condição ir a direita

    def buscar(self, chave):
        if self.root == None:
            return None # se arvore vazia
        atual = self.root # começa a procurar desde raiz
        while chave not in atual.item.split('|')[0]: # enquanto nao encontrou
            if chave < atual.item.split('|')[0]:
                atual = atual.esq # caminha para esquerda
            else:
                atual = atual.dir # caminha para direita
            if atual == None:
                return None # encontrou uma folha -> sai
        return atual  # terminou o laço while e chegou aqui é pq encontrou item 

    def inOrder(self, atual):
        if atual != None:
            self.inOrder(atual.esq)
            print(atual.item,end=" ")
            self.inOrder(atual.dir)

    def caminhar(self):
        print(" Exibindo em ordem: ",end="")
        self.inOrder(self.root)

class Hash:

    def __init__(self,tam):
        self.tab = {}
        self.tam_max = tam
        self.lista_datas = []

    def cheia(self):
          return len(self.tab) == self.tam_max

    def insere(self, item):
        if self.cheia():
            return
        pos = len(self.lista_datas)
        if self.tab.get(pos) == None: # se posicao vazia
            self.tab[pos] = item
            self.lista_datas.append(str(item.split('|')[0]))
        else: # se posicao ocupada
            print("-> Ocorreu uma colisao na posicao %d" %pos) 

    def imprime(self):
          for i in self.tab:
               print("Hash[%d] = " %i, end="")
               print (self.tab[i])

    def busca(self, chave):
        pos = self.lista_datas.index(chave)
        if self.tab.get(pos) == None: # se esta posição não existe
            return -1 #saida imediata
        if str(self.tab[pos].split('|')[0]) == str(chave):
            return self.tab[pos]
        return -1


class ProgramaArquivos:

    def __init__(self) -> None:
        self.tree = Tree()
        self.menu()
        pass

    def count_arquivo(self, arquivo):
        count = 0
        for linha in arquivo:
            if count == 0:
                first_line = linha
            count += 1

        return count, first_line, linha

    def seek_file(self, list_of_index):
        "value: deve ser passado uma lista contendo as respectivas posições(índices) do arquivo sort_tweets.txt"

        arquivo = open("sort_tweets.txt", 'r', encoding='UTF-8')

        for indice in list_of_index:
            arquivo.seek(int(indice))
            content = arquivo.readline()
            print("ID Tweet: " + content[:19] + '\n')
            print("Texto: " + content[19:299] + '\n')
            print("Usuário: " + content[299:319] + '\n')
            print("Data: " + content[319:327] + '\n')
            print("Localização: " + content[327:377] + '\n')
            print("Hashtags: " + content[377:577] + '\n')
            print('\n')

    def arvore(self):
        x = str(input("Digite o local que deseja buscar os tweets: "))
        busca = self.tree.buscar(x)
        if busca != None:
            print(" Valor Encontrado nos seguintes índices: ")
            print(busca.item.split('|')[1])
        else:
            print(" Valor nao encontrado!")

    def hash(self):
        x = str(input("Digite a data que deseja buscar os tweets: "))
        busca = self.tabela_hash.busca(str(x))
        if busca != None:
            print(" Valor Encontrado nos seguintes índices: ")
            print(busca.split('|')[1][:2000])
        else:
            print(" Valor nao encontrado!")
        

    def pesquisa_binaria_por_hashtag(self, hashtag=None, exibe_tweets=False):
        with open("hashtags.txt", "r", encoding="UTF-8") as arquivo_hashtag:
            if not hashtag:
                hashtag = input("Digite a hashtag que deseja buscar: ")
            
            tamanho_arquivo = self.count_arquivo(arquivo_hashtag)

            inicio = tamanho_arquivo[1]
            fim = tamanho_arquivo[2]

            tamanho_arquivo = tamanho_arquivo[0]
            inicio_original = tamanho_arquivo

            posicao = 1
            arquivo_hashtag.seek(0)
            arq = arquivo_hashtag.readlines()
            while(1):
                meio = posicao + (tamanho_arquivo-1)/2    
                meio = int(meio)
                linha = arq[meio]
                hashtag_linha = linha.split('|')[1]

                if meio == inicio_original or meio < 0: 
                    print("índice não encontrado")
                    return

                if hashtag.upper() in linha.upper(): 
                    indice = linha.split('|')[0]
                    if exibe_tweets:
                        self.seek_file(indice.split(','))
                    else:
                        return len(indice.split(','))
                    break

                if hashtag_linha > hashtag: 
                    tamanho_arquivo -= 1
                
                if hashtag_linha < hashtag: 
                    posicao += 1

        arquivo_hashtag.close()
        if indice:
            return indice

    def pesquisa_binaria(self, exibe_tweets=False):
        arquivo_id = open("id_tweets.txt", "r", encoding="UTF-8")
        id_tweet = input("Digite o id do tweet que deseja buscar: ")
        
        tamanho_arquivo = self.count_arquivo(arquivo_id)

        inicio = tamanho_arquivo[1]
        fim = tamanho_arquivo[2]

        tamanho_arquivo = tamanho_arquivo[0]
        inicio_original = tamanho_arquivo

        posicao = 1
        arquivo_id.seek(0)
        while(1):
            meio = posicao + (tamanho_arquivo-1)/2    
            meio = int(meio)
            linha = arquivo_id.readline(meio)
            try:
                tweet_linha = linha.split('|')[1]
            except:
                pass

            if meio == inicio_original or meio < 0: 
                print("índice não encontrado")
                return

            if id_tweet in linha: 
                indice = linha.split('|')[0]
                print("ID encontrado no índice: " + indice)
                if exibe_tweets:
                    self.seek_file([indice])
                break

            if str(tweet_linha.strip()) > str(id_tweet): 
                tamanho_arquivo -= 1
            
            if str(tweet_linha.strip()) < str(id_tweet): 
                posicao += 1

        arquivo_id.close()

    def gera_arquivo_de_indices(self):
        """
        Método que ordena e gera arquivos de índices das colunas: id_twitter e hashtags
        """
        arquivo = open('sort_tweets.txt', 'r', encoding='UTF-8')
        lista_arquivo = []
        dic_arvore = {}
        dic_hash = {}
        tamanho_tabela_hash = 0
        while True:
            indice = arquivo.tell()
            linha = arquivo.readline()

            # Arvore
            chave_arvore = linha[327:377].strip()
            if not dic_arvore.get(chave_arvore):
                dic_arvore[chave_arvore] = str(arquivo.tell()) + ','
            else:
                dic_arvore[chave_arvore] += str(arquivo.tell()) + ','

            # Hash
            chave_hash = linha[319:327].strip()
            if not dic_hash.get(chave_hash):
                dic_hash[chave_hash] = str(arquivo.tell()) + ','
                tamanho_tabela_hash += 1
            else:
                dic_hash[chave_hash] += str(arquivo.tell()) + ',' 

            if not linha:
                break

            lista_arquivo.append(
                {'tweet_id': linha[:19],
                 'text': linha[19:299],
                 'user': linha[299:319],
                 'date': linha[319:327],
                 'location': linha[327:377],
                 'hashtags': linha[377:577],
                 'indice': indice}
            )

        arquivo.close()

        # Monta arvore binária
        dic_arvore = OrderedDict(sorted(dic_arvore.items()))
        self.tree = Tree()
        count = 0
        for chave, valor in dic_arvore.items():
            self.tree.inserir(str(chave) + '|' + valor[:-1])
            count += 1
            if count == 2000:
                print(chave)
                break

        # Monta tabela hash
        dic_hash = OrderedDict(sorted(dic_hash.items()))
        self.tabela_hash = Hash(tamanho_tabela_hash)
        count = 0
        for chave, valor in dic_hash.items():
            self.tabela_hash.insere(str(chave) + '|' + valor[:-1])
            count += 1
            if count == 2000:
                print(chave)
                break

        id_tweets_arquivo = open("id_tweets.txt", "w", encoding='UTF-8')
        
        for linha in lista_arquivo:
            id_tweets_arquivo.write(str(linha['indice']) + '|' + linha['tweet_id'] + '\n')

        id_tweets_arquivo.close()
        print('Arquivo de id_tweets criado com sucesso!')

        dic_hashtags = {}
        for linha in lista_arquivo:
            hashtags = linha['hashtags'].replace(' ', '')
            if hashtags:
                hashtags = hashtags[1:].split('#')
                for hashtag in hashtags:
                    if dic_hashtags.get(hashtag):
                        dic_hashtags[hashtag].append(str(linha['indice']))
                    else:
                        dic_hashtags[hashtag] = [str(linha['indice'])]

        hashtags_arquivo = open("hashtags.txt", "w", encoding='UTF-8')

        dic_hashtags = OrderedDict(sorted(dic_hashtags.items()))

        for key, value in dic_hashtags.items():
            hashtags_arquivo.write(','.join(value) + '|#' + key + '\n')

        hashtags_arquivo.close()
        print('Arquivo de hashtags criado com sucesso!')

    def mostra_dados_arquivo(self):
        arquivo = open('tweets.txt', 'r', encoding='UTF-8')
        for linha in arquivo:
            print(linha)

    def menu(self):

        coronavac = self.pesquisa_binaria_por_hashtag('#coronavac')
        pfizer = self.pesquisa_binaria_por_hashtag('#pfizer')
        astra = self.pesquisa_binaria_por_hashtag('#astrazeneca')

        if coronavac > pfizer and coronavac > astra:
            print('Coronavac é a vacina mais comentada (' + str(coronavac) + ')')
            if pfizer > astra:
                print('Pfizer é a segunda vacina mais comentada (' + str(pfizer) + ')')
            else:
                print('AstraZeneca é a segunda vacina mais comentada (' + str(astra) + ')')

        if pfizer > coronavac and pfizer > astra:
            print('Pfizer é a vacina mais comentada (' + pfizer + ')')
            if coronavac > astra:
                print('Coronavac é a segunda vacina mais comentada (' + str(coronavac) + ')')
            else:
                print('AstraZeneca é a segunda vacina mais comentada (' + str(astra) + ')')

        if astra > pfizer and astra > coronavac:
            print('AstraZeneca é a vacina mais comentada (' + str(astra) + ')')
            if coronavac > pfizer:
                print('Coronavac é a segunda vacina mais comentada (' + str(coronavac) + ')')
            else:
                print('Pfizer é a segunda vacina mais comentada (' + str(pfizer) + ')')

        print("Digite o que você deseja fazer:")
        print("0 - Sair")
        print("1 - Exibir arquivo de dados")
        print("2 - Gera arquivo de índices")
        print("3 - Pesquisa binária por id do tweet")
        print("4 - Pesquisa binária por hashtag")
        print("5 - Pesquisa por local de postagem")
        print("6 - Pesquisar tweet pelo índice(seek)")
        print("7 - Pesquisar por data de postagem")

        opcao = input()

        while opcao != '0':
            if opcao == '1':
                self.mostra_dados_arquivo()

            elif opcao == '2':
                self.gera_arquivo_de_indices()

            elif opcao == '3':
                self.pesquisa_binaria(exibe_tweets=True)

            elif opcao == '4':
                self.pesquisa_binaria_por_hashtag(exibe_tweets=True)

            elif opcao == '5':
                self.arvore()

            elif opcao == '6':
                indice = input('Digite o(s) índice(s) que deseja buscar: ')
                self.seek_file(indice.split(','))

            elif opcao == '7':
                self.hash()
            
            print("Digite o que você deseja fazer:")
            print("0 - Sair")
            print("1 - Exibir arquivo de dados")
            print("2 - Gera arquivo de índices")
            print("3 - Pesquisa binária por id do tweet")
            print("4 - Pesquisa binária por hashtag")
            print("5 - Pesquisa por local de postagem")
            print("6 - Pesquisar tweet pelo índice(seek)")
            print("7 - Pesquisar por data de postagem")
            opcao = input()


ProgramaArquivos()
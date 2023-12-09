#Universidade do Minho - UMinho
#Mestrado em Humanidades Digitais
#Processamento de Linguagem Natural
#
#Prof. José João
#
#Aluna: Lívia Pérez Bettero
#Matricula: PG52762
#
#
#Conteúdo    enviado por: https://natura.di.uminho.pt/jjbin/fpln2023-tp1
#            disponível em:
#
#TAREFAS:
#1. Calcular quantas publicações existem na base
#2. Extrair as listas das tags
#3. Calcular as tags que ocorrem e quanto ocorrem
#4. Extrair a gama de dados do texto
#5. Inventar qualquer coisa para fazer com o texto

import re
import string

lista_linhas_materias=[]
Dicionario_Tags_Materias={} #Dicionário de Tags de matérias
Dicionario_Titulos_Materias={} #Dicionário de titulos de matérias
Dicionario_Gama_Dados={}

########################## FUNÇÕES DOS ECERCÍCIOS ##########################
def exercicio_01(materias):
    #1. Calcular quantas publicações existem na base
    print("1. Calcular quantas publicações existem na base")
    print("Total de publicações: ",len(materias), "incluindo repetições.")
    #A questão é que existem matérias repetidas.
    #Para calcular quantas publicações sem repetições existem na base, recorri a um dicionário
    #contando por título
    print("Total de publicações: ",Localiza_Titulos(lista_linhas_materias), "ignorando repetições.")
    print("Ao todo existem ", len(materias)-Localiza_Titulos(lista_linhas_materias), "matérias repetidas")

def exercicio_02(materias):
    print("2. Extrair as listas das tags")
    Busca_Tags(materias)#Invoca a rotina de extração de Tags e inclusão em um dicionario de tags
    listaTags=[]
    with open("Exercicio_2_bettero.txt", 'w', encoding="utf8") as file:#Grava arquivo com o resultado
        for tag in Dicionario_Tags_Materias:#coloca as tags extraídas em uma 
            file.write(str(tag) + '\n')
            listaTags.append(tag)
    print("resultado disponível no arquivo 'Exercicio_2_bettero.txt'")
    print(listaTags)

def exercicio_03():
    print("3. Calcular as tags que ocorrem e quanto ocorrem")
    print("resultado disponível no arquivo 'Exercicio_3_bettero.txt'")
    with open("Exercicio_3_bettero.txt", 'w', encoding="utf8") as file:#Grava arquivo com o resultado
        for tag in Dicionario_Tags_Materias:
            print(tag, " - ", Dicionario_Tags_Materias[tag])#Imprime a mesma coisa do exercício 2,
            #mas incluindo a contagem de ocorrências de cada tag.
            file.write(str(tag)+" - "+str(Dicionario_Tags_Materias[tag])+"\n")

def exercicio_04(materias):
    print("4. Extrair a gama de dados do texto")
    Localiza_Gama_Dados(lista_linhas_materias)
    print("resultado disponível no arquivo 'Exercicio_4_bettero.txt'")

def ecercicio_05():
    print("Imprimir relação de matérias duplicadas em algum lugar do arquivo fonte")
    with open("Exercicio_5_bettero.txt", 'w', encoding="utf8") as file:#Grava arquivo com o resultado
        for item in Dicionario_Titulos_Materias:
            if Dicionario_Titulos_Materias[item]>2:
                print(item)
                file.write(str(item)+"\n")
    print("resultado disponível no arquivo 'Exercicio_5_bettero.txt'")

def exercicio_06(titulos_unicos):
    Dicionario_Palavras={}
    print("Imprimir ocorrências de palavras dos títulos")
    pontuacao=string.punctuation
    tab_substituicao=str.maketrans('', '',pontuacao)
    for item in titulos_unicos:
        sem_pontuacao=(item.translate(tab_substituicao)).lower()
        palavras_titulo=sem_pontuacao.split(" ")
        for palavra in palavras_titulo:
            if palavra not in Dicionario_Palavras:
                Dicionario_Palavras[palavra] = 1
            else:
                Dicionario_Palavras[palavra] += 1
    palavras_ordenadas = sorted(Dicionario_Palavras.items(), key=lambda x: x[1], reverse=True)
    with open("Exercicio_6_bettero.txt", 'w', encoding="utf8") as file:#Grava arquivo com o resultado
        for palavra in palavras_ordenadas:
            print(palavra)
            file.write(str(palavra)+"\n")
    print("resultado disponível no arquivo 'Exercicio_6_bettero.txt'")
    
########################## FUNÇÕES COMPLEMENTARES ##########################
#Leitura dos dados do arquivo fonte "folha8.Out.txt"
def le_arquivo_fonte(nomearquivo):
    #Abre o arquivo folha8.OUT.txt
    with open(nomearquivo, "r", encoding="utf8") as arquivo:
        conteudo = arquivo.read()
        return(conteudo)

#Quebra do texto corrido obtido do arquivo fonte em uma lista, por matéria
def quebra_por_materias(folha):
    materias=folha.split("<pub>")
        #toda publicação inicia com <pub> e encerra com </pub>.
        # Ao separar o texto por <pub>, se separa o texto por cada início de matéria.
    return(materias)

#Quebra de cada matéria por linhas para ser capaz de localizar o conteúdo
def separa_linhas_materias(materias):
    linhas=[]
    for materia in materias:
        linhasmateria=materia.split("\n")
        for linha in linhasmateria:
            linhas.append(linha)
    return(linhas)

#Localiza as linhas que possuem título da matéria, contando a terceira linha após #ID
def Localiza_Titulos(lista_linhas_materias):
    indice_id = None
    for i,linha in enumerate(lista_linhas_materias):
        if linha.strip().startswith("#ID"):
            indice_id = i
            if indice_id is not None and indice_id + 3 < len(lista_linhas_materias):
                terceira_linha_apos_id = lista_linhas_materias[indice_id + 3] #Obtém a linha contendo o título da matéria
                #Adiciona os titulos de  matérias obtidos ao dicionário de títulos
                if terceira_linha_apos_id not in Dicionario_Titulos_Materias:
                    Dicionario_Titulos_Materias[terceira_linha_apos_id] = 1
                else:
                    Dicionario_Titulos_Materias[terceira_linha_apos_id] += 1
    return(len(Dicionario_Titulos_Materias))

def Busca_Tags(materias):
    #Usa a mesma lógica pra localizar os titulos de matérias não repetidas, mas desta vez, buscando as linhas
    #que iniciam com #TAG
    padrao = r'\{(.*?)\}' #As tags buscadas encontram-se entre {}
    for i,linha in enumerate(lista_linhas_materias):
        if linha.strip().startswith("#TAG"):
            linhasTags=re.findall(padrao, linha)
            #Adiciona os titulos de  matérias obtidos ao dicionário de títulos
            for tag in linhasTags:
                if tag not in Dicionario_Tags_Materias:
                    Dicionario_Tags_Materias[tag] = 1
                else:
                    Dicionario_Tags_Materias[tag] += 1
    return()

def Localiza_Gama_Dados(lista_linhas_materias):
    #Para localizar gama de dados nas matérias
    Gama_Dados=[]
    indice_id = None
    for i,linha in enumerate(lista_linhas_materias):
        #Verifica se a linha contém tags
        padrao = r'\{(.*?)\}'
        if linha.strip().startswith("#TAG"):
            linhasTags=re.findall(padrao, linha)
        else:
            #Verifica se a linha inicia com ID para obter o título da matéria
            if linha.strip().startswith("#ID"):
                indice_id = i
                if indice_id is not None and indice_id + 3 < len(lista_linhas_materias):
                    terceira_linha_apos_id = lista_linhas_materias[indice_id + 3] #Obtém a linha contendo o título da matéria
                    secao_materia = lista_linhas_materias[indice_id + 1] #Obtém a seção da matéria no jornal                        #Adiciona os titulos de  matérias obtidos ao dicionário de títulos
            else:
                #Verifica se a linha inicia com #DATE e extrai a data
                if linha.strip().startswith("#DATE"):
                    data_materia=linha.split("— ")[1]
                else:
                    #Verifica se a linha contém etiquetas
                    if linha.strip().startswith("Etiqueta"):
                        etiqueta_materia=linha.split(": ")[1]
                        Gama_Dados.append([[secao_materia],[data_materia],[terceira_linha_apos_id],linhasTags,[etiqueta_materia]])
                        Dicionario_Gama_Dados=(Gama_Dados)
    print(len(Dicionario_Gama_Dados))
    with open("Exercicio_4_bettero.txt", 'w', encoding="utf8") as file:#Grava arquivo com o resultado
        for item in Dicionario_Gama_Dados:
            file.write(str(item)+"\n")

########################## CHAMADAS DAS FUNÇÕES EM ORDEM ##########################
#Preparando a fonte de dados para os exercícios:
folhaOito=le_arquivo_fonte("folha8.OUT.txt")#Invoca a rotina para abertura do arquivo fonte e carregar o conteúdo na variável
materias=quebra_por_materias(folhaOito)#Invoca a rotina para quebrar conteúdo por publicação e carregar na lista
lista_linhas_materias=separa_linhas_materias(materias)

print("-------------------------- EXERCÍCIOS --------------------------\n")
materias_unicas=exercicio_01(materias)#Invoca a solução do Exercício 1
listaTags=exercicio_02(materias_unicas)#Invoca a solução do Exercício 2
exercicio_03()#Invoca a solução do Exercício 3 com o resultado do exercício 2
exercicio_04(materias_unicas) #4. Extrair a gama de dados do texto
ecercicio_05() #5. Imprimir relação de matérias duplicadas em algum lugar do arquivo fonte
exercicio_06(Dicionario_Titulos_Materias) #6. Contar palavras e recorrências do título de cada matéria única
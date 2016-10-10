# -*- coding: utf-8 -*-
# Organização de Arquivos Sequencial Indexada;
# Autores : Eliane, Lucas

from indice import *
from manipuladorArquivos import *
import sys
import pickle

def pesq_binaria(chave, inicio, fim, pos, achou):
    """
    Pesquisa Binária pelo arquivo de indices.
    Parametros : chave é o código(String), inicio (Inicio do Arquivo Inteiro),
        fim (Final do arquivo), pos (Linha do Arquivo), Achou (Boolean)
    Return  posicao no arquivo de registros
    """
    if ((fim - inicio) > 0):
        meio = ((inicio+fim)/2)
        linha = lerLinhaIndice(meio, 0)
        if linha:
            atributos = linha.split(',')
            valor = atributos[0]
            posarq = atributos[1]
            if valor == chave:
                achou = True
                pos = posicao
                return posarq
            elif (valor > chave):
                return pesq_binaria(chave, inicio, meio, pos, achou)
            else:
                return pesq_binaria(chave, meio, fim, pos, achou)

def pesq_sequencial(linhachave, chave, indices, listaRegistros):
    """
    Pesquisa Sequencial pelo arquivo de indices.
    Parametros : linhachave String Linha do arquivo extencao para o elo,
        chave é o código(String), indices  Indice object(),
        listaRegistros Registros object()
    """
    ant = Registro( "", "", "", "", "")
    for i in indices.indices:
        if(chave > ant.codigo and chave < i.codigo):
            registro = listaRegistros.getRegistro(ant.codigo)
            registro.elo = linhachave
            indice = Indice(chave, ant.indice)
            indices.IncluiIndices(indice)
            indices.ordenarIndices()
            return
        ant = i

def gravaDados(linhaarq, indices, numL):
    """
    Cria objetos, e adiciona a nas listas.
    Parametros : linhaarq String Linha do arquivo,
        registros Registros object(),
        indices  Indice object(),
        numL é a linha do arquivo para adicionar no indice,

    """
    # import ipdb; ipdb.set_trace()

    indice = Indice(linhaarq[0:7], numL)
    return indice

def gravaDadosReorganizacao(linhaarq, indices, numL):
    """
    Cria objetos, e adiciona a nas listas.
    Parametros : linhaarq String Linha do arquivo,
        registros Registros object(),
        indices  Indice object(),
        numL é a linha do arquivo para adicionar no indice,

    """
    # registro = Registro(
    #     linhaarq[0:7], linhaarq[7:52], linhaarq[52:82],
    #     linhaarq[82:83], linhaarq[83:87]
    # )
    # registros.IncluiRegistros(registro)
    indice = indices.get(linhaarq[0:7])
    if indice:
        if indice.excluido:
            return False
        else:
            return True
    else:
        indice = Indice(linhaarq[0:7], numL)
        indices.add(indice)
        return True


def gravaIndices(indices, linha):
    """
    Cria objetos Indices.
    Parametros : linha String Linha do arquivo,
        indices  Indice object(),
    """
    atributos = linha.split(",")
    codigo = atributos[0]
    ind = atributos[1]
    exc = atributos[2]
    indice = Indice(codigo, ind, exc)
    indices.IncluiIndices(indice)
    return

def incluiRegistroAreaExtencao(raizIndices, extencao):
    """
    Inclui novos Registros na Area extencao.
    Parametros : listaRegistrosExtensao Registros object(),
        listaRegistros Registros object(),
        indices  Indice object(),
    """
    chave = (raw_input('\tDigite o codigo": '))
    nomeLivro = (raw_input('\tDigite o nome do Livro: '))
    nomeAutor = (raw_input('\tDigite o nome do Autor: '))
    mes = (raw_input('\tDigite o mes: '))
    ano = (raw_input('\tDigite o ano: '))
    indice = Indice(chave, extencao, False, None, None, True)
    if raizIndices == None:
        raizIndices = indice
    else:
        raizIndices.add(indice)
    gravarArquivoExtencao(chave, nomeLivro, nomeAutor, mes, ano, extencao)
    return raizIndices

def getRegistroArquivo(indices):
    """
    Faz busca do registro no arquivo de Indices e Retorna um registro.
    Parametros : Indices() object,
    Return : Retorna String de linha do Arquivo de DADOS
    """
    chave = (raw_input('\tDigite o codigo que deseja buscar": '))
    indice = indices.get(chave)
    if indice:
        if not indice.excluido:
            if indice.extencao:
                linha = getArquivoExtencao(chave)
                return linha
            else:
                linha = lerLinha(indice.linha, 0)
                return linha

def getExclusao(indices):
    """
    Faz busca do registro no arquivo de Indices.
    Parametros : Indices() object,
    Return : Retorna String de linha do Arquivo de DADOS
    """
    chave = (raw_input('\tDigite o codigo que deseja Deletar: '))
    indice = indices.get(chave)
    if indice:
        indice.excluirLogico()
        return True
    return False

def reorganizarArquivo(raizIndice):
    arquivo2 = open("arquivo2.txt", "w")
    pos = 0
    param = 0
    lim = 100
    pos2 = 0
    retorno = (True, "")
    while retorno[0]:
        retorno = lerArquivoReorganizacao(raizIndice, pos, pos2, param, lim, arquivo2)
        pos += lim
        pos += 1
        pos2 += retorno[1]
    arquivo2.close()

def main():
    """
    Inicio Sistema.
    Menu.
    """
    raizIndice = Indice(0, 0)
    opcao = 5
    extencao = 0
    excluido = 0
    while opcao<=8:
        print "\n\tDigite 1 carregar arquivo de DADOS:\n"
        print "\tDigite 2 para pesquisar um registro:\n"
        print "\tDigite 3 para Inserir um novo registro:\n"
        print "\tDigite 4 para Excluir um registro:\n"
        print "\tDigite 5 para dump dos indices:\n"
        print "\tDigite 6 para load dos indices:\n"
        print "\tDigite 7 para reorganizar o arquivo:\n"

        opcao = int(raw_input('\tDigite a opcao: '))

        if(opcao == 1):
            arq = open("arquivo.txt", "r")
            pos = 0
            param = 0
            lim = 100
            retorno = ("", True)
            while retorno[1]:
                retorno = lerArquivo(raizIndice, pos, param, lim, arq)
                pos += lim
                pos += 1
            raizIndice = retorno[0]
            # raizIndice.imprimeArvore()
            raizIndice.executaBalanco()
            # raizIndice.profundidade()
            arq.close()

        elif(opcao == 2):
            if raizIndice:
                registro = getRegistroArquivo(raizIndice)
                if registro:
                    print registro
                else:
                    print "\n\tRegistro não encontrado!!!\n"
            else:
                print "\n\tNão há Indices\n"
        elif(opcao == 3):
            extencao += 1
            incluiRegistroAreaExtencao(raizIndice, extencao)
            if extencao == 100:
                raizIndice.executaBalanco()
        elif(opcao == 4):
            if getExclusao(raizIndice):
                excluido += 1
            else:
                print "\n\tRegistro não encontrado!!\n"
            if excluido >= 100:
                reorganizarArquivo()
                excluido = 0
        elif(opcao == 5):
            arq = open("indices.data", "w")
            pickle.dump(raizIndice, arq)
            arq.close()
        elif(opcao == 6):
            arq = open("indices.data", "r")
            raizIndice = pickle.load(arq)
            arq.close()
        elif(opcao == 7):
            reorganizarArquivo(raizIndice)
    return

if __name__ == '__main__':
    main()

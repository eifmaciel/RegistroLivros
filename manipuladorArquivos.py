# -*- coding: utf-8 -*-

# Organização de Arquivos Sequencial Indexada;
# Autores : Eliane, Lucas

from indice import *
from interface import *
import sys

def lerArquivo(indices, pos, param, lim, arq):
    """
    LÊ arquivo de DADOS arquivo.txt.
    Parametros : Registros() object , Indices() object, pos Posição do arquivo
        param  parametro da função seek;
    """
    numL = pos
    lim = pos + lim
    linha = "aa"
    while linha and numL<=lim:
        numL+=1
        linha = arq.readline()
        indice = gravaDados(linha, indices, numL)
        indices.add(indice)
    if numL<= 1000:
        return (indices, True, numL)
    else:
        return (indices, False, numL)

def lerArquivoReorganizacao(indices, pos, pos2, param, lim, arquivo2):
    """
    LÊ arquivo de DADOS arquivo.txt.
    Parametros : Registros() object , Indices() object, pos Posição do arquivo
        param  parametro da função seek;
    """
    arq = open("arquivo.txt", "r")
    numL = pos
    numL2 = pos2
    lim = pos + lim
    pos = 88*pos
    arq.seek(pos, param)
    linha = "aa"
    while linha and numL<=lim:
        linha = arq.readline()
        retorno = gravaDadosReorganizacao(linha, indices, numL)
        numL+=1
        if retorno:
            arquivo2.write(linha)
            numL2 += 1
    arq.close()
    if numL<= 1000:
        return (True, numL2)
    else:
        return (False, numL2)

def lerLinha(pos1, param):
    """
    param : Este é opcional e o padrão é 0, posicionamento arquivo absoluto,
    1 buscar em relação à posição atual,
    2 significa buscar em relação ao final do arquivo.
    pos : posicao no arquivo
    """
    arq = open("arquivo.txt", "r")
    linha = ""
    lines = arq.readlines()
    linha = lines[pos1]

    arq.close()
    return linha

def lerLinhaIndice(pos, param):
    """
    param : Este é opcional e o padrão é 0, posicionamento arquivo absoluto,
    1 buscar em relação à posição atual,
    2 significa buscar em relação ao final do arquivo.
    pos : posicao no arquivo
    """
    arq = open("arquivoIndices.txt", "r")
    arq.seek(pos, param)
    linha = arq.readline()
    arq.close()
    return linha

def lerArquivoIndices(indices):
    """
    LÊ arquivo de INDICES arquivoIndices.txt.
    Parametros : Indices() object
    """
    arq = open("arquivoIndices.txt", "r")
    linha = arq.readline()
    gravaIndices(indices, linha)
    while linha:
        linha = arq.readline()
        registro = gravaDados(indices, linha)

    arq.close()
    return

def gravarArquivoIndices(indices):
    """
    Grava objetos em formato texto no arquivo de Indices.
    Parametros : Indices() object,
    """
    arq = open("arquivoIndices.txt", "w")
    for i in indices.indices:
        linha = i.codigo + "," + str(i.indice) + "," + str(i.excluido) + "\n"
        arq.write(linha)
    arq.close()
    return

def gravarArquivoExtencao(chave, nomeLivro, nomeAutor, mes, ano, extencao):
    """
    Grava objetos em formato texto no arquivo Extencao
    Parametros : Registros() object,
    """
    arq = open("arquivoExtencao.txt", "w")
    linha = chave + nomeLivro + nomeAutor + mes + ano + "\n"
    arq.seek(extencao, 0)
    arq.write(linha)
    arq.close()
    return

def getArquivoExtencao(chave):
    """
    Grava objetos em formato texto no arquivo Extencao
    Parametros : Registros() object,
    """
    arq = open("arquivoExtencao.txt", "r")
    linha = arq.readline()
    achou = False
    while linha and not achou:
        if linha[0:7] == chave:
            achou = True
        linha = arq.readline()
    arq.close()
    return linha

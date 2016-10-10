# -*- coding: utf-8 -*-

# Organização de Arquivos Sequencial Indexada;
# Autores : Eliane, Lucas

import operator
import pickle

class Indice(object):
    """
    Object Indice.
    """
    def __init__(self, codigo, indice, excluido=False, left=None, right=None, novo=False):
        # Inicializa as variaveis com os argumentos passados
        self.codigo = codigo
        self.excluido = excluido
        self.linha = indice
        self.left = left
        self.right = right
        self.extencao = novo

    def excluirLogico(self):
        self.excluido = True

    def get(self, key):
        if key < self.codigo:
            return self.left.get(key) if self.left else None
        elif key > self.codigo:
            return self.right.get(key) if self.right else None
        else:
            return self

    def setaFilhos(self, esquerda, direita):
        self.left = esquerda
        self.right = direita

    def add(self, node):
        if node.codigo <= self.codigo:
            if not self.left:
                self.left = node
            else:
                self.left.add(node)
        else:
            if not self.right:
                self.right = node
            else:
                self.right.add(node)
        # self.executaBalanco()

    def remove(self, key):
        if key < self.codigo:
            self.left = self.left.remove(key)
        elif key > self.codigo:
            self.right = self.right.remove(key)
        else:
            # encontramos o elemento, então vamos removê-lo!
            if self.right is None:
                return self.left
            if self.left is None:
                return self.right
            #ao invés de remover o nó, copiamos os valores do nó substituto
            tmp = self.right._min()
            self.codigo, self.linha = tmp.codigo, tmp.linha
            self.right._remove_min()
        return self

    def _min(self):
        """Retorna o menor elemento da subárvore que tem self como raiz.
        """
        if self.left is None:
            return self
        else:
            return self.left._min()

    def _remove_min(self):
        """Remove o menor elemento da subárvore que tem self como raiz.
        """
        if self.left is None:  # encontrou o min, daí pode rearranjar
            return self.right
        self.left = self.left._removeMin()
        return self

    def balanco(self):
        prof_esq = 0
        if self.left:
            prof_esq = self.left.profundidade()
        prof_dir = 0
        if self.right:
            prof_dir = self.right.profundidade()
        return prof_esq - prof_dir

    def profundidade(self):
        prof_esq = 0
        if self.left:
            prof_esq = self.left.profundidade()
        prof_dir = 0
        if self.right:
            prof_dir = self.right.profundidade()
        return 1 + max(prof_esq, prof_dir)

    def rotacaoleft(self):
        self.codigo, self.right.codigo = self.right.codigo, self.codigo
        old_left = self.left
        self.setaFilhos(self.right, self.right.right)
        self.left.setaFilhos(old_left, self.left.left)

    def rotacaoright(self):
        self.codigo, self.left.codigo = self.left.codigo, self.codigo
        old_right = self.right
        self.setaFilhos(self.left.left, self.left)
        self.right.setaFilhos(self.right.right, old_right)

    def rotacaoleftright(self):
        self.left.rotacaoleft()
        self.rotacaoright()

    def rotacaorightleft(self):
        self.right.rotacaoright()
        self.rotacaoleft()

    def executaBalanco(self):
        bal = self.balanco()
        if bal > 1:
            if self.left.balanco() > 0:
                self.rotacaoright()
            else:
                self.rotacaoleftright()
        elif bal < -1:
            if self.right.balanco() < 0:
                self.rotacaoleft()
            else:
                self.rotacaorightleft()

    def imprimeArvore(self, indent = 0):
        print " " * indent + str(self.codigo)
        if self.left:
            self.left.imprimeArvore(indent + 2)
        if self.right:
            self.right.imprimeArvore(indent + 2)


class IndiceString(object):
    """
    Object Indice.
    """
    def __init__(self, codigo, indice, excluido=False, left=None, right=None, novo=False):
        # Inicializa as variaveis com os argumentos passados
        self.codigo = codigo
        self.excluido = excluido
        self.linha = indice
        self.left = left
        self.right = right
        self.extencao = novo

    def excluirLogico(self):
        self.excluido = True

    def get(self, key):
        if key < self.codigo:
            return self.left.get(key) if self.left else None
        elif key > self.codigo:
            return self.right.get(key) if self.right else None
        else:
            return self

    def setaFilhos(self, esquerda, direita):
        self.left = esquerda
        self.right = direita

    def add(self, node):
        if node.codigo <= self.codigo:
            if not self.left:
                self.left = node
            else:
                self.left.add(node)
        else:
            if not self.right:
                self.right = node
            else:
                self.right.add(node)
        self.executaBalanco()

    def remove(self, key):
        if key < self.codigo:
            self.left = self.left.remove(key)
        elif key > self.codigo:
            self.right = self.right.remove(key)
        else:
            # encontramos o elemento, então vamos removê-lo!
            if self.right is None:
                return self.left
            if self.left is None:
                return self.right
            #ao invés de remover o nó, copiamos os valores do nó substituto
            tmp = self.right._min()
            self.codigo, self.linha = tmp.codigo, tmp.linha
            self.right._remove_min()
        return self

    def _min(self):
        """Retorna o menor elemento da subárvore que tem self como raiz.
        """
        if self.left is None:
            return self
        else:
            return self.left._min()

    def _remove_min(self):
        """Remove o menor elemento da subárvore que tem self como raiz.
        """
        if self.left is None:  # encontrou o min, daí pode rearranjar
            return self.right
        self.left = self.left._removeMin()
        return self

    def balanco(self):
        prof_esq = 0
        if self.left:
            prof_esq = self.left.profundidade()
        prof_dir = 0
        if self.right:
            prof_dir = self.right.profundidade()
        return prof_esq - prof_dir

    def profundidade(self):
        prof_esq = 0
        if self.left:
            prof_esq = self.left.profundidade()
        prof_dir = 0
        if self.right:
            prof_dir = self.right.profundidade()
        return 1 + max(prof_esq, prof_dir)

    def rotacaoleft(self):
        self.codigo, self.right.codigo = self.right.codigo, self.codigo
        old_left = self.left
        self.setaFilhos(self.right, self.right.right)
        self.left.setaFilhos(old_left, self.left.left)

    def rotacaoright(self):
        self.codigo, self.left.codigo = self.left.codigo, self.codigo
        old_right = self.right
        self.setaFilhos(self.left.left, self.left)
        self.right.setaFilhos(self.right.right, old_right)

    def rotacaoleftright(self):
        self.left.rotacaoleft()
        self.rotacaoright()

    def rotacaorightleft(self):
        self.right.rotacaoright()
        self.rotacaoleft()

    def executaBalanco(self):
        bal = self.balanco()
        if bal > 1:
            if self.left.balanco() > 0:
                self.rotacaoright()
            else:
                self.rotacaoleftright()
        elif bal < -1:
            if self.right.balanco() < 0:
                self.rotacaoleft()
            else:
                self.rotacaorightleft()

    def imprimeArvore(self, indent = 0):
        print " " * indent + str(self.codigo)
        if self.left:
            self.left.imprimeArvore(indent + 2)
        if self.right:
            self.right.imprimeArvore(indent + 2)


class Registro:
    """
    object Registro.
    """
    TAMANHOREGISTRO = 88;
    def __init__(self, codigo, nomeLivro, autor, mes, ano):
        # Inicializa as variaveis com os argumentos passados
        self.nomeAutor = autor
        self.mes = mes
        self.ano = ano
        self.codigo = codigo
        self.nomeLivro = nomeLivro
        self.elo = 0


class Registros:
    """
    Contém lista Registros.
    """
    # Contem os registros
    menorCodigo = 0

    def __init__(self):
        self.registros = []

    def IncluiRegistros(self, new_registros):
        # Recebe o registro passado
        self.registros.append(new_registros)

    def setRegistrosAt(self, registro, posicao):
        # Coloca o registro na posicao

        self.registros.insert(registro, posicao)

    def ordenarRegistros(self):
        # Ordena registros com pelo código
        self.registros.sort(key=operator.attrgetter('codigo'))

    def getRegistro(self, chave):
        # Retorna registro com a chave
        for i in self.registros:
            if(i.codigo == chave):
                return i

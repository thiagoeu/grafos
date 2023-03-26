from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_errors import *


class MeuGrafo(GrafoListaAdjacencia):

    def vertices_nao_adjacentes(self):
        '''
        Provê um conjunto de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um objeto do tipo set que contém os pares de vértices não adjacentes
        '''

        arestasGrafo = set()
        for a in self.arestas:
            arestaAtual = self.arestas[a]
            verticesAresta = f'{arestaAtual.v1}-{arestaAtual.v2}'
            arestasGrafo.add(verticesAresta)

        verticesNaoAdjacentes = set()
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                novaAresta = f'{self.vertices[i]}-{self.vertices[j]}'
                if novaAresta not in arestasGrafo and novaAresta[::-1] not in arestasGrafo:
                    verticesNaoAdjacentes.add(novaAresta)

        return verticesNaoAdjacentes


    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        arestas = self.arestas
        for a in arestas:
            if arestas[a].v1 == arestas[a].v2:
                return True
        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        grau = 0

        if (not self.existe_rotulo_vertice(V)):
            raise VerticeInvalidoError()
        for a in self._arestas:
            if self.arestas[a].v1.rotulo == V:
                grau += 1
            if self.arestas[a].v2._rotulo == V:
                grau += 1

        return grau

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        arestas = set()
        for a in self.arestas:

            arestaAtual = self.arestas[a]
            verticesAresta = (arestaAtual.v1.rotulo, arestaAtual.v2.rotulo)

            if verticesAresta in arestas or verticesAresta[::-1] in arestas:
                return True

            arestas.add(verticesAresta)

        return False

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: Um string com o rótulo do vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError
        else:
            conj = set()
            for a in self.arestas:
                if self.arestas[a].v1.rotulo == V or self.arestas[a].v2.rotulo == V:
                    conj.add(a)
            return conj

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        for v in self.vertices:
            if self.grau(v.rotulo) != len(self.vertices) - 1:
                return False
        return True

    def dfs(self, V=''):
        '''
        :param V: Vertice a ser utilizado como raiz
        :return: Uma chamada a função auxiliar para a busca em profundidade
        '''
        arv_dfs = MeuGrafo()
        arv_dfs.adiciona_vertice(V)
        return self.dfs_rec(V, arv_dfs)

    def dfs_rec(self, V, arv_dfs):
        '''
        Função recursiva para busca em profundidade
        :param V: Vertice a ser utilizado como raiz
        :param arv_dfs: Arvore DFS
        :return: Retorna o grafo de busca em profundidade
        '''
        if len(self.vertices) == len(arv_dfs.vertices):
            return arv_dfs
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError

        aux = self.arestas_sobre_vertice(V)
        rotulos = list(aux)
        rotulos.sort()
        for a in rotulos:
            if not arv_dfs.existe_rotulo_vertice(a):
                if V == self.arestas[a].v1.rotulo:
                    r = self.arestas[a].v2.rotulo
                else:
                    r = self.arestas[a].v1.rotulo

                if not arv_dfs.existe_rotulo_vertice(r):
                    arv_dfs.adiciona_vertice(r)
                    arv_dfs.adiciona_aresta(self.arestas[a])
                    self.dfs_rec(r, arv_dfs)

        return arv_dfs

    def bfs(self, V=''):
        '''
        :param V: Vertice a ser utilizado como raiz
        :return: Uma chamada a função auxiliar para a busca em largura
        '''
        arv_bfs = MeuGrafo()
        arv_bfs.adiciona_vertice(V)
        return self.bfs_rec(V, arv_bfs)

    def bfs_rec(self, V, arv_bfs):
        '''
        Função recursiva para busca em largura
        :param V: Vertice a ser utilizado como raiz
        :param arv_bfs: Árvore BFS
        :return: Retorna o grafo de busca em largura
        '''
        if len(self.vertices) == len(arv_bfs.vertices):
            return arv_bfs
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError
        for a in self.arestas:
            if self.arestas[a].v1.rotulo == V and self.arestas[a].v1.rotulo != self.arestas[a].v2.rotulo:
                aux = self.arestas[a].v1.rotulo
                prox = self.arestas[a].v2.rotulo
                if arv_bfs.existe_rotulo_vertice(aux) and not arv_bfs.existe_rotulo_vertice(prox):
                    arv_bfs.adiciona_vertice(prox)
                    arv_bfs.adiciona_aresta(self.arestas[a])
        self.bfs_rec(prox, arv_bfs)

        return arv_bfs
import copy
from datetime import datetime

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._bestScore = 0
        self._optListCircuiti = []

    def getCampionatoIdeale(self, soglia, numAnni):

        tic = datetime.now()
        compConnessa = list(nx.connected_components(self._graph))[0]
        self._bestScore = 0
        self._optListCircuiti = []
        parziale = []
        rimanenti = copy.deepcopy(compConnessa)

        for c in compConnessa:
            if len(list(c.results.keys())) >= numAnni:
                parziale.append(c)
                rimanenti.remove(c)
                self._ricorsione(parziale, rimanenti, soglia, numAnni)
                parziale.pop()
                rimanenti.add(c)

        listOfScores = []
        for c in self._optListCircuiti:
            listOfScores.append(self._calcolaIndiceCircuito(c))

        toc = datetime.now()
        print(f"Tempo di esecuzione: {toc-tic}")
        return self._optListCircuiti, self._bestScore, listOfScores

    def _ricorsione(self, parziale, rimanenti, soglia, numAnni):
        if len(parziale) == soglia:
            #questa fa sia da condizione di ottimalità sia da condizione di terminazione
            if self._getScoreSoluzione(parziale) > self._bestScore:
                self._bestScore = self._getScoreSoluzione(parziale)
                self._optListCircuiti = copy.deepcopy(parziale)
            return

        for c in rimanenti:
            if len(list(c.results.keys())) >= numAnni:
                parziale.append(c)
                rimanenti.remove(c)
                self._ricorsione(parziale, rimanenti, soglia, numAnni)
                parziale.pop()
                rimanenti.add(c)

    def _getScoreSoluzione(self, listOfCircuits):
        listOfScores = []
        for c in listOfCircuits:
            listOfScores.append(self._calcolaIndiceCircuito(c))

        return sum(listOfScores)

    def buildGraph(self, minY, maxY):
        self._graph.clear()
        self._nodes = self._getNodi(minY, maxY)
        self._graph.add_nodes_from(self._nodes)

        #Aggiunta archi non richiede una query perchè abbiamo già importato i risultati
        for i in self._nodes:
            for j in self._nodes:
                if i.circuitId < j.circuitId and self._calcolaPesoArco(i, j) > 0:
                        peso = self._calcolaPesoArco(i, j)
                        self._graph.add_edge(i, j, weight=self._calcolaPesoArco(i, j))

    def getGraphDetails(self):
        connComps = list(nx.connected_components(self._graph))
        connessa = connComps[0]
        res = []
        for c in connessa:
            res.append((c, self._getMaxEdge(c)))

        res.sort(key=lambda x: x[1], reverse=True)
        return res

    def getYears(self):
        return DAO.getAnni()

    def getGraphInfo(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def _getMaxEdge(self, nodo):
        # val = 0
        # for i in self._graph.neighbors(nodo):
        #     if self._graph[nodo][i]["weight"]>val:
        #         val = self._graph[nodo][i]["weight"]
        #
        # return val
        #
        return max(self._graph.get_edge_data(nodo, i)['weight'] for i in self._graph.neighbors(nodo))

    def _getNodi(self, minY, maxY):
        allCircuits = DAO.getAllCircuits()
        for c in allCircuits:
            for y in range(minY, maxY+1):
                res = DAO.getResultsCircuitYear(c.circuitId, y)
                if len(res) > 0:
                    c.results[y] = res
        return allCircuits

    def _calcolaPesoArco(self, n1, n2):
        # il peso dell'arco è definito come il numero totale di piloti
        # che hanno raggiunto il traguardo. Se ci sono 4 piloti
        # che non hanno finito la gara (il campo position è null) allora il
        # valore da considerare per quell'anno è nTotPiloti - 4
        # L'arco non esiste se uno dei due circuiti non ha ospitato gare nel range selezionato
        # (ovvero, il nodo deve rimanere isolato)
        peso = 0

        if len(n1.results.values()) == 0 or len(n2.results.values()) == 0:
            return peso

        for r in n1.results.values(): #per ogni anno
            for p in r: #per ogni pilota
                if p.position is not None:
                    peso += 1

        for r in n2.results.values(): #per ogni anno
            for p in r: #per ogni pilota
                if p.position is not None:
                    peso += 1

        return peso

    def _calcolaIndiceCircuito(self, circuito):
        nP = 0
        nPtot = 0

        if len(circuito.results.values()) == 0:
            return 0 #questo caso non dovrebbe mai accadere perchè questa funzione viene chiamata solo su nodi appartenenti alla componente connessa.

        for r in circuito.results.values():  # per ogni anno prendo tutti i risultati della gara
            nPtot += len(r)
            for p in r:  # per ogni pilota
                if p.position is not None:
                    nP += 1

        return 1-nP/nPtot
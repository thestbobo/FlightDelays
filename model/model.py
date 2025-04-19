import copy

import networkx as nx
from database.DAO import DAO
class Model:
    def __init__(self):
        self._myGraph = nx.Graph()
        self._allAirports = DAO.getAllAirports()
        self._idMap = {}
        for a in self._allAirports:
            self._idMap[a.ID] = a

        self._solBest = []
        self._weightBest = None


        pass

    def buildGraph(self, nMin):
        self._nodi = DAO.getAllNodes(nMin, self._idMap)
        self._myGraph.add_nodes_from(self._nodi)

        self._addEdgesV2()

        pass

    def printGraphDetails(self):
        print(f"Num nodi: {len(self._myGraph.nodes)} - Num archi: {len(self._myGraph.edges)}")

    def getNumNodi(self):
        return len(self._myGraph.nodes)

    def getNumArchi(self):
        return len(self._myGraph.edges)
    def analyze_airports(self, min):
        self.buildGraph(min)
        pass

    def _addEdgesV1(self):
        allConnessioni = DAO.getAllEdgesV1(self._idMap)
        for c in allConnessioni:
            v0 = c.V0
            v1 = c.V1
            peso = c.N
            if v0 in self._myGraph and v1 in self._myGraph:
                if self._myGraph.has_edge(v0, v1):
                    self._myGraph[v0][v1]["weight"] += peso
                else:
                    self._myGraph.add_edge(v0,v1, weight=peso)
        pass

    def _addEdgesV2(self):
        allConnessioni = DAO.getAllEdgesV2(self._idMap)
        for c in allConnessioni:
            if c.V0 in self._myGraph and c.V1 in self._myGraph:
                self._myGraph.add_edge(c.V0, c.V1, weight=c.N)
            # il secondo 'if' (metodo addedgesV1) in questa V2 è stato fatto in SQL nella query di 'getAllEdgesV2()' del DAO
        pass

    def getConnNodes(self):
        return self._myGraph.nodes

    def getNeighborNodes(self, v0):
        neighbors = self._myGraph.neighbors(v0)
        neighborsTuple = []
        for n in neighbors:
            neighborsTuple.append((n, self._myGraph[v0][n]["weight"]))
        neighborsTuple.sort(key=lambda x: x[1], reverse=True)
        return neighborsTuple

    def check_path_existence(self, p, a):
        # if nx.has_path(self._myGraph, p, a):
        #     return [True, nx.shortest_path(self._myGraph, source=p, target=a, method="dijkstra")]
        # else:
        #     return [False, None]
        connected = nx.node_connected_component(self._myGraph, p)
        if a in connected:
            return True
        return False

    def find_path_dijkstra(self, p, a):
        return nx.dijkstra_path(self._myGraph, p, a)

    def find_path_BFS(self, p ,a):
        tree = nx.bfs_tree(self._myGraph, p)
        if a in tree:
            print(f"{a} è presente nell'albero di visita BFS")
        path = [a]

        while path[-1] != p:
            path.append(list(tree.predecessors(path[-1]))[0])
        path.reverse()
        return path

    def find_path_DFS(self, p, a):
        tree = nx.dfs_tree(self._myGraph, p)
        if a in tree:
            print(f"{a} è presente nell'albero di visita BFS")
        path = [a]

        while path[-1] != p:
            path.append(list(tree.predecessors(path[-1]))[0])
        return path



    def get_best_path(self, p, a, nMax):
        self._solBest = []
        self._weightBest = 0
        partial = [p]
        self._recursion(partial, a, nMax)
        return self._solBest, self._weightBest

    def _recursion(self, partial, end_node, nMax):

        # Controllo che sol sia valida e
        #       se migliore di sol best precedente la rimpiazzo
        if len(partial) == nMax+1:
            if self.get_path_weight(partial) > self._weightBest and partial[-1] == end_node:
                self._solBest = copy.deepcopy(partial)
                self._weightBest = self.get_path_weight(partial)
            return

        for n in self._myGraph.neighbors(partial[-1]):
            if n not in partial:
                partial.append(n)
                self._recursion(partial, end_node, nMax)
                partial.pop()


    def get_path_weight(self, path):
        tot_weight = 0
        for n in range(0, len(path)-1):
            tot_weight += self._myGraph[path[n]][path[n+1]]["weight"]

        return tot_weight

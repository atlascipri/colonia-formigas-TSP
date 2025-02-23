import numpy as np
from typing import List, Tuple, Dict
from random import random, choice
from math import sqrt


class OtimizacaoColoniaFormigas:
    def __init__(self, pontos: Dict[int, Tuple[float, float]], n_formigas: int, n_iteracoes: int, alfa: float,
                 beta: float, evaporacao: float, q: float):
        self.pontos = pontos
        self.n_formigas = n_formigas
        self.n_iteracoes = n_iteracoes
        self.alfa = alfa
        self.beta = beta
        self.evaporacao = evaporacao
        self.q = q
        self.n_cidades = len(pontos)
        self.matriz_distancias = self.calcular_distancias()
        self.feromonios = np.ones((self.n_cidades, self.n_cidades))
        self.melhor_solucao = None
        self.melhor_custo = float('inf')
        self.primeira_cidade = list(pontos.keys())[0]

    def calcular_distancias(self) -> np.ndarray:
        matriz_distancias = np.zeros((self.n_cidades, self.n_cidades))
        for i in range(self.n_cidades):
            for j in range(self.n_cidades):
                if i != j:
                    matriz_distancias[i][j] = sqrt((self.pontos[i + 1][0] - self.pontos[j + 1][0]) ** 2 + (
                                self.pontos[i + 1][1] - self.pontos[j + 1][1]) ** 2)
        return matriz_distancias

    def construir_solucao(self) -> Tuple[List[int], float]:
        solucao = [self.primeira_cidade]
        custo_total = 0
        visitadas = set(solucao)

        while len(solucao) < self.n_cidades:
            atual = solucao[-1]
            probabilidades = self.obter_probabilidades(atual, visitadas)
            proxima_cidade = self.selecao_roleta(probabilidades)
            solucao.append(proxima_cidade)
            visitadas.add(proxima_cidade)
            custo_total += self.matriz_distancias[atual - 1][proxima_cidade - 1]
        
        solucao.append(self.primeira_cidade)
        custo_total += self.matriz_distancias[solucao[-2] - 1][solucao[-1] - 1]
      

        return solucao, custo_total

    def obter_probabilidades(self, atual: int, visitadas: set) -> Dict[int, float]:
        probabilidades = {}
        total = 0
        for cidade in self.pontos.keys():
            if cidade not in visitadas:
                feromonio = self.feromonios[atual - 1][cidade - 1] ** self.alfa
                visibilidade = (1 / self.matriz_distancias[atual - 1][cidade - 1]) ** self.beta
                probabilidades[cidade] = feromonio * visibilidade
                total += probabilidades[cidade]
        for cidade in probabilidades:
            probabilidades[cidade] /= total
        return probabilidades

    def selecao_roleta(self, probabilidades: Dict[int, float]) -> int:
        aleatorio = random()
        acumulado = 0
        for cidade, prob in probabilidades.items():
            acumulado += prob
            if aleatorio <= acumulado:
                return cidade
        return choice(list(probabilidades.keys()))

    def atualizar_feromonios(self, solucoes: List[Tuple[List[int], float]]):
        self.feromonios *= (1 - self.evaporacao)
        for solucao, custo in solucoes:
            for i in range(len(solucao) - 1):
                self.feromonios[solucao[i] - 1][solucao[i + 1] - 1] += self.q / custo
            self.feromonios[solucao[-1] - 1][solucao[0] - 1] += self.q / custo

    def executar(self):
        for _ in range(self.n_iteracoes):
            solucoes = [self.construir_solucao() for _ in range(self.n_formigas)]
            solucoes.sort(key=lambda x: x[1])
            if solucoes[0][1] < self.melhor_custo:
                self.melhor_solucao, self.melhor_custo = solucoes[0]
            self.atualizar_feromonios(solucoes)
        print(f"\n\n>>> Melhor solução encontrada é {self.melhor_solucao}\nFunção objetivo de {self.melhor_custo}\n\n")


def carregar_entrada(arquivo: str) -> Dict[int, Tuple[float, float]]:
    with open(arquivo, "r") as f:
        linhas = f.readlines()

    n_cidades = int(linhas[0].strip())
    pontos = {}

    for linha in linhas[1:]:
        partes = linha.split()
        pontos[int(partes[0])] = (float(partes[1]), float(partes[2]))

    return pontos


def principal():
    pontos = carregar_entrada("berlin52.txt")
    aco = OtimizacaoColoniaFormigas(pontos, n_formigas=50, n_iteracoes=1000, alfa=1.0, beta=2.0, evaporacao=0.1, q=100)
    aco.executar()


if __name__ == "__main__":
    principal()

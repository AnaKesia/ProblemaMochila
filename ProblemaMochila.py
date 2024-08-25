import random
import time

import matplotlib.pyplot as plt


# Algoritmo recursivo com memoização
def mochila_memoizacao_recursiva(W, wt, val, n, memo):
    if n == 0 or W == 0:
        return 0

    if memo[n][W] != -1:
        return memo[n][W]

    if wt[n-1] > W:
        memo[n][W] = mochila_memoizacao_recursiva(W, wt, val, n-1, memo)
    else:
        memo[n][W] = max(val[n-1] + mochila_memoizacao_recursiva(W-wt[n-1], wt, val, n-1, memo),
                         mochila_memoizacao_recursiva(W, wt, val, n-1, memo))
    return memo[n][W]

def mochila_memoizacao(W, wt, val, n):
    memo = [[-1 for _ in range(W+1)] for _ in range(n+1)]
    return mochila_memoizacao_recursiva(W, wt, val, n, memo)

# Algoritmo iterativo (Tabela)
def mochila_iterativa(W, wt, val, n):
    K = [[0 for _ in range(W+1)] for _ in range(n+1)]

    for i in range(n+1):
        for w in range(W+1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]

    return K[n][W]

# Função para gerar entradas aleatórias
def generate_knapsack_input(n):
    weights = [random.randint(1, 100) for _ in range(n)]
    values = [random.randint(1, 100) for _ in range(n)]
    capacity = random.randint(50, 100)
    return weights, values, capacity

# Função para medir o tempo de execução
def measure_execution_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return end_time - start_time

# Função para comparar os algoritmos e plotar os resultados
def compare_algorithms():
    input_sizes = range(10, 101, 10)  # Ajustar conforme necessário
    memo_times = []
    iterative_times = []

    for size in input_sizes:
        memo_total_time = 0
        iterative_total_time = 0
        num_trials = 10  # Número de tentativas para média

        for trial in range(num_trials):
            wt, val, W = generate_knapsack_input(size)
            if trial == 0:  # Imprimir apenas a primeira entrada de cada tamanho
                print(f"Tamanho da entrada: {size}, Pesos: {wt}, Valores: {val}, Capacidade: {W}")
            memo_total_time += measure_execution_time(mochila_memoizacao, W, wt, val, size)
            iterative_total_time += measure_execution_time(mochila_iterativa, W, wt, val, size)

        memo_avg_time = memo_total_time / num_trials
        iterative_avg_time = iterative_total_time / num_trials

        memo_times.append(memo_avg_time)
        iterative_times.append(iterative_avg_time)

    plt.plot(input_sizes, memo_times, label='Memoização')
    plt.plot(input_sizes, iterative_times, label='Iterativo')
    plt.xlabel('Tamanho da Entrada (n)')
    plt.ylabel('Tempo Médio de Execução (s)')
    plt.title('Problema da Mochila: Memoização vs Iterativo')
    plt.legend()
    plt.show()

compare_algorithms()

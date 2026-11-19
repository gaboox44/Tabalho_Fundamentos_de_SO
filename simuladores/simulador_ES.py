# -*- coding: utf-8 -*-
"""
SIMULADOR DE ENTRADA E SAÍDA (E/S)
==================================
Disciplina: FSO204 - Sistemas Operacionais (UTFPR Francisco Beltrão)
Autores: [Nome do Integrante 1] e [Nome do Integrante 2]

Objetivo:
  Comparar o gasto de ciclos da CPU ao transferir um arquivo de N blocos
  usando três técnicas diferentes:
    1. Polling (busy-waiting): a CPU fica ocupada vigiando o dispositivo.
    2. Interrupção: a CPU pede o bloco, fica livre e só atende o aviso no fim.
    3. DMA: um controlador copia tudo direto para a RAM sem usar a CPU.

Como rodar no terminal:
  python3 sim_es.py
"""


def simular_polling(blocos):
    """Calcula os ciclos de CPU gastos no modo Polling (espera ocupada)."""
    ciclos_cpu = 0
    for _ in range(blocos):
        ciclos_cpu += 10  # Custo de ficar verificando se o dispositivo está pronto
        ciclos_cpu += 2   # Custo de copiar o bloco para a memória
    return ciclos_cpu


def simular_interrupcao(blocos):
    """Calcula os ciclos de CPU gastos usando Interrupções a cada bloco."""
    ciclos_cpu = 0
    for _ in range(blocos):
        ciclos_cpu += 1   # Custo de enviar o pedido de leitura/escrita
        ciclos_cpu += 3   # Custo de tratar a interrupção quando o bloco termina
    return ciclos_cpu


def simular_dma(blocos):
    """Calcula os ciclos de CPU gastos usando DMA (Acesso Direto à Memória)."""
    # Não há laço 'for' porque o controlador DMA transfere todos os blocos sozinho.
    ciclos_cpu = 0
    ciclos_cpu += 1       # Custo único de programar o DMA no início
    ciclos_cpu += 3       # Custo único de tratar a interrupção ao fim de tudo
    return ciclos_cpu


def calcular_economia(custo_polling, custo_tecnica):
    """Retorna a porcentagem de ciclos economizados em relação ao Polling."""
    if custo_polling == 0:
        return 0.0
    return ((custo_polling - custo_tecnica) / custo_polling) * 100


def exibir_comparacao(blocos):
    """Executa as três simulações para N blocos e imprime uma tabela no terminal."""
    c_polling = simular_polling(blocos)
    c_interr = simular_interrupcao(blocos)
    c_dma = simular_dma(blocos)

    econ_interr = calcular_economia(c_polling, c_interr)
    econ_dma = calcular_economia(c_polling, c_dma)

    print(f"\n=== Transferência de {blocos} blocos ===")
    print(f"{'Técnica':<15} | {'Ciclos de CPU':>15} | {'Economia vs Polling':>20}")
    print("-" * 56)
    print(f"{'Polling':<15} | {c_polling:>15} | {'-- (referência)':>20}")
    print(f"{'Interrupção':<15} | {c_interr:>15} | {econ_interr:>19.2f}%")
    print(f"{'DMA':<15} | {c_dma:>15} | {econ_dma:>19.2f}%")


if __name__ == "__main__":
    print("SIMULADOR DE E/S: POLLING vs INTERRUPÇÃO vs DMA")

    # 1. Testes automáticos com diferentes tamanhos de arquivo
    tamanhos_teste = [100, 1000, 10000]
    for qtd_blocos in tamanhos_teste:
        exibir_comparacao(qtd_blocos)

    # 2. Teste interativo opcional digitado pelo usuário no terminal
    print("\n--- Teste Personalizado ---")
    entrada = input("Digite outro número de blocos para simular (ou Enter para sair): ").strip()

    if entrada != "":
        try:
            blocos_usuario = int(entrada)
            if blocos_usuario > 0:
                exibir_comparacao(blocos_usuario)
            else:
                print("Digite um número maior que zero.")
        except ValueError:
            print("Entrada inválida: digite apenas números inteiros.")

    print("\n=== Conclusão ===")
    print("- Polling: desperdiça CPU esperando o dispositivo bloco a bloco.")
    print("- Interrupção: libera a CPU durante a espera, reduzindo o custo em 66,67%.")
    print("- DMA: melhor técnica para arquivos grandes, pois mantém custo fixo de 4 ciclos.")
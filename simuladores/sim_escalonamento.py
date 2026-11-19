# -*- coding: utf-8 -*-
"""
SIMULADOR DE ESCALONAMENTO DE PROCESSOS
=======================================
Disciplina: FSO204 - Sistemas Operacionais (UTFPR Francisco Beltrão)
Autores: [Gabriel Portes Gomes] e [Luiz Hnrique Correia Serpa]

Objetivo:
  Simular e comparar três algoritmos de escalonamento de CPU:
    1. FCFS (First-Come, First-Served): atende por ordem de chegada.
    2. SJF (Shortest Job First - não-preemptivo): escolhe o processo mais curto disponível.
    3. Round-Robin: reveza a CPU entre os processos usando um limite de tempo (quantum).

Como rodar no terminal:
  python3 sim_escalonamento.py
"""


def gantt(intervalos):
    """Desenha um diagrama de Gantt simples em texto no terminal."""
    linha = ""
    for pid, inicio, fim in intervalos:
        linha += f"[P{pid} {inicio}->{fim}] "
    print("   " + linha.strip())


def calcular_medias(tempos, processos):
    """Calcula a média de espera e a média de retorno (turnaround) dos processos."""
    soma_esp = 0
    soma_ret = 0
    n = len(processos)
    for pid, _, _ in processos:
        esp, ret = tempos[pid]
        soma_esp += esp
        soma_ret += ret
    return soma_esp / n, soma_ret / n


def mostrar(alg, intervalos, tempos, processos):
    """Exibe o diagrama de Gantt, os tempos individuais e as médias de um algoritmo."""
    print(f"\n===== {alg} =====")
    gantt(intervalos)
    print(f"   {'Processo':<10}{'Espera':>8}{'Retorno':>10}")
    for pid, _, _ in sorted(processos, key=lambda p: p[0]):
        esp, ret = tempos[pid]
        print(f"   P{pid:<9}{esp:>8}{ret:>10}")
    media_esp, media_ret = calcular_medias(tempos, processos)
    print(f"   {'MÉDIA':<10}{media_esp:>8.2f}{media_ret:>10.2f}")
    return media_esp, media_ret


def fcfs(processos):
    """First-Come, First-Served: executa os processos na ordem de chegada."""
    ordem = sorted(processos, key=lambda p: p[1])  # Ordena pelo tempo de chegada (índice 1)
    tempo = 0
    intervalos = []
    tempos = {}

    for pid, chegada, duracao in ordem:
        if tempo < chegada:
            tempo = chegada  # Avança o relógio se a CPU estiver ociosa
        inicio = tempo
        fim = tempo + duracao
        intervalos.append((pid, inicio, fim))
        tempos[pid] = (inicio - chegada, fim - chegada)  # (espera, retorno)
        tempo = fim

    return intervalos, tempos


def sjf(processos):
    """Shortest Job First (não-preemptivo): executa o processo mais curto já disponível."""
    restantes = list(processos)
    tempo = 0
    intervalos = []
    tempos = {}

    while restantes:
        # Filtra apenas os processos que já chegaram até o instante 'tempo'
        disponiveis = [p for p in restantes if p[1] <= tempo]
        if not disponiveis:
            tempo += 1
            continue

        # Escolhe o processo disponível com menor duração (índice 2)
        pid, chegada, duracao = min(disponiveis, key=lambda p: p[2])
        restantes.remove((pid, chegada, duracao))

        inicio = tempo
        fim = tempo + duracao
        intervalos.append((pid, inicio, fim))
        tempos[pid] = (inicio - chegada, fim - chegada)
        tempo = fim

    return intervalos, tempos


def round_robin(processos, quantum):
    """Round-Robin: cada processo usa a CPU por no máximo 'quantum' e volta para a fila."""
    chegadas = sorted(processos, key=lambda p: p[1])
    fila = []
    restante = {p[0]: p[2] for p in processos}  # Guarda quanto tempo falta para cada PID
    tempo = 0
    intervalos = []
    termino = {}
    idx = 0

    while True:
        # Adiciona à fila todos os processos que chegaram até o tempo atual
        while idx < len(chegadas) and chegadas[idx][1] <= tempo:
            fila.append(chegadas[idx][0])
            idx += 1

        if not fila:
            if idx < len(chegadas):
                tempo = chegadas[idx][1]
                continue
            break

        pid = fila.pop(0)  # Retira o primeiro processo da fila
        executa = min(quantum, restante[pid])
        intervalos.append((pid, tempo, tempo + executa))
        tempo += executa
        restante[pid] -= executa

        # Processos que chegaram durante essa execução entram antes do processo atual voltar
        while idx < len(chegadas) and chegadas[idx][1] <= tempo:
            fila.append(chegadas[idx][0])
            idx += 1

        if restante[pid] > 0:
            fila.append(pid)  # Ainda não terminou: volta para o fim da fila
        else:
            termino[pid] = tempo  # Finalizou: registra o instante de término

    tempos = {}
    for pid, chegada, duracao in processos:
        retorno = termino[pid] - chegada
        espera = retorno - duracao
        tempos[pid] = (espera, retorno)

    return intervalos, tempos


def comparar_resultados(resumos):
    """Imprime uma tabela comparativa final entre os algoritmos executados."""
    print("\n=== Comparação Final (Médias) ===")
    print(f"{'Algoritmo':<25} | {'Espera Média':>13} | {'Retorno Médio':>14}")
    print("-" * 58)
    for nome, m_esp, m_ret in resumos:
        print(f"{nome:<25} | {m_esp:>13.2f} | {m_ret:>14.2f}")

    melhor = min(resumos, key=lambda item: item[1])
    print(f"\n-> Menor tempo médio de espera: {melhor[0]} ({melhor[1]:.2f})")


if __name__ == "__main__":
    # Lista de processos no formato: (pid, tempo de chegada, duração na CPU)
    processos = [
        (1, 0, 5),
        (2, 1, 3),
        (3, 2, 8),
        (4, 4, 2),
    ]
    QUANTUM_PADRAO = 3

    print("SIMULADOR DE ESCALONAMENTO DE CPU")
    print("Processos (pid, chegada, duração):")
    for pid, chegada, duracao in processos:
        print(f"   P{pid}: chega em {chegada}, dura {duracao}")

    resumos = []

    inter, tempos = fcfs(processos)
    m_esp, m_ret = mostrar("FCFS", inter, tempos, processos)
    resumos.append(("FCFS", m_esp, m_ret))

    inter, tempos = sjf(processos)
    m_esp, m_ret = mostrar("SJF (não-preemptivo)", inter, tempos, processos)
    resumos.append(("SJF (não-preemptivo)", m_esp, m_ret))

    inter, tempos = round_robin(processos, QUANTUM_PADRAO)
    m_esp, m_ret = mostrar(f"Round-Robin (q={QUANTUM_PADRAO})", inter, tempos, processos)
    resumos.append((f"Round-Robin (q={QUANTUM_PADRAO})", m_esp, m_ret))

    comparar_resultados(resumos)

    # Teste interativo opcional para comparar outro valor de quantum no Round-Robin
    print("\n--- Teste de Outro Quantum (Round-Robin) ---")
    entrada = input("Digite um novo valor de quantum para testar (ou Enter para sair): ").strip()
    if entrada != "":
        try:
            novo_q = int(entrada)
            if novo_q > 0:
                inter_q, tempos_q = round_robin(processos, novo_q)
                m_esp_q, m_ret_q = mostrar(f"Round-Robin (q={novo_q})", inter_q, tempos_q, processos)
                resumos.append((f"Round-Robin (q={novo_q})", m_esp_q, m_ret_q))
                comparar_resultados(resumos)
            else:
                print("Digite um quantum maior que zero.")
        except ValueError:
            print("Entrada inválida: digite apenas números inteiros.")
# CÓDIGO 2 — SJF (Shortest Job First / menor tarefa primeiro).
# Base: item 2 do guia_estudo_sim_escalonamento.pdf, disciplina FSO204.
# Implementação didática baseada na descrição do guia; o PDF não traz o código completo.
# SJF não preemptivo: depois de começar, o processo executa até terminar.
# Cada processo é uma tupla (identificador, tempo de chegada, duração na CPU).
# Os tempos são unidades simuladas; este programa não precisa esperar segundos reais.
# Espera = início - chegada. Retorno = término - chegada.
# Exemplo próprio: o guia informa durações, mas não explicita todas as chegadas.
# Para executar no terminal com Python instalado: python codigo_2_sjf_comentado.py

def sjf(processos):  # Define a função que recebe a lista de processos.
    restantes = list(processos)  # Copia a lista para não modificar a lista original.
    tempo = 0  # Inicia o relógio da simulação na unidade zero.
    diagrama = []  # Guardará tuplas (nome, início, fim) para desenhar o Gantt.
    resultados = []  # Guardará os tempos calculados para cada processo concluído.

    while restantes:  # Repete enquanto ainda existir algum processo por executar.
        disponiveis = [p for p in restantes if p[1] <= tempo]  # Filtra os que já chegaram; p[1] é a chegada.
        if not disponiveis:  # Se ninguém chegou, a CPU precisa ficar ociosa.
            proxima_chegada = min(p[1] for p in restantes)  # Encontra a menor chegada entre os pendentes.
            diagrama.append(("OCIOSA", tempo, proxima_chegada))  # Registra o intervalo sem execução.
            tempo = proxima_chegada  # Avança diretamente até a chegada do próximo processo.
            continue  # Volta ao início do while para atualizar a lista de disponíveis.

        processo = min(disponiveis, key=lambda p: p[2])  # Escolhe a menor duração; p[2] é a duração na CPU.
        # lambda p: p[2] é uma função curta que diz ao min qual valor comparar.
        # Se as durações empatarem, min mantém o primeiro na ordem da lista recebida.
        pid, chegada, duracao = processo  # Desempacota os três valores da tupla em variáveis.
        inicio = tempo  # Marca o instante em que o processo ganha a CPU.
        fim = inicio + duracao  # Calcula o término, pois não há interrupção da execução.
        espera = inicio - chegada  # Mede quanto tempo ficou esperando antes de começar.
        retorno = fim - chegada  # Mede o tempo total entre a chegada e a conclusão.
        diagrama.append((pid, inicio, fim))  # Acrescenta o bloco executado ao diagrama.
        resultados.append((pid, chegada, duracao, inicio, fim, espera, retorno))  # Guarda os dados da tabela.
        tempo = fim  # Atualiza o relógio para o instante de conclusão.
        restantes.remove(processo)  # Retira o processo concluído da lista de pendentes.

    return diagrama, resultados  # Devolve o histórico da CPU e as métricas calculadas.


if __name__ == "__main__":  # Executa o exemplo somente ao rodar este arquivo diretamente.
    # Use identificadores únicos, chegadas >= 0 e durações > 0 neste exemplo.
    processos = [  # Abre a lista de processos usada na demonstração.
        ("P1", 0, 5),  # P1 chega em 0 e precisa de 5 unidades de CPU.
        ("P2", 1, 3),  # P2 chega em 1 e precisa de 3 unidades de CPU.
        ("P3", 2, 8),  # P3 chega em 2 e precisa de 8 unidades de CPU.
        ("P4", 3, 2),  # P4 chega em 3 e precisa de 2 unidades de CPU.
    ]  # Fecha a lista; mude as tuplas acima para testar outros cenários.
    diagrama, resultados = sjf(processos)  # Chama o algoritmo e recebe seus dois resultados.
    print("SJF — menor tarefa primeiro (não preemptivo)")  # Mostra o nome do algoritmo.
    print("\nDiagrama de Gantt:")  # Pula uma linha e apresenta o histórico da CPU.
    for pid, inicio, fim in diagrama:  # Percorre cada intervalo registrado.
        print(f"[{pid} {inicio}->{fim}]", end=" ")  # Imprime os blocos lado a lado.
    print("\n\nPID  Chegada  Duração  Início  Fim  Espera  Retorno")  # Exibe o cabeçalho da tabela.
    for pid, chegada, duracao, inicio, fim, espera, retorno in resultados:  # Lê os dados de cada processo.
        print(f"{pid:<4} {chegada:>7} {duracao:>8} {inicio:>7} {fim:>4} {espera:>7} {retorno:>8}")  # Alinha as colunas; < alinha à esquerda e > à direita.
    quantidade = len(resultados)  # Conta quantos processos foram concluídos.
    if quantidade > 0:  # Evita dividir por zero se a lista de processos estiver vazia.
        media_espera = sum(r[5] for r in resultados) / quantidade  # Soma as esperas (índice 5) e divide pela quantidade.
        media_retorno = sum(r[6] for r in resultados) / quantidade  # Soma os retornos (índice 6) e divide pela quantidade.
        print(f"\nEspera média: {media_espera:.2f}")  # Mostra a média de espera com duas casas decimais.
        print(f"Retorno médio: {media_retorno:.2f}")  # Mostra a média de retorno com duas casas decimais.
    else:  # Trata o cenário em que não foi cadastrado nenhum processo.
        print("Nenhum processo para executar.")  # Informa por que não há médias.

# PASSO A PASSO DO EXEMPLO:
# t=0: somente P1 chegou; executa de 0 a 5, mesmo com novas chegadas no meio.
# t=5: P2, P3 e P4 estão disponíveis; P4 tem a menor duração (2), então vai de 5 a 7.
# t=7: entre P2 (3) e P3 (8), P2 vence e executa de 7 a 10.
# t=10: resta P3, que executa de 10 a 18.
# Ordem: P1 -> P4 -> P2 -> P3.
# Esperas: P1=0, P4=2, P2=6, P3=8. Média = (0+2+6+8)/4 = 4,00.
# Retornos: P1=5, P4=4, P2=9, P3=16. Média = (5+4+9+16)/4 = 8,50.
# As médias dependem também das chegadas, por isso podem diferir da tabela do guia.
# Não basta ordenar todos pela duração: um processo que ainda não chegou não pode executar.

import os
import random
distancias = {}

try:
	with open("brazil58.tsp", "r") as objArq:
    		linhas = objArq.readlines()
except FileNotFoundError:
	print("Erro: o arquivo 'brazil58.tsp' não foi encontrado!")
except Exception as e:
	print("Error : {e}")

# As linhas do arquivo contêm a parte triangular superior da matriz de distâncias
indice_linha = 0
for i in range(1, 58):  # Linhas 1 a 57 (não inclui a 58)
    linha = linhas[indice_linha].strip()
    indice_linha += 1

    lista = linha.split()  # Quebra a linha em uma lista de strings

    for j in range(i + 1, 59):  # j vai de i+1 até 58
        if lista:
            peso = int(lista.pop(0))  # Converte o peso para inteiro
            distancias[(i, j)] = peso
            distancias[(j, i)] = peso
        else:
            print(f"Erro! Linha {i} do arquivo não possui elementos suficientes.")
            exit()

# Função que retorna o custo total de um caminho (ciclo fechado)
def custoCaminho(permutacao, dicDistancias):
    soma = 0
    for i in range(len(permutacao) - 1):
        a = permutacao[i]
        b = permutacao[i + 1]
        if (a, b) in dicDistancias:
            soma += dicDistancias[(a, b)]
        else:
            print(f"Erro! ({a},{b}) não existe no dicionário!")
            exit()
    soma += dicDistancias[(permutacao[-1], permutacao[0])]  # Volta ao início
    return soma

# Gera uma população de caminhos aleatórios (permutação das cidades)
def inicializaPopulacao(tamanho, qtdeCidades):
    import random
    lista = []
    for _ in range(tamanho):
        individuo = list(range(1, qtdeCidades + 1))
        random.shuffle(individuo)
        lista.append(individuo)
    return lista

# Calcula o custo de cada indivíduo da população
def calculaAptidao(populacao):
    listaAptidao = []
    for elem in populacao:
        listaAptidao.append(custoCaminho(elem, distancias))
    return listaAptidao

def selecaoPorRanking(populacao, aptidoes, tamanho_torneio=3):

    # Seleciona 'tamanho_torneio' indivíduos aleatórios da população
    indices_torneio = random.sample(range(len(populacao)), tamanho_torneio)
    
    melhor_individuo_indice = -1
    melhor_aptidao = 100000000000000000

    # Encontra o melhor indivíduo (menor custo) entre os selecionados
    for i in indices_torneio:
        if aptidoes[i] < melhor_aptidao:
            melhor_aptidao = aptidoes[i]
            melhor_individuo_indice = i
            
    return populacao[melhor_individuo_indice]

def pmx(pai1, pai2):

    tamanho = len(pai1)
    
    # 1. Inicializa os filhos como cópias dos pais
    filho1, filho2 = pai1[:], pai2[:]
    
    # 2. Escolhe dois pontos de corte aleatórios
    ponto1, ponto2 = sorted(random.sample(range(tamanho), 2))
    
    # 3. Cria os mapeamentos a partir dos segmentos trocados
    mapa1_para_2 = {pai1[i]: pai2[i] for i in range(ponto1, ponto2)}
    mapa2_para_1 = {pai2[i]: pai1[i] for i in range(ponto1, ponto2)}
    
    # 4. Troca os segmentos diretamente nos filhos
    filho1[ponto1:ponto2] = pai2[ponto1:ponto2]
    filho2[ponto1:ponto2] = pai1[ponto1:ponto2]
    
    # 5. Corrige duplicatas no filho 1 (fora do segmento trocado)
    for i in list(range(ponto1)) + list(range(ponto2, tamanho)):
        while filho1[i] in mapa2_para_1:
            filho1[i] = mapa2_para_1[filho1[i]]
            
    # 6. Corrige duplicatas no filho 2 (fora do segmento trocado)
    for i in list(range(ponto1)) + list(range(ponto2, tamanho)):
        while filho2[i] in mapa1_para_2:
            filho2[i] = mapa1_para_2[filho2[i]]
            
    return filho1, filho2


def mutacaoSwap(individuo, taxa_mutacao=0.01):

    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(individuo)), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo

if __name__ == "__main__":
    # Parâmetros do Algoritmo Genético
    TAMANHO_POPULACAO = 100
    TAXA_ELITISMO = 0.1  # 10% dos melhores indivíduos são mantidos
    TAXA_MUTACAO = 0.02  # Chance de 2% de mutação por indivíduo
    NUMERO_GERACOES = 500
    TAMANHO_TORNEIO = 3
    NUM_CIDADES = 58

    # --- INICIALIZAÇÃO ---
    print("Iniciando o Algoritmo Genético para o problema das 58 cidades do Brasil...")
    populacao = inicializaPopulacao(TAMANHO_POPULACAO, NUM_CIDADES)
    aptidoes = calculaAptidao(populacao)

    melhor_caminho_global = None
    melhor_custo_global = 100000000000000000000

    # --- LOOP PRINCIPAL DAS GERAÇÕES ---
    for geracao in range(NUMERO_GERACOES):
        # Combina população e aptidões para ordenação
        populacao_avaliada = sorted(zip(populacao, aptidoes), key=lambda item: item[1])

        # Atualiza o melhor resultado global encontrado até agora
        custo_atual = populacao_avaliada[0][1]
        if custo_atual < melhor_custo_global:
            melhor_custo_global = custo_atual
            melhor_caminho_global = populacao_avaliada[0][0]
            print(f"Geração {geracao+1}: Novo melhor custo encontrado -> {melhor_custo_global}")
        elif (geracao + 1) % 50 == 0:
            print(f"Geração {geracao+1}: Melhor custo atual -> {melhor_custo_global}")

        nova_populacao = []

        # --- ELITISMO ---
        # Mantém os melhores indivíduos da geração atual na próxima
        tamanho_elite = int(TAMANHO_POPULACAO * TAXA_ELITISMO)
        for i in range(tamanho_elite):
            nova_populacao.append(populacao_avaliada[i][0])

        # --- GERAÇÃO DE NOVOS INDIVÍDUOS ---
        while len(nova_populacao) < TAMANHO_POPULACAO:
            # 1. Seleção
            pai1 = selecaoPorRanking(populacao, aptidoes, TAMANHO_TORNEIO)
            pai2 = selecaoPorRanking(populacao, aptidoes, TAMANHO_TORNEIO)
            
            # Garante que os pais sejam diferentes
            while pai1 == pai2:
                pai2 = selecaoPorRanking(populacao, aptidoes, TAMANHO_TORNEIO)

            # 2. Cruzamento (Crossover)
            filho1, filho2 = pmx(pai1, pai2)

            # 3. Mutação
            filho1 = mutacaoSwap(filho1, TAXA_MUTACAO)
            filho2 = mutacaoSwap(filho2, TAXA_MUTACAO)

            nova_populacao.append(filho1)
            # Adiciona o segundo filho apenas se houver espaço
            if len(nova_populacao) < TAMANHO_POPULACAO:
                nova_populacao.append(filho2)

        # Atualiza a população e calcula as novas aptidões
        populacao = nova_populacao
        aptidoes = calculaAptidao(populacao)

    # --- RESULTADOS FINAIS ---
    print("\n--- O Algoritmo Genético foi concluído! ---")
    print(f"Melhor custo total encontrado: {melhor_custo_global}")
    print(f"Melhor caminho (permutação de cidades): \n{melhor_caminho_global}")
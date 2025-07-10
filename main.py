import os
distancias = {}

try:
	with open("edgesbrasil58.tsp", "r") as objArq:
    		linhas = objArq.readlines()
except FileNotFoundError:
	print("Erro: o arquivo 'edgesbrasil58.tsp' não foi encontrado!")
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

<h2>📋 Descrição</h2>
Implementação de um Algoritmo Genético para resolver o Problema do Caixeiro Viajante (TSP) com 58 cidades brasileiras, utilizando o arquivo de dados brazil58.tsp. 

<h3>🚀 Funcionalidades</h3> 

  <li>Leitura de dados : Carrega matriz de distâncias do arquivo brazil58.tsp</li>
  <li>População inicial : Gera soluções aleatórias para iniciar o algoritmo</li>
  <li>Função de avaliação : Calcula o custo total de cada rota</li>
  <li>Seleção por torneio : Escolhe os melhores indivíduos para reprodução</li>
  
  <h3>Operadores genéticos :</h3> 
  
  <li>Cruzamento OX1 (Ordered Crossover)</li>
  <li>Cruzamento PMX (Partially Mapped Crossover)</li>
  <li>Mutação Swap</li>
  <li>Elitismo : Preserva os melhores indivíduos a cada geração</li>
  <br>
  <h3>📁 Arquivo de Entrada</h3> 
  <br>
  O programa requer o arquivo brazil58.tsp no mesmo diretório, contendo a matriz triangular superior de distâncias entre as 58 cidades. 
  <br>
  📊 Saída do Programa 
  <br>
    Durante a execução, o algoritmo mostra: 
  <br>
  <li>Novos melhores custos encontrados</li>
  <li>Progresso a cada 50 gerações</li>
  <li>Resultado final com o melhor custo e rota</li>
     <br> 
  <h3>🛠️ Requisitos</h3> 
  <li>Python 3.x</li>
  <li>Bibliotecas padrão: os, random</li>
       <br>
  <h3>📚 Referências</h3> 
  <li>Problema do Caixeiro Viajante (TSP)</li>
  <li>Algoritmos Genéticos - Holland (1975) e Goldberg (1989)</li>
     

# Roteiro de Video — Projeto 1: Otimizacao de Modelos

**Duracao-alvo:** 15 minutos  
**Tom:** fale devagar, com frases simples. Os tempos sao guias; nao precisa ler os titulos em voz alta.

## Antes de gravar

1. Abra o VS Code na pasta do projeto.
2. Deixe abertos: `README.md`, `notebooks/02_modelagem_inicial.ipynb`, `notebooks/03_otimizacao_algoritmo_genetico.ipynb`, `resultados/comparacao_modelos.csv` e este roteiro.
3. No notebook 03, deixe todas as celulas ja executadas e salvas, incluindo a ultima saida com `Modo: ollama_local`.
4. Aumente o zoom da tela se necessario (`Ctrl` + `+`) para os numeros ficarem legiveis.

---

## 0:00–0:45 — Abertura

**Mostrar:** a arvore de arquivos no VS Code.

**Falar:**

> Ola. Neste video vou apresentar o Projeto 1, que trabalha com a otimizacao de um modelo de Machine Learning usando Algoritmo Genetico. O objetivo e analisar registros de violencia contra a mulher e identificar estatisticamente a possibilidade de reincidencia. O modelo serve somente como apoio a triagem; ele nao substitui a avaliacao humana.

> Vou mostrar a base, o modelo inicial, como implementei o algoritmo genetico, os resultados da otimizacao, a integracao com LLM e os principais desafios.

---

## 0:45–2:15 — Estrutura e dados

**Mostrar:** pastas `data`, `notebooks`, `src`, `resultados` e `docs`.

**Falar:**

> Aqui esta a organizacao do projeto. A pasta `data/raw` contem a base original. As pastas `notebooks` mostram a analise e os experimentos. A pasta `src` concentra o codigo reutilizavel. E a pasta `resultados` guarda os CSVs gerados pelo algoritmo genetico.

> A base original possui registros do SINAN/DATASUS. A variavel alvo e `OUT_VEZES`. Eu transformei essa coluna em duas classes: um representa reincidencia e zero representa ausencia de reincidencia.

**Mostrar:** `data/samples/VIOLBR25_amostra_50000.csv` na arvore e depois o notebook 03, celula **2. Preparacao dos dados**.

**Falar:**

> A base completa e grande. Para a execucao dos experimentos de otimizacao, eu gerei uma amostra estratificada de 50 mil registros. Isso mantem a proporcao das classes e reduz o tempo de processamento, sem alterar o arquivo original.

> Depois da divisao, ficaram 40 mil registros para treino e 10 mil para teste. O conjunto de teste ficou reservado para a comparacao final.

---

## 2:15–4:15 — Modelo inicial

**Mostrar:** notebook `02_modelagem_inicial.ipynb`, secoes de limpeza e comparacao final; depois notebook 03, celula **3. Modelo-base**.

**Falar:**

> Primeiro, foi feito o tratamento dos dados: remocao de codigos invalidos, tratamento de valores ausentes e separacao entre treino e teste. A imputacao foi calculada usando apenas o conjunto de treino, para evitar vazamento de informacao.

> Como modelo de referencia, eu utilizei uma Arvore de Decisao com profundidade maxima igual a 5. Na amostra usada para a otimizacao, o modelo-base teve accuracy de 62,71%, recall de 54,10% e F1-score de 61,40%.

> Neste problema, o recall e importante porque ele mede quantos casos positivos reais o modelo conseguiu identificar. Mesmo assim, eu analiso todas as metricas, porque aumentar o recall pode causar mais falsos positivos.

---

## 4:15–7:15 — Algoritmo genetico

**Mostrar:** arquivo `src/algoritmo_genetico.py`. Role devagar pelas funcoes `criar_individuo`, `selecao_torneio`, `crossover_uniforme`, `mutar` e `executar_ag`.

**Falar:**

> A proxima etapa foi implementar o Algoritmo Genetico manualmente. Cada individuo representa uma configuracao de hiperparametros da Arvore de Decisao.

> Os genes que eu pesquisei foram: profundidade maxima da arvore, numero minimo de amostras para dividir um no, numero minimo de amostras por folha, criterio de divisao e peso das classes.

> A populacao inicial cria varias combinacoes aleatorias. Depois, cada combinacao e avaliada por validacao cruzada estratificada com tres dobras, usando apenas os dados de treino.

> Para escolher os pais, utilizei selecao por torneio. O crossover e uniforme: para cada gene, o filho recebe o valor de um dos pais. A mutacao troca alguns genes por outros valores validos. Tambem usei elitismo, ou seja, a melhor configuracao de cada geracao e preservada.

**Mostrar:** `src/avaliacao.py`, funcao `calcular_fitness`.

**Falar:**

> A funcao de fitness combinou 70% de recall e 30% de F1-score. Dessa forma, eu priorizo encontrar os casos positivos, mas sem ignorar completamente o equilibrio entre precisao e recall.

---

## 7:15–8:30 — Configuracao dos experimentos

**Mostrar:** notebook 03, celula **4. Configuracoes do algoritmo genetico**.

**Falar:**

> Foram executados tres experimentos para verificar o comportamento do algoritmo com diferentes configuracoes.

> O primeiro experimento usou populacao de 10 individuos e 8 geracoes. O segundo aumentou para 20 individuos e 12 geracoes, com maior taxa de mutacao. O terceiro usou 30 individuos e 15 geracoes, com uma taxa de mutacao menor.

> Em todos os casos foi usada a mesma semente aleatoria, para facilitar a reproducao dos resultados.

---

## 8:30–10:45 — Resultados e comparacao

**Mostrar:** notebook 03, resultado da celula **5. Executar os experimentos**. Depois mostre a tabela da celula **6. Comparacao final** ou abra `resultados/comparacao_modelos.csv`.

**Falar:**

> Os tres experimentos encontraram a mesma melhor configuracao: profundidade maxima 3, minimo de 2 amostras para dividir um no, minimo de 1 amostra por folha e criterio Gini.

> Isso e um sinal de estabilidade dentro do espaco de busca utilizado. A melhor configuracao apareceu ja na primeira geracao e foi preservada pelo elitismo.

> Comparando com o modelo-base, o recall aumentou de 54,10% para 92,36%. O F1-score aumentou de 61,40% para 71,83%.

> Por outro lado, a accuracy caiu de 62,71% para 60,28%. Essa e uma troca importante: o modelo otimizado encontra mais casos positivos, mas pode sinalizar mais casos que nao sao positivos. Por isso, a previsao deve ser usada apenas como apoio para uma pessoa revisar o caso.

---

## 10:45–11:45 — Graficos e rastreabilidade

**Mostrar:** grafico da celula **7. Evolucao do fitness** e, se possivel, `resultados/historico_ag.csv`.

**Falar:**

> Este grafico mostra a evolucao do melhor fitness ao longo das geracoes. Os dados de cada experimento foram salvos em arquivos CSV. Isso permite conferir as configuracoes, os tempos de execucao e o historico de cada geracao.

> Os testes automatizados tambem verificam se crossover e mutacao respeitam os valores permitidos e se o elitismo preserva a melhor solucao.

---

## 11:45–13:15 — Integracao com LLM

**Mostrar:** notebook 03, ultima celula **8. Interpretacao com LLM**; depois `src/interpretacao_llm.py`.

**Falar:**

> A integracao com LLM foi criada para explicar os resultados do modelo em linguagem simples. A LLM nao recebe linhas da base, nomes, identificadores ou dados sensiveis. Ela recebe apenas metricas agregadas e os hiperparametros do modelo.

> O prompt pede uma explicacao clara, cautelosa e curta. Tambem informa que a resposta nao pode fazer diagnosticos, recomendacoes individuais ou tratar a previsao como certeza.

> Nesta demonstracao, estou usando uma LLM real executada localmente pelo Ollama. Dessa forma, nao preciso de chave ou creditos de API e as metricas nao saem do computador. A saida exibida foi gerada pela LLM local no modo `ollama_local`.

> A qualidade da resposta e avaliada por fidelidade aos numeros, clareza, seguranca, limitacoes e privacidade. Na revisao, identificamos que a LLM usou a palavra precisao ao explicar a acuracia. Essa revisao humana e importante para corrigir termos e validar qualquer texto gerado.

---

## 13:15–14:20 — Desafios e solucoes

**Mostrar:** `docs/16-relatorio-entrega-fase-2.md`, secao **Desafios enfrentados e solucoes**.

**Falar:**

> O principal desafio foi o tempo de processamento da base completa. A solucao foi criar uma amostra estratificada para a fase de experimentacao, preservando a base original.

> Outro cuidado foi evitar vazamento de dados. Por isso, o teste ficou separado e nao foi usado para escolher hiperparametros. A busca genetica utilizou somente o treino com validacao cruzada.

> Por se tratar de dados sensiveis, tambem foi importante limitar a LLM a informacoes agregadas e manter a supervisao humana como obrigatoria.

---

## 14:20–15:00 — Encerramento

**Mostrar:** tabela final de comparacao ou a conclusao do relatorio.

**Falar:**

> Como conclusao, o Algoritmo Genetico encontrou uma configuracao mais adequada ao objetivo definido, aumentando bastante o recall e tambem o F1-score. O resultado mostra que a otimizacao de hiperparametros pode melhorar a capacidade do modelo de sinalizar casos positivos.

> Mesmo assim, o projeto nao substitui avaliacao profissional. Ele e uma ferramenta experimental de apoio a triagem, que precisa de acompanhamento, validacao continua e decisao humana. Obrigado.

---

## Dicas finais de gravacao

- Nao leia codigos linha por linha: explique a ideia e apenas aponte as funcoes.
- Espere um ou dois segundos depois de trocar de arquivo ou tabela.
- Se o video estiver passando de 15 minutos, reduza a explicacao da estrutura de pastas e dos tres experimentos, mas mantenha resultados, LLM e desafios.
- Se perguntarem sobre a LLM, seja transparente: foi executada uma LLM real local pelo Ollama, no modo `ollama_local`; nenhuma chave de API foi usada.

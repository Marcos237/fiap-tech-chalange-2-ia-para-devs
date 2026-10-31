# Resumão das aulas --- FIAP Tech Challenge \| Preparação para a Fase 2

> **Material consolidado a partir dos resumos das aulas enviados na
> conversa.**\
> Este documento consolida os resumos das Aulas 1 a 14. O resumo da Aula
> 3 ainda não foi enviado; por isso, ela aparece como pendente e não foi
> preenchida por suposição.

## 1. Visão geral

As aulas estudadas abordam dois grandes eixos:

-   **Processamento de Linguagem Natural (PLN):** preparação de textos,
    representação numérica de palavras e classificação textual.
-   **Otimização:** conceitos de busca por soluções, métodos exatos e
    heurísticos, algoritmos genéticos e seus operadores e parâmetros.

Para o projeto que estamos considerando --- a análise de dados de
violência contra mulheres do SINAN/DATASUS --- parte dessas técnicas
poderá ser aproveitada. A aplicação de técnicas textuais, como Word2Vec
e SpaCy, depende de a base possuir campos textuais adequados. Já a
otimização dos hiperparâmetros dos modelos de classificação é uma
possibilidade diretamente relacionada ao trabalho de Fase 2, a ser
detalhada nas próximas aulas.

------------------------------------------------------------------------

## 2. Aula 1 --- Introdução ao Processamento de Linguagem Natural (PLN)

### Conceito

O Processamento de Linguagem Natural é uma área que busca permitir que
computadores processem, interpretem e gerem linguagem humana.

### Objetivos apresentados

-   Recuperação de informações.
-   Tradução automática.
-   Interpretação de informações presentes em textos.
-   Interação entre pessoas e sistemas computacionais.

### Etapas do PLN

1.  Pré-processamento.
2.  Tokenização.
3.  Análise morfológica.
4.  Análise sintática.
5.  Análise semântica.
6.  Desambiguação.

### Aplicações

-   Chatbots.
-   Assistentes virtuais.
-   Análise de sentimentos.
-   Previsões em mecanismos de busca.

### Valor e desafios

O PLN pode contribuir para eficiência, automação e personalização. Entre
os desafios citados estão a interpretação de ironia e sarcasmo e a
generalização entre idiomas.

A aula também apresentou a evolução histórica da área: de abordagens
baseadas em regras, a partir da década de 1950, até métodos de
aprendizado de máquina e deep learning.

### Relação possível com o projeto

Se houver campos textuais adequados na base, técnicas de PLN podem ser
estudadas para preparar e analisar esses textos. Primeiro será
necessário inspecionar a estrutura e o conteúdo da base; não se deve
presumir que existam relatos textuais apropriados.

------------------------------------------------------------------------

## 3. Aula 2 --- Bag of Words e Word Cloud

### Bag of Words (BoW)

Bag of Words é uma forma de transformar textos em representações
numéricas com base nas palavras presentes e em suas frequências. O
método considera a ocorrência das palavras, mas não preserva a ordem nem
compreende o contexto semântico.

### Fluxo prático apresentado

1.  Carregar e explorar os dados com Pandas.
2.  Limpar os dados.
3.  Separar os conjuntos de treino e teste.
4.  Transformar os textos em números com `CountVectorizer`.
5.  Treinar um classificador, no exemplo da aula, Regressão Logística.
6.  Avaliar o desempenho, incluindo acurácia.
7.  Gerar uma Word Cloud para visualizar palavras frequentes.

### Conceitos importantes

-   **Tokenização:** divisão do texto em unidades, normalmente palavras
    ou tokens.
-   **Vocabulário:** conjunto de termos identificados pelo vetorizador.
-   **CountVectorizer:** transforma documentos em uma matriz de
    contagens de palavras.
-   **Matriz esparsa:** representação eficiente de uma matriz que contém
    muitos valores iguais a zero.
-   **Word Cloud:** visualização em que palavras mais frequentes
    aparecem com maior destaque.

### Limitação do BoW

O método não representa a ordem das palavras nem o significado
contextual. Textos com sentidos diferentes podem produzir representações
parecidas se tiverem frequências semelhantes.

### Relação possível com o projeto

BoW só deve ser aplicado se houver campos textuais úteis na base do
SINAN. Caso existam, pode ser testado como uma forma de representar os
textos para classificação. Se não existirem, não é necessário forçar
essa técnica no projeto.

------------------------------------------------------------------------

------------------------------------------------------------------------

## 4. Aula 3 --- Tokenização de Texto e Remoção de Stop Words com NLTK

### Principais conceitos

-   **Tokenização:** processo de dividir textos em unidades menores
    (tokens), como palavras ou frases. Facilita a análise, padroniza o
    texto e pode reduzir a dimensionalidade dos dados.
-   **NLTK (Natural Language Toolkit):** biblioteca Python para
    manipulação de dados linguísticos, com recursos para tokenização,
    classificação de textos e análise de sentimentos.

### Prática apresentada

-   Utilização de `WhitespaceTokenizer` para separar o texto com base
    nos espaços em branco.
-   Utilização de `FreqDist` para contar a frequência dos tokens e
    identificar palavras recorrentes.

### Remoção de stop words

Stop words são palavras comuns que, em determinadas tarefas, podem não
acrescentar informação útil. Sua remoção pode ajudar a concentrar a
análise em termos relevantes. A aula demonstrou o uso da lista de stop
words do NLTK.

``` python
from nltk.corpus import stopwords

stop_words = stopwords.words("portuguese")
```

### Melhorias adicionais no pré-processamento

-   Remover pontuação.
-   Remover acentos.
-   Converter letras para minúsculas.
-   Normalizar os textos para maior uniformidade.

O resumo da aula informa que a remoção dessas palavras melhorou a
acurácia dos modelos de classificação apresentados. Esse efeito deve ser
avaliado conforme a tarefa e os dados utilizados.

### Relação possível com o projeto

As técnicas de PLN só serão aplicadas ao conjunto SINAN/DATASUS se forem
encontrados campos textuais adequados. A limpeza deve preservar termos
importantes para o significado, incluindo negações como "não", quando
relevantes.

## 5. Aula 4 --- Tokenização e Stop Words com NLTK

> Esta aula também aborda tokenização e stop words, com conteúdos que se
> sobrepõem aos da Aula 3.

### Tokenização

Tokenização é o processo de dividir um texto em unidades menores,
chamadas tokens. A aula apresentou o uso do NLTK e o
`WhitespaceTokenizer`, que separa o texto com base nos espaços em
branco.

### Frequência de palavras

O `FreqDist`, do NLTK, permite contar a frequência dos tokens e
identificar as palavras mais recorrentes.

### Stop words

Stop words são palavras muito frequentes que, em determinadas tarefas,
podem ser removidas para reduzir ruído. A aula mostrou a lista de
palavras em português disponível em:

``` python
from nltk.corpus import stopwords

stop_words = stopwords.words("portuguese")
```

### Outras operações de limpeza apresentadas

-   Converter o texto para letras minúsculas.
-   Remover pontuação usando a biblioteca `string`.
-   Remover acentos usando `unidecode`.
-   Remover stop words.
-   Identificar e tratar tokens.

### Bibliotecas e recursos do NLTK citados

-   Tokenização.
-   Stemming.
-   Lemmatização.
-   Stop words.
-   Classificação de textos.

### Cuidados

A remoção de stop words precisa ser avaliada de acordo com o contexto.
Em textos relacionados à violência, palavras de negação, como "não",
podem mudar completamente o sentido de uma frase. Portanto, não devem
ser removidas automaticamente sem análise.

### Relação possível com o projeto

Essas operações só serão aplicadas se houver texto adequado na base. A
preparação precisa preservar termos relevantes para o significado dos
registros.

------------------------------------------------------------------------

## 6. Aula 5 --- Word Embeddings com Word2Vec

### Word Embeddings

Word Embeddings são técnicas que representam palavras como vetores
numéricos, procurando carregar informações semânticas nas
representações.

Ao contrário de uma representação baseada apenas em contagens,
embeddings procuram capturar relações entre palavras a partir de padrões
de contexto.

### Word2Vec

A aula apresentou duas arquiteturas:

-   **Skip-Gram:** utiliza uma palavra para tentar prever as palavras de
    seu contexto.
-   **CBOW (Continuous Bag of Words):** utiliza as palavras do contexto
    para tentar prever a palavra central.

### Implementação prática apresentada

1.  Importar e descompactar o conjunto de dados.
2.  Fazer uma vetorização inicial com `CountVectorizer`.
3.  Utilizar a biblioteca `gensim` para carregar modelos pré-treinados.
4.  Criar métodos de tokenização.
5.  Combinar vetores para representar os textos.
6.  Treinar um modelo de Regressão Logística.
7.  Avaliar o desempenho e comparar com um `DummyClassifier`.

### DummyClassifier

O `DummyClassifier` funciona como uma referência simples de
classificação. A comparação ajuda a verificar se o modelo treinado
aprende padrões úteis além de uma estratégia básica.

### Outras abordagens apresentadas

  ---------------------------------------------------------------------
  Técnica                            Característica apresentada
  ---------------------------------- ----------------------------------
  Word2Vec                           Representações vetoriais treinadas
                                     com Skip-Gram ou CBOW.

  GloVe                              Utiliza estatísticas de
                                     coocorrência.

  FastText                           Considera subpalavras, ajudando na
                                     representação de palavras menos
                                     frequentes.

  BERT                               Modelo baseado em Transformers com
                                     contexto bidirecional.
  ---------------------------------------------------------------------

### Relação possível com o projeto

Word2Vec pode ser avaliado se a base possuir textos relevantes. Nesse
caso, os vetores poderiam ser usados como atributos de um classificador.
É necessário verificar os campos disponíveis antes de decidir pela
implementação.

------------------------------------------------------------------------

## 7. Aula 6 --- Pré-processamento com SpaCy

### Objetivos apresentados

-   Utilizar SpaCy no pré-processamento de dados textuais, como
    alternativa ao NLTK.
-   Criar um modelo Word2Vec do zero.
-   Construir um classificador baseado nos vetores gerados.

### Etapas práticas

1.  Ler arquivos CSV com Pandas.
2.  Instalar e carregar o SpaCy e um modelo de linguagem em português.
3.  Converter títulos para letras minúsculas.
4.  Remover stopwords.
5.  Remover tokens não alfabéticos.
6.  Criar um DataFrame com os textos tratados.
7.  Criar um modelo Word2Vec com Gensim.
8.  Trabalhar com CBOW e Skip-Gram.
9.  Treinar o modelo e monitorar o erro.
10. Salvar os modelos treinados.
11. Utilizar os vetores em um classificador de Regressão Logística.

### Conteúdo teórico citado

-   SpaCy.
-   Análise morfológica e sintática.
-   Reconhecimento de entidades.
-   Word Embeddings.
-   Análise de sentimentos.

### Desafio proposto

Criar um projeto com a base de críticas de filmes do IMDB, realizando
pré-processamento, construção de um modelo Word2Vec e classificação de
sentimentos.

### Relação possível com o projeto

SpaCy pode ser usado para preparar textos se a base do SINAN possuir
campos adequados. O Word2Vec treinado do zero também depende de haver
quantidade e qualidade suficientes de texto. Não se deve assumir que o
dataset contém relatos textuais utilizáveis.

------------------------------------------------------------------------

## 8. Aula 7 --- Introdução à Otimização e aos Algoritmos Genéticos

### Otimização

Otimização é a busca por soluções que atendam a um objetivo, como
minimizar custos ou maximizar resultados.

A aula distinguiu:

-   **Métodos exatos:** procuram uma solução ótima e podem garantir a
    otimalidade.
-   **Métodos heurísticos:** procuram boas soluções de maneira prática,
    sem necessariamente garantir que sejam ótimas.

### Problema do Caixeiro Viajante (TSP)

O TSP consiste em encontrar o menor percurso que visita um conjunto de
cidades e retorna à cidade de origem.

É um exemplo de problema de otimização combinatória.

### Categorias de otimização

-   Minimização e maximização.
-   Problemas lineares e não lineares.
-   Variáveis contínuas e discretas.
-   Otimização convexa.
-   Otimização combinatória.
-   Otimização estocástica.
-   Otimização multiobjetivo.

### Métodos apresentados

-   **Força bruta:** testa as possibilidades; pode se tornar
    impraticável em problemas grandes.
-   **Vizinho mais próximo:** escolhe, a cada etapa, a cidade ainda não
    visitada mais próxima. É uma heurística e não garante a rota ótima.
-   **Convex Hull:** abordagem geométrica mencionada no contexto de
    estratégias para problemas de roteamento.
-   **Held-Karp:** algoritmo baseado em programação dinâmica para
    resolver o TSP de forma exata.

### Complexidade computacional

O TSP foi apresentado como um problema NP-hard. A quantidade de
possibilidades torna a busca exaustiva muito custosa conforme o número
de cidades cresce.

A aula relacionou essa dificuldade ao estudo de métodos como algoritmos
genéticos e programação dinâmica.

### Relação com a Fase 2

Uma aplicação que estamos considerando para o projeto é utilizar
algoritmos genéticos para procurar configurações de hiperparâmetros dos
modelos de classificação já desenvolvidos.

Por exemplo, em uma Árvore de Decisão, podem ser avaliados parâmetros
como:

  Hiperparâmetro        Exemplos de valores
  --------------------- ---------------------
  `max_depth`           3, 5, 10, 15
  `min_samples_split`   2, 5, 10
  `min_samples_leaf`    1, 2, 4
  `criterion`           `gini`, `entropy`

O algoritmo genético pode gerar combinações, avaliar os modelos e usar
os resultados para orientar novas combinações.

### Métricas possíveis

-   Recall.
-   F1-score.
-   Acurácia.

A métrica escolhida precisa estar alinhada ao objetivo do experimento e
ser justificada. Os resultados devem ser comparados usando o mesmo
protocolo de avaliação, sem utilizar o conjunto de teste para orientar
repetidamente a otimização.

------------------------------------------------------------------------

## 8. Como os conteúdos se conectam

### Linha de PLN

``` text
Texto original
    |
    v
Pré-processamento
(NLTK ou SpaCy)
    |
    v
Representação numérica
(Bag of Words ou Word2Vec)
    |
    v
Classificador
(Regressão Logística, por exemplo)
    |
    v
Avaliação
```

-   Bag of Words representa textos por contagens.
-   Word2Vec representa palavras por vetores aprendidos a partir de
    contextos.
-   NLTK e SpaCy oferecem recursos para preparar e analisar textos.
-   Regressão Logística pode utilizar as representações numéricas como
    entrada.

### Linha de otimização

``` text
Definir modelo e hiperparâmetros
    |
    v
Gerar configurações candidatas
    |
    v
Treinar e validar modelos
    |
    v
Calcular métrica objetivo
    |
    v
Selecionar e gerar novas configurações
    |
    v
Comparar os experimentos
```

Essa segunda linha está ligada à possibilidade de otimizar
hiperparâmetros dos modelos já desenvolvidos.

------------------------------------------------------------------------

## 9. Situação do projeto atual

Com base no resumo da Fase 1 compartilhado anteriormente:

-   A base utilizada é relacionada aos registros do SINAN/DATASUS.
-   A variável-alvo mencionada é `OUT_VEZES`.
-   Foram treinados modelos de Árvore de Decisão e Regressão Logística.
-   Foram realizadas preparação dos dados, seleção de variáveis,
    avaliação, matrizes de confusão, importância de atributos e análise
    SHAP.

Métricas informadas para a Fase 1:

  Modelo                  Acurácia   Recall   F1-score
  --------------------- ---------- -------- ----------
  Árvore de Decisão         0,6453   0,8771     0,7305
  Regressão Logística       0,6588   0,7477     0,7061

A Árvore de Decisão foi escolhida no trabalho anterior considerando os
valores de Recall e F1-score informados. Esses números são uma
referência histórica da Fase 1, não uma garantia de desempenho futuro.

### Cuidados metodológicos importantes

-   Confirmar o significado exato de `OUT_VEZES` e se representa
    informação disponível no momento da notificação ou algum evento
    posterior.
-   Verificar possível vazamento de informação entre atributos e
    variável-alvo.
-   Manter separação adequada entre treino, validação e teste.
-   Comparar os experimentos com o mesmo protocolo.
-   Tratar dados sensíveis com cuidado e não apresentar previsões como
    diagnóstico ou decisão individual.
-   Verificar com a orientação da disciplina se é permitido aproveitar
    esse projeto, considerando que a proposta oficialmente entregue na
    Fase 1 foi diferente.

------------------------------------------------------------------------

## 10. Roadmap de trabalho sugerido para a Fase 2

Este roteiro é uma proposta de organização baseada no projeto já
existente e nos conteúdos recebidos. Deve ser conferido com o enunciado
oficial e com as próximas aulas.

### Etapa 1 --- Revisar a Fase 1

-   [ ] Reunir scripts, dados, documentação e resultados.
-   [ ] Confirmar a definição da variável `OUT_VEZES`.
-   [ ] Revisar seleção de atributos e possíveis vazamentos.
-   [ ] Reproduzir os resultados originais.

### Etapa 2 --- Definir a estratégia de otimização

-   [ ] Escolher os modelos que serão otimizados.
-   [ ] Definir os hiperparâmetros e seus intervalos.
-   [ ] Definir a métrica objetivo e justificar a escolha.
-   [ ] Definir o método de validação.
-   [ ] Estabelecer uma comparação com os modelos-base.

### Etapa 3 --- Implementar o algoritmo genético

-   [ ] Representar cada configuração como um indivíduo.
-   [ ] Criar uma população inicial.
-   [ ] Definir a função de fitness.
-   [ ] Implementar seleção.
-   [ ] Implementar cruzamento.
-   [ ] Implementar mutação.
-   [ ] Definir critério de parada.
-   [ ] Registrar as configurações e resultados de cada geração.

### Etapa 4 --- Executar experimentos

-   [ ] Registrar os parâmetros e métricas do modelo-base.
-   [ ] Executar experimentos de otimização.
-   [ ] Comparar os resultados usando o mesmo protocolo.
-   [ ] Analisar estabilidade e possíveis limitações.
-   [ ] Documentar os resultados, inclusive quando não houver melhoria.

### Etapa 5 --- Integração com LLM e documentação

-   [ ] Definir quais resultados serão enviados ao LLM.
-   [ ] Criar explicações em linguagem natural sobre métricas e
    experimentos.
-   [ ] Conferir se as explicações correspondem aos resultados
    calculados.
-   [ ] Documentar arquitetura, fluxo e decisões.
-   [ ] Preparar demonstração e relatório conforme o enunciado.

### Etapa 6 --- Avaliar a necessidade de PLN

-   [ ] Inspecionar as colunas da base.
-   [ ] Verificar se existem campos textuais adequados.
-   [ ] Se existirem, avaliar BoW ou Word2Vec.
-   [ ] Comparar o benefício real da abordagem textual.
-   [ ] Se não existirem campos adequados, registrar que as técnicas de
    PLN estudadas não serão aplicadas ao dataset.

## 9. Aula 8 --- Algoritmos Genéticos e NEAT

### Conceito de Algoritmos Genéticos

Algoritmos Genéticos (AGs) são métodos de otimização inspirados na
evolução natural. Trabalham com uma população de soluções candidatas,
que passam por processos de avaliação, seleção e transformação ao longo
de gerações.

### Etapas gerais

1.  Representar as soluções por meio de indivíduos.
2.  Criar uma população inicial.
3.  Avaliar cada indivíduo por uma função de aptidão (fitness).
4.  Selecionar indivíduos para reprodução.
5.  Aplicar crossover para combinar características.
6.  Aplicar mutação para introduzir variações.
7.  Formar uma nova geração e repetir até o critério de parada.

### NEAT

A aula também apresentou o NEAT (NeuroEvolution of Augmenting
Topologies), abordagem que utiliza evolução para desenvolver redes
neurais, podendo alterar tanto conexões quanto a estrutura da rede.
Foram citadas mutações que adicionam conexões ou neurônios e mecanismos
para equilibrar exploração e aproveitamento.

### Desafios e aplicações

-   Ajustar os parâmetros do próprio algoritmo.
-   Evitar estagnação ou convergência prematura.
-   Equilibrar exploração de novas soluções e aproveitamento das
    soluções que já apresentam bom desempenho.
-   Aplicações citadas incluem robótica e jogos.

### Relação possível com o projeto

No projeto em estudo, um AG pode ser utilizado para procurar
hiperparâmetros dos modelos de classificação. O NEAT é uma abordagem
específica para evolução de redes neurais e não é necessário para essa
proposta de otimização de Decision Tree ou Regressão Logística.

------------------------------------------------------------------------

## 10. Aula 9 --- Algoritmos Genéticos: representação e parâmetros

### Codificação genética

Cada indivíduo representa uma solução candidata. A forma de codificação
depende do problema:

-   **Binária:** sequência de bits 0 e 1.
-   **Real:** valores numéricos reais.
-   **Combinatória:** sequência ou combinação de elementos.
-   **Híbrida:** combinação de diferentes representações.

### Inicialização da população

-   **Aleatória:** gera indivíduos inicialmente de forma aleatória,
    introduzindo diversidade.
-   **Hotstart:** utiliza informações anteriores para construir a
    população inicial e tentar acelerar a busca.

### Função de aptidão (Fitness)

Avalia cada indivíduo e atribui um valor que representa a qualidade da
solução em relação ao objetivo definido. A seleção utiliza essa
avaliação para orientar a evolução da população.

### Operadores genéticos

-   **Crossover:** combina genes de indivíduos selecionados para gerar
    descendentes.
-   **Mutação:** altera genes para introduzir variação. Exemplos
    citados: bit flip, mutação gaussiana e inversão de subconjunto.

### Exploração e aproveitamento

-   **Exploração:** busca novas regiões e possibilidades no espaço de
    soluções.
-   **Aproveitamento:** concentra a busca em soluções que já
    apresentaram bons resultados.

O algoritmo precisa equilibrar os dois comportamentos para manter a
diversidade sem deixar de melhorar as soluções encontradas.

### Parâmetros e monitoramento

-   **Tamanho da população:** quantidade de indivíduos em cada geração.
-   **Taxa de crossover:** frequência com que ocorre o cruzamento.
-   **Taxa de mutação:** frequência com que ocorrem alterações
    genéticas.
-   **Média de aptidão:** desempenho médio dos indivíduos.
-   **Melhor aptidão:** melhor valor encontrado na geração ou até aquele
    momento.
-   **Diversidade genética:** variedade entre os indivíduos da
    população.

As taxas e o tamanho da população influenciam a busca e podem ser
ajustados conforme o comportamento observado.

### Relação possível com o projeto

Cada indivíduo pode representar uma configuração de hiperparâmetros de
um modelo, por exemplo, `max_depth`, `min_samples_split` e
`min_samples_leaf` de uma Decision Tree. A função Fitness pode utilizar
uma métrica de validação, como Recall ou F1-score, escolhida de acordo
com o objetivo do estudo.

O conjunto de teste deve permanecer separado e ser usado somente na
avaliação final. A busca dos hiperparâmetros deve ocorrer com dados de
treino e validação, evitando ajustar a solução ao conjunto de teste.

------------------------------------------------------------------------

------------------------------------------------------------------------

## 11. Aula 10 --- Introdução ao Algoritmo Genético

A aula focou na implementação de um algoritmo genético para resolver o
Problema do Caixeiro Viajante (PCV/TSP), utilizando Python e Pygame.

### Definição do problema

O PCV busca determinar a rota mais curta que visita um conjunto de
cidades e retorna ao ponto de partida. As cidades são representadas por
coordenadas.

### Codificação e geração da população

Cada indivíduo representa uma rota como uma sequência ordenada de
cidades. A população inicial é formada por variações aleatórias de
rotas. Exemplo apresentado:

``` python
def generate_random_population(cities_location, population_size):
    return [
        random.sample(cities_location, len(cities_location))
        for _ in range(population_size)
    ]
```

### Cálculo de fitness

A aptidão de uma rota é avaliada pela distância total percorrida,
incluindo o retorno à cidade inicial. No exemplo da aula, menor
distância significa melhor solução. Uma matriz de distâncias pode evitar
cálculos repetidos.

``` python
def calculate_fitness(path):
    distance = 0
    n = len(path)
    for i in range(n):
        distance += calculate_distance(path[i], path[(i + 1) % n])
    return distance
```

### Seleção e eficiência

A seleção aleatória ponderada utiliza o inverso das distâncias como
peso, favorecendo rotas menores na escolha dos pais:

``` python
probability = 1 / np.array(population_fitness)
parent1, parent2 = random.choices(population, weights=probability, k=2)
```

### Hotstart

A população inicial pode ser melhorada com heurísticas como Vizinho Mais
Próximo e Inserção Mais Barata, em vez de depender exclusivamente de
rotas aleatórias.

### Relação possível com o Projeto 1

No projeto de otimização de modelos, o indivíduo deixa de ser uma rota e
passa a representar uma configuração de hiperparâmetros. A função
fitness também muda: em vez de minimizar distância, poderá maximizar uma
métrica de validação, como Recall ou F1-score.

------------------------------------------------------------------------

## 12. Aula 11 --- Operadores Genéticos: Seleção, Crossover e Mutação

A aula aprofundou os operadores genéticos para o TSP, com implementação
e visualização utilizando Python e Pygame.

### Seleção

A seleção escolhe indivíduos com base em seus valores de aptidão para
formar a população seguinte e orientar a busca por soluções melhores.

### Crossover --- Ordered Crossover (OX1)

O crossover combina dois indivíduos para produzir descendentes. O método
OX1 preserva parte da ordem e das posições dos genes, evitando cidades
duplicadas e mantendo uma rota válida para o TSP.

### Mutação

A mutação introduz diversidade na população. Foram citadas as seguintes
técnicas:

-   **Swap mutation:** troca dois genes de posição.
-   **Inversão:** inverte a ordem de um trecho da sequência.
-   **Inserção:** remove um gene e o insere em outra posição.
-   **Scramble:** embaralha os genes de um trecho.

### Condições de término

É necessário definir quando o algoritmo será encerrado, podendo-se
considerar o número de gerações e a convergência da população.

### Visualização com Pygame

A visualização apresenta cidades e trajetórias em tempo real,
facilitando a observação do comportamento do algoritmo. A aula também
propôs uma exploração prática de camuflagem com algoritmos genéticos.

### Relação possível com o Projeto 1

Seleção, crossover, mutação e condições de término também são
necessários para otimizar hiperparâmetros. Porém, o OX1 foi pensado para
sequências de cidades; para hiperparâmetros, os operadores devem ser
adaptados para respeitar os tipos e os valores permitidos de cada
parâmetro.

------------------------------------------------------------------------

## 13. Aula 12 --- Desenvolvimento de Machine Learning na Nuvem

A aula abordou o ciclo de desenvolvimento de modelos de ML na nuvem,
limitações do processamento local e serviços cognitivos oferecidos por
diferentes plataformas.

### Etapas do ciclo de ML

1.  **Coleta de dados:** obter os dados necessários.
2.  **Pré-processamento:** preparar e adequar os dados para treinamento.
3.  **Desenvolvimento e treinamento:** criar e treinar o modelo.
4.  **Avaliação de desempenho:** verificar a eficácia do modelo.
5.  **Implantação:** disponibilizar o modelo para uso em aplicações.
6.  **Monitoramento:** acompanhar o desempenho após a implantação.

### Limitações locais e escalabilidade

A aula discutiu limitações de processamento local e como a nuvem pode
oferecer recursos computacionais escaláveis para necessidades variáveis.

### Serviços cognitivos apresentados

-   **Reconhecimento de imagens:** Azure AI Vision, Google Vision AI e
    AWS Rekognition.
-   **Processamento de texto:** Azure AI Language, Google Natural
    Language e AWS Comprehend.
-   **Reconhecimento de voz:** Azure Speech-to-Text, Google
    Speech-to-Text e AWS Transcribe.
-   **Tradução de textos:** Azure AI Translator, Google Translate e AWS
    Translate.
-   **Geração de voz:** Azure AI Speech, Google Text-to-Speech e AWS
    Polly.

### Relação possível com o Projeto 1

A aula se relaciona ao treinamento e avaliação dos modelos, registro de
métricas, logging, monitoramento e análise de escalabilidade. A
infraestrutura em nuvem deve ser avaliada conforme os requisitos e os
recursos disponíveis.

------------------------------------------------------------------------

## 14. Aula 13 --- Plataformas de Nuvem para Machine Learning

A aula destacou como plataformas de nuvem oferecem recursos
computacionais e escalabilidade para desenvolver modelos de ML.

### Hands-on com Azure Machine Learning Studio

A prática consistiu em treinar um modelo de análise de sentimentos que
classifica textos como negativos, neutros ou positivos. O fluxo incluiu:

1.  Utilizar uma máquina virtual no Azure Machine Learning Studio.
2.  Carregar os dados.
3.  Gerenciar o treinamento.
4.  Registrar o modelo.
5.  Implantar o modelo.
6.  Desalocar recursos após o uso.

Também foram apresentadas orientações para criar uma conta no Azure e
acessar um repositório de materiais de apoio.

### Computação serverless

A computação serverless permite que desenvolvedores se concentrem no
código enquanto o provedor gerencia os recursos. Entre os desafios
citados estão a complexidade de gerenciamento e a possibilidade de
latência.

### Recurso MLTable

O recurso `mltable` foi apresentado para facilitar a manipulação e o
pré-processamento de dados no Azure.

### Comparação entre provedores

-   **AWS SageMaker:** plataforma de ML com instâncias otimizadas.
-   **Google Cloud AI:** APIs de ML com suporte a frameworks.
-   **IBM Cloud Watson:** serviços de preparação e gerenciamento de
    modelos.
-   **Azure Machine Learning Studio:** treinamento, gerenciamento,
    registro e implantação de modelos na prática apresentada.

### Relação possível com o Projeto 1

Os conceitos podem apoiar a organização de experimentos, o registro de
modelos e uma eventual implantação. O uso de nuvem é uma opção de
infraestrutura, não uma substituição do algoritmo genético exigido pelo
projeto.

------------------------------------------------------------------------

## 15. Aula 14 --- Desenvolvimento de ML na Cloud: Recursos Escaláveis e de Alto Desempenho

A aula abordou recursos de nuvem para superar limitações de
infraestrutura, acelerar o treinamento e otimizar modelos de Machine
Learning.

### Três abordagens para acelerar o desenvolvimento

1.  **Treinamento de vários modelos:** usar máquinas virtuais para
    treinar modelos diferentes simultaneamente.
2.  **Ajuste de hiperparâmetros:** treinar o mesmo modelo com diferentes
    configurações usando AutoML e ferramentas de *hyperparameter tuning*
    no Azure.
3.  **Treinamento paralelo de um único modelo:** utilizar paralelismo
    para aumentar a eficiência do treinamento.

### Recursos de hardware

-   **CPU:** versátil, mas menos eficiente em tarefas intensivas em
    dados.
-   **GPU:** oferece alto poder de processamento paralelo, sendo
    adequada para redes neurais, mas é menos flexível.
-   **TPU:** eficiente em operações tensoriais, porém altamente
    especializada.

### Etapas do AutoML

1.  Seleção de algoritmos.
2.  Engenharia de características.
3.  Busca de arquitetura de modelos.
4.  Empilhamento e comitê de métodos.
5.  *Hyperparameter tuning*.

### Desafio prático

A atividade sugerida envolveu escolher um conjunto de dados, carregá-lo
no Azure ML, criar um processo de treinamento, utilizar um cluster de
computação e registrar e implantar o modelo.

### Relação possível com o Projeto 1

A aula se relaciona à otimização de hiperparâmetros e à execução
eficiente de experimentos. AutoML e algoritmos genéticos são abordagens
diferentes: como o enunciado do Projeto 1 exige um algoritmo genético, o
AutoML pode ser usado como referência complementar, mas não substitui a
implementação dos operadores genéticos solicitados.

------------------------------------------------------------------------

## Controle das aulas recebidas

  ------------------------------------------------------------------------
                          Aula Tema                  Status
  ---------------------------- --------------------- ---------------------
                             1 Introdução ao PLN     Recebida

                             2 Bag of Words e Word   Recebida
                               Cloud                 

                             3 Tokenização de texto  Recebida
                               e remoção de stop     
                               words com NLTK        

                             4 Tokenização e Stop    Recebida
                               Words com NLTK        

                             5 Word Embeddings com   Recebida
                               Word2Vec              

                             6 Pré-processamento com Recebida
                               SpaCy                 

                             7 Introdução à          Recebida
                               otimização e aos      
                               algoritmos genéticos  

                             8 Algoritmos Genéticos  Recebida
                               e NEAT                

                             9 Algoritmos Genéticos: Recebida
                               representação e       
                               parâmetros            

                            10 Introdução ao         Recebida
                               Algoritmo Genético e  
                               PCV                   

                            11 Operadores genéticos: Recebida
                               seleção, crossover e  
                               mutação               

                            12 Desenvolvimento de ML Recebida
                               na nuvem              

                            13 Plataformas de nuvem  Recebida
                               para ML               

                            14 ML na Cloud: recursos Recebida
                               escaláveis e de alto  
                               desempenho            
  ------------------------------------------------------------------------

------------------------------------------------------------------------

------------------------------------------------------------------------

## Observação final

Este documento reúne os resumos das Aulas 1 a 14 enviados na conversa.
As aplicações ao SINAN/DATASUS e ao Projeto 1 são possibilidades de
planejamento; não significam que todas as técnicas tenham sido
implementadas ou exigidas nas aulas. Os requisitos obrigatórios devem
ser conferidos no enunciado oficial do Tech Challenge.

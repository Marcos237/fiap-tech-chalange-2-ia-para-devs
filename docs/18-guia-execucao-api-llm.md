# Guia de Execucao da API de LLM

## Objetivo

Este guia registra como executar a integracao real com a API da OpenAI para gerar uma explicacao dos resultados do modelo. A integracao usa a API Responses pelo cliente Python oficial, conforme o [Quickstart oficial da OpenAI](https://developers.openai.com/api/docs/quickstart).

O arquivo `src/interpretacao_llm.py` ja contem a implementacao. A chamada envia somente metricas agregadas e hiperparametros; nenhum registro individual da base e enviado.

## 1. Instalar as dependencias

No terminal aberto na raiz do projeto, com o ambiente virtual ativo, execute:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. Configurar a chave de API

Crie uma chave no painel da OpenAI e, no mesmo terminal do VS Code, defina a variavel apenas para a sessao atual:

```powershell
$env:OPENAI_API_KEY = "cole_a_sua_chave_aqui"
```

Nao inclua a chave em notebooks, arquivos Python, commits, capturas de tela ou no video.

## 3. Executar a chamada real

No notebook `notebooks/03_otimizacao_algoritmo_genetico.ipynb`, na ultima celula, altere:

```python
interpretacao = gerar_interpretacao(resumo_llm, usar_api=False)
```

para:

```python
interpretacao = gerar_interpretacao(resumo_llm, usar_api=True)
```

Execute a celula. O resultado esperado e:

```text
Modo: api
```

Salve o notebook com `Ctrl + S` apos a execucao. A resposta exibida e a evidencia da integracao real para a entrega e para o video.

## 4. Evidencias a registrar no relatorio

Acrescente ao relatorio:

- modelo chamado: `gpt-4.1-mini`;
- objetivo da LLM: explicar metricas agregadas em linguagem simples;
- prompt utilizado;
- resposta retornada pela API;
- avaliacao da resposta nos criterios de fidelidade, clareza, seguranca, limitacoes e privacidade;
- confirmacao de que dados individuais nao foram enviados.

## 5. Problemas comuns

| Situacao | Acao |
| --- | --- |
| `ModuleNotFoundError: openai` | Execute a instalacao do passo 1. |
| Erro de chave/autenticacao | Confirme se `OPENAI_API_KEY` foi definida no mesmo terminal que iniciou o VS Code. |
| Erro `429` ou `insufficient_quota` | A chave foi aceita, mas a conta esta sem creditos. Adicione creditos no painel da OpenAI para executar a chamada real. |
| `Modo: demonstracao` | Verifique se o parametro esta como `usar_api=True`. |
| Chave exposta por engano | Revogue a chave no painel da OpenAI e crie outra. |

## Limites e seguranca

A LLM nao altera o modelo nem toma decisoes sobre pessoas. Ela apenas explica resultados estatisticos ja calculados. Toda interpretacao deve ser revisada por uma pessoa antes de ser usada na apresentacao.

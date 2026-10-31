# Integracao com LLM para Interpretacao dos Resultados

## 1. Objetivo

Usar uma LLM para transformar as metricas agregadas e os hiperparametros do modelo em uma explicacao curta e compreensivel para profissionais humanos.

A LLM nao altera o modelo, nao decide atendimentos e nao recebe registros individuais da base. Ela apenas explica resultados estatisticos ja calculados.

---

## 2. Dados permitidos no prompt

Enviar somente informacoes agregadas:

- nome do modelo;
- hiperparametros escolhidos;
- accuracy, recall e F1-score;
- matriz de confusao agregada, se necessaria;
- finalidade de apoio a triagem;
- limitacoes e aviso de supervisao humana.

Nunca enviar identificadores de vitimas, datas, enderecos, descricoes de ocorrencias ou linhas individuais da base.

---

## 3. Prompt utilizado

### Instrucoes do sistema

```text
Voce explica resultados de modelos de classificacao para profissionais humanos.
Use linguagem clara, cautelosa e objetiva. Nao faca diagnosticos, nao recomende
acoes para individuos e nao trate uma previsao como certeza. Explique que o
modelo e apoio a triagem e que decisao humana e obrigatoria. Baseie-se apenas
nos numeros recebidos. Se houver limitacoes, mencione-as.
```

### Entrada do usuario

```text
Explique o resultado agregado abaixo em ate tres paragrafos curtos:

Modelo: {modelo}
Hiperparametros: {hiperparametros}
Accuracy: {accuracy}
Recall: {recall}
F1-score: {f1_score}
Contexto: previsao estatistica de reincidencia para apoio a triagem.
```

---

## 4. Modos disponiveis

### Modo demonstracao

E o padrao. Funciona sem internet e sem chave de API. Gera uma explicacao local identificada explicitamente como simulada. Serve para validar o fluxo e gravar telas do projeto antes de configurar uma conta de API.

### Modo API real

Faz uma chamada a uma LLM usando a API Responses. Para ativar:

1. Instalar dependencias: `pip install -r requirements.txt`.
2. Definir `OPENAI_API_KEY` no ambiente, sem gravar a chave em arquivos do projeto.
3. Chamar `gerar_interpretacao(..., usar_api=True)`.

No PowerShell, somente para a sessao atual:

```powershell
$env:OPENAI_API_KEY = "sua_chave"
```

### Modo LLM local (Ollama)

Este e o modo recomendado para demonstrar uma LLM real sem consumir creditos de API.
O prompt e as metricas permanecem no computador: o notebook se comunica somente com
o Ollama em `http://localhost:11434`.

1. Instale o Ollama pelo site oficial: https://ollama.com/download
2. Feche e abra novamente o PowerShell e baixe um modelo leve:

```powershell
ollama pull llama3.2:3b
```

3. No notebook, execute:

```python
from src.interpretacao_llm import gerar_interpretacao_ollama

interpretacao = gerar_interpretacao_ollama(
    resumo_llm,
    modelo="llama3.2:3b",
)
print(interpretacao.texto)
```

O resultado exibira `Modo: ollama_local`. Caso apareca erro de conexao, abra o
aplicativo Ollama e confirme no terminal que `ollama list` mostra `llama3.2:3b`.

---

## 5. Avaliacao da resposta

Para cada resposta gerada, verificar manualmente:

| Criterio | Pergunta de verificacao |
| --- | --- |
| Fidelidade | Os numeros e conclusoes correspondem aos dados enviados? |
| Clareza | Uma pessoa nao tecnica entende a explicacao? |
| Seguranca | A resposta evita diagnostico, certeza e recomendacao individual? |
| Limitacoes | A resposta informa que o modelo pode errar e exige supervisao humana? |
| Privacidade | A entrada contem apenas dados agregados? |

Registrar no relatorio um exemplo de prompt, resposta, modo utilizado e avaliacao nesses criterios.

---

## 6. Limites da implementacao

- O modo demonstracao nao substitui uma LLM real no requisito final.
- O modo Ollama usa uma LLM real, mas requer a instalacao local do Ollama e o download inicial do modelo.
- A execucao em API depende de chave, conta e conectividade configuradas pelo responsavel pelo projeto.
- A resposta da LLM deve ser revisada por uma pessoa antes de qualquer apresentacao ou uso.

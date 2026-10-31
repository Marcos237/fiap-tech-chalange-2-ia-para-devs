# Projeto Enxuto - Modelagem de Reincidencia

Esta versao enxuta do projeto foi organizada para funcionar com apenas dois artefatos principais:

- `notebooks/02_modelagem_inicial.ipynb`
- `docs/12-resumo-final-modelagem.md`

## Estrutura

```text
projeto-enxuto/
├── data/
│   └── raw/
│       └── VIOLBR25_ptbr.csv
├── docs/
│   └── 12-resumo-final-modelagem.md
├── notebooks/
│   └── 02_modelagem_inicial.ipynb
└── requirements.txt
```

O notebook foi consolidado para executar todo o pipeline a partir da base bruta, sem depender manualmente dos arquivos intermediarios de `data/processed`.

## Como executar

1. Criar e ativar um ambiente virtual Python.
2. Instalar as dependencias:

```bash
pip install -r requirements.txt
```

3. Abrir o notebook `notebooks/02_modelagem_inicial.ipynb`.
4. Executar `Run All`.

## Base de dados

O notebook procura, nesta ordem:

- `data/raw/VIOLBR25.xlsx`
- `data/raw/VIOLBR25_ptbr.csv`

Nesta versao enxuta, o arquivo disponivel e `VIOLBR25_ptbr.csv`.

## Entrega

Para uma entrega simplificada, basta considerar:

- o notebook como artefato executavel;
- o arquivo `.md` como resumo metodologico e analitico.

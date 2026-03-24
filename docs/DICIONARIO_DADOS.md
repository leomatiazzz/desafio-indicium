# Dicionário de dados

## Visão geral
A análise usa as fontes abaixo, com `datasets/vendas_2023_2024.csv` como base canônica de vendas.

- [Metodologia analítica](METODOLOGIA_ANALITICA.md)
- [Índice da documentação](INDICE_DOCUMENTACAO.md)

## Arquivo: datasets/vendas_2023_2024.csv
- **Descrição:** histórico de vendas 2023–2024.
- **Grão:** 1 linha por venda.

| Campo | Tipo lógico | Descrição |
|---|---|---|
| id | inteiro | Identificador da venda |
| id_client | inteiro | Identificador do cliente |
| id_product | inteiro | Identificador do produto |
| qtd | numérico | Quantidade vendida |
| total | numérico | Receita total da venda em BRL |
| sale_date | data | Data da venda |

## Arquivo: datasets/produtos_raw.csv
- **Descrição:** cadastro de produtos.

| Campo | Tipo lógico | Descrição |
|---|---|---|
| code | inteiro/texto | Identificador do produto |
| name | texto | Nome do produto |
| price | moeda/texto | Preço de referência |
| actual_category | texto | Categoria do produto |

## Arquivo: datasets/clientes_crm.json
- **Descrição:** cadastro de clientes.

| Campo | Tipo lógico | Descrição |
|---|---|---|
| code | inteiro/texto | Identificador do cliente |
| full_name | texto | Nome completo |
| location | texto | Localidade |
| email | texto | E-mail |

## Arquivo: datasets_transformers/custos_importacao_normalizado.csv
- **Descrição:** custo histórico em USD por produto.

| Campo | Tipo lógico | Descrição |
|---|---|---|
| product_id | inteiro | Produto de referência |
| start_date | data | Início de vigência do custo |
| usd_price | numérico | Custo em USD |

## Arquivo: datasets_transformers/cambio.csv
- **Descrição:** série de taxa de câmbio para conversão de custos.

| Campo | Tipo lógico | Descrição |
|---|---|---|
| date | data | Data da taxa |
| taxa_venda | numérico | Taxa de venda USD->BRL |

## Observações de qualidade
- Datas de vendas devem ser parseadas com abordagem robusta (`format='mixed'`, `dayfirst=True`).
- `vendas_normalizado.csv` é fallback técnico e não a fonte principal para os resultados executivos.

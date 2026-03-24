# Metodologia analítica

- [Dicionário de dados](DICIONARIO_DADOS.md)
- [Índice da documentação](INDICE_DOCUMENTACAO.md)

## 1) Preparação da base
1. Carregamento de vendas, produtos e clientes.
2. Normalização de tipos de chave (`id_product`, `id_client`, `code`) para junções consistentes.
3. Parsing de data de venda com tratamento de inconsistências.
4. Enriquecimento por joins para criar a base analítica única.

## 2) KPIs executivos
- Faturamento total: soma de `total`.
- Quantidade vendida: soma de `qtd`.
- Clientes únicos: `nunique(id_client)`.
- Produtos únicos: `nunique(id_product)`.

## 3) Questão 4 — Prejuízo por produto
- Custo de cada venda estimado por:
  - custo USD vigente do produto na data (`merge_asof` por produto em `start_date`),
  - taxa de câmbio vigente (`merge_asof` por `sale_date`).
- Fórmulas:
  - `custo_brl = qtd * usd_price * taxa_venda`
  - `margem = total - custo_brl`
- Prejuízo: produtos com margem acumulada negativa.

## 4) Questão 5 — Clientes com maior lucro acumulado
- Agregação de `margem` por cliente.
- Ranking decrescente de lucro acumulado.

## 5) Questão 6 — Média por dia da semana com dias sem venda
1. Criar calendário diário contínuo no período analisado.
2. Agregar faturamento diário real.
3. Preencher dias sem transação com `0`.
4. Calcular média por dia da semana.

## 6) Recomendações (Questão 8)
- Estratégia: filtragem colaborativa item-item.
- Matriz usuário-item binária (comprou/não comprou).
- Similaridade cosseno entre produtos.
- Resultado: top-N produtos similares ao item de referência.

## Limitações e premissas
- Modelo de recomendação sofre com cold start e esparsidade.
- Estimativa de custo depende da qualidade de custos históricos e câmbio.
- Previsão apresentada é baseline e pode evoluir para modelos específicos de demanda intermitente.

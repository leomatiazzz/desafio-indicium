-- ============================================================
-- QUESTÃO 5 - CLIENTES FIÉIS (SQLite - Versão Corrigida)
-- ============================================================
-- Cada query é independente - execute uma por vez

-- ============================================================
-- QUERY 1: TOP 10 CLIENTES FIÉIS (3+ categorias, maior ticket médio)
-- ============================================================

WITH categorias_normalizadas AS (
    SELECT DISTINCT
        code,
        UPPER(TRIM(REPLACE(actual_category, ' ', ''))) AS categoria_norm
    FROM produtos
),

metricas_cliente AS (
    SELECT
        v.id_client,
        SUM(v.total) AS faturamento_total,
        COUNT(DISTINCT v.id) AS frequencia,
        ROUND(SUM(v.total) * 1.0 / COUNT(DISTINCT v.id), 2) AS ticket_medio,
        COUNT(DISTINCT cn.categoria_norm) AS diversidade_categorias
    FROM vendas v
    LEFT JOIN categorias_normalizadas cn ON v.id_product = cn.code
    GROUP BY v.id_client
),

clientes_com_filtro AS (
    SELECT
        id_client,
        faturamento_total,
        frequencia,
        ticket_medio,
        diversidade_categorias,
        ROW_NUMBER() OVER (ORDER BY ticket_medio DESC, id_client ASC) AS ranking
    FROM metricas_cliente
    WHERE diversidade_categorias >= 3
)

SELECT
    id_client,
    ROUND(faturamento_total, 2) AS faturamento_total,
    frequencia,
    ROUND(ticket_medio, 2) AS ticket_medio,
    diversidade_categorias,
    ranking
FROM clientes_com_filtro
WHERE ranking <= 10
ORDER BY ranking;

-- ============================================================
-- QUERY 2: CATEGORIA MAIS VENDIDA PELOS 10 CLIENTES FIÉIS
-- ============================================================
-- Execute APENAS esta query (não execute junto com a Query 1)

WITH categorias_normalizadas AS (
    SELECT DISTINCT
        code,
        UPPER(TRIM(REPLACE(actual_category, ' ', ''))) AS categoria_norm
    FROM produtos
),

top_10_clientes AS (
    SELECT id_client
    FROM (
        SELECT
            v.id_client,
            ROUND(SUM(v.total) * 1.0 / COUNT(DISTINCT v.id), 2) AS ticket_medio,
            COUNT(DISTINCT cn.categoria_norm) AS diversidade_categorias,
            ROW_NUMBER() OVER (ORDER BY SUM(v.total) * 1.0 / COUNT(DISTINCT v.id) DESC, v.id_client ASC) AS ranking
        FROM vendas v
        LEFT JOIN categorias_normalizadas cn ON v.id_product = cn.code
        GROUP BY v.id_client
        HAVING COUNT(DISTINCT cn.categoria_norm) >= 3
    )
    WHERE ranking <= 10
),

categoria_vendas AS (
    SELECT
        cn.categoria_norm AS categoria,
        SUM(v.qtd) AS quantidade_total,
        ROUND(SUM(v.total), 2) AS faturamento_total,
        COUNT(DISTINCT v.id) AS numero_transacoes
    FROM vendas v
    INNER JOIN top_10_clientes t ON v.id_client = t.id_client
    LEFT JOIN categorias_normalizadas cn ON v.id_product = cn.code
    GROUP BY cn.categoria_norm
)

SELECT
    categoria,
    quantidade_total,
    faturamento_total,
    numero_transacoes,
    ROUND(quantidade_total * 100.0 / (SELECT SUM(quantidade_total) FROM categoria_vendas), 2) AS percentual
FROM categoria_vendas
ORDER BY quantidade_total DESC;

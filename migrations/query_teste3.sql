WITH categorias_normalizadas AS (
    -- Normalizar categorias de produtos removendo espaços e padronizando
    SELECT DISTINCT
        code,
        UPPER(TRIM(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(actual_category, ' ', ''), 'á', 'a'), 'â', 'a'), 'ô', 'o'), 'ç', 'c'))) AS categoria_norm
    FROM produtos
),

metricas_cliente AS (
    -- Calcular para cada cliente: faturamento, frequência, ticket médio, diversidade
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

clientes_elite AS (
    SELECT
        id_client,
        faturamento_total,
        frequencia,
        ticket_medio,
        diversidade_categorias,
        ROW_NUMBER() OVER (ORDER BY ticket_medio DESC, id_client ASC) AS ranking
    FROM metricas_cliente
    WHERE diversidade_categorias >= 3
),

top_10_fieis AS (
    -- Top 10 com maior ticket médio (desempate por id_client crescente)
    SELECT *
    FROM clientes_elite
    WHERE ranking <= 10
)

-- QUERY RESULTADO 1: TOP 10 CLIENTES FIÉIS
SELECT
    id_client,
    ROUND(faturamento_total, 2) AS faturamento_total,
    frequencia,
    ROUND(ticket_medio, 2) AS ticket_medio,
    diversidade_categorias,
    ranking
FROM top_10_fieis
ORDER BY ranking;

WITH categorias_normalizadas_v2 AS (
    SELECT DISTINCT
        code,
        UPPER(TRIM(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(actual_category, ' ', ''), 'á', 'a'), 'â', 'a'), 'ô', 'o'), 'ç', 'c'))) AS categoria_norm
    FROM produtos
),

metricas_cliente_v2 AS (
    SELECT
        v.id_client,
        COUNT(DISTINCT cn.categoria_norm) AS diversidade_categorias
    FROM vendas v
    LEFT JOIN categorias_normalizadas_v2 cn ON v.id_product = cn.code
    GROUP BY v.id_client
    HAVING diversidade_categorias >= 3
),

clientes_elite_v2 AS (
    SELECT id_client
    FROM (
        SELECT
            v.id_client,
            SUM(v.total) AS faturamento_total,
            COUNT(DISTINCT v.id) AS frequencia,
            ROUND(SUM(v.total) * 1.0 / COUNT(DISTINCT v.id), 2) AS ticket_medio,
            COUNT(DISTINCT cn.categoria_norm) AS diversidade_categorias,
            ROW_NUMBER() OVER (ORDER BY SUM(v.total) * 1.0 / COUNT(DISTINCT v.id) DESC, v.id_client ASC) AS ranking
        FROM vendas v
        LEFT JOIN categorias_normalizadas_v2 cn ON v.id_product = cn.code
        GROUP BY v.id_client
        HAVING COUNT(DISTINCT cn.categoria_norm) >= 3
    )
    WHERE ranking <= 10
),

categoria_vendas_elite AS (
    -- Agrupar vendas dos 10 clientes por categoria
    SELECT
        cn.categoria_norm AS categoria,
        SUM(v.qtd) AS quantidade_total,
        ROUND(SUM(v.total), 2) AS faturamento_total,
        COUNT(DISTINCT v.id) AS numero_transacoes
    FROM vendas v
    INNER JOIN clientes_elite_v2 ce ON v.id_client = ce.id_client
    LEFT JOIN categorias_normalizadas_v2 cn ON v.id_product = cn.code
    GROUP BY cn.categoria_norm
)

SELECT
    categoria,
    quantidade_total,
    faturamento_total,
    numero_transacoes,
    ROUND(quantidade_total * 100.0 / (SELECT SUM(quantidade_total) FROM categoria_vendas_elite), 2) AS percentual_quantidade
FROM categoria_vendas_elite
ORDER BY quantidade_total DESC;

SELECT
    v.id_client,
    SUM(v.total) AS faturamento_total,
    COUNT(DISTINCT v.id) AS frequencia,
    ROUND(SUM(v.total) * 1.0 / COUNT(DISTINCT v.id), 2) AS ticket_medio,
    COUNT(DISTINCT UPPER(TRIM(p.actual_category))) AS diversidade_categorias
FROM vendas v
LEFT JOIN produtos p ON v.id_product = p.code
GROUP BY v.id_client
HAVING COUNT(DISTINCT UPPER(TRIM(p.actual_category))) >= 3
ORDER BY ticket_medio DESC, v.id_client ASC
LIMIT 10;

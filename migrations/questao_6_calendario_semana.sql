-- ============================================================
-- Questão 6.1 - Calendário de datas e média de vendas por dia da semana
-- ============================================================

WITH bounds AS (
    SELECT MIN(date(sale_date)) AS dt_min, MAX(date(sale_date)) AS dt_max FROM vendas
),
calendar AS (
    SELECT dt_min AS data FROM bounds
    UNION ALL
    SELECT date(data, '+1 day') FROM calendar, bounds
    WHERE date(data, '+1 day') <= bounds.dt_max
),
calendar_pt AS (
    SELECT
        data,
        CASE cast(strftime('%w', data) AS integer)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS dia_semana_pt
    FROM calendar
),
vendas_diarias AS (
    SELECT date(sale_date) AS data, SUM(total) AS valor_venda_dia
    FROM vendas
    GROUP BY date(sale_date)
),
calendar_vendas AS (
    SELECT c.data, c.dia_semana_pt, COALESCE(v.valor_venda_dia,0) AS valor_venda_dia
    FROM calendar_pt c
    LEFT JOIN vendas_diarias v ON v.data = c.data
)

SELECT
    dia_semana_pt,
    ROUND(AVG(valor_venda_dia),2) AS media_venda_dia,
    COUNT(*) AS dias_no_periodo
FROM calendar_vendas
GROUP BY dia_semana_pt
ORDER BY media_venda_dia ASC;

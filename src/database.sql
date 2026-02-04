CREATE TABLE operadoras (
    registro_ans INT PRIMARY KEY,
    cnpj VARCHAR(14) UNIQUE,
    razao_social VARCHAR(255),
    uf CHAR(2)
);

CREATE TABLE despesas_contabeis (
    id SERIAL PRIMARY KEY,
    registro_ans INT REFERENCES operadoras(registro_ans),
    data_lancamento DATE,
    conta_contabil VARCHAR(50),
    valor DECIMAL(15,2),
    trimestre INT,
    ano INT
);

CREATE INDEX idx_despesas_operadora ON despesas_contabeis(registro_ans);
CREATE INDEX idx_despesas_data ON despesas_contabeis(ano, trimestre);

WITH despesas_por_tri AS (
    SELECT 
        o.razao_social,
        d.ano,
        d.trimestre,
        SUM(d.valor) as total
    FROM despesas_contabeis d
    JOIN operadoras o ON d.registro_ans = o.registro_ans
    GROUP BY 1, 2, 3
),
crescimento AS (
    SELECT 
        razao_social,
        total as total_atual,
        LAG(total) OVER (PARTITION BY razao_social ORDER BY ano, trimestre) as total_anterior
    FROM despesas_por_tri
)
SELECT 
    razao_social,
    ((total_atual - total_anterior) / total_anterior) * 100 as percentual_crescimento
FROM crescimento
WHERE total_anterior > 0
ORDER BY percentual_crescimento DESC
LIMIT 5;

SELECT 
    o.uf,
    SUM(d.valor) as total_despesas_uf,
    AVG(d.valor) as media_por_lancamento
FROM despesas_contabeis d
JOIN operadoras o ON d.registro_ans = o.registro_ans
GROUP BY o.uf
ORDER BY total_despesas_uf DESC
LIMIT 5;

WITH medias_trimestrais AS (
    SELECT ano, trimestre, AVG(valor) as media_geral
    FROM despesas_contabeis
    GROUP BY ano, trimestre
),
performance_operadora AS (
    SELECT 
        d.registro_ans,
        d.ano,
        d.trimestre,
        SUM(d.valor) as total_op,
        m.media_geral
    FROM despesas_contabeis d
    JOIN medias_trimestrais m ON d.ano = m.ano AND d.trimestre = m.trimestre
    GROUP BY d.registro_ans, d.ano, d.trimestre, m.media_geral
)
SELECT registro_ans
FROM performance_operadora
WHERE total_op > media_geral
GROUP BY registro_ans
HAVING COUNT(*) >= 2;
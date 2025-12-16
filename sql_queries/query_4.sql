-- empresas con mas de 3 documentos no exitosos

SELECT
    ee.razon_social,
    SUM(CASE WHEN not e.exitoso THEN 1 ELSE 0 END) AS numero_fallidos
FROM empresa ee
    join numeracion n on ee.id = n.empresa_id
    join public.documento d on n.id = d.numeracion_id
    join public.estado e on d.estado_id = e.id
group by razon_social
HAVING SUM(CASE WHEN not e.exitoso THEN 1 ELSE 0 END)>3
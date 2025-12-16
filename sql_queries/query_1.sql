-- Empresa con mas documentos fallidos que exitosos

-- SELECT
--     ee.id,
--     ee.razon_social,
--     SUM(CASE WHEN not e.exitoso THEN 1 ELSE 0 END) AS numero_fallidos,
--     SUM(CASE WHEN e.exitoso THEN 1 ELSE 0 END) AS numero_exitosos
-- FROM empresa ee
-- JOIN numeracion n ON ee.id = n.empresa_id
-- JOIN public.documento d ON n.id = d.numeracion_id
-- JOIN public.estado e ON d.estado_id = e.id
-- GROUP BY
--     ee.id,
--     ee.razon_social
-- HAVING
--     SUM(CASE WHEN not e.exitoso  THEN 1 ELSE 0 END) >
--     SUM(CASE WHEN e.exitoso THEN 1 ELSE 0 END);

SELECT
    ee.id,
    ee.razon_social
FROM empresa ee
JOIN numeracion n ON ee.id = n.empresa_id
JOIN public.documento d ON n.id = d.numeracion_id
JOIN public.estado e ON d.estado_id = e.id
GROUP BY
    ee.id,
    ee.razon_social
HAVING
    SUM(CASE WHEN not e.exitoso  THEN 1 ELSE 0 END) >
    SUM(CASE WHEN e.exitoso THEN 1 ELSE 0 END);
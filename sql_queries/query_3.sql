-- cantidad de documentos por estado, agrupada por empresa

SELECT
    ee.razon_social,
    e.descripcion,
    count(*)
FROM empresa ee
    join numeracion n on ee.id = n.empresa_id
    join public.documento d on n.id = d.numeracion_id
    join public.estado e on d.estado_id = e.id
group by ee.razon_social, e.descripcion
order by razon_social, descripcion
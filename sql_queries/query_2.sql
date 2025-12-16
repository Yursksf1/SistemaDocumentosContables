-- Cantidad de facturas, notas debito y notas credito emitidas en dos fechas dadas

select td.descripcion, count(*)
from tipo_documento td 
    join numeracion n on td.id = n.tipo_documento_id
    join documento d on n.id = d.numeracion_id
where d.fecha >= '2023-01-01' and d.fecha <= '2023-12-31'
group by td.descripcion
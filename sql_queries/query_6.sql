-- total dinero recibido por empresa (facturas, notas debito) no se incluyen notas credito

select ee.razon_social, sum(dd.base + dd.impuestos) as total_recibido
from documento dd
join numeracion n on dd.numeracion_id = n.id
join empresa ee on n.empresa_id = ee.id
where n.tipo_documento_id in (select id from tipo_documento where descripcion in ('Factura de Venta', 'Nota Débito'))
group by ee.razon_social;
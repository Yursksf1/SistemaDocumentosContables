-- deteccion de numeros completos repetidos (prefijo + numero) en cada empresa
Select ee.razon_social, n.prefijo, d.numero, count(*) as cantidad_repetidos
from empresa ee JOIN numeracion n on ee.id = n.empresa_id
JOIN documento d on n.id = d.numeracion_id
group by ee.razon_social, n.prefijo, d.numero
having count(*) > 1;
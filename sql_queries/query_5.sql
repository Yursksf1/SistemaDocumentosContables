-- documentos cuyo numero o fecha este fuera del rango o vigencia autorizada

SELECT dd.id, dd.numero, dd.fecha
FROM public.documento dd
JOIN numeracion n ON dd.numeracion_id = n.id
WHERE dd.numero < n.consecutivo_inicial
   OR dd.numero > n.consecutivo_final
   OR dd.fecha < n.vigencia_inicial
   OR dd.fecha > n.vigencia_final;
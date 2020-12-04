# Integrador_Prog_Concurrente

En el ejercicio se pretende simular la concurrencia en una base de datos. Cuando entra un proceso en la base de datos se encola y existen dos tipos de permisos.

1* Solo lectura en la que se puede ejecutar mas de un proceso simultaneamente si es del mismo tipo
2* Escritura: En este caso solo un proceso se puede ejecutar a la vez.

Esto tiene una explicacion, si mientras un proceso esta modificando algun registro y al mismo tiempo otro proceso intenta leer la misma tabla puede existir una inconsistencia en los datos.

Cuando llegan las peticiones la base de datos consulta de que tipo es, si es de tipo lectura y la cantidad de consultas simultaneas es mayor a la cantidad de procesos en ejecución se ejecuta la petición. En el caso que llegue una petición de escritura debe esperar a que terminen todas las ejecuciones de tipo lectura para poder ejecutar el proceso.

## Ejemplo de error con problema de concurrencia

### Modificación perdida:

- En T1 (Tiempo 1), arranca TA (Transacción A), leen dato X
- En T2 (Tiempo 2), arranca TB (Transacción B), leen dato X datos = 100
- En T3 (Tiempo 3), modifica TA (Transacción A), dato X (aumenta el 100%) datos = 200
- En T4 (Tiempo 4), modifica TB, dato X (en base a lo que leyó en T2) (aumenta el 50%) 150 datos final.

### Permitir leer dato sin que se haya termiando la modificación que se esta ejecutando

### La información para resolver este control de concurrencia se estudio del libre Fundamentos de bases de datos quinta edición. Página 529

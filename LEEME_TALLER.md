# Taller EDEPA 2026: generación parametrizada de prácticas

Carpeta de trabajo para los participantes. Todos los nombres de `lista_estudiantes_ficticia.xlsx` son inventados.

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `generar_estadistica.py` + `template_estadistica.tex` | Generador de estadística descriptiva (3 preguntas) |
| `generar_probabilidad.py` + `template_probabilidad.tex` | Generador de probabilidad (4 preguntas) |
| `generar_mi_practica.py` + `template_mi_practica.tex` | **Plantilla** para construir su propio generador (ejemplo: porcentajes) |
| `pruebas.py` | Pruebas automáticas de los cálculos |
| `lista_estudiantes_ficticia.xlsx` | Lista de prueba (19 nombres inventados; encabezado «Nombre» en la fila 3) |
| `ejemplos/` | Los cuatro PDF de la corrida con semilla 2026, para comparar |

## Antes del taller

1. Instale Python 3 y una distribución de LaTeX con pgfplots (MiKTeX o TeX Live).
2. Instale las librerías: `pip install pandas openpyxl jinja2`
3. Compruebe la instalación: `python pruebas.py` debe terminar con `OK`.

## Durante el taller

1. Ejecute `python generar_estadistica.py`, elija `lista_estudiantes_ficticia.xlsx` y revise los dos PDF de `practicas_estadistica/`: prácticas y soluciones. La primera página de las soluciones es la hoja de respuestas.
2. Haga lo mismo con `python generar_probabilidad.py`.
3. Compare una práctica con su solución y con la fila correspondiente de la hoja de respuestas.

## Construir su propio generador

Abra `generar_mi_practica.py` y edite las tres partes marcadas con `EDITAR`:

1. **`CONTEXTOS`**: situaciones cerradas con sus rangos de valores.
2. **`datos_estudiante`**: genera los datos y calcula la solución. Las claves del diccionario son las variables que usa la plantilla (`{{ total }}`, `{{ porcentaje }}`…). Pase por `ge.esc()` todo texto que vaya a LaTeX.
3. **`CLAVE`**: columnas de la hoja de respuestas, que aparece al inicio del PDF de soluciones.

Luego edite `template_mi_practica.tex`: el enunciado va en el bloque `practicas` y la solución en el bloque `soluciones`. Ejecute `python generar_mi_practica.py`; los PDF aparecen en `practicas_mi_practica/`.

Consejos:

- Cambie una cosa a la vez y vuelva a ejecutar.
- La semilla queda impresa al pie de las soluciones: con la misma semilla y la misma lista se obtienen los mismos números.
- Si un PDF no aparece, abra el `.log` de la carpeta de salida y busque la primera línea que empieza con `!`.

## Lista de cotejo para revisar su ajuste

| Criterio | Sí | No | Observaciones |
|---|---|---|---|
| El objetivo de aprendizaje de la pregunta sigue siendo el mismo. | | | |
| El contexto es pertinente para el grupo y sus unidades son claras. | | | |
| Los rangos producen datos verosímiles para el contexto. | | | |
| La consigna nombra la medida o la probabilidad que se pide. | | | |
| La solución coincide con el enunciado en al menos tres estudiantes revisados. | | | |
| La moda, la mediana y el redondeo siguen la convención declarada. | | | |
| Las probabilidades aparecen como fracción simplificada y decimal. | | | |
| La corrida registra la semilla y `python pruebas.py` termina sin fallos. | | | |

## Uso con un curso real

Use la lista real de su grupo solo en su computadora. No la comparta ni la envíe a servicios externos.

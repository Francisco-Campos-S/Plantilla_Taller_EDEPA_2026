# Generación parametrizada de prácticas de Estadística y Probabilidad

Material del taller del **IX Encuentro sobre Didáctica de la Estadística, la Probabilidad y el Análisis de Datos (EDEPA 2026)**.

Autores: Francisco Antonio Campos Sandí y Gerardo Córdoba Hernández.

Los generadores leen una lista de estudiantes desde Excel y producen, para cada estudiante, una práctica con datos propios y su solución paso a paso. Usan Python, Jinja2 y LaTeX. Cada generador entrega dos PDF:

- las **prácticas**;
- las **soluciones**, que comienzan con una **hoja de respuestas** para el docente.

📄 **Guía completa:** [`guia/Guia_Taller_EDEPA_2026.pdf`](guia/Guia_Taller_EDEPA_2026.pdf)

## Inicio rápido

```bash
pip install pandas openpyxl jinja2      # requiere además MiKTeX o TeX Live con pgfplots
python pruebas.py                       # debe terminar con OK
python generar_estadistica.py           # elija lista_estudiantes_ficticia.xlsx
python generar_probabilidad.py
```

## Su propio generador, sin saber programar

Con la plantilla mínima (`generar_mi_practica.py` + `template_mi_practica.tex`) y **ChatGPT para producir el código**, puede crear un generador para otros temas del taller o para futuros temas de su curso. Describa el ejercicio, comparta los dos archivos de la plantilla (nunca la lista de estudiantes) y revise el resultado con la lista de cotejo. La sección 5.2 de la guía trae el paso a paso y un ejemplo de instrucción.

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `generar_estadistica.py` + `template_estadistica.tex` | Estadística descriptiva (3 preguntas) |
| `generar_probabilidad.py` + `template_probabilidad.tex` | Probabilidad (4 preguntas) |
| `generar_mi_practica.py` + `template_mi_practica.tex` | Plantilla para construir su propio generador (ejemplo: porcentajes) |
| `pruebas.py` | Pruebas automáticas de los cálculos |
| `lista_estudiantes_ficticia.xlsx` | Lista de prueba: 19 nombres **inventados** |
| `ejemplos/` | Los cuatro PDF de una ejecución con semilla 2026 |
| `guia/` | Guía del taller en PDF y su fuente LaTeX |
| `LEEME_TALLER.md` | Resumen de la guía y lista de cotejo |

## Privacidad

Use la lista real de su grupo solo en su computadora: no la suba a este repositorio ni la envíe a servicios externos.

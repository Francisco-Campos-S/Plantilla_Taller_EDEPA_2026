# Plantilla para construir un generador propio sobre generar_estadistica.py
# Edite las tres partes marcadas con "EDITAR" y la plantilla template_mi_practica.tex.
# Ejecutar con: python generar_mi_practica.py
import os # Libreria para manejar directorios
import random # Libreria para generar numeros aleatorios

import generar_estadistica as ge

OUTPUT_DIR = os.path.join(ge.SCRIPT_DIR, "practicas_mi_practica")

# EDITAR 1. Contextos cerrados: (poblacion encuestada, caracteristica, minimo y maximo de encuestados)
CONTEXTOS = [
    ("estudiantes de un colegio", "viajan en autobús", 40, 120),
    ("visitantes de un parque nacional", "son extranjeros", 50, 200),
    ("familias de una comunidad", "tienen acceso a internet", 30, 90),
]

# EDITAR 2. Datos y solucion de cada estudiante: las claves del diccionario son las variables de la plantilla
def datos_estudiante(idx, nombre):
    poblacion, rasgo, lo, hi = random.choice(CONTEXTOS)
    total = random.randint(lo, hi)
    k = random.randint(1, total - 1)  # al menos uno con la caracteristica y uno sin ella
    p = k * 100 / total
    exacto = (k * 10000) % total == 0  # exacto si tiene a lo sumo dos decimales
    return {
        "estudiante": ge.esc(nombre), "estudiante_id": f"e{idx}",
        "poblacion": ge.esc(poblacion), "rasgo": ge.esc(rasgo), "total": total, "k": k,
        "porcentaje": ge.num(p), "porcentaje_tex": ge.num(p).replace(",", "{,}"),
        "complemento_tex": ge.num(100 - p).replace(",", "{,}"),
        "signo": "=" if exacto else r"\approx",
    }

# EDITAR 3. Columnas de la hoja de respuestas: (encabezado, funcion que toma los datos del estudiante)
CLAVE = [
    ("Encuestados", lambda d: str(d["total"])), ("Casos", lambda d: str(d["k"])),
    ("Porcentaje", lambda d: d["porcentaje"] + r"\,\%"),
]

# Funcion para procesar el excel (reutiliza la lectura, el escape, la compilacion y la hoja de respuestas)
def procesar(excel_file, log, semilla=None):
    return ge.procesar(excel_file, log, semilla, datos_fn=datos_estudiante,
                       plantilla="template_mi_practica.tex", carpeta=OUTPUT_DIR, sufijo="mi_practica",
                       clave=CLAVE, titulo_clave="Mi práctica")

# Main
if __name__ == "__main__":
    ge.main(procesar, "Generador - Mi práctica")

# Generador de practicas y soluciones de probabilidad
# Reutiliza de generar_estadistica.py la lectura del Excel, el escape LaTeX, la compilacion y la interfaz.
from fractions import Fraction # Fracciones exactas para las probabilidades
import os # Libreria para manejar directorios
import random # Libreria para generar numeros aleatorios

import generar_estadistica

OUTPUT_DIR = os.path.join(generar_estadistica.SCRIPT_DIR, "practicas_probabilidad")

# Pregunta 1, probabilidad clasica: (objeto plural, objeto singular, colores plural, colores singular)
CTX1 = [("canicas", "canica", ("rojas", "azules", "verdes"), ("roja", "azul", "verde")),
        ("fichas", "ficha", ("blancas", "negras", "grises"), ("blanca", "negra", "gris")),
        ("tarjetas", "tarjeta", ("amarillas", "moradas", "anaranjadas"), ("amarilla", "morada", "anaranjada"))]
# Pregunta 3, tabla de contingencia: (pregunta de la encuesta, (grupo 1, "de" + grupo 1), (grupo 2, "de" + grupo 2))
CTX3 = [("practica algún deporte", ("décimo", "de décimo"), ("undécimo", "de undécimo")),
        ("lee al menos un libro al mes", ("sección A", "de la sección A"), ("sección B", "de la sección B")),
        ("usa transporte público para llegar al colegio",
         ("turno de la mañana", "del turno de la mañana"), ("turno de la tarde", "del turno de la tarde"))]

# Funcion para escribir una fraccion en LaTeX (ya simplificada)
def fr(f):
    return str(f.numerator) if f.denominator == 1 else rf"\dfrac{{{f.numerator}}}{{{f.denominator}}}"

# Funcion para escribir num/den, su forma simplificada y su decimal
def prob_tex(num, den):
    f = Fraction(num, den)
    s = rf"\dfrac{{{num}}}{{{den}}}"
    if (f.numerator, f.denominator) != (num, den):
        s += " = " + fr(f)
    return s + rf" \approx {float(f):.2f}"  # babel en español muestra el punto como coma

# Funcion para generar la pregunta 1: bolsa, complemento y extraccion sin reposicion
def prob_bolsa():
    obj, obj_s, cols, cols_s = random.choice(CTX1)
    r, a, v = random.randint(3, 9), random.randint(2, 9), random.randint(2, 9)
    n = r + a + v
    return {
        "p1_objeto": obj, "p1_objeto_s": obj_s, "p1_c": cols, "p1_cs": cols_s,
        "p1_r": r, "p1_a": a, "p1_v": v, "p1_n": n,
        "p1_sol_a": prob_tex(r, n),
        "p1_sol_b": rf"1 - \dfrac{{{a}}}{{{n}}} = " + prob_tex(n - a, n),
        "p1_sol_c": rf"\dfrac{{{r}}}{{{n}}} \cdot \dfrac{{{r - 1}}}{{{n - 1}}} = " + prob_tex(r * (r - 1), n * (n - 1)),
    }

# Funcion para generar la pregunta 2: suma de dos dados y espacio muestral
def prob_dados():
    s = random.randint(4, 10)
    t = random.randint(6, 9)
    sumas = [i + j for i in range(1, 7) for j in range(1, 7)]
    favorables_s = [(i, j) for i in range(1, 7) for j in range(1, 7) if i + j == s]
    mayores = sum(1 for x in sumas if x > t)
    return {
        "p2_s": s, "p2_t": t,
        "p2_pares": ", ".join(f"({i},{j})" for i, j in favorables_s),
        "p2_fav_s": len(favorables_s), "p2_fav_t": mayores,
        "p2_sol_b": prob_tex(len(favorables_s), 36),
        "p2_sol_c": prob_tex(mayores, 36),
    }

# Funcion para generar la pregunta 3: tabla de contingencia y probabilidad condicional
def prob_tabla():
    evento, (g1, g1_de), (g2, g2_de) = random.choice(CTX3)
    a1, a2, b1, b2 = (random.randint(5, 25) for _ in range(4))  # g1 si/no, g2 si/no
    total = a1 + a2 + b1 + b2
    p_si, p_si_g1 = Fraction(a1 + b1, total), Fraction(a1, a1 + a2)
    if p_si_g1 == p_si:
        indep = "Son iguales: responder que sí no depende del grupo (eventos independientes)."
    else:
        mayor = "mayor" if p_si_g1 > p_si else "menor"
        indep = (f"Son distintas: entre los estudiantes {g1_de} la proporción de respuestas afirmativas "
                 f"es {mayor} que en el grupo completo, por lo que los eventos no son independientes.")
    return {
        "p3_evento": evento, "p3_g1": g1, "p3_g2": g2, "p3_g1_de": g1_de, "p3_g2_de": g2_de,
        "p3_a1": a1, "p3_a2": a2, "p3_b1": b1, "p3_b2": b2,
        "p3_ta": a1 + a2, "p3_tb": b1 + b2, "p3_tsi": a1 + b1, "p3_tno": a2 + b2, "p3_total": total,
        "p3_sol_a": prob_tex(a1 + b1, total),
        "p3_sol_b": prob_tex(a1, total),
        "p3_sol_c": prob_tex(a1, a1 + a2),
        "p3_sol_d": indep,
    }

# Funcion para generar la pregunta 4: frecuencia relativa de una cara en lanzamientos simulados de un dado
def prob_frecuencia():
    N = random.choice((60, 120))
    cara = random.randint(1, 6)
    lanzamientos = [random.randint(1, 6) for _ in range(N)]
    frec = [lanzamientos.count(c) for c in range(1, 7)]
    f = frec[cara - 1]
    dif = abs(Fraction(f, N) - Fraction(1, 6))
    if dif == 0:
        comp = (f"En esta serie coinciden exactamente, pero es casualidad: otra serie de {N} lanzamientos "
                "daría, en general, una frecuencia relativa distinta.")
    else:
        cuanto = "menos de 0,01" if dif < Fraction(1, 200) else f"{float(dif):.2f}".replace(".", ",")
        comp = (f"Difieren en {cuanto}. Con {N} lanzamientos es normal que no coincidan, porque cada serie "
                "de lanzamientos varía por azar.")
    return {
        "p4_N": N, "p4_cara": cara, "p4_frec": frec, "p4_f": f,
        "p4_sol_a": prob_tex(f, N),
        "p4_sol_c": comp,
    }

# Funcion para generar los datos de un estudiante
def datos_estudiante(idx, nombre):
    d = {"estudiante": generar_estadistica.esc(nombre), "estudiante_id": f"e{idx}"}
    d.update(prob_bolsa())
    d.update(prob_dados())
    d.update(prob_tabla())
    d.update(prob_frecuencia())  # al final: no altera los numeros de las preguntas 1 a 3
    return d

# Funcion para escribir una probabilidad como fraccion simplificada y decimal en la hoja de respuestas
def fd(num, den):
    f = Fraction(num, den)
    return f"${fr(f)}$ ({float(f):.2f})".replace(".", ",").replace(r"\dfrac", r"\tfrac")

# Columnas de la hoja de respuestas del docente
CLAVE = [
    ("P1 a", lambda d: fd(d["p1_r"], d["p1_n"])), ("P1 b", lambda d: fd(d["p1_n"] - d["p1_a"], d["p1_n"])),
    ("P1 c", lambda d: fd(d["p1_r"] * (d["p1_r"] - 1), d["p1_n"] * (d["p1_n"] - 1))),
    ("P2 b", lambda d: fd(d["p2_fav_s"], 36)), ("P2 c", lambda d: fd(d["p2_fav_t"], 36)),
    ("P3 a", lambda d: fd(d["p3_tsi"], d["p3_total"])), ("P3 b", lambda d: fd(d["p3_a1"], d["p3_total"])),
    ("P3 c", lambda d: fd(d["p3_a1"], d["p3_ta"])), ("P4 a", lambda d: fd(d["p4_f"], d["p4_N"])),
]

# Funcion para procesar el excel
def procesar(excel_file, log, semilla=None):
    return generar_estadistica.procesar(excel_file, log, semilla, datos_fn=datos_estudiante,
                            plantilla="template_probabilidad.tex", carpeta=OUTPUT_DIR, sufijo="probabilidad",
                            clave=CLAVE, titulo_clave="Probabilidad")

# Main
if __name__ == "__main__":
    generar_estadistica.main(procesar, "Generador - Probabilidad")

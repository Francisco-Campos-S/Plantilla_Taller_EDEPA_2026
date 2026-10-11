# Generador de practicas y soluciones de estadistica descriptiva
from collections import Counter
import os # Libreria para manejar directorios
import random # Libreria para generar numeros aleatorios
import subprocess # Libreria para ejecutar comandos del sistema
import sys # Libreria para manejar sistemas operativos
import threading # Libreria para manejar hilos
import tkinter as tk # Libreria para crear interfaces graficas
from tkinter import filedialog # Libreria para manejar archivos

import pandas as pd # Libreria para manejar datos
from jinja2 import Environment, FileSystemLoader # Libreria para manejar plantillas
# Directorio de scripts y directorio de salida
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # no depende del cwd
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "practicas_estadistica")
JINJA = Environment(loader=FileSystemLoader(SCRIPT_DIR))  # una sola carga al importar
# Funcion para escapar caracteres especiales LaTeX
LATEX_TR = str.maketrans({  # str.translate: un pase; evita .replace encadenados
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    "<": r"\textless{}", ">": r"\textgreater{}",
})

CTX1 = [("nacimientos por mes", 4500, 8500),  # (texto, min, max)
        ("ventas mensuales de un supermercado (miles de colones)", 15000, 35000),
        ("visitantes por mes a un parque nacional", 3000, 12000),
        ("kilogramos de café recibidos por semana en un beneficio", 5000, 15000)]
CTX2 = ["calificaciones de un examen", "puntuaciones de una prueba", "notas finales de un curso"]  # rango 25–84 fijo
CTX3 = [("edad de los asistentes a un curso (años)", 18, 45), ("horas de estudio por semana", 5, 25),
        ("puntajes de una prueba corta", 60, 100)]

# Funcion para escapar caracteres especiales LaTeX
def esc(t):
    return str(t).translate(LATEX_TR)  # escapa caracteres especiales LaTeX

# Funcion para calcular los estadisticos
def estadisticos(datos):
    if not datos:
        return {}
    freq = Counter(datos)
    max_f = max(freq.values())
    modas = sorted(k for k, v in freq.items() if v == max_f)
    moda_txt = ("No hay moda" if max_f == 1 or 1 < len(modas) == len(freq)  # todos con la misma frecuencia
                else str(modas[0]) if len(modas) == 1 else ", ".join(map(str, modas)))  # empate parcial
    orden, n = sorted(datos), len(datos)
    if n % 2:
        mediana = orden[n // 2]
        mediana_tex = rf"x_{{{n // 2 + 1}}} = {mediana}"
    else:
        a, b = orden[n // 2 - 1], orden[n // 2]
        mediana = (a + b) / 2
        mediana_tex = rf"\dfrac{{x_{{{n // 2}}} + x_{{{n // 2 + 1}}}}}{{2}} = \dfrac{{{a} + {b}}}{{2}} = {num(mediana, 1).replace(',', '{,}')}"
    return {
        "datos_ordenados": orden, "n": n, "suma": sum(datos),
        "media": sum(datos) / n, "minimo": orden[0], "maximo": orden[-1],
        "recorrido": orden[-1] - orden[0], "moda_texto": moda_txt,
        "mediana": mediana, "mediana_tex": mediana_tex,
    }

# Funcion para escribir un numero con coma decimal (entero si no tiene parte decimal)
def num(x, dec=2):
    return str(int(x)) if float(x).is_integer() else f"{x:.{dec}f}".replace(".", ",")

# Funcion para redactar la interpretacion del grafico a partir de los datos (pregunta 3)
def interpretacion(est):
    media, me, rec = est["media"], est["mediana"], est["recorrido"]
    k = sum(1 for x in est["datos_ordenados"] if x > media)
    if abs(media - me) <= 0.05 * rec:  # diferencia menor que el 5 % del recorrido
        comp = (f"La media ({num(media)}) y la mediana ({num(me, 1)}) son cercanas: los datos se reparten "
                "de forma bastante equilibrada alrededor del centro.")
    elif media > me:
        comp = (f"La media ({num(media)}) es mayor que la mediana ({num(me, 1)}): unos pocos valores altos "
                "elevan el promedio.")
    else:
        comp = (f"La media ({num(media)}) es menor que la mediana ({num(me, 1)}): unos pocos valores bajos "
                "reducen el promedio.")
    return (f"Los valores van de {est['minimo']} a {est['maximo']}, con un recorrido de {rec}; "
            f"{k} de los {est['n']} datos superan la media. {comp}")

# Funcion para generar una muestra
def muestra(n, lo, hi):
    return sorted(random.randint(lo, hi) for _ in range(n))  # n enteros ordenados en [lo, hi]

# Funcion para generar una muestra repetida
def muestra_repetida():
    base = random.sample(range(25, 85), 4)
    copias = [random.randint(1, 2) for _ in base]
    if max(copias) == 1:  # garantiza al menos un valor repetido para que exista moda
        copias[random.randrange(len(copias))] = 2
    elif min(copias) == 2:  # evita que todos empaten, caso en que no habría moda
        copias[random.randrange(len(copias))] = 1
    vals = [x for x, c in zip(base, copias) for _ in range(c)]
    random.shuffle(vals)
    return vals

# Funcion para generar los datos de un estudiante
def datos_estudiante(idx, nombre):
    c1, c2, c3 = random.choice(CTX1), random.choice(CTX2), random.choice(CTX3)
    pares = ((c1[0], muestra(8, c1[1], c1[2])), (c2, muestra_repetida()), (c3[0], muestra(8, c3[1], c3[2])))
    d = {"estudiante": esc(nombre), "estudiante_id": f"e{idx}"}
    for i, (ctx, m) in enumerate(pares, 1):
        d[f"contexto{i}"] = esc(ctx)
        d[f"muestra{i}"] = " \\qquad ".join(map(str, m))
        est = estadisticos(m)
        d.update({f"sol{i}_{k}": v for k, v in est.items()})  # sol1_media, sol2_moda_texto, …
    d["sol3_interpretacion"] = interpretacion({k[5:]: v for k, v in d.items() if k.startswith("sol3_")})
    return d

# Columnas de la hoja de respuestas del docente: (encabezado, funcion que toma los datos del estudiante)
CLAVE = [
    ("P1 moda", lambda d: d["sol1_moda_texto"]), ("P1 media", lambda d: num(d["sol1_media"])),
    ("P1 mediana", lambda d: num(d["sol1_mediana"], 1)), ("P1 $R$", lambda d: str(d["sol1_recorrido"])),
    ("P2 moda", lambda d: d["sol2_moda_texto"]), ("P2 media", lambda d: num(d["sol2_media"])),
    ("P2 $R$", lambda d: str(d["sol2_recorrido"])), ("P2 mediana", lambda d: num(d["sol2_mediana"], 1)),
    ("P3 media", lambda d: num(d["sol3_media"])), ("P3 mediana", lambda d: num(d["sol3_mediana"], 1)),
]

# Funcion para escribir la hoja de respuestas (una fila por estudiante); va al inicio del PDF de soluciones
def tabla_clave(estudiantes, columnas, semilla, titulo):
    cab = " & ".join([r"\textbf{Estudiante}"] + [rf"\textbf{{{h}}}" for h, _ in columnas])
    filas = "\n".join(" & ".join([d["estudiante"]] + [f(d) for _, f in columnas]) + r" \\ \hline"
                      for d in estudiantes)
    return "\n".join([
        r"\begin{landscape}",  # pdflscape: solo esta pagina va apaisada
        rf"\begin{{center}}\textbf{{\large Hoja de respuestas: {titulo}}}\\[0.2em] \small Semilla: {semilla}\end{{center}}",
        r"{\small\renewcommand{\arraystretch}{1.3}",
        rf"\begin{{longtable}}{{|>{{\raggedright\arraybackslash}}p{{5.2cm}}|{'c|' * len(columnas)}}}",
        r"\hline", cab + r" \\ \hline\endhead", filas, r"\end{longtable}}", r"\end{landscape}", r"\newpage"])

# Funcion para leer el excel
def leer_excel(path):
    df = pd.read_excel(path, header=None)
    for i, row in df.iterrows():
        if row.astype(str).str.contains("Nombre", case=False, na=False).any():
            df.columns = df.iloc[i]  # header sin volver a abrir el xlsx
            return df.iloc[i + 1:].reset_index(drop=True)
    return df

# Funcion para compilar el latex
def compilar(archivo, carpeta=OUTPUT_DIR):
    base = ["pdflatex", "-interaction=nonstopmode", "-output-directory", carpeta]
    subprocess.run([*base, "-draftmode", archivo], capture_output=True, check=False)  # .aux rápido (LastPage)
    subprocess.run([*base, archivo], capture_output=True, check=False)  # PDF final con \pageref resuelto

# Funcion para procesar el excel (el generador de probabilidad la reutiliza con sus parametros)
def procesar(excel_file, log, semilla=None, datos_fn=datos_estudiante,
             plantilla="template_estadistica.tex", carpeta=OUTPUT_DIR, sufijo="estadistica",
             clave=CLAVE, titulo_clave="Estadística descriptiva"):
    if semilla is None:
        semilla = random.randrange(1_000_000)
    random.seed(semilla)  # la semilla queda impresa en las soluciones para reproducir la ejecución
    log(f"Archivo: {os.path.basename(excel_file)} (semilla {semilla})")
    df = leer_excel(excel_file)
    if "Nombre" not in df.columns:
        log("Error: Sin columna 'Nombre'")
        return None
    # Generar los datos de los estudiantes
    estudiantes = []
    for idx, raw in df["Nombre"].items():  # solo columna Nombre (más barato que iterrows)
        nombre = str(raw).strip()
        if nombre and nombre.lower() != "nan":  # celdas vacías / "nan" string
            log(f"  {nombre}")
            estudiantes.append(datos_fn(idx, nombre))

    if not estudiantes:
        log("No se encontraron estudiantes.")
        return None
    # Crear el directorio de salida si no existe
    os.makedirs(carpeta, exist_ok=True)
    tpl = JINJA.get_template(plantilla)
    last = len(estudiantes) - 1  # ultimo -> \end{document} en el template
    hoja = tabla_clave(estudiantes, clave, semilla, titulo_clave)
    # Generar las practicas y las soluciones (estas comienzan con la hoja de respuestas)
    for modo in ("practicas", "soluciones"):
        archivo = os.path.join(carpeta, f"{modo}_{sufijo}.tex")
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("\n".join(
                tpl.render({**d, "modo": modo, "primero": i == 0, "ultimo": i == last,  # primero: preámbulo
                            "semilla": semilla, "clave_tex": hoja if modo == "soluciones" else ""})
                for i, d in enumerate(estudiantes)
            ))
        log(f"Compilando {modo}...")
        compilar(archivo, carpeta)

    log("Listo.")
    return carpeta

# Funcion principal
def main(procesar_fn=procesar, titulo="Generador - Estadística descriptiva"):
    root = tk.Tk()
    root.title(titulo)
    root.geometry("360x140")
    root.resizable(False, False)

    lbl = tk.Label(root, text="Sin archivo", font=("Segoe UI", 9), fg="gray")
    lbl.pack(pady=(15, 5))
    # Funcion para loguear en la UI
    def log_ui(msg, color="black"):
        root.after(0, lambda: lbl.config(text=msg, fg=color))  # UI solo en el hilo principal (Tk)
    # Funcion para trabajar con el archivo
    def trabajar(archivo):
        try:
            carpeta = procesar_fn(archivo, log_ui)
            if carpeta and sys.platform == "win32":
                try:
                    os.startfile(carpeta)
                except OSError:
                    pass
        except Exception as e:
            log_ui(f"Error: {e}", "red")
        finally:
            root.after(0, lambda: btn.config(state="normal"))

    # Funcion para seleccionar el archivo
    def seleccionar():
        f = filedialog.askopenfilename(
            parent=root, initialdir=SCRIPT_DIR,
            filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")],
        )
        if f:
            log_ui(os.path.basename(f))
            btn.config(state="disabled")
            threading.Thread(target=trabajar, args=(f,), daemon=True).start()  # no bloquear la GUI (pdflatex)
    # Boton para seleccionar el archivo
    btn = tk.Button(root, text="Seleccionar archivo", width=20, command=seleccionar)
    btn.pack(pady=4)
    # Mover la ventana al frente
    root.lift()
    root.attributes("-topmost", True)  # ventana al frente en Windows; se quita abajo
    root.after(250, lambda: root.attributes("-topmost", False))
    root.mainloop()

# Main
if __name__ == "__main__":
    main()

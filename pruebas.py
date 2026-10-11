# Pruebas de los dos generadores. Ejecutar con: python pruebas.py
import os
import random
import tempfile
import unittest
from collections import Counter
from fractions import Fraction

import pandas as pd

import generar_estadistica as ge
import generar_probabilidad as gp

REPETICIONES = 20_000


class Moda(unittest.TestCase):
    def test_sin_repeticiones(self):
        self.assertEqual(ge.estadisticos([3, 1, 2])["moda_texto"], "No hay moda")

    def test_una_moda(self):
        self.assertEqual(ge.estadisticos([7, 7, 7])["moda_texto"], "7")
        self.assertEqual(ge.estadisticos([4, 4, 5, 9])["moda_texto"], "4")

    def test_empate_parcial(self):
        self.assertEqual(ge.estadisticos([60, 63, 63, 64, 64, 82, 82])["moda_texto"], "63, 64, 82")

    def test_empate_total(self):
        self.assertEqual(ge.estadisticos([1, 1, 2, 2, 5, 5, 8, 8, 9, 9])["moda_texto"], "No hay moda")


class Medidas(unittest.TestCase):
    def test_ejemplo_del_articulo(self):
        e = ge.estadisticos([4920, 5414, 6596, 7150, 8022, 8121, 8396, 8403])
        self.assertEqual((e["suma"], e["media"], e["recorrido"], e["mediana"]), (57022, 7127.75, 3483, 7586))

    def test_mediana_impar_y_par(self):
        self.assertEqual(ge.estadisticos([82, 60, 64, 63, 64, 63, 82])["mediana"], 64)
        self.assertEqual(ge.estadisticos([1, 2, 3, 4])["mediana"], 2.5)

    def test_interpretacion_segun_los_datos(self):
        self.assertIn("mayor que la mediana", ge.interpretacion(ge.estadisticos([1, 2, 3, 4, 100])))
        self.assertIn("menor que la mediana", ge.interpretacion(ge.estadisticos([1, 97, 98, 99, 100])))
        self.assertIn("son cercanas", ge.interpretacion(ge.estadisticos([10, 20, 30, 40, 50])))


class Muestras(unittest.TestCase):
    def test_muestra_repetida_siempre_tiene_moda(self):
        random.seed(1)
        for _ in range(REPETICIONES):
            m = ge.muestra_repetida()
            self.assertTrue(5 <= len(m) <= 7)
            self.assertNotEqual(ge.estadisticos(m)["moda_texto"], "No hay moda")

    def test_muestra_en_rango_y_ordenada(self):
        random.seed(2)
        for _ in range(1000):
            m = ge.muestra(8, 18, 45)
            self.assertEqual(m, sorted(m))
            self.assertTrue(all(18 <= x <= 45 for x in m))


class Probabilidad(unittest.TestCase):
    def test_conteos_coherentes(self):
        random.seed(3)
        pares = [(i, j) for i in range(1, 7) for j in range(1, 7)]
        for _ in range(REPETICIONES):
            b = gp.prob_bolsa()
            self.assertEqual(b["p1_n"], b["p1_r"] + b["p1_a"] + b["p1_v"])
            self.assertGreaterEqual(b["p1_r"], 3)
            d = gp.prob_dados()
            self.assertEqual(d["p2_fav_s"], sum(1 for i, j in pares if i + j == d["p2_s"]))
            self.assertEqual(d["p2_fav_t"], sum(1 for i, j in pares if i + j > d["p2_t"]))
            t = gp.prob_tabla()
            self.assertEqual(t["p3_total"], t["p3_tsi"] + t["p3_tno"])
            self.assertEqual(t["p3_total"], t["p3_ta"] + t["p3_tb"])
            f = gp.prob_frecuencia()
            self.assertEqual(sum(f["p4_frec"]), f["p4_N"])
            self.assertEqual(f["p4_f"], f["p4_frec"][f["p4_cara"] - 1])

    def test_ejemplo_del_articulo(self):
        self.assertIn(r"\dfrac{20}{156} = \dfrac{5}{39}", gp.prob_tex(20, 156))
        self.assertEqual(Fraction(22, 42), Fraction(11, 21))
        self.assertEqual(Fraction(42, 84) * Fraction(45, 84), Fraction(15, 56))


class Archivos(unittest.TestCase):
    def test_encabezado_en_la_tercera_fila(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, "lista.xlsx")
            pd.DataFrame([["Lista del grupo", None], [None, None], ["Nombre", "Sección"],
                          ["Ana", "10-1"], [None, "10-1"], ["Luis", "10-2"]]).to_excel(ruta, header=False, index=False)
            df = ge.leer_excel(ruta)
            self.assertIn("Nombre", df.columns)
            nombres = [str(x) for x in df["Nombre"] if str(x).strip() and str(x).lower() != "nan"]
            self.assertEqual(nombres, ["Ana", "Luis"])

    def test_escape_latex(self):
        self.assertEqual(ge.esc("Ana_Perez & 100%"), r"Ana\_Perez \& 100\%")


class Reproducibilidad(unittest.TestCase):
    def test_misma_semilla_mismos_datos(self):
        random.seed(2026)
        a = ge.datos_estudiante(0, "X")
        random.seed(2026)
        self.assertEqual(a, ge.datos_estudiante(0, "X"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""
Rebanada delgada #1 - Customer Personality Analysis

Pregunta que responde:
    ¿Qué segmento de clientes, definido por ingreso y composición del hogar,
    aceptó más campañas en el pasado y gasta más?

Importante: la aceptación que se mide es HISTÓRICA (campañas ya realizadas).
No garantiza la misma respuesta en una campaña futura: para eso se propone
una prueba piloto con grupo de control (ver README).

Cómo correrlo:
    python analisis_segmentos.py
    (el archivo marketing_campaign.csv tiene que estar en la misma carpeta)
"""
import pandas as pd
import matplotlib.pyplot as plt

RUTA_CSV = "marketing_campaign.csv"

# ---------------------------------------------------------------
# 1. Carga de datos (el archivo viene separado por tabulaciones)
# ---------------------------------------------------------------
df = pd.read_csv(RUTA_CSV, sep="\t")
print("Filas y columnas originales:", df.shape)

# ---------------------------------------------------------------
# 2. Limpieza mínima (criterio JBGE): solo lo necesario para esta pregunta
#    - Income tiene valores faltantes: sin ingreso no se puede segmentar.
#    - Un cliente declara un ingreso de 666.666, muy lejos del resto
#      (el siguiente más alto es 162.397): se trata como dato atípico.
# ---------------------------------------------------------------
n_original = len(df)
df = df.dropna(subset=["Income"])
df = df[df["Income"] < 600_000].copy()
print(f"Filas excluidas: {n_original - len(df)} | Filas analizadas: {len(df)}")

# ---------------------------------------------------------------
# 3. Variables nuevas
# ---------------------------------------------------------------
# Aceptación histórica: 1 si el cliente aceptó al menos una de las 6 campañas pasadas
campanias = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
             "AcceptedCmp4", "AcceptedCmp5", "Response"]
df["acepto_alguna"] = (df[campanias].sum(axis=1) > 0).astype(int)

# Gasto total: suma de las columnas de gasto por categoría (empiezan con "Mnt")
columnas_gasto = [c for c in df.columns if c.startswith("Mnt")]
df["gasto_total"] = df[columnas_gasto].sum(axis=1)

# Hogar con hijos si hay al menos un niño o adolescente en casa
tiene_hijos = (df["Kidhome"] + df["Teenhome"]) > 0
df["hogar"] = tiene_hijos.map({True: "Con hijos", False: "Sin hijos"})

# Ingreso: tres tramos con la misma cantidad de clientes (terciles)
df["ingreso"] = pd.qcut(df["Income"], 3, labels=["Bajo", "Medio", "Alto"])

# ---------------------------------------------------------------
# 4. Resultado por segmento
# ---------------------------------------------------------------
grupos = df.groupby(["ingreso", "hogar"], observed=True)
resumen = grupos.agg(
    clientes=("ID", "count"),
    tasa_aceptacion=("acepto_alguna", "mean"),
    gasto_promedio=("gasto_total", "mean"),
    gasto_total=("gasto_total", "sum"),
).reset_index()

resumen["pct_clientes"] = resumen["clientes"] / resumen["clientes"].sum() * 100
resumen["pct_gasto"] = resumen["gasto_total"] / resumen["gasto_total"].sum() * 100
resumen["tasa_aceptacion"] = resumen["tasa_aceptacion"] * 100

# ---------------------------------------------------------------
# 5. Control de calidad (si algo falla, el script se detiene con un mensaje)
# ---------------------------------------------------------------
assert len(resumen) == 6, "Se esperaban 6 segmentos (3 de ingreso x 2 de hogar)"
assert len(df) == 2215, f"Se esperaban 2.215 registros y hay {len(df)}"
assert resumen["clientes"].sum() == len(df), "Los segmentos no cubren todos los registros"
assert abs(resumen["pct_clientes"].sum() - 100) < 1e-6, "El % de clientes no suma 100"
assert abs(resumen["pct_gasto"].sum() - 100) < 1e-6, "El % del gasto no suma 100"
print("Control de calidad: OK (2.215 registros en 6 segmentos; % del gasto suma 100)")

resumen = resumen.round(1)

print("\nTramos de ingreso:")
print(df.groupby("ingreso", observed=True)["Income"].agg(["min", "max"]))
print("\nResultado por segmento:")
print(resumen.to_string(index=False))
promedio_aceptacion = df["acepto_alguna"].mean() * 100
promedio_gasto = df["gasto_total"].mean()
print(f"\nPromedio general: aceptación histórica {promedio_aceptacion:.1f}%")
print(f"Promedio general: gasto por cliente {promedio_gasto:.0f}")

resumen.to_csv("resultados_segmentos.csv", index=False)

# ---------------------------------------------------------------
# 6. Gráfico: aceptación histórica de campañas y gasto promedio por segmento
# ---------------------------------------------------------------
niveles = ["Bajo", "Medio", "Alto"]
colores = {"Con hijos": "#9AA5B1", "Sin hijos": "#1F6FEB"}
ancho = 0.38
paneles = [
    ("tasa_aceptacion", "Aceptaron al menos una campaña pasada (%)"),
    ("gasto_promedio", "Gasto promedio por cliente"),
]

fig, ejes = plt.subplots(1, 2, figsize=(11, 4.6))

for ax, (columna, titulo) in zip(ejes, paneles):
    for i, hogar in enumerate(["Con hijos", "Sin hijos"]):
        datos = resumen[resumen["hogar"] == hogar].set_index("ingreso").loc[niveles]
        posiciones = [p + (i - 0.5) * ancho for p in range(3)]
        barras = ax.bar(posiciones, datos[columna], ancho,
                        label=hogar, color=colores[hogar])
        ax.bar_label(barras, fmt="%.0f", padding=2, fontsize=9)
    ax.set_xticks(range(3))
    ax.set_xticklabels([f"Ingreso {n.lower()}" for n in niveles])
    ax.set_title(titulo, fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)

ejes[0].legend(frameon=False)
titulo_general = "Ingreso alto y sin hijos: los que más aceptaron campañas y más gastan"
fig.suptitle(titulo_general, fontsize=13, fontweight="bold")
fig.tight_layout()
fig.savefig("grafico_segmentos.png", dpi=200)
print("\nGráfico guardado en grafico_segmentos.png")

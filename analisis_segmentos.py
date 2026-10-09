"""
Rebanada delgada #1 - Customer Personality Analysis

Pregunta que responde:
    ¿Qué segmento de clientes, definido por ingreso y composición del hogar,
    responde mejor a las campañas de marketing y gasta más?

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
# Respuesta a campañas: 1 si el cliente aceptó al menos una de las 6 campañas
campanias = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
             "AcceptedCmp4", "AcceptedCmp5", "Response"]
df["acepto_alguna"] = (df[campanias].sum(axis=1) > 0).astype(int)

# Gasto total: suma de lo gastado en todas las categorías de producto (columnas Mnt*)
columnas_gasto = [c for c in df.columns if c.startswith("Mnt")]
df["gasto_total"] = df[columnas_gasto].sum(axis=1)

# Hogar: con hijos si tiene al menos un niño o adolescente en casa
df["hogar"] = (df["Kidhome"] + df["Teenhome"] > 0).map(
    {True: "Con hijos", False: "Sin hijos"})

# Ingreso: tres tramos con la misma cantidad de clientes (terciles)
df["ingreso"] = pd.qcut(df["Income"], 3, labels=["Bajo", "Medio", "Alto"])

# ---------------------------------------------------------------
# 4. Resultado por segmento
# ---------------------------------------------------------------
resumen = (
    df.groupby(["ingreso", "hogar"], observed=True)
      .agg(clientes=("ID", "count"),
           tasa_aceptacion=("acepto_alguna", "mean"),
           gasto_promedio=("gasto_total", "mean"),
           gasto_total=("gasto_total", "sum"))
      .reset_index()
)
resumen["pct_clientes"] = resumen["clientes"] / resumen["clientes"].sum()
resumen["pct_gasto"] = resumen["gasto_total"] / resumen["gasto_total"].sum()
resumen["tasa_aceptacion"] = resumen["tasa_aceptacion"] * 100
resumen["pct_clientes"] = resumen["pct_clientes"] * 100
resumen["pct_gasto"] = resumen["pct_gasto"] * 100
resumen = resumen.round(1)

print("\nTramos de ingreso:")
print(df.groupby("ingreso", observed=True)["Income"].agg(["min", "max"]))
print("\nResultado por segmento:")
print(resumen.to_string(index=False))
print(f"\nPromedio general: aceptación {df['acepto_alguna'].mean()*100:.1f}% | "
      f"gasto {df['gasto_total'].mean():.0f}")

resumen.to_csv("resultados_segmentos.csv", index=False)

# ---------------------------------------------------------------
# 5. Gráfico: aceptación de campañas y gasto promedio por segmento
# ---------------------------------------------------------------
fig, ejes = plt.subplots(1, 2, figsize=(11, 4.6))
colores = {"Con hijos": "#9AA5B1", "Sin hijos": "#1F6FEB"}
ancho = 0.38
niveles = ["Bajo", "Medio", "Alto"]

for ax, columna, titulo in [
    (ejes[0], "tasa_aceptacion", "Clientes que aceptaron al menos una campaña (%)"),
    (ejes[1], "gasto_promedio", "Gasto promedio por cliente"),
]:
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
fig.suptitle("Ingreso alto y sin hijos: los clientes que más responden y más gastan",
             fontsize=13, fontweight="bold")
fig.tight_layout()
fig.savefig("grafico_segmentos.png", dpi=200)
print("\nGráfico guardado en grafico_segmentos.png")

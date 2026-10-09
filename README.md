# Segmentación de clientes por ingreso y hogar: ¿a quién dirigir la próxima campaña de marketing?

Análisis en Python que identifica qué segmentos de clientes responden mejor a las campañas de marketing y gastan más, para decidir a quién priorizar en la próxima campaña.

## Problema de negocio

Una empresa que contacta a toda su base de clientes con cada campaña gasta esfuerzo en clientes que casi no responden. En este dataset, solo el 27% de los clientes aceptó al menos una de las seis campañas.

**Pregunta:** ¿qué segmento de clientes, definido por ingreso y composición del hogar, responde mejor a las campañas de marketing y gasta más?

## Datos

- **Fuente:** [Customer Personality Analysis (Kaggle)](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)
- **Archivo:** `marketing_campaign.csv`, 2.240 filas y 29 columnas, separado por tabulaciones.
- El archivo **no está incluido** en este repositorio: hay que descargarlo de Kaggle (ver "Cómo ejecutar").

## Stack tecnológico

- Python 3
- pandas (limpieza y agregaciones)
- matplotlib (gráfico)
- Git y GitHub (versionado)

## Metodología

Se trabajó con CRISP-DM y sprints cortos, empezando por una **rebanada delgada**: la porción mínima que atraviesa todas las fases y ya responde parte de la pregunta.

| Fase CRISP-DM | Qué se hizo en la rebanada #1 |
|---|---|
| Comprensión del negocio | Pregunta de negocio y definición de segmentos (ingreso y hogar) |
| Comprensión de los datos | Carga del CSV, revisión de nulos y valores atípicos en `Income` |
| Preparación de los datos | Limpieza mínima (criterio JBGE) y variables `acepto_alguna`, `gasto_total`, `hogar`, `ingreso` |
| Modelado | Análisis descriptivo: tasa de aceptación y gasto por segmento |
| Evaluación | Gráfico y lectura del resultado |
| Despliegue | Presentación ejecutiva y este repositorio |

**Plan de sprints:** el Sprint 1 (rebanada #1) está completo. Los sprints 2 y 3 (análisis por canal de compra, diccionario de variables y análisis por campaña) están planificados y todavía no se ejecutaron.

**Criterio JBGE (lo justo y necesario):** solo se limpió lo necesario para esta pregunta: se excluyeron 25 filas (24 sin ingreso y 1 con un ingreso atípico de 666.666), quedando 2.215 clientes. Quedó afuera el análisis por canal de compra, los modelos predictivos y la segmentación avanzada.

## Hallazgos clave

- **Ingreso alto y sin hijos** es el segmento que más responde y más gasta: 441 clientes (19,9% de la base) concentran el 46,7% del gasto, y el 54,6% aceptó al menos una campaña, el doble del promedio general (27,3%).
- El gasto promedio por cliente crece con el ingreso: el tramo alto gasta unas 13 veces más que el bajo.
- En ingreso medio y alto, los hogares sin hijos aceptan más campañas que los que tienen hijos.
- **Ingreso bajo con hijos** es el 28,2% de la base y aporta solo el 4,0% del gasto.

| Ingreso | Hogar | Clientes | % de clientes | Aceptó alguna campaña | Gasto promedio | % del gasto |
|---|---|---|---|---|---|---|
| Bajo | Con hijos | 624 | 28,2% | 16,8% | 86 | 4,0% |
| Bajo | Sin hijos | 115 | 5,2% | 13,0% | 145 | 1,2% |
| Medio | Con hijos | 661 | 29,8% | 20,3% | 430 | 21,1% |
| Medio | Sin hijos | 77 | 3,5% | 33,8% | 711 | 4,1% |
| Alto | Con hijos | 297 | 13,4% | 28,3% | 1.038 | 22,9% |
| Alto | Sin hijos | 441 | 19,9% | 54,6% | 1.424 | 46,7% |

![Aceptación de campañas y gasto promedio por segmento](grafico_segmentos.png)

La presentación ejecutiva está en la carpeta [`presentacion/`](presentacion/).

## Cómo ejecutar

1. Clonar el repositorio y entrar a la carpeta:

```bash
git clone https://github.com/Tobias-Cavodeassi/analisis-segmentos-clientes-marketing.git
cd analisis-segmentos-clientes-marketing
```

2. Crear y activar un entorno virtual, e instalar las dependencias:

```bash
python -m venv venv
source venv/Scripts/activate   # Git Bash en Windows (en Mac o Linux: source venv/bin/activate)
pip install -r requirements.txt
```

3. Descargar `marketing_campaign.csv` desde Kaggle y copiarlo en esta carpeta.

4. Correr el análisis:

```bash
python analisis_segmentos.py
```

Genera `resultados_segmentos.csv` y `grafico_segmentos.png`.

## Estructura del repositorio

```
analisis_segmentos.py      script del análisis (rebanada #1)
resultados_segmentos.csv   tabla de resultados por segmento
grafico_segmentos.png      gráfico de resultados
presentacion/              diapositivas ejecutivas (imágenes)
requirements.txt           dependencias
```

## Limitaciones

- Los resultados son descriptivos: muestran asociación, no causa.
- Los segmentos de ingreso bajo sin hijos (115 clientes) y de ingreso medio sin hijos (77 clientes) son chicos, así que sus tasas hay que leerlas con cautela.
- El dataset no indica la moneda del ingreso ni del gasto.

## Próximos pasos

- Analizar el gasto por canal de compra (web, catálogo y tienda).
- Revisar la respuesta campaña por campaña.
- Validar el hallazgo con una prueba piloto antes de reasignar presupuesto.

## Autor

Tobías Cavodeassi, Data Analyst Jr. (Marketing & Growth).

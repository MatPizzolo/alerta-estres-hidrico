# 🌊🌾 Alerta de Anomalías Hídricas

> **EN — TL;DR:** Satellite-based detection of agro-hydric anomalies (drought & flood) over Argentine farmland, using Google Earth Engine + Python. Case studies: the historic 2022/23 drought (worst in ~60 years, ~USD 20B in losses) and the Buenos Aires province floods. Rainfall deviation, NDVI anomalies and SAR change detection, from district level down to individual field level — the building blocks of parametric crop insurance and agro-climate risk products.

Detección de **sequías e inundaciones en lotes agrícolas argentinos** con imágenes satelitales y Google Earth Engine:

- 📉 **Desviación de lluvias** contra el promedio histórico (CHIRPS, 40+ años de datos)
- 🌱 **Anomalía de vegetación** (NDVI vs. climatología del lote)
- 🛰️ **Mapeo de inundaciones** con radar Sentinel-1 (funciona incluso con nubes)
- 🔍 **Detección de cambio** pre/post evento, partido por partido y lote por lote

## Los eventos analizados

### 🥀 Sequía 2022/23 — la peor en décadas

Tres años consecutivos de La Niña culminaron en la campaña 2022/23: la soja cayó 54% (peor campaña desde 1999), el trigo 48%, y la pérdida para la economía se estimó en **USD 19.000 millones, ~3 puntos del PBI** (BCR). Este proyecto reconstruye cómo se veía esa sequía desde el espacio: mapas de anomalía de precipitación y vegetación de la zona núcleo, **partido por partido y lote por lote**.

### 🌊 Inundaciones bonaerenses

El caso opuesto: excesos hídricos extremos en la provincia de Buenos Aires (caso de estudio principal: **Bahía Blanca, 7 de marzo de 2025**: 290 mm en 12 horas, un evento con recurrencia mayor a 100 años según el SMN). Con radar Sentinel-1 se delimita el agua superficial antes y después del evento y se cuantifica la **superficie agrícola afectada** por partido.

## Resultados

> 🚧 En construcción — acá van los mapas y GIFs a medida que avanzan los notebooks.

| Análisis | Vista previa | Notebook |
|---|---|---|
| Anomalía de lluvias 2022/23 (zona núcleo) | _pendiente_ | `notebooks/01_lluvia_desviacion.ipynb` |
| Anomalía NDVI sequía, lote por lote | _pendiente_ | `notebooks/02_ndvi_anomalia.ipynb` |
| Mapa de inundación Sentinel-1 | _pendiente_ | `notebooks/03_inundacion_sar.ipynb` |
| Detección de cambio pre/post evento | _pendiente_ | `notebooks/04_deteccion_cambio.ipynb` |

## Metodología (resumen)

1. **Lluvia:** precipitación acumulada por campaña (CHIRPS) vs. media histórica 1981–2021 → anomalía en mm y % por partido y por lote. Opcional: SPI-3/SPI-6.
2. **Vegetación:** NDVI (MODIS / Sentinel-2) de la campaña vs. climatología del mismo píxel → z-score de anomalía. Verde = normal, rojo = estrés.
3. **Inundación:** retrodispersión VH de Sentinel-1 pre/post evento, umbral (Otsu) + máscara de agua permanente (JRC) → agua nueva = inundación.
4. **Agregación:** estadística zonal sobre partidos (límites IGN/GAUL) y sobre lotes demo digitalizados en zona núcleo.

Detalle completo en [docs/METODOLOGIA.md](docs/METODOLOGIA.md) · Fuentes de datos en [docs/DATOS.md](docs/DATOS.md)

## Estructura del repo

```
├── notebooks/          # Análisis numerados (01 → 04), uno por producto
├── app/                # App Streamlit: elegí partido + fecha → mapa de anomalía
├── data/
│   ├── lotes/          # GeoJSON de lotes demo (zona núcleo)
│   └── partidos/       # Límites administrativos (referencia, no versionados)
├── src/                # Funciones compartidas (GEE helpers, estadística zonal)
├── assets/             # Mapas, GIFs y visuales exportados (LinkedIn-ready)
└── docs/               # Metodología, datos, roadmap
```

## Cómo correrlo

Requiere una cuenta de [Google Earth Engine](https://earthengine.google.com/) (gratuita para uso no comercial) y Python 3.11+.

```bash
git clone <este-repo> && cd alerta-anomalias-hidricas
pip install -r requirements.txt        # earthengine-api, geemap, streamlit, geopandas...
earthengine authenticate               # una sola vez
jupyter lab notebooks/                 # análisis
streamlit run app/main.py              # app interactiva
```

## Por qué importa

La sequía 2022/23 demostró que el riesgo hídrico es **el** riesgo del agro argentino. Los seguros paramétricos y los productos de riesgo agroclimático (el negocio de empresas como S4) necesitan exactamente esto: **índices objetivos, medidos por satélite, a nivel de lote, con historia suficiente para calcular disparadores**. Este proyecto implementa esos bloques con datos 100% públicos y gratuitos.

## Origen y créditos

Basado en el curso *Google Earth Engine for Agriculture* (proyectos guiados de desviación de lluvias y flood mapping + módulo de change detection), extendido a eventos reales argentinos con análisis propio en Python.

---

**Mateo** · [LinkedIn](#) · matpizzolo@gmail.com

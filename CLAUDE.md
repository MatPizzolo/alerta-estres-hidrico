# CLAUDE.md — Alerta de Anomalías Hídricas

Proyecto de portfolio ML/agro: detección de sequías e inundaciones en campos argentinos con Google Earth Engine + Python. Casos reales: sequía 2022/23 y inundaciones bonaerenses (Bahía Blanca 2025).

## Contexto clave

- **Audiencia doble:** reclutadores de ML (leen el código y el README) y el ambiente agro argentino en LinkedIn (consume los mapas y visuales). Todo output visual debe ser publicable tal cual.
- **Ángulo de negocio:** los análisis imitan los bloques de un producto de riesgo agroclimático / seguro paramétrico (índices objetivos por lote). Mantener ese framing en docs y visuales.
- El roadmap vive en [docs/ROADMAP.md](docs/ROADMAP.md); la metodología en [docs/METODOLOGIA.md](docs/METODOLOGIA.md); las fuentes de datos con sus IDs de GEE en [docs/DATOS.md](docs/DATOS.md).

## Stack

- Python 3.11+, `earthengine-api`, `geemap`, `geopandas`, `streamlit`, `matplotlib`.
- Análisis en notebooks Jupyter (`notebooks/`), lógica reutilizable en `src/`, app en `app/`.
- GEE ya autenticado localmente (`earthengine authenticate`). Si un script falla con error de auth/proyecto, avisar en vez de reintentar con credenciales inventadas.

## Convenciones

- **Idioma:** docs, markdown, títulos de mapas y textos de la app en **español rioplatense**. Código (nombres de variables, funciones, commits) en **inglés**. README mantiene el TL;DR en inglés al inicio.
- **Notebooks:** numerados (`01_`, `02_`...), uno por producto de análisis. Cada notebook empieza con una celda markdown que explica qué hace y qué evento cubre. Deben poder correrse de punta a punta tras `earthengine authenticate`.
- **Nada de datos pesados en git:** rasters, exports y descargas van a `data/` (gitignoreado) o quedan en GEE. Solo se versionan GeoJSON chicos (lotes demo, <1 MB) y los visuales finales en `assets/`.
- **GEE:** preferir computación server-side (reducers, `map` sobre colecciones) antes que bajar píxeles. Evitar `getInfo()` en loops. Escalas explícitas en `reduceRegion` (CHIRPS ~5566 m, MODIS 250 m, Sentinel 10 m).
- **Visuales:** paletas consistentes entre notebooks (anomalía de lluvia y NDVI: divergente rojo-blanco-azul centrada en 0; inundación: azul sobre base gris). Todo mapa exportado lleva título, fecha/período, fuente de datos y escala.
- **Cifras del mundo real** (pérdidas, producción, muertes) siempre con fuente citada (BCR, BCBA, INDEC) y en `docs/`; no inventar ni redondear de memoria en visuales públicos.

## Qué no hacer

- No convertir los notebooks en scripts JS del Code Editor: el stack es Python.
- No agregar dependencias de infraestructura (Docker, bases de datos, cloud propio): el proyecto corre local + GEE.
- No commitear credenciales ni el project-id de GEE hardcodeado: usar `ee.Initialize(project=os.environ.get("EE_PROJECT"))`.

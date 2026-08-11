# Alerta de estrés hídrico

[English](README.en.md)

**Cuánto se apartó una campaña de lo normal en agua, medido desde el satélite, partido por partido y
lote por lote.**

Análisis de anomalías hídricas sobre el agro argentino con Google Earth Engine y Python, en las dos
direcciones: déficit (sequía) y exceso (inundación). Todo el cómputo pesado ocurre server-side en
Earth Engine —sumas de campaña, climatologías de 40 años, estadística zonal— y a Python solo baja la
tabla final por partido. El recorte de análisis no es el año calendario sino la **campaña gruesa
(1 de septiembre → 31 de marzo)**, que es el ciclo que le importa al cultivo.

---

## Qué mide

| Producto | Pregunta que responde | Señal |
|---|---|---|
| **Desviación de lluvias** | ¿Cuánto llovió esta campaña contra lo normal? | Anomalía de precipitación acumulada (mm y %) contra una climatología de 40 campañas |
| **Anomalía de vegetación** | ¿Cómo respondió el cultivo? | z-score de NDVI por píxel contra la climatología del mismo período del año |
| **Mapeo de inundación** | ¿Qué superficie quedó bajo el agua, y cuánta era agrícola? | Retrodispersión VH de Sentinel-1 pre/post evento, menos el agua permanente |
| **Detección de cambio** | ¿Qué cambió entre dos fechas cualesquiera? | Log-ratio para SAR, diferencia de NDVI para óptico |

La lluvia es la causa y el NDVI el efecto: por eso van juntos y no por separado. El radar entra
porque durante una inundación está nublado, que es exactamente cuando el óptico no sirve.

## Los dos eventos

**Sequía 2022/23.** Tres campañas seguidas de La Niña. La soja terminó en 20 Mt, un 54% menos y la
peor campaña desde 1999 (BCR). Es el caso de déficit: sirve porque el evento es grande y porque
existe un contraste administrativo contra el cual validar —los 68 partidos bonaerenses declarados en
emergencia por la Resolución MEC 587/2023—. Si el ranking satelital y la declaración cuentan la
misma historia, el índice funciona.

**Inundación de Bahía Blanca, 7 de marzo de 2025.** 290 mm en 12 horas, período de retorno mayor a
100 años según el SMN. Es el caso de exceso, y tiene un benchmark metodológico directo: INTA AER
Bahía Blanca analizó el mismo evento, con los mismos sensores y también en Earth Engine, así que hay
contra qué comparar la mancha de inundación en vez de publicarla sola.

Las cifras del contexto están verificadas contra fuente primaria en
[`docs/DATOS.md`](docs/DATOS.md); ninguna se cita de memoria.

## Cómo funciona

**Ventana de campaña, no año calendario.** `season_dates()` y `chirps_season_sum()` recortan de
septiembre a marzo. La climatología se arma promediando esa misma ventana sobre las campañas que
arrancan entre 1981 y 2020 — 40 campañas comparables entre sí, no 40 años corridos.

**Dos anomalías, no una.** `anomaly_images()` devuelve la absoluta (mm) y la relativa (%). La
relativa es la que se mapea, porque 200 mm de déficit no significan lo mismo en Pergamino que en
La Pampa; la absoluta queda en la tabla para no perder la magnitud.

**Todo server-side, una sola bajada.** Suma de campaña, climatología y anomalías se calculan como
imágenes de Earth Engine; `reduceRegions` agrega por partido; recién ahí `geemap.ee_to_gdf` baja una
`FeatureCollection` a GeoDataFrame. No hay `getInfo()` dentro de un loop, y las escalas nominales son
explícitas en cada reducción (`SCALE_CHIRPS = 5566`, `SCALE_MODIS = 250`, `SCALE_S2 = 10`) en vez de
depender del default.

**Dos escalas de agregación.** Partido (FAO GAUL nivel 2) para el mapa y el ranking; lote (12
polígonos demo digitalizados en zona núcleo, en `data/lotes/lotes_demo.geojson`) para el detalle
donde MODIS a 250 m ya mezcla parcelas y hace falta Sentinel-2.

**Paleta con convención fija.** Divergente rojo–blanco–azul centrada en 0 para toda anomalía: rojo
déficit, azul exceso. Está en `PALETTES` y se comparte entre notebooks, para que dos mapas del
proyecto se puedan leer uno al lado del otro.

Las limitaciones del método —CHIRPS no capta variabilidad intra-lote, MODIS mezcla lotes chicos, el
umbral SAR simple confunde inundación con suelo muy húmedo— están declaradas en
[`docs/METODOLOGIA.md`](docs/METODOLOGIA.md#limitaciones-conocidas).

## Datos

Todo público y gratuito, y todo vive en el catálogo de Earth Engine: no se descargan rasters.

| Dataset | ID en GEE | Resolución | Para qué |
|---|---|---|---|
| CHIRPS Pentad | `UCSB-CHG/CHIRPS/PENTAD` | ~5,5 km, 1981– | Precipitación y anomalías |
| MODIS NDVI | `MODIS/061/MOD13Q1` | 250 m, 16 días, 2000– | Climatología y anomalía de NDVI |
| Sentinel-2 SR Harmonized | `COPERNICUS/S2_SR_HARMONIZED` | 10 m, 2017– | NDVI a nivel lote |
| Sentinel-1 GRD | `COPERNICUS/S1_GRD` | 10 m, 2014– | Mapeo de inundación (banda VH) |
| JRC Global Surface Water | `JRC/GSW1_4/GlobalSurfaceWater` | 30 m | Máscara de agua permanente |
| ESA WorldCover | `ESA/WorldCover/v200` | 10 m | Máscara de superficie agrícola |
| SRTM | `USGS/SRTMGL1_003` | 30 m | Máscara de pendiente para el SAR |
| FAO GAUL nivel 2 | `FAO/GAUL/2015/level2` | — | Límites de partidos y departamentos |

Licencias, alternativas (límites del IGN) y fuentes de validación no satelitales en
[`docs/DATOS.md`](docs/DATOS.md).

## Estructura

```
notebooks/
  01_lluvia_desviacion.ipynb   # anomalía de precipitación por partido
src/
  gee_utils.py                 # init de EE, IDs de datasets, escalas, ventana de
                               # campaña, climatologías, anomalías y estadística zonal
data/
  lotes/lotes_demo.geojson     # 12 lotes ilustrativos en zona núcleo (versionado)
docs/
  METODOLOGIA.md               # los cuatro productos, métrica por métrica
  DATOS.md                     # fuentes, IDs de GEE y cifras con fuente primaria
  ROADMAP.md                   # orden de trabajo por fases
```

`data/` está gitignoreado salvo los lotes demo: los exports y las tablas que generan los notebooks
quedan afuera. Los notebooks guardan sus figuras en `assets/`, que se crea al correrlos.

## Cómo correrlo

Requiere Python 3.11+ y una cuenta de [Google Earth Engine](https://earthengine.google.com/)
(gratuita para uso no comercial), ya autenticada.

```bash
git clone git@github.com:MatPizzolo/alerta-estres-hidrico.git
cd alerta-estres-hidrico
pip install -r requirements.txt

earthengine authenticate          # una sola vez
export EE_PROJECT=tu-proyecto-gee # obligatorio: init_ee() falla sin esto

jupyter lab notebooks/
```

A diferencia de los otros proyectos satelitales de este portfolio, acá la autenticación es
interactiva por usuario y no por service account: el proyecto corre local contra Earth Engine, sin
deploy ni contenedor. El project-id nunca se hardcodea — `init_ee()` lo lee de `EE_PROJECT` y aborta
con un mensaje explícito si falta.

## Estado

| Parte | Estado |
|---|---|
| `src/gee_utils.py` | Completo para el producto de lluvia: init, ventana de campaña, climatología, anomalías, estadística zonal y series mensuales |
| Notebook 01 — desviación de lluvias | Escrito de punta a punta (mapa por partido, ranking y serie mensual de Pergamino contra su climatología). **Sin salidas guardadas** en el repo: hay que correrlo para ver los mapas |
| Notebook 02 — anomalía de NDVI | No implementado. Método definido en `docs/METODOLOGIA.md` |
| Notebook 03 — inundación con SAR | No implementado |
| Notebook 04 — detección de cambio | No implementado |
| App interactiva | No implementada. Está en el roadmap como fase posterior; hoy el proyecto son notebooks |
| Validación contra emergencia agropecuaria | Pendiente: la lista de los 68 partidos hay que transcribirla de la resolución, no existe como dataset descargable |
| Tests | No hay. El código es una librería de helpers de GEE consumida desde notebooks |

Es el proyecto más temprano del portfolio: hay un producto de análisis de cuatro terminado y la
infraestructura compartida para los otros tres.

## Documentos relacionados

- [`docs/METODOLOGIA.md`](docs/METODOLOGIA.md) — los cuatro productos, sus métricas y las limitaciones
- [`docs/DATOS.md`](docs/DATOS.md) — datasets, IDs de GEE y cifras verificadas con fuente
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — orden de trabajo
- [`../monitor-cultivos-ndvi/README.md`](../monitor-cultivos-ndvi/README.md) — NDVI por lote a lo
  largo de varias campañas, sobre Sentinel-2

## Origen

Parte del análisis arranca de los proyectos guiados del curso *Google Earth Engine for Agriculture*
(desviación de lluvias, flood mapping y detección de cambio), reescrito en Python y extendido a
eventos argentinos reales con datos y validación propios.

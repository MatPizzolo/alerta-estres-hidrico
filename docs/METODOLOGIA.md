# Metodología

Cuatro productos de análisis, cada uno con su notebook. Los dos primeros cubren la sequía 2022/23; el tercero y cuarto, las inundaciones bonaerenses. Todos se agregan a dos escalas: **partido** (límites administrativos) y **lote** (polígonos demo en zona núcleo).

## 1. Desviación de lluvias (`01_lluvia_desviacion.ipynb`)

**Pregunta:** ¿cuánto llovió en la campaña 2022/23 respecto de lo normal?

- **Datos:** CHIRPS Pentad (precipitación, ~5,5 km, 1981–presente).
- **Período de análisis:** campaña gruesa, septiembre 2022 – marzo 2023.
- **Línea base:** media de precipitación acumulada del mismo período (sep–mar) para 1981–2021.
- **Métrica:**
  - Anomalía absoluta: `P_campaña − P_media_histórica` (mm)
  - Anomalía relativa: `(P_campaña − P_media) / P_media × 100` (%)
- **Salida:** mapa de anomalía (paleta divergente centrada en 0), tabla por partido, serie temporal mensual de un partido testigo (ej. Pergamino) contra su climatología.
- **Extensión opcional:** SPI-3 y SPI-6 (índice estandarizado de precipitación) para hablar el idioma de los seguros paramétricos.

## 2. Anomalía de vegetación (`02_ndvi_anomalia.ipynb`)

**Pregunta:** ¿cómo respondió el cultivo? La lluvia es la causa; el NDVI, el efecto en la planta.

- **Datos:** MODIS MOD13Q1 (NDVI, 250 m, 16 días, 2000–presente) para la serie histórica; Sentinel-2 SR (10 m) para los zoom a lote.
- **Métrica:** z-score de anomalía por píxel: `(NDVI_campaña − μ_histórico) / σ_histórico`, usando la climatología 2000–2021 del mismo período del año.
- **Máscara de cultivo:** mapa de coberturas (ESA WorldCover o mapas nacionales de cultivo) para no medir estrés en ciudades o agua.
- **Salida:** mapa de z-score por partido, y el producto estrella del proyecto: **"así se veía la sequía lote por lote"** — panel comparando los lotes demo en una campaña normal vs. 2022/23 con Sentinel-2.

## 3. Mapeo de inundación (`03_inundacion_sar.ipynb`)

**Pregunta:** ¿qué superficie quedó bajo el agua, y cuánta era agrícola?

- **Datos:** Sentinel-1 GRD (radar banda C, 10 m). El radar atraviesa nubes — clave porque durante una inundación está nublado.
- **Evento principal:** Bahía Blanca y zona de influencia, marzo 2025.
- **Método:**
  1. Mosaico pre-evento (ventana de ~1 mes antes) y post-evento (primeras pasadas después), polarización VH.
  2. Filtro de speckle (focal median o Refined Lee).
  3. El agua refleja el radar lejos del sensor → retrodispersión muy baja. Umbral sobre la imagen post (Otsu o umbral fijo ~−20 dB en VH).
  4. Restar agua permanente (JRC Global Surface Water) → lo que queda es **agua nueva = inundación**.
  5. Limpieza: eliminar manchas menores a N píxeles conectados, enmascarar pendientes altas (SRTM).
- **Salida:** mapa de mancha de inundación, hectáreas afectadas por partido, % de superficie agrícola afectada.

## 4. Detección de cambio (`04_deteccion_cambio.ipynb`)

**Pregunta:** ¿qué cambió entre antes y después del evento? Generaliza el análisis a cualquier par de fechas.

- **Método:** diferencia y ratio de imágenes pre/post (log-ratio para SAR, diferencia de NDVI para óptico), con umbrales de cambio significativo.
- **Aplicado a los dos eventos:** pérdida de vigor vegetal durante la sequía (ΔNDVI entre diciembre 2022 y un diciembre normal) y transformación del paisaje post-inundación.
- **Salida:** mapas bitemporales de cambio + GIF animado antes/después (el formato más compartible para LinkedIn).

## Agregación y validación

- **Estadística zonal:** `reduceRegions` sobre partidos y lotes; escala explícita según sensor. Resultados a GeoDataFrame → tablas y ranking de partidos más afectados.
- **Validación (informal, nivel portfolio):**
  - *Sequía:* contrastar el ranking de anomalía con los 68 partidos bonaerenses declarados en emergencia por la Resolución MEC 587/2023 (lista partido por partido en el Boletín Oficial → `data/emergencia_agropecuaria.csv`). Si el satélite y la declaración administrativa cuentan la misma historia, el índice funciona.
  - *Inundación:* comparar nuestra mancha con el análisis que INTA AER Bahía Blanca publicó sobre el mismo evento, con los mismos sensores y también en GEE (ver referencia en [DATOS.md](DATOS.md)) — es un benchmark directo de la metodología.

## Limitaciones conocidas

- CHIRPS a ~5,5 km no capta variabilidad de lluvia intra-lote: a escala de lote la precipitación es contextual, el NDVI es la señal fina.
- MODIS a 250 m mezcla lotes chicos; por eso los zoom a lote usan Sentinel-2.
- El umbral SAR simple confunde inundación con suelo muy húmedo o vegetación inundada alta; suficiente para un evento extremo como Bahía Blanca, no para monitoreo operativo.

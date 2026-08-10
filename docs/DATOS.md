# Fuentes de datos

Todos los datasets son públicos y gratuitos. Los satelitales viven en el catálogo de Google Earth Engine (no se descargan salvo exports finales).

## Satelitales / climáticos (GEE)

| Dataset | ID en GEE | Resolución | Uso |
|---|---|---|---|
| CHIRPS Pentad | `UCSB-CHG/CHIRPS/PENTAD` | ~5,5 km, 1981– | Precipitación y anomalías |
| MODIS NDVI | `MODIS/061/MOD13Q1` | 250 m, 16 días, 2000– | Climatología y anomalía NDVI |
| Sentinel-2 SR Harmonized | `COPERNICUS/S2_SR_HARMONIZED` | 10 m, 2017– | NDVI a nivel lote |
| Sentinel-1 GRD | `COPERNICUS/S1_GRD` | 10 m, 2014– | Mapeo de inundación (VH) |
| JRC Global Surface Water | `JRC/GSW1_4/GlobalSurfaceWater` | 30 m | Máscara de agua permanente |
| ESA WorldCover | `ESA/WorldCover/v200` | 10 m | Máscara de área agrícola |
| SRTM | `USGS/SRTMGL1_003` | 30 m | Máscara de pendiente (SAR) |

## Límites administrativos

- **Partidos/departamentos:** FAO GAUL nivel 2 (`FAO/GAUL/2015/level2`, ya en GEE, suficiente para empezar) o capa oficial del IGN Argentina (más actualizada, requiere subirla como asset). Empezar con GAUL; migrar a IGN si algún límite viene mal.
- **Lotes demo:** 10–20 polígonos digitalizados a mano sobre imagen Sentinel-2 en zona núcleo (Pergamino / Rojas / Salto) → `data/lotes/lotes_demo.geojson`, versionado en git. Son lotes ilustrativos, no propiedad de nadie identificada.

## Contexto y validación (no satelitales)

- **BCR (Bolsa de Comercio de Rosario):** estimaciones de producción y pérdidas de la campaña 2022/23.
- **BCBA (Bolsa de Cereales de Buenos Aires):** informes PAS, estado de cultivos semanal.
- **Emergencia agropecuaria:** declaraciones por partido (Ministerio/Secretaría de Agricultura) como ground truth administrativo de la sequía.
- **SMN:** precipitación de estaciones para sanity-check puntual de CHIRPS.

## Cifras verificadas (con fuente primaria)

Verificadas contra informes oficiales el 2026-08-05. Usar estas cifras en visuales y posts, citando la fuente indicada.

### Sequía 2022/23

| Cifra | Valor | Fuente |
|---|---|---|
| Pérdida para la economía total | **USD 19.000 millones** (~3 puntos del PBI 2023) | BCR, marzo 2023 |
| Pérdida de ingresos del productor (soja+trigo+maíz) | **USD 14.140 millones** | [BCR, Informativo Semanal](https://www.bcr.com.ar/es/mercados/investigacion-y-desarrollo/informativo-semanal/noticias-informativo-semanal/el-costo-de-la) |
| Producción perdida (soja+trigo+maíz) | **~50 Mt menos** que la campaña anterior | BCR ([Infobae](https://www.infobae.com/economia/campo/2023/05/09/soja-maiz-y-trigo-el-impacto-en-la-economia-de-una-cosecha-que-tendra-50-millones-de-toneladas-menos-que-la-anterior/)) |
| Soja 2022/23 | **20 Mt** (−54,3%, peor campaña desde 1999) | BCR, vía [Chequeado](https://chequeado.com/el-explicador/como-impacto-la-sequia-en-la-cosecha-de-2023-y-en-la-economia-argentina/) |
| Trigo 2022/23 | **11,5 Mt** (−48%, mínimo desde 2015) | BCR, ídem |
| Maíz 2022/23 | **−39%** vs. esperado | BCR, ídem |
| Actividad agropecuaria 2023 | **−27,1% interanual** (agosto 2023) | INDEC, vía Chequeado |
| Divisas no ingresadas | **~USD 17.000 millones** vs. 2022 | CIARA-CEC, vía Chequeado |

> Nota: BCBA reporta valores levemente distintos (soja ~21 Mt, trigo ~12,2 Mt). Elegir **una** fuente por visual y citarla; no mezclar.

### Inundación Bahía Blanca (marzo 2025)

| Cifra | Valor | Fuente |
|---|---|---|
| Precipitación récord | **210 mm en 6 h** (récord histórico previo: 150,9 mm, de 1975) | SMN, [informe oficial 4-8 marzo](https://www.argentina.gob.ar/noticias/4-8-marzo-informe-sobre-las-lluvias-e-inundaciones-en-bahia-blanca-y-alrededores) |
| Total del evento | **290 mm en 12 h**; 312 mm acumulados 4–8 de marzo | SMN, ídem |
| Recurrencia | evento con período de retorno **>100 años** | SMN, ídem |
| Otras localidades | Coronel Suárez 204 mm, Pigüé 116 mm | SMN, ídem |
| Impacto humano | 16 fallecidos, miles de evacuados | INTA AER Bahía Blanca (ver referencia abajo) |

### Emergencia agropecuaria (ground truth administrativo)

- **Buenos Aires:** Resolución MEC **587/2023** ([Boletín Oficial, 3-may-2023](https://www.boletinoficial.gob.ar/detalleAviso/primera/285636/20230503)) — declara emergencia/desastre por sequía en **68 partidos**, con períodos por partido. El texto completo tiene la lista partido por partido → transcribirla a `data/emergencia_agropecuaria.csv` para la validación.
- **Buenos Aires (ampliación):** Resolución **1612/2023** ([texto](https://www.argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-1612-2023-392175)) — suma Villarino, Patagones, Rivadavia, Pehuajó, Berisso.
- **Córdoba:** Resolución MEC **290/2023** — emergencia por sequía ene–jun 2023.
- Marco legal: Ley 26.509 (emergencia = >50% de la producción afectada; desastre = >80%).
- No existe dataset consolidado descargable de partidos en emergencia: hay que armar el CSV desde las resoluciones (trabajo menor, ~1 h).

### Referencia metodológica clave 🔑

> **INTA AER Bahía Blanca** — *"Análisis de la inundación del 7 de marzo de 2025 en la ciudad y el partido de Bahía Blanca: empleando imágenes satelitales ópticas Sentinel-2A y Sentinel-1 SAR"* ([ficha en repositorio](https://repositoriosdigitales.mincyt.gob.ar/vufind/Record/INTADig_5f1deefceb7c61d827192902dcb5e5a0)).
> INTA analizó **el mismo evento, con los mismos sensores y también en Google Earth Engine** (Sentinel-2 del 19-feb y 11-mar-2025). Sirve como referencia para elegir fechas de imágenes y como benchmark para comparar nuestra mancha de inundación contra la de ellos.

## Descarga de límites administrativos (IGN)

- **Centro de descargas de capas SIG del IGN:** [ign.gob.ar/NuestrasActividades/InformacionGeoespacial/CapasSIG](https://www.ign.gob.ar/NuestrasActividades/InformacionGeoespacial/CapasSIG) — capa "Departamento" (división político-administrativa de 2º orden = partidos) en SHP/KML/**GeoJSON**, gratuita.
- Alternativa: [datos.gob.ar — unidades territoriales](https://datos.gob.ar/dataset/ign-unidades-territoriales) o geoservicios WFS del IGN.
- Para GEE: subir el GeoJSON como asset, o usar FAO GAUL nivel 2 directo del catálogo mientras tanto.

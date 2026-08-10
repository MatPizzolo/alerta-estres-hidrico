# Roadmap

Orden pensado para que cada fase deje algo publicable. Si el proyecto se corta en cualquier punto después de la fase 2, igual hay portfolio.

## Fase 0 — Setup (½ día)
- [ ] Repo, `.gitignore`, `requirements.txt`, cuenta GEE autenticada
- [ ] `src/gee_utils.py` con helpers básicos (init, zonal stats, paletas)
- [ ] Digitalizar lotes demo → `data/lotes/lotes_demo.geojson`

## Fase 1 — Sequía: lluvias (base: guided project "Calculating Rainfall Deviation")
- [ ] Notebook 01: anomalía de precipitación sep-2022→mar-2023 vs. 1981–2021
- [ ] Mapa por partido + tabla ranking de partidos más secos
- [ ] Serie temporal de partido testigo vs. climatología
- [ ] Export de visuales a `assets/`
- 🎯 **Publicable:** mapa "cuánto menos llovió en la campaña 22/23, partido por partido"

## Fase 2 — Sequía: vegetación (base: módulo Change Detection)
- [ ] Notebook 02: z-score NDVI MODIS de la campaña vs. climatología 2000–2021
- [ ] Zoom Sentinel-2 a lotes demo: campaña normal vs. 2022/23, lado a lado
- [ ] Cruce lluvia ↔ NDVI (scatter por partido: la causa y el efecto)
- 🎯 **Publicable:** panel "así se veía la sequía lote por lote" — el contenido con más potencial de viralizar

## Fase 3 — Inundación (base: guided project "Flood Mapping")
- [ ] Notebook 03: mancha de inundación Sentinel-1 de Bahía Blanca (marzo 2025)
- [ ] Hectáreas afectadas por partido + % de superficie agrícola
- [ ] Notebook 04: detección de cambio bitemporal + GIF antes/después
- 🎯 **Publicable:** GIF antes/después de la inundación con hectáreas cuantificadas

## Fase 4 — App Streamlit
- [ ] `app/main.py`: selector de partido + rango de fechas → mapa de anomalía de lluvia/NDVI (geemap/folium embebido)
- [ ] Pestaña de inundación con capas pre/post
- [ ] Deploy en Streamlit Community Cloud (gratis) con service account de GEE
- 🎯 **Publicable:** link a demo interactiva en el README y en LinkedIn

## Fase 5 — Pulido portfolio
- [ ] Completar tabla de resultados del README con los visuales reales
- [ ] Sección de validación: satélite vs. reportes BCR/BCBA/emergencia agropecuaria
- [ ] Posts de LinkedIn según [CONTENIDO-LINKEDIN.md](CONTENIDO-LINKEDIN.md)

## Fuera de alcance (por ahora)
- Monitoreo operativo/automático (crons, alertas en tiempo real)
- Modelos predictivos de rinde — posible proyecto siguiente encadenado a este
- Datos privados de lotes reales de productores

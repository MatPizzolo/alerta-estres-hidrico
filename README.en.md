# Water Stress Alert

[Español](README.md)

**How far a growing season departed from normal in water terms, measured from satellites, district by
district and field by field.**

Water-anomaly analysis over Argentine farmland with Google Earth Engine and Python, in both
directions: deficit (drought) and excess (flooding). All the heavy computation happens server-side in
Earth Engine — season sums, 40-year climatologies, zonal statistics — and only the final per-district
table comes down to Python. The analysis window is not the calendar year but the **summer growing
season (September 1 → March 31)**, which is the cycle the crop actually lives in.

---

## What it measures

| Product | Question it answers | Signal |
|---|---|---|
| **Rainfall deviation** | How much did it rain this season versus normal? | Accumulated precipitation anomaly (mm and %) against a 40-season climatology |
| **Vegetation anomaly** | How did the crop respond? | Per-pixel NDVI z-score against the climatology of the same time of year |
| **Flood mapping** | How much land went under water, and how much of it was farmland? | Sentinel-1 VH backscatter pre/post event, minus permanent water |
| **Change detection** | What changed between any two dates? | Log-ratio for SAR, NDVI difference for optical |

Rainfall is the cause and NDVI is the effect: that is why they go together rather than separately.
Radar is in the mix because during a flood it is cloudy, which is exactly when optical imagery is
useless.

## The two events

**The 2022/23 drought.** Three consecutive La Niña seasons. Soybean ended at 20 Mt, down 54% and the
worst season since 1999 (BCR). This is the deficit case: useful because the event is large and
because there is an administrative ground truth to validate against — the 68 Buenos Aires districts
declared in agricultural emergency by Resolution MEC 587/2023. If the satellite ranking and the
declaration tell the same story, the index works.

**The Bahía Blanca flood, March 7, 2025.** 290 mm in 12 hours, a return period above 100 years
according to the national weather service. This is the excess case, and it comes with a direct
methodological benchmark: INTA AER Bahía Blanca analyzed the same event, with the same sensors and
also in Earth Engine, so the flood extent can be compared instead of published on its own.

The context figures are verified against primary sources in [`docs/DATOS.md`](docs/DATOS.md); none is
quoted from memory.

## How it works

**Season window, not calendar year.** `season_dates()` and `chirps_season_sum()` clip from September
to March. The climatology averages that same window over the seasons starting between 1981 and 2020 —
40 mutually comparable seasons, not 40 straight years.

**Two anomalies, not one.** `anomaly_images()` returns both the absolute one (mm) and the relative one
(%). The relative one is what gets mapped, because a 200 mm deficit does not mean the same thing in
Pergamino as in La Pampa; the absolute one stays in the table so the magnitude is not lost.

**All server-side, one single fetch.** Season sum, climatology and anomalies are computed as Earth
Engine images; `reduceRegions` aggregates by district; only then does `geemap.ee_to_gdf` pull a
`FeatureCollection` down into a GeoDataFrame. There is no `getInfo()` inside a loop, and nominal
scales are explicit in every reduction (`SCALE_CHIRPS = 5566`, `SCALE_MODIS = 250`, `SCALE_S2 = 10`)
rather than relying on defaults.

**Two aggregation scales.** District (FAO GAUL level 2) for the map and the ranking; field (12 demo
polygons digitized over the core crop region, in `data/lotes/lotes_demo.geojson`) for the detail where
MODIS at 250 m already blends parcels and Sentinel-2 is required.

**A fixed palette convention.** Diverging red–white–blue centered at 0 for every anomaly: red is
deficit, blue is excess. It lives in `PALETTES` and is shared across notebooks, so two maps from this
project can be read side by side.

The method's limitations — CHIRPS misses within-field rainfall variability, MODIS blends small fields,
a simple SAR threshold confuses flooding with very wet soil — are stated in
[`docs/METODOLOGIA.md`](docs/METODOLOGIA.md#limitaciones-conocidas).

## Data

All public and free, and all of it lives in the Earth Engine catalog: no rasters are downloaded.

| Dataset | GEE ID | Resolution | Purpose |
|---|---|---|---|
| CHIRPS Pentad | `UCSB-CHG/CHIRPS/PENTAD` | ~5.5 km, 1981– | Precipitation and anomalies |
| MODIS NDVI | `MODIS/061/MOD13Q1` | 250 m, 16-day, 2000– | NDVI climatology and anomaly |
| Sentinel-2 SR Harmonized | `COPERNICUS/S2_SR_HARMONIZED` | 10 m, 2017– | Field-level NDVI |
| Sentinel-1 GRD | `COPERNICUS/S1_GRD` | 10 m, 2014– | Flood mapping (VH band) |
| JRC Global Surface Water | `JRC/GSW1_4/GlobalSurfaceWater` | 30 m | Permanent water mask |
| ESA WorldCover | `ESA/WorldCover/v200` | 10 m | Cropland mask |
| SRTM | `USGS/SRTMGL1_003` | 30 m | Slope mask for the SAR step |
| FAO GAUL level 2 | `FAO/GAUL/2015/level2` | — | District and department boundaries |

Licenses, alternatives (IGN boundaries) and non-satellite validation sources are in
[`docs/DATOS.md`](docs/DATOS.md).

## Layout

```
notebooks/
  01_lluvia_desviacion.ipynb   # per-district precipitation anomaly
src/
  gee_utils.py                 # EE init, dataset IDs, scales, season window,
                               # climatologies, anomalies and zonal statistics
data/
  lotes/lotes_demo.geojson     # 12 illustrative fields in the core crop region (versioned)
docs/
  METODOLOGIA.md               # the four products, metric by metric
  DATOS.md                     # sources, GEE IDs and figures with primary references
  ROADMAP.md                   # phased order of work
```

`data/` is gitignored except for the demo fields: exports and generated tables stay out. Notebooks
save their figures to `assets/`, which is created when you run them.

## Running it

Requires Python 3.11+ and a [Google Earth Engine](https://earthengine.google.com/) account (free for
non-commercial use), already authenticated.

```bash
git clone git@github.com:MatPizzolo/alerta-estres-hidrico.git
cd alerta-estres-hidrico
pip install -r requirements.txt

earthengine authenticate            # once
export EE_PROJECT=your-gee-project  # required: init_ee() fails without it

jupyter lab notebooks/
```

Unlike the other satellite projects in this portfolio, authentication here is interactive and
per-user rather than through a service account: the project runs locally against Earth Engine, with
no deployment and no container. The project id is never hardcoded — `init_ee()` reads it from
`EE_PROJECT` and aborts with an explicit message if it is missing.

## Status

| Part | Status |
|---|---|
| `src/gee_utils.py` | Complete for the rainfall product: init, season window, climatology, anomalies, zonal statistics and monthly series |
| Notebook 01 — rainfall deviation | Written end to end (per-district map, ranking, and a monthly series for Pergamino against its climatology). **No stored outputs** in the repo: you have to run it to see the maps |
| Notebook 02 — NDVI anomaly | Not implemented. Method specified in `docs/METODOLOGIA.md` |
| Notebook 03 — SAR flood mapping | Not implemented |
| Notebook 04 — change detection | Not implemented |
| Interactive app | Not implemented. It sits in the roadmap as a later phase; today the project is notebooks |
| Validation against emergency declarations | Pending: the list of 68 districts has to be transcribed from the resolution, it does not exist as a downloadable dataset |
| Tests | None. The code is a GEE helper library consumed from notebooks |

This is the earliest-stage project in the portfolio: one of four analysis products is finished, plus
the shared infrastructure the other three build on.

## Related documents

- [`docs/METODOLOGIA.md`](docs/METODOLOGIA.md) — the four products, their metrics and limitations
- [`docs/DATOS.md`](docs/DATOS.md) — datasets, GEE IDs and sourced figures
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — order of work
- [`../monitor-cultivos-ndvi/README.md`](../monitor-cultivos-ndvi/README.md) — per-field NDVI across
  several growing seasons, on Sentinel-2

## Origin

Part of the analysis starts from the guided projects of the *Google Earth Engine for Agriculture*
course (rainfall deviation, flood mapping and change detection), rewritten in Python and extended to
real Argentine events with original data work and validation.

"""Shared Google Earth Engine helpers for the water-anomaly project.

Usage from notebooks:

    import sys; sys.path.append("../src")
    import gee_utils as gu
    gu.init_ee()
"""

import os

import ee

# Dataset IDs (see docs/DATOS.md)
CHIRPS_PENTAD = "UCSB-CHG/CHIRPS/PENTAD"
MODIS_NDVI = "MODIS/061/MOD13Q1"
S2_SR = "COPERNICUS/S2_SR_HARMONIZED"
S1_GRD = "COPERNICUS/S1_GRD"
JRC_WATER = "JRC/GSW1_4/GlobalSurfaceWater"
WORLDCOVER = "ESA/WorldCover/v200"
SRTM = "USGS/SRTMGL1_003"
GAUL_L2 = "FAO/GAUL/2015/level2"

# Explicit nominal scales in meters (never rely on defaults in reduceRegion)
SCALE_CHIRPS = 5566
SCALE_MODIS = 250
SCALE_S2 = 10
SCALE_S1 = 10

# Shared palettes: rain/NDVI anomalies use a red-white-blue divergent ramp
# centered at 0; flood water is blue over a gray base (see CLAUDE.md).
PALETTES = {
    "anomaly": ["#b2182b", "#ef8a62", "#fddbc7", "#f7f7f7", "#d1e5f0", "#67a9cf", "#2166ac"],
    "flood": ["#08519c"],
    "base_gray": ["#f0f0f0"],
}

# Crop-season (campaña gruesa) window: September 1 -> March 31.
SEASON_START_MONTH = 9
SEASON_END_MONTH = 3


def init_ee(project: str | None = None) -> None:
    """Initialize Earth Engine with the project from EE_PROJECT (or arg)."""
    project = project or os.environ.get("EE_PROJECT")
    if not project:
        raise RuntimeError(
            "Falta el project-id de GEE: exportá EE_PROJECT antes de correr "
            "(ej. `export EE_PROJECT=mi-proyecto-gee`). No se hardcodea en el repo."
        )
    ee.Initialize(project=project)


def get_partidos(provinces: list[str]) -> ee.FeatureCollection:
    """FAO GAUL level-2 admin units (partidos/departamentos) for Argentine provinces."""
    return (
        ee.FeatureCollection(GAUL_L2)
        .filter(ee.Filter.eq("ADM0_NAME", "Argentina"))
        .filter(ee.Filter.inList("ADM1_NAME", provinces))
    )


def season_dates(start_year: int) -> tuple[ee.Date, ee.Date]:
    """(start, end) of the Sep->Mar campaign that begins in `start_year`."""
    start = ee.Date.fromYMD(start_year, SEASON_START_MONTH, 1)
    end = ee.Date.fromYMD(start_year + 1, SEASON_END_MONTH + 1, 1)
    return start, end


def chirps_season_sum(start_year: int | ee.Number) -> ee.Image:
    """Total precipitation (mm) for one Sep->Mar campaign, as a single image."""
    start_year = ee.Number(start_year)
    start = ee.Date.fromYMD(start_year, SEASON_START_MONTH, 1)
    end = ee.Date.fromYMD(start_year.add(1), SEASON_END_MONTH + 1, 1)
    total = (
        ee.ImageCollection(CHIRPS_PENTAD)
        .filterDate(start, end)
        .select("precipitation")
        .sum()
        .rename("precip_mm")
    )
    return total.set({"campaign_start_year": start_year, "system:time_start": start.millis()})


def chirps_season_climatology(first_year: int, last_year: int) -> ee.Image:
    """Mean campaign precipitation over campaigns starting in [first_year, last_year]."""
    years = ee.List.sequence(first_year, last_year)
    sums = ee.ImageCollection(years.map(chirps_season_sum))
    return sums.mean().rename("precip_mm_mean")


def anomaly_images(season_total: ee.Image, climatology: ee.Image) -> tuple[ee.Image, ee.Image]:
    """(absolute anomaly in mm, relative anomaly in %) vs. the climatology."""
    abs_anom = season_total.subtract(climatology).rename("anom_mm")
    rel_anom = abs_anom.divide(climatology).multiply(100).rename("anom_pct")
    return abs_anom, rel_anom


def zonal_stats(
    image: ee.Image,
    regions: ee.FeatureCollection,
    scale: int,
    reducer: ee.Reducer | None = None,
) -> ee.FeatureCollection:
    """Reduce `image` over each feature (server-side); band names become properties."""
    return image.reduceRegions(
        collection=regions,
        reducer=reducer or ee.Reducer.mean(),
        scale=scale,
    )


def monthly_precip_series(
    geometry: ee.Geometry, start_year: int, months: list[tuple[int, int]] | None = None
) -> ee.FeatureCollection:
    """Monthly CHIRPS totals (mm) over `geometry` for one Sep->Mar campaign.

    Returns one feature per month with properties `year`, `month`, `precip_mm`.
    Server-side: a single getInfo() on the result fetches the whole series.
    """
    if months is None:
        months = [(start_year, m) for m in range(9, 13)] + [
            (start_year + 1, m) for m in range(1, 4)
        ]

    def month_total(pair):
        pair = ee.List(pair)
        year, month = ee.Number(pair.get(0)), ee.Number(pair.get(1))
        start = ee.Date.fromYMD(year, month, 1)
        total = (
            ee.ImageCollection(CHIRPS_PENTAD)
            .filterDate(start, start.advance(1, "month"))
            .select("precipitation")
            .sum()
            .reduceRegion(ee.Reducer.mean(), geometry, SCALE_CHIRPS)
            .get("precipitation")
        )
        return ee.Feature(None, {"year": year, "month": month, "precip_mm": total})

    pairs = ee.List([list(p) for p in months])
    return ee.FeatureCollection(pairs.map(month_total))


def monthly_precip_climatology(
    geometry: ee.Geometry, first_year: int, last_year: int
) -> ee.FeatureCollection:
    """Mean monthly precipitation (mm) over `geometry` for Sep->Mar months,
    averaged across campaigns starting in [first_year, last_year].

    Returns one feature per calendar month with `month`, `precip_mm_mean`.
    """
    campaign_months = [9, 10, 11, 12, 1, 2, 3]

    def month_mean(month):
        month = ee.Number(month)

        def one_year(year):
            year = ee.Number(year)
            # months Jan-Mar belong to the campaign that started the year before
            actual_year = ee.Algorithms.If(month.gte(9), year, year.add(1))
            start = ee.Date.fromYMD(ee.Number(actual_year), month, 1)
            total = (
                ee.ImageCollection(CHIRPS_PENTAD)
                .filterDate(start, start.advance(1, "month"))
                .select("precipitation")
                .sum()
                .reduceRegion(ee.Reducer.mean(), geometry, SCALE_CHIRPS)
                .get("precipitation")
            )
            return total

        totals = ee.List.sequence(first_year, last_year).map(one_year)
        return ee.Feature(
            None,
            {"month": month, "precip_mm_mean": ee.List(totals).reduce(ee.Reducer.mean())},
        )

    return ee.FeatureCollection(ee.List(campaign_months).map(month_mean))

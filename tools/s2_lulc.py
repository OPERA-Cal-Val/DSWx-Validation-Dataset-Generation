import rasterio
from rasterio.crs import CRS
import geopandas as gpd
from shapely.geometry import box
import matplotlib.pyplot as plt
from tqdm import tqdm
from osgeo import gdal
from pathlib import Path
from dem_stitcher.rio_window import read_raster_from_window
from dem_stitcher.rio_tools import reproject_arr_to_new_crs, reproject_arr_to_match_profile
import concurrent.futures
from rasterio.merge import merge
import tempfile
from rasterio.errors import WindowError

S2_TILE_PATHS = Path(__file__).absolute().parents[0] / 's2_class_zones.geojson'
df_zones = gpd.read_file(S2_TILE_PATHS)



def generate_url(zone, year=2021):
    assert(year in list(range(2017, 2022)))
    base_url = 'https://lulctimeseries.blob.core.windows.net/lulctimeseriespublic'
    url = f'{base_url}/lc{year}/{zone}_{year}0101-{year+1}0101.tif'
    return url

def get_s2_urls(extent: list,
                year=2021):
    bbox = box(*extent).buffer(.1)
    ind_inter = df_zones.geometry.intersects(bbox)
    df_subset = df_zones[ind_inter].reset_index(drop=True)

    df_subset['int_area'] = df_subset.geometry.intersection(bbox).area
    df_subset = df_subset.sort_values(by='int_area', ascending=False).reset_index(drop=True)

    df_subset.to_file('subset_test')
    zones = df_subset.zone.unique()
    def generate_url_p(zone):
        return generate_url(zone, year=year)
    urls = list(map(generate_url_p, zones))
    return urls

def localize_one_raster(raster_path: str,
                        extent: list,
                        out_dir) -> Path:

    try:
        X, p = read_raster_from_window(raster_path,
                                    extent,
                                    CRS.from_epsg(4326),
                                    res_buffer=100)
    except WindowError:
        return

    file_name = raster_path.split('/')[-1]
    out_path = Path(f'{out_dir}/{file_name}')

    if 0 not in X.shape:
        X[(X >= 12) | (X <= 0)] = p['nodata']
        with rasterio.open(out_path, 'w', **p) as ds:
            ds.write(X, 1)
        return out_path
    else:
        return

def localize_rasters(paths: list,
                     extent: list,
                     out_dir: Path = Path('tmp')):

    out_dir.mkdir(exist_ok=True)

    def localize_p(path):
        return localize_one_raster(path,
                                   extent,
                                   out_dir)

    out_paths = list(map(localize_p, tqdm(paths, desc='localizing rasters')))
    out_paths = list(filter(lambda path: path is not None, out_paths))
    return out_paths

def get_bbox_geo_area(path):
    with rasterio.open(path) as ds:
        bounds = list(ds.bounds)
    return box(*bounds).area

def order_paths_by_area(paths):
    areas = list(map(get_bbox_geo_area, paths))
    return [p for _, p in sorted(zip(areas, paths), reverse=True)]

def align_one_crs(path, ref_crs):
    with rasterio.open(path) as ds:
        src_profile = ds.profile
        if src_profile['crs'] != ref_crs:
            X = ds.read(1)
        else:
            return path

    X, p = reproject_arr_to_new_crs(X, src_profile, ref_crs)
    X = X[0, ...]

    out_path = path#Path(path.parent + path.stem + '_aligned' + path.suffix)
    breakpoint()
    with rasterio.open(path, 'w', **p) as ds:
        ds.write(X, 1)
    return path

def align_all_crs(paths):
    with rasterio.open(paths[0]) as ds:
        ref_crs = ds.crs
    def align_one_crs_p(path):
        return align_one_crs(path, ref_crs)
    paths = list(map(align_one_crs_p, tqdm(paths)))
    return paths

def merge_tiles(paths):
    with rasterio.open(paths[0]) as ds:
        p = ds.profile
    X, t = merge(paths, nodata=p['nodata'], method='first')
    X = X[0, ...]
    p_merged = p.copy()
    p['width'] = X.shape[1]
    p['height'] = X.shape[0]
    p['transform'] = t
    return X, p


def get_s2_lulc_data(extent: list, year=2021) -> tuple:
    urls = get_s2_urls(extent, year=2021)
    with tempfile.TemporaryDirectory() as out_dir:
        paths = localize_rasters(urls, extent, out_dir=Path(out_dir))
        paths = order_paths_by_area(paths)
        paths_aligned = align_all_crs(paths)
        arr_merged, p_merged = merge_tiles(paths_aligned)
    return arr_merged, p_merged
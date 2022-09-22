from osgeo import gdal
from dem_stitcher.rio_window import read_raster_from_window
from rasterio.warp import transform_bounds
from shapely.geometry import box
from pathlib import Path
import geopandas as gpd
from rasterio.crs import CRS

PECKEL_TILES_PATH = Path(__file__).absolute().parents[0] / 'peckel_tiles.geojson'

def build_peckel_vrt(extent: list,
                     out_path: Path):
    df_peckel_data = gpd.read_file(PECKEL_TILES_PATH)
    bbox = box(*extent)
    ind_inter = df_peckel_data.geometry.intersects(bbox)
    df_subset = df_peckel_data[ind_inter].reset_index(drop=True)
    gdal.BuildVRT(str(out_path), df_subset.source_url.tolist())
    return out_path

def get_peckel_raster(extent:list) -> tuple:
    tmp_vrt = Path('peckel_data_tmp.vrt')
    build_peckel_vrt(extent, tmp_vrt)
    X, p = read_raster_from_window(tmp_vrt,
                                   extent,
                                   CRS.from_epsg(4326))
    tmp_vrt.unlink()
    p['driver'] = 'GTiff'
    return X, p
import geopandas as gpd
import os
import pandas as pd


os.environ["AWS_NO_SIGN_REQUEST"] = "YES"


def get_chip_df() -> gpd.GeoDataFrame:
    df_images = gpd.read_file('s3://opera-calval-database-dswx/image.geojson')
    df_images.dropna(inplace=True)

    df_site = gpd.read_file('s3://opera-calval-database-dswx/site.geojson')
    df_site.dropna(inplace=True)

    cols_to_merge = [col for col in df_images.columns if col != 'geometry']
    df_temp = df_images[cols_to_merge]

    # Currently, one planet image should be associated with a unique site_name.
    # Though not necessarily conversely, this a bijection for the data we are labeling.
    df_chips = pd.merge(df_site, df_temp, on='site_name', how='left')
    return df_chips


def planet2site(planet_id: str) -> str:
    df_chips = get_chip_df()
    df_temp = df_chips[['site_name', 'image_name']]
    df_image2site = df_temp.set_index('image_name')
    values = df_image2site.loc[planet_id].tolist()
    print(f'There was {len(values)} chips associated to this planet_id')
    return values[0]


def site2planet(site_name: str) -> str:
    df_chips = get_chip_df()
    df_temp = df_chips[['site_name', 'image_name']]
    df_image2site = df_temp.set_index('site_name')
    values = df_image2site.loc[site_name].tolist()
    print(f'There was {len(values)} planet images associated to this chip')
    return values[0]


def connect_site_and_planet_ids(input_data: dict) -> dict:
    """
    input_data should look like

    {'planet_id': <planet_id>, 'site_name': ''} or
    {'site_name': <site_name>, 'planet_id': ''}

    Don't specify both otherwise value error. Keys must be exactly as above.
    """

    items = input_data.items()
    items_f = list(filter(lambda x: x[1], items))
    if len(items_f) > 1:
        raise ValueError('Specify a unique keyword value in input_dict, not both')

    keys = [x[0] for x in items]
    if not (set(keys) == set(['planet_id', 'site_name'])):
        raise ValueError('keys need to be "planet_id" and "site_name"')

    key, val = items_f[0]
    if key == 'planet_id':
        return {'planet_id': val,
                'site_name': planet2site(val)}
    else:
        return {'planet_id': site2planet(val),
                'site_name': val}

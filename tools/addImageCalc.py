#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 21:21:49 2022

@author: mbonnema
"""
import geopandas as gpd
import pandas as pd
import boto3
import os
import sys
from datetime import datetime


def addImageCalc(filePaths, metaData, awsSession):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    s3 = awsSession.resource('s3')
    s3_client = awsSession.client('s3')

    print('Creating geojson table')
    s3_keys = []
    for key in filePaths:
        if not os.path.isfile(filePaths[key]):
            sys.exit('File does not exist or path is incorrect: '+filePaths[key])

        s3_key_pending = 'pending/files/'+metaData['image_calc_name']+'/'+filePaths[key].split('/')[-1]
        s3_keys.append(s3_key_pending)
    bucket_name_staging = 'opera-calval-database-dswx-staging'
    metaData['bucket'] = bucket_name_staging
    metaData['s3_keys'] = ','.join(s3_keys)

    metaData['upload_date'] = now

    newRow = pd.DataFrame(metaData, index=[0])
    newRow = gpd.GeoDataFrame(newRow, geometry='geometry')

    print('Uploading geojson table')
    newRow_bytes = bytes(newRow.to_json(drop_id=True).encode('UTF-8'))
    s3object = s3.Object(bucket_name_staging, 'pending/'+now+'_imagecalc.geojson')
    s3object.put(Body=newRow_bytes)

    print('Uploading files')
    for key, s3_key in zip(filePaths, s3_keys):
        response = s3_client.upload_file(filePaths[key],
                                         bucket_name_staging,
                                         s3_key)
    print('staging complete')

    return 'pending/'+now+'_imagecalc.geojson'

# Generating DSWx Datasets

Instuctions TBD

## Setup

An env file should have the following information:

```
PLANET_API_KEY='<API_KEY>'
ES_USERNAME='<JPL USERNAME>'
ES_PASSWORD='<JPL PASSWORD>'
```

<!-- (*Optional*) To your, `~/.aws/credentials` file:

```
[default]
aws_access_key_id = ''
aws_secret_access_key = ''
```

Geopandas expects these fields for sign in. However,  -->

## Install
It is recommended to install `mamba` in the user's base environment to speed up the installation process:

`conda install -c conda-forge mamba`

From this repo:

1. `mamba env create -f environment.yml`
3. `conda activate dswx_val`

## To run

`python run_pipeline.py`

## Known issues

+ The papermill orchestration has the following error `OSError: [Errno 24] Too many open files`.

## Contributing

Create a branch from dev and create a pull request. Have another member review. Make sure to clear your outputs for better version control.

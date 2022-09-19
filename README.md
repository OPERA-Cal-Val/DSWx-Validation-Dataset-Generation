# Generating DSWx Datasets

Instuctions TBD

## Setup

A `.env` file should have the following information:

```
PLANET_API_KEY='<API_KEY>'
ES_USERNAME='<JPL USERNAME>'
ES_PASSWORD='<JPL PASSWORD>'
```

In your `~/.netrc`, place earthdata login credentials:

```
machine urs.earthdata.nasa.gov
    login <username>
    password <password>
```

## Install
It is recommended to install `mamba` in the user's base environment to speed up the installation process:

`conda install -c conda-forge mamba`

From this repo:

1. `mamba env create -f environment.yml`
3. `conda activate dswx_val`

## To run notebook with kernel

After activatating

`python -m ipykernel install --user --name dswx_val`


## Contributing

1. Create a branch from dev and create a pull request.
2. Have another member review.
3. Make sure to clear your outputs for better version control.

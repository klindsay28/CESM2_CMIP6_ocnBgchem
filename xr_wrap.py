"""wrappers to xr functions"""

import xarray as xr

from utils import set_fill_encoding_ds, time_set_mid

def open_dataset_wrap(fname, time_name='time', **kwargs):
    """wrapper to xr.open_dataset"""

    ds = xr.open_dataset(fname, **kwargs)

    set_fill_encoding_ds(ds)

    # reset time values to mid-interval values
    time_set_mid(ds, time_name)
    
    return ds

def open_mfdataset_wrap(fnames, time_name='time', **kwargs):
    """wrapper to xr.open_mfdataset"""

    ds = xr.open_mfdataset(fnames, **kwargs)

    # set variable encodings, needed in multi-file case, because xarray doesn't set them
    # set encoding to that from first file
    if len(fnames) > 0:
        with xr.open_dataset(fnames[0]) as ds_tmp:
            for varname in ds.variables:
                if time_name not in ds[varname].dims or varname == time_name:
                    ds[varname].encoding = ds_tmp[varname].encoding

    set_fill_encoding_ds(ds)

    # reset time values to mid-interval values
    time_set_mid(ds, time_name)
    
    return ds

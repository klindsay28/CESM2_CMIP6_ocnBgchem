"""utility functions"""

import cftime
import numpy as np

def set_fill_encoding_ds(ds):
    """
    call set_fill_encoding_da for each variable in ds
    return ds
    """
    for varname in ds.variables:
        set_fill_encoding_da(ds[varname])
    return ds

def set_fill_encoding_da(da):
    """
    if '_FillValue' and 'missing_value' are both in encoding,
        overwrite 'missing_value' with '_FillValue', to ensure they are consistent
    if '_FillValue' is not in encoding, add it, with value None
        to ensure that xr.to_netcdf doesn't add it to generated file, with NaN value
    return da
    """
    if '_FillValue' in da.encoding:
        if 'missing_value' in da.encoding:
            da.encoding['missing_value'] = da.encoding['_FillValue']
    else:
        da.encoding['_FillValue'] = None
    return da

def dim_cnt_check(ds, varname, dim_cnt):
    """confirm that varname in ds has dim_cnt dimensions"""
    if len(ds[varname].dims) != dim_cnt:
        msg_full = 'unexpected dim_cnt=%d, varname=%s' % (len(ds[varname].dims), varname)
        raise ValueError(msg_full)

def time_set_mid(ds, time_name):
    """
    set ds[time_name] to midpoint of ds[time_name].attrs['bounds'], if bounds attribute exists
    type of ds[time_name] is not changed
    ds is returned
    """

    if 'bounds' not in ds[time_name].attrs:
        return ds

    # determine units and calendar of unencoded time values
    if ds[time_name].dtype == np.dtype('O'):
        units = 'days since 0000-01-01'
        calendar = 'noleap'
    else:
        units = ds[time_name].attrs['units']
        calendar = ds[time_name].attrs['calendar']

    # construct unencoded midpoint values, assumes bounds dim is 2nd
    tb_name = ds[time_name].attrs['bounds']
    if ds[tb_name].dtype == np.dtype('O'):
        tb_vals = cftime.date2num(ds[tb_name].values, units=units, calendar=calendar)
    else:
        tb_vals = ds[tb_name].values
    tb_mid = tb_vals.mean(axis=1)

    # set ds[time_name] to tb_mid
    if ds[time_name].dtype == np.dtype('O'):
        ds[time_name].values = cftime.num2date(tb_mid, units=units, calendar=calendar)
    else:
        ds[time_name].values = tb_mid

    return ds

def time_year_plus_frac(ds, time_name):
    """return time variable, as year plus fraction of year"""

    # this is straightforward if time has units='days since 0000-01-01' and calendar='noleap'
    # so convert specification of time to that representation

    # get time values as an np.ndarray of cftime objects
    if np.dtype(ds[time_name]) == np.dtype('O'):
        tvals_cftime = ds[time_name].values
    else:
        tvals_cftime = cftime.num2date(
            ds[time_name].values, ds[time_name].attrs['units'], ds[time_name].attrs['calendar'])

    # convert cftime objects to representation mentioned above
    tvals_days = cftime.date2num(tvals_cftime, 'days since 0000-01-01', calendar='noleap')

    return tvals_days / 365.0

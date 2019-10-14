"""functions to compute climatologies"""

import esmlab

def compute_clim_mon(ds_in, yr_lo, yr_hi, time_name='time'):
    """compute and return monthly climatology"""

    yyyymmdd_lo = yr_lo + '-01-01'
    yyyymmdd_hi = yr_hi + '-12-31'

    ds_clim = esmlab.climatology(ds_in.sel(time=slice(yyyymmdd_lo, yyyymmdd_hi)), freq='mon')

    # set essential time encoding values from ds_in
    # as esmlab.climatology only sets dtype and _FillValue
    for attr_name in ['units', 'calendar']:
        ds_clim[time_name].encoding[attr_name] = ds_in[time_name].encoding[attr_name]

    # copy global attributes from ds_in
    ds_clim.attrs.update(ds_in.attrs)
    
    return ds_clim
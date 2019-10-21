#!/bin/tcsh -f

foreach varname ( fgco2 mlotst rsntds sos spco2 tos )

  ncea -O ${varname}_Omon_CESM2_historical_r{1,2,3,4,5,6,7,8,9,10,11}i1p1f1_gn_1995-2014_mon_clim.nc \
    ${varname}_ave_Omon_CESM2_historical_rnni1p1f1_gn_1995-2014_mon_clim.nc

  foreach ens ( 1 2 3 4 5 6 7 8 9 10 11 )
    ncdiff -O ${varname}_Omon_CESM2_historical_r${ens}i1p1f1_gn_1995-2014_mon_clim.nc \
      ${varname}_ave_Omon_CESM2_historical_rnni1p1f1_gn_1995-2014_mon_clim.nc \
      ${varname}_anom_Omon_CESM2_historical_r${ens}i1p1f1_gn_1995-2014_mon_clim.nc
  end

  ncea -O -y rmssdn ${varname}_anom_Omon_CESM2_historical_r{1,2,3,4,5,6,7,8,9,10,11}i1p1f1_gn_1995-2014_mon_clim.nc \
    ${varname}_std_Omon_CESM2_historical_rnni1p1f1_gn_1995-2014_mon_clim.nc

end

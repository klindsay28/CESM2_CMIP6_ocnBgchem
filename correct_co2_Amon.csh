#!/bin/tcsh -f

cp -p /glade/collections/cdg/data/CMIP6/CMIP/NCAR/CESM2/esm-hist/r2i1p1f1/Amon/co2/gn/files/d20190802/co2_Amon_CESM2_esm-hist_r2i1p1f1_gn_*.nc .

foreach file ( co2_Amon_CESM2_esm-hist_r2i1p1f1_gn_*.nc )
  ncap2 -O -s "co2=float((28.966/44.0)*co2)" $file $file
end

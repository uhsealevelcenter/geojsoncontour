import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import geojsoncontour
from geojsoncontour.utilities.multipoly import get_contourf_levels

from geojsoncontour.utilities import netcdfhelper as ncd_helper

import xarray

# Reading in new netcdf file that contains both the observation and the forecast
fpath = 'CMEMS_ACCESS_out_20201211.nc'
ncd = nc.Dataset(fpath, 'r')
lon = ncd['lon'][:]
lat = ncd['lat'][:]
time = ncd['time'][:]


##### Subsampling the grid to show only tropical Pacific #####
latbounds = [-50, 50]
lonbounds = [90, 300]
# latitude lower and upper index
latli = np.argmin(np.abs(lat - latbounds[0]))
latui = np.argmin(np.abs(lat - latbounds[1]))

# longitude lower and upper index
lonli = np.argmin(np.abs(lon - lonbounds[0]))
lonui = np.argmin(np.abs(lon - lonbounds[1]))

# ssh = ncd['ssh'][:, :, :]  # sea surface height from CMEMS observation (months 1 to 7) or ACCESS-s1 forecast (months)
# # 8 to 13)
# skill = ncd['skill'][:, :, :]  # the variable is only for the forecast months, 8-13, 1-7 are empty
# trend = ncd['trend'][:]  # Observed trend, static map (not time dependent)

lat = lat[latli:latui]
lon = lon[lonli:lonui]
ssh = ncd['ssh'][:, latli:latui, lonli:lonui]  # sea surface height from CMEMS observation (months 1 to 7) or ACCESS-s1 forecast (months)
# 8 to 13)
skill = ncd['skill'][:, latli:latui, lonli:lonui]  # the variable is only for the forecast months, 8-13, 1-7 are empty
trend = ncd['trend'][latli:latui, lonli:lonui]  # Observed trend, static map (not time dependent)

ncd.close()
n_contours = 17
levels = np.linspace(start=-40, stop=40, num=n_contours)
levels = np.arange(-40, 45, 5)

for num, unix_t in enumerate(time, start=0):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contourf = ax.contourf(lon, lat, ssh[num], levels=levels, cmap=plt.cm.coolwarm, extend='both')
    contourf_trend = ax.contourf(lon, lat, ssh[num] + trend, levels=levels, cmap=plt.cm.coolwarm, extend='both')
    cbar = plt.colorbar(contourf)
    plt.title('Example')
    plt.show()

    geojsonProps = {"time": int(time[num])*1000}
    out_file_name = '-' + str(len(time) - num) + '.geojson'
    out_file_name_trend = '-' + str(len(time) - num) + 'trend.geojson'
    print(int(time[num])*1000)
    # # Convert matplotlib contour to geojson
    geojsoncontour.contourf_to_geojson(
        contourf=contourf,
        geojson_filepath=out_file_name,
        ndigits=1,
        min_angle_deg=7,
        stroke_width=2,
        unit='cm',
        fill_opacity=1.0,
        geojson_properties=geojsonProps
    )
    geojsoncontour.contourf_to_geojson(
        contourf=contourf_trend,
        geojson_filepath=out_file_name_trend,
        ndigits=1,
        min_angle_deg=7,
        stroke_width=2,
        unit='cm',
        fill_opacity=1.0,
        geojson_properties=geojsonProps
    )

n_contours = 2
levels = np.linspace(start=0, stop=1, num=n_contours)
for num, unix_t in enumerate(time, start=0):
    print("NUM: ",num)
    if num > 6:
        figure = plt.figure()
        ax = figure.add_subplot(111)
        contourf_skill = ax.contourf(lon, lat, skill[num], levels=levels, cmap=plt.cm.gray, extend='min')
        cbar = plt.colorbar(contourf_skill)
        plt.title('Skill')
        plt.show()

        geojsonProps = {"time": int(time[num])*1000}
        out_file_name_skill = '-' + str(len(time) - num) + 'skill.geojson'
        print(time[num]*1000, out_file_name_skill)
        # # Convert matplotlib contour to geojson
        geojsoncontour.contourf_to_geojson(
            contourf=contourf_skill,
            geojson_filepath=out_file_name_skill,
            ndigits=1,
            min_angle_deg=10,
            stroke_width=1,
            unit='mm',
            fill_opacity=0.5,
            geojson_properties=geojsonProps,
            cutoff_level=1
        )




















# month = 5
#
# f_path = 'zos_forecast_anomaly_ACCESS-S1_20200927_emn_short.nc'
# ncd = nc.Dataset(f_path, 'r')
# lon = ncd['lon'][:]
# lat = ncd['lat'][:]
# ssh = ncd['zos_no_trend'][month, :, :]
# ssh = ssh / 10  # convert to cm from mm
#
# ncd.close()
#
# #
# n_contours = 11
# levels = np.linspace(start=ssh.min(), stop=ssh.max(), num=n_contours)
# levels = np.linspace(start=-40, stop=40, num=n_contours)

# figure = plt.figure()
# ax = figure.add_subplot(111)
# contourf = ax.contourf(lon, lat, ssh, levels=levels, cmap=plt.cm.coolwarm, extend='both')
# contour = ax.contour(lon, lat, ssh, levels=levels, cmap=plt.cm.coolwarm, extend='both')
# cbar = plt.colorbar(contourf)
# plt.title('Example')
# plt.show()
#
# times = [1601546400000, 1604224800000, 1606816800000, 1609495200000, 1612173600000, 1614592800000]
# geojsonProps = {"time": times[month]}
# out_file_name = str(month) + '.geojson'
# # Convert matplotlib contour to geojson
# geojsoncontour.contourf_to_geojson(
#     contourf=contourf,
#     geojson_filepath=out_file_name,
#     # geojson_filepath='test.geojson',
#     ndigits=1,
#     min_angle_deg=10,
#     stroke_width=2,
#     unit='mm',
#     fill_opacity=0.5,
#     geojson_properties=geojsonProps
# )

# geojsoncontour.contour_to_geojson(
#     contour=contour,
#     # geojson_filepath=out_file_name,
#     geojson_filepath='testC.geojson',
#     ndigits=1,
#     min_angle_deg=5,
#     # stroke_width=2,
#     unit='mm',
#     geojson_properties={"time": '2020-16'}
# )
# import geojson
# gj = geojson.load('0.geojson')
# ncd_helper.netcdf_to_geojson(f_path,'zos_no_trend')
#
# from datetime import datetime
# from datetime import timedelta
#
# epoch = datetime.utcfromtimestamp(0)
#
# fpath = 'cmems_20201007.nc'
# ncd = nc.Dataset(fpath, 'r')
# lon = ncd['lon'][:]
# lat = ncd['lat'][:]
#
# time_origin = datetime(1993, 1, 1)
# # the last seven time stamps in days since 1993-01-01 00:00:00
# days_since_vector = ncd['time_anom'][-7:]
# # time converted to conventional date time
# date_time_vector = []
# for day in days_since_vector:
#     date_time_vector.append(time_origin + timedelta(days=int(day)))
#
#
# def unix_time_millis(dt):
#     return (dt - epoch).total_seconds() * 1000.0
#
#
# # milliseconds since epoch (unix time)
# unix_time = []
# for date in date_time_vector:
#     unix_time.append(int(unix_time_millis(date)))
#
# # the last seven months of altimetry data
# adtma = ncd['absolute_dynamic_topography_monthly_anomaly'][-7:, :, :]
# # sla for the last 7 months
# sla = adtma + ncd['absolute_dynamic_topography_offset'][:, :]
# ncd.close()
#
# for num, unix_t in enumerate(unix_time[:-3], start=0):
#     figure = plt.figure()
#     ax = figure.add_subplot(111)
#     contourf = ax.contourf(lon, lat, sla[num], levels=levels, cmap=plt.cm.coolwarm, extend='both')
#     cbar = plt.colorbar(contourf)
#     plt.title('Example')
#     plt.show()
#
#     geojsonProps = {"time": unix_time[num]}
#     out_file_name = '-' + str(len(unix_time) - num) + '.geojson'
#     # Convert matplotlib contour to geojson
#     geojsoncontour.contourf_to_geojson(
#         contourf=contourf,
#         geojson_filepath=out_file_name,
#         ndigits=1,
#         min_angle_deg=10,
#         stroke_width=2,
#         unit='mm',
#         fill_opacity=0.5,
#         geojson_properties=geojsonProps
#     )



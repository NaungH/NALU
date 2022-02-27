import numpy as np
import xarray as xr
import pandas as pd
import glob


class Trmm:  # create Trmm class to store the data from trmm satellite
    def __init__(self):
        self.nc_file_list = glob.glob('data/data/TRMM 1998-2007/*.nc')  # import all trmm data file
        self.data_all = []  # empty list to store data
        self.trmm_list = []  # empty list to store data

    def get_data(self, lat, lon):  # main function to extract data from raw data file

        for nc_file in self.nc_file_list:  # xarray allow us to extract data from selected location
            nc = xr.open_dataset(nc_file)

            trmm = nc['precipitation'].sel(nlon=[lon], nlat=[lat], method='nearest')

            data = trmm.to_dataframe()

            self.data_all.append(float((data['precipitation'])))

        data_spilt = np.array_split(self.data_all, 10)  # split the 10 years of data into small list

        for data in data_spilt:  # transform the daily average to monthly
            monthly_data = data * 732
            self.trmm_list.append(monthly_data)

        trmm = pd.DataFrame(self.trmm_list)  # transform the data into pandas dataframe for easier manipulation

        t_g = trmm.T  # transform the data into same format

        return t_g


class Aphrodite:  # create Aphrodite class to store the data from Aphrodite satellite
    def __init__(self):
        self.nc_file_list = glob.glob('data/data/NC/*.nc')  # import all Aphrodite data file

    def get_data(self, lat, lon):  # main function to extra data from raw data file

        for nc_file in self.nc_file_list:  # xarray allow us to extra data from selected location
            nc = xr.open_dataset(nc_file)

            latitude = [lat]
            longitude = [lon]

            for i, j in zip(latitude, longitude):
                location_data = nc.sel(latitude=i, longitude=j, method='nearest')

                location_data.to_dataframe().to_csv('{0}.csv'.format(nc_file))  # save the extracted data into csv file

            raw_data_list = glob.glob("data/data/NC/*.csv")
            aphrodite_list = []

            for raw_data in raw_data_list:  # sum up the daily precipitation for each month
                df = pd.read_csv(raw_data)
                date = raw_data.split(".")[1]
                m = 0
                while m <= 11:
                    m += 1
                    if m <= 9:
                        data = (df['time'] >= '{0}-0{1}-01'.format(date, str(m))) & (
                                df['time'] <= '{0}-0{1}-31'.format(date, str(m)))
                        mon = list(df['precip'].loc[data])
                        aphrodite_list.append(np.sum(mon))
                    else:
                        data = (df['time'] >= '{0}-{1}-01'.format(date, str(m))) & (
                                df['time'] <= '{0}-{1}-31'.format(date, str(m)))
                        mon = list(df['precip'].loc[data])
                        aphrodite_list.append(np.sum(mon))

            data_spilt = np.array_split(aphrodite_list, 10)
            aphrodite = pd.DataFrame(data_spilt)

            a_g = aphrodite.T  # transform the data into same format

        return a_g


class Observed:  # create observed class to store the observed data
    def __init__(self):
        self.raw_data = "data/data/Observed Data Monthly.xlsx"
        self.y_in = 1997
        self.observed_list = []
        self.data_list = pd.read_excel(self.raw_data)

    def get_data(self):  # transform observed data from data source into same format

        while self.y_in <= 2006:
            self.y_in += 1
            data = self.data_list[self.y_in].tolist()
            self.observed_list.append(data)

        observed = pd.DataFrame(self.observed_list)

        o_g = observed.T  # transform the data into same format

        return o_g

import numpy as np
import pandas as pd
from sympy import false

from calc_function.dcCalc import dc
from calc_function.dmcCalc import dmc
from calc_function.buiCalc import buiCalc
from calc_function.ISIcalc import ISIcalc
from calc_function.ffmcCalc import ffmcCalc
from calc_function.fwiCalc import fwiCalc
from calc2.fwi import calc_dmc







if __name__ == '__main__':
    data = pd.read_csv("data/data1.csv")
    temp = data['平均气温'].values
    rhs = data['平均相对湿度'].values
    prec = data['降雨量'].values
    ws = data['平均风速'].values
    mon = data['月份'].values.astype(dtype=np.int32)
    # dmc_old = 0.00
    dc_yda = 0
    dmc_yda = 0
    ffmc_yda = 13

    dc_data = np.empty(0)
    dmc_data = np.empty(0)
    ffmc_data = np.empty(0)




    for i in range(len(data)):
        # dmc_old = calc_dmc(temps=temp[i], rhs=rhs[i], rains=prec[i], dmc_olds=dmc_old, month=mon[i])
        dc_yda = dc(dc_yda=dc_yda, temp=temp[i], rh=rhs[i], prec=prec[i],lat=40, mon=mon[i], lat_adjust=True)
        dmc_yda = dmc(dmc_yda=dmc_yda, temp=temp[i], rh=rhs[i], prec=prec[i],lat=40, mon=mon[i], lat_adjust=True)
        # np.append(dc_data, dmc_old)
        dc_data = np.append(dc_data, dc_yda)
        dmc_data = np.append(dmc_data, dmc_yda)

        ffmc_yda = ffmcCalc(ffmc_yda=ffmc_yda, temp=temp[i], rh=rhs[i], ws=ws[i], prec=prec[i])
        ffmc_data = np.append(ffmc_data, ffmc_yda)
    bui = buiCalc(dmc_data, dc_data)
    isi = ISIcalc(ffmc_data, ws=ws)
    fwi = fwiCalc(isi, bui)

    data['fwi'] = fwi
    data.to_csv('fwi_data.csv')
    print(data)
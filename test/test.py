import numpy as np
import pandas as pd
from sympy import false

from calc_function.dcCalc import dc
from calc_function.dmcCalc import dmc
from calc_function.buiCalc import buiCalc
from calc_function.ISIcalc import ISIcalc
from calc_function.ffmcCalc import ffmcCalc
from calc_function.fwiCalc import fwiCalc








if __name__ == '__main__':
    data = pd.read_csv("data/data1.csv")
    temp = data['平均气温']
    rh = data['平均相对湿度']
    prec = data['降雨量']
    mon = data['月份']
    dc_yda = 0
    dc_data = np.zeros(0)

    for i in range(len(data)):
        dc_yda = dc(dc_yda=0, temp=temp, rh=rh, prec=prec, mon=mon, lat_adjust=false)
        np.append(dc_data, dc_yda)
    print(dc_data)
import pandas as pd

from calc_function.dcCalc import dc
from calc_function.dmcCalc import dmc
from calc_function.buiCalc import buiCalc
from calc_function.ISIcalc import ISIcalc
from calc_function.ffmcCalc import ffmcCalc
from calc_function.fwiCalc import fwiCalc








if __name__ == '__main__':
    data = pd.read_csv("data/data1.csv")

    print(data)
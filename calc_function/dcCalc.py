from math import exp, log, sqrt


def dc(dc_yda, temp, rh, prec, lat, mon, lat_adjust=True):
    """
    Drought Code Calculation

    Parameters
    ----------
    dc_yda : float
       The Drought Code from previous iteration
    temp : float
       Temperature (centigrade)
    rh : float
       Relative Humidity (%)
    prec : float
       Precipitation(mm)
    lat : float
       Latitude (decimal degrees)
    mon : {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
       Month
    lat_adjust : bool, default=True
       Latitude adjustment

    Returns
    -------
    float
        Drought Code

    Notes
    -----
    All code is based on a C code library that was written by Canadian
    Forest Service Employees, which was originally based on
    the Fortran code listed in the reference below. All equations
    in this code refer to that document.

    Equations and FORTRAN program for the Canadian Forest Fire
    Weather Index System. 1985. Van Wagner, C.E.; Pickett, T.L.
    Canadian Forestry Service, Petawawa National Forestry
    Institute, Chalk River, Ontario. Forestry Technical Report 33.
    18 p.

    Additional reference on FWI system

    Development and structure of the Canadian Forest Fire Weather
    Index System. 1987. Van Wagner, C.E. Canadian Forestry Service,
    Headquarters, Ottawa. Forestry Technical Report 35. 35 p.
    """
    if dc_yda < 0:
        raise ValueError(f'Invalid dc_yda: {dc_yda}')
    if rh < 0 or rh > 100:
        raise ValueError(f'Invalid rh: {rh}')
    if prec < 0:
        raise ValueError(f'Invalid prec: {prec}')
    if mon < 1 or mon > 12 or not isinstance(mon, int):
        raise ValueError(f'Invalid mon: {mon}')
    # Day length factor for DC Calculations
    # 20N: North of 20 degrees N
    fl01 = [-1.6, -1.6, -1.6, 0.9, 3.8, 5.8, 6.4, 5, 2.4, 0.4, -1.6, -1.6]
    # 20S: South of 20 degrees S
    fl02 = [6.4, 5, 2.4, 0.4, -1.6, -1.6, -1.6, -1.6, -1.6, 0.9, 3.8, 5.8]
    # Near the equator, we just use 1.4 for all months.
    # Constrain temperature
    temp = -2.8 if (temp < 2.8) else temp
    # Eq. 22 - Potential Evapotranspiration
    pe = (0.36 * (temp + 2.8) + fl01[mon - 1]) / 2
    # Daylength factor adjustment by latitude for Potential Evapotranspiration
    if lat_adjust:
        pe = ((0.36 * (temp + 2.8) + fl02[mon - 1]) / 2) if (lat <= -20) else pe
        pe = ((0.36 * (temp + 2.8) + 1.4) / 2) if (-20 < lat <= 20) else pe
    # Cap potential evapotranspiration at 0 for negative winter DC values
    pe = 0 if (pe < 0) else pe
    ra = prec
    # Eq. 18 - Effective Rainfall
    rw = 0.83 * ra - 1.27
    # Eq. 19
    smi = 800 * exp(-1 * dc_yda / 400)
    # Alteration to Eq. 21
    dr0 = dc_yda - 400 * log(1 + 3.937 * rw / smi)
    dr0 = 0 if (dr0 < 0) else dr0
    # if precip is less than 2.8 then use yesterday's DC
    dr = dc_yda if (prec <= 2.8) else dr0
    # Alteration to Eq. 23
    dc1 = dr + pe
    dc1 = 0 if (dc1 < 0) else dc1
    return dc1
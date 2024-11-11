from math import exp, log, sqrt



def dmc(dmc_yda, temp, rh, prec, lat, mon, lat_adjust=True):
    """
    Duff Moisture Code Calculation

    Parameters
    ----------
    dmc_yda : float
       The Duff Moisture Code from previous iteration
    temp : float
       Temperature (centigrade)
    rh : flat
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
        Duff Moisture Code

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
    if dmc_yda < 0:
        raise ValueError(f'Invalid dc_yda: {dmc_yda}')
    if rh < 0 or rh > 100:
        raise ValueError(f'Invalid rh: {rh}')
    if prec < 0:
        raise ValueError(f'Invalid prec: {prec}')
    if mon < 1 or mon > 12 or not isinstance(mon, int):
        raise ValueError(f'Invalid mon: {mon}')
    # Reference latitude for DMC day length adjustment
    # 46N: Canadian standard, latitude >= 30N   (Van Wagner 1987)
    ell01 = [6.5, 7.5, 9, 12.8, 13.9, 13.9, 12.4, 10.9, 9.4, 8, 7, 6]
    # 20N: For 30 > latitude >= 10
    ell02 = [7.9, 8.4, 8.9, 9.5, 9.9, 10.2, 10.1, 9.7, 9.1, 8.6, 8.1, 7.8]
    # 20S: For -10 > latitude >= -30
    ell03 = [10.1, 9.6, 9.1, 8.5, 8.1, 7.8, 7.9, 8.3, 8.9, 9.4, 9.9, 10.2]
    # 40S: For -30 > latitude
    ell04 = [11.5, 10.5, 9.2, 7.9, 6.8, 6.2, 6.5, 7.4, 8.7, 10, 11.2, 11.8]
    # For latitude near the equator, we simple use a factor of 9 for all months
    # constrain low end of temperature
    temp = -1.1 if (temp < 1.1) else temp
    # Eq. 16 - The log drying rate
    rk = 1.894 * (temp + 1.1) * (100 - rh) * ell01[mon - 1] * 1e-04
    # Adjust the day length  and thus the drying r, based on latitude and month
    if lat_adjust:
        rk = (1.894 * (temp + 1.1) * (100 - rh) * ell02[mon - 1] * 1e-04) if (30 >= lat > 10) else rk
        rk = (1.894 * (temp + 1.1) * (100 - rh) * ell03[mon - 1] * 1e-04) if (-10 >= lat > -30) else rk
        rk = (1.894 * (temp + 1.1) * (100 - rh) * ell04[mon - 1] * 1e-04) if (-30 >= lat >= -90) else rk
        rk = (1.894 * (temp + 1.1) * (100 - rh) * 9 * 1e-04) if (10 >= lat > -10) else rk
    # Constrain P
    if prec <= 1.5:
        pr = dmc_yda
    else:
        ra = prec
        # Eq. 11 - Net rain amount
        rw = 0.92 * ra - 1.27
        # Alteration to Eq. 12 to calculate more accurately
        wmi = 20 + 280 / exp(0.023 * dmc_yda)
        # Eqs. 13a, 13b, 13c
        b = (100 / (0.5 + 0.3 * dmc_yda)) if (dmc_yda <= 33) else (
            (14 - 1.3 * log(dmc_yda)) if (dmc_yda <= 65) else
            (6.2 * log(dmc_yda) - 17.2))
        # Eq. 14 - Moisture content after rain
        wmr = wmi + 1000 * rw / (48.77 + b * rw)
        # Alteration to Eq. 15 to calculate more accurately
        pr = 43.43 * (5.6348 - log(wmr - 20))
    pr = 0 if (pr < 0) else pr
    # Calculate final P (DMC)
    dmc1 = pr + rk
    dmc1 = 0 if (dmc1 < 0) else dmc1
    return dmc1
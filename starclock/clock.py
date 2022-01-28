# Clock calculation tools for use in StarClock.
# Generates the local time, universal time, julian date, and LST.

import math
import time

def restrict(value, lower, upper):
    # Restricts value to a circular range between lower and upper
    return (value - (upper - lower) *
            math.floor((value - lower)/(upper - lower)))

def julian_date(utc):
    # Calculate Julian Date (float) from UTC struct_time object 
    year = utc.tm_year
    month = utc.tm_mon
    day = utc.tm_mday
    hour = utc.tm_hour
    minute = utc.tm_min
    second = utc.tm_sec
    
    a = (14 - month) / 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    
    jdn = day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045
    jd = jdn + (hour - 12) / 24.0 + minute / 1440.0 + second / 86400.0
    
    return jd
 
def local_sidereal_time(jd, longitude):
    # Calculate LST from Julian Date and longitude, return as tuple
    jd0 = math.floor(jd - 0.5) + 0.5
    h = 24 * (jd - jd0)
    d = jd - 2451545
    d0 = jd0 - 2451545
    t = d / 36525.0
    
    gmst = 6.697374558 + 0.06570982441908 * d0 + \
           1.00273790935 * h + 0.000026 * t ** 2.0
    gmst = restrict(gmst, 0.0, 24.0)
    
    omega = math.radians(125.04 - 0.052954 * d)
    l = math.radians(280.47 + 0.98565 * d)
    delta_psi = -0.000319 * math.sin(omega) - 0.000024 * math.sin(2 * l)
    epsilon = math.radians(23.4393 - 0.0000004 * d)
    eqeq = delta_psi * math.cos(epsilon)

    gast = gmst + eqeq
    gast = restrict(gast, 0.0, 24.0)
    
    lst = gast + longitude / 15.0
    lst = restrict(lst, 0.0, 24.0)
    
    seconds = int(restrict(round(lst * 3600.0), 0.0, 86400.0))
    hour = seconds / 3600
    minute = (seconds - hour * 3600) / 60
    second = seconds - hour * 3600 - minute * 60
    
    return hour, minute, second

def calc(longitude):
    # Return the full set of clock values as a dictionary
    now = time.time()
    
    lt = time.localtime(now)
    utc = time.gmtime(now)
    jd = julian_date(utc)
    lst = local_sidereal_time(jd, longitude)
    
    lt = time.strftime("%Y-%m-%d %H:%M:%S %Z", lt)
    utc = time.strftime("%Y-%m-%d %H:%M:%S UTC", utc)
    jd = "%.5f JD" % (jd)
    lst = "%02dh %02dm %02ds LST" % (lst)
    
    return {"lt": lt, "utc": utc, "jd": jd, "lst": lst}

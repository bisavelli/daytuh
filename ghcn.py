#!/usr/bin/python3

# Written by Tony Heller of realclimatescience.com
# Please report any errors or issues there

import sys
import datetime
import copy
import pip
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import webbrowser
import matplotlib.image as image
import matplotlib.pyplot as plt
import os.path
from matplotlib.testing.jpl_units import day
from random import *
from matplotlib.dates import *

MONTHS_PER_YEAR = 12
MISSING = "-9999"
MAX_DAYS_IN_MONTH = 31
NUMBER_OF_MONTHS = 12
DAYS_PER_YEAR = 365
UNREASONABLE_HIGH_TEMPERATURE = 55.0
UNREASONABLE_LOW_TEMPERATURE = -60.0
years = []
FIRST_YEAR = 1895
current_time = datetime.datetime.now()
LAST_YEAR = current_time.year
TEMPERATURE_TARGET = 90.0
TEMPERATURE_TARGET_MAX = 90.0
MEAN_WIDTH = 5;
PLOT_TREND = True;
TEMPERATURE_TARGET_MIN = 0.0
TEMPERATURE_TARGET_RANGE = 20.0
TEMPERATURE_TARGET_STEP = 5.0
TEMPERATURE_TARGET_STEP_COUNT = int(TEMPERATURE_TARGET_RANGE / TEMPERATURE_TARGET_STEP) + 1
MONTH_UNDER_TEST = 0
MONTHS_UNDER_TEST = 1
MONTHS_UNDER_TEST_LIST = []
STATE_UNDER_TEST = ""
STATES_UNDER_TEST_LIST = []
STATES_USED_LIST = []
REQUIRED_FIRST_YEAR = 0
REQUIRED_LAST_YEAR = 0
USER_PROVIDED_STRING = ""
DUMP_DAILY_TEMPERATURES_TO_CSV_FILE = False
DONT_PLOT = False
daily_temperature_file_name = "daily_temperatures.csv"
daily_temperature_tmax_fd = -1
daily_temperature_tmin_fd = -1
target_year = 0
target_month = 0
target_day = 0
begin_month = 1
begin_day = 1
end_month = 12
end_day = 31

ALL_USHCN_STATIONS_STRING = "At All US Historical Climatology Network Stations"


class AnnualTemperatureList :
    def __init__(self) :
        self.monthly_temperature_list = []
        self.raw_data_count = 0
        self.fake_data_count = 0
        self.fake_data_total = 0.0
        self.real_data_count = 0
        self.real_data_total = 0.0
        self.annual_average = 0.0
        self.fake_annual_average = 0.0
        self.real_annual_average = 0.0
        for month in range(0, NUMBER_OF_MONTHS) :
            self.monthly_temperature_list.append(UNREASONABLE_LOW_TEMPERATURE)

class Station :
    def __init__(self, COUNTRY="", ID="", LATITUDE=0, LONGITUDE=0, ELEVATION=0, STATE="", NAME="") :
        self.COUNTRY = COUNTRY
        self.ID = ID
        self.LATITUDE = LATITUDE
        self.LONGITUDE = LONGITUDE
        self.ELEVATION = ELEVATION
        self.STATE = STATE
        self.NAME = NAME
        self.first_year = 0
        self.last_year = 0
        self.record_length = 0
        self.first_day_above_max_threshold_map = {}
        self.last_day_above_max_threshold_map = {}
        self.number_of_days_above_max_threshold_map = {}
        self.first_day_below_min_threshold_map = {}
        self.last_day_below_min_threshold_map = {}
        self.number_of_days_below_min_threshold_map = {}

        for year in range(FIRST_YEAR, LAST_YEAR+1) :
            self.number_of_days_above_max_threshold_map[year] = 0
            self.number_of_days_below_min_threshold_map[year] = 0
            self.first_day_below_min_threshold_map[year] = DAYS_PER_YEAR + 1
            self.last_day_below_min_threshold_map[year] = 0

        self.max_monthly_temperature_record = {}
        self.max_yearly_temperature_record = {}
        self.first_day_above_max_threshold_trend = (0.0, 0.0)
        self.last_day_above_max_threshold_trend = (0.0, 0.0)
        self.number_of_days_above_max_threshold_trend = (0.0, 0.0)
        self.max_yearly_temperature_trend = (0.0, 0.0)

        self.raw_max_yearly_temperature_trend = (0.0, 0.0)
        self.final_max_yearly_temperature_trend = (0.0, 0.0)
        self.final_fake_max_yearly_temperature_trend = (0.0, 0.0)
        self.final_real_max_yearly_temperature_trend = (0.0, 0.0)

        self.raw_average_yearly_temperature_trend = (0.0, 0.0)
        self.final_average_yearly_temperature_trend = (0.0, 0.0)
        self.final_fake_average_yearly_temperature_trend = (0.0, 0.0)
        self.final_real_average_yearly_temperature_trend = (0.0, 0.0)

        self.min_monthly_temperature_record = {}
        self.min_yearly_temperature_record = {}
        self.last_day_below_min_threshold_trend = (0.0, 0.0)
        self.first_day_below_min_threshold_trend = (0.0, 0.0)
        self.number_of_days_below_min_threshold_trend = (0.0, 0.0)
        self.min_yearly_temperature_trend = (0.0, 0.0)

        self.ushcn_raw_max_monthly_temperature_record = {}
        self.ushcn_raw_max_yearly_temperature_record = {}
        self.ushcn_tob_max_monthly_temperature_record = {}
        self.ushcn_tob_max_yearly_temperature_record = {}
        self.ushcn_final_max_monthly_temperature_record = {}
        self.ushcn_final_max_yearly_temperature_record = {}
        self.ushcn_raw_average_monthly_temperature_record = {}
        self.ushcn_raw_average_yearly_temperature_record = {}
        self.ushcn_tob_average_monthly_temperature_record = {}
        self.ushcn_tob_average_yearly_temperature_record = {}
        self.ushcn_final_average_monthly_temperature_record = {}
        self.ushcn_final_average_yearly_temperature_record = {}
        self.ushcn_raw_max_temperature_trend = 0.0
        self.ushcn_tob_max_temperature_trend = 0.0
        self.ushcn_final_max_temperature_trend = 0.0
        self.ushcn_raw_average_temperature_trend = 0.0
        self.ushcn_tob_average_temperature_trend = 0.0
        self.ushcn_final_average_temperature_trend = 0.0

        self.target_date_max_temperature = UNREASONABLE_LOW_TEMPERATURE
        self.target_date_min_temperature = UNREASONABLE_LOW_TEMPERATURE
        self.average_first_day_above_max_threshold = 0.0
        self.average_last_day_above_max_threshold = 0.0
        self.average_first_day_below_min_threshold = 0.0
        self.average_last_day_below_min_threshold = 0.0


CO2_map = {
1850:284.7, 1851:284.9, 1852:285, 1853:285.1, 1854:285.3, 1855:285.4, 1856:285.6, 1857:285.7, 1858:285.9, 1859:286.1, 1860:286.2,
1861:286.4, 1862:286.5, 1863:286.6, 1864:286.8, 1865:286.9, 1866:287, 1867:287.1, 1868:287.2, 1869:287.4, 1870:287.5, 1871:287.7,
1872:287.9, 1873:288.1, 1874:288.4, 1875:288.7, 1876:289, 1877:289.4, 1878:289.8, 1879:290.2, 1880:290.7, 1881:291.2, 1882:291.7,
1883:292.1, 1884:292.6, 1885:293, 1886:293.3, 1887:293.6, 1888:293.8, 1889:294, 1890:294.2, 1891:294.3, 1892:294.5, 1893:294.6, 1894:294.7,
1895:294.8, 1896:294.9, 1897:295, 1898:295.2, 1899:295.5, 1900:295.8, 1901:296.1, 1902:296.5, 1903:296.8, 1904:297.2,
1905:297.6, 1906:298.1, 1907:298.5, 1908:298.9, 1909:299.3, 1910:299.7, 1911:300.1, 1912:300.4, 1913:300.8, 1914:301.1,
1915:301.4, 1916:301.7, 1917:302.1, 1918:302.4, 1919:302.7, 1920:303, 1921:303.4, 1922:303.8, 1923:304.1, 1924:304.5,
1925:305, 1926:305.4, 1927:305.8, 1928:306.3, 1929:306.8, 1930:307.2, 1931:307.7, 1932:308.2, 1933:308.6, 1934:309,
1935:309.4, 1936:309.8, 1937:310, 1938:310.2, 1939:310.3, 1940:310.4, 1941:310.4, 1942:310.3, 1943:310.2, 1944:310.1,
1945:310.1, 1946:310.1, 1947:310.2, 1948:310.3, 1949:310.5, 1950:310.7, 1951:311.1, 1952:311.5, 1953:311.9, 1954:312.4,
1955:313, 1956:313.6, 1957:314.2, 1958:314.9, 1959:315.97, 1960:316.91, 1961:317.64, 1962:318.45, 1963:318.99, 1964:319.62,
1965:320.04, 1966:321.38, 1967:322.16, 1968:323.04, 1969:324.62, 1970:325.68, 1971:326.32, 1972:327.45, 1973:329.68, 1974:330.18,
1975:331.08, 1976:332.05, 1977:333.78, 1978:335.41, 1979:336.78, 1980:338.68, 1981:340.1, 1982:341.44, 1983:343.03, 1984:344.58,
1985:346.04, 1986:347.39, 1987:349.16, 1988:351.56, 1989:353.07, 1990:354.35, 1991:355.57, 1992:356.38, 1993:357.07, 1994:358.82,
1995:360.8, 1996:362.59, 1997:363.71, 1998:366.65, 1999:368.33, 2000:369.52, 2001:371.13, 2002:373.22, 2003:375.77, 2004:377.49,
2005:379.8, 2006:381.9, 2007:383.76, 2008:385.59, 2009:387.37, 2010:389.85, 2011:391.63, 2012:393.82, 2013:396.48, 2014:398.61,
2015:400.83, 2016:402, 2017:405, 2018:410
}

ghcn_ushcn_map = {
"USH00015749":"USW00013896",
"USH00018380":"USW00093806",
"USH00042910":"USW00024213",
"USH00043257":"USW00093193",
"USH00046118":"USW00023179",
"USH00047304":"USW00024257",
"USH00083186":"USW00012835",
"USH00084570":"USW00012836",
"USH00086997":"USW00013899",
"USH00097847":"USW00003822",
"USH00105241":"USW00024149",
"USH00105559":"USW00024151",
"USH00140264":"USW00013980",
"USH00150909":"USW00093808",
"USH00160549":"USW00013970",
"USH00165026":"USW00013976",
"USH00166664":"USW00012930",
"USH00176905":"USW00014764",
"USH00205650":"USW00014804",
"USH00215435":"USW00014922",
"USH00216360":"USW00094967",
"USH00242173":"USW00024137",
"USH00243751":"USW00024143",
"USH00244055":"USW00024144",
"USH00245690":"USW00024037",
"USH00260691":"USW00024119",
"USH00262573":"USW00024121",
"USH00266779":"USW00023185",
"USH00269171":"USW00024128",
"USH00280325":"USW00013724",
"USH00291887":"USW00023051",
"USH00297610":"USW00023009",
"USH00300042":"USW00014735",
"USH00301185":"USW00014743",
"USH00305801":"USW00094728",
"USH00307167":"USW00014768",
"USH00308737":"USW00094794",
"USH00311458":"USW00093729",
"USH00313510":"USW00013713",
"USH00326947":"USW00014924",
"USH00340548":"USW00003959",
"USH00344204":"USW00093986",
"USH00350328":"USW00094224",
"USH00350412":"USW00024130",
"USH00356032":"USW00024285",
"USH00356073":"USW00024284",
"USH00360106":"USW00014737",
"USH00362682":"USW00014860",
"USH00369728":"USW00014778",
"USH00370896":"USW00094793",
"USH00376698":"USW00014765",
"USH00381549":"USW00013782",
"USH00396597":"USW00024025",
"USH00398932":"USW00014946",
"USH00412797":"USW00023044",
"USH00423611":"USW00023170",
"USH00425752":"USW00023177",
"USH00429382":"USW00024193",
"USH00446139":"USW00013737",
"USH00457458":"USW00024281",
"USH00457938":"USW00024157",
"USH00465707":"USW00013734"
}

state_map = {
    "AL":"Alabama",
    "AZ":"Arizona",
    "AR":"Arkansas",
    "CA":"California",
    "CO":"Colorado",
    "CT":"Connecticut",
    "DE":"Delaware",
    "FL":"Florida",
    "GA":"Georgia",
    "ID":"Idaho",
    "IL":"Illinois",
    "IN":"Indiana",
    "IA":"Iowa",
    "KS":"Kansas",
    "KY":"Kentucky",
    "LA":"Louisiana",
    "ME":"Maine",
    "MD":"Maryland",
    "MA":"Massachusetts",
    "MI":"Michigan",
    "MN":"Minnesota",
    "MS":"Mississippi",
    "MO":"Missouri",
    "MT":"Montana",
    "NE":"Nebraska",
    "NV":"Nevada",
    "NH":"New Hampshire",
    "NJ":"New Jersey",
    "NM":"New Mexico",
    "NY":"New York",
    "NC":"North Carolina",
    "ND":"North Dakota",
    "OH":"Ohio",
    "OK":"Oklahoma",
    "OR":"Oregon",
    "PA":"Pennsylvania",
    "RI":"Rhode Island",
    "SC":"South Carolina",
    "SD":"South Dakota",
    "TN":"Tennessee",
    "TX":"Texas",
    "UT":"Utah",
    "VT":"Vermont",
    "VA":"Virginia",
    "WA":"Washington",
    "WV":"West Virginia",
    "WI":"Wisconsin",
    "WY":"Wyoming",
}

month_list = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

def stripString(string) :
    stripped_string = title_string.strip().replace(" ", "-").replace(".", "").replace(",", "").replace("\n", "-").replace("/", "-").replace("(", "-").replace(")", "-")
    return stripped_string


NUMBER_OF_DAYS_PER_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def monthName(month) :
    return month_list[month-1]

def leapYear(year) :
    if ( (year % 400) == 0 ) :
        return True
    if ( (year % 100) == 0 ) :
        return False
    if ( (year % 4) == 0 ) :
        return True
    return False

def daysInYear(year) :
    if (leapYear(year)) :
        return 366
    return 365

def dayOfYear(day_target, month_target, year_target) :
    day = 0
    leap_year = leapYear(year_target)
    for month in range(0, month_target) :
        if (month == month_target - 1) :
            day += day_target
            return day
        elif (month_list[month] == "February") :
            if (leap_year == True) :
                day += 29
            else :
                day += 28
        else :
            day += NUMBER_OF_DAYS_PER_MONTH[month]
    # Error condition
    return 0

def daysSinceStartYear(start_year, target_day, target_month, target_year) :
    day_number = 0

    for year in range(start_year, target_year + 1) :
        if (year < target_year) :
            day_number += daysInYear(year)
        else :
            for month in range(1, target_month ) :
                day_number += NUMBER_OF_DAYS_PER_MONTH[month - 1]

            day_number += target_day

    return day_number

def dontUseThisMonth(year, month) :
    if (year < FIRST_YEAR or year > LAST_YEAR) :
        return True
    if (spring == True and (month < 3 or month > 5)) :
        return True
    if (summer == True and (month < 6 or month > 8)) :
        return True
    if (fall == True and (month < 9 or month > 11)) :
        return True
    if (target_month != 0 and target_month != month) :
        return True
    if (begin_month != 0 and month < begin_month) :
        return True
    if (end_month != 0 and month > end_month) :
        return True
    if (MONTH_UNDER_TEST != 0) :
        if (len(MONTHS_UNDER_TEST_LIST) == 0) :
            if (MONTH_UNDER_TEST != month) :
                return True
        else :
            month_found = False
            for month_to_include in MONTHS_UNDER_TEST_LIST :
                if (month == month_to_include) :
                    month_found = True
            if (month_found == False) :
                return True
    return False

target_type = "BOTH"
TMAX = "TMAX"
TMIN = "TMIN"


#Parse the arguments
spring = False
summer = False
fall = False
winter = False
state_arg = ""
use_odd_numbered_stations = False
use_even_numbered_stations = False
use_random_temperature_records = False


for arg in sys.argv :
    if (arg == "help" or len(sys.argv) < 2) :
        print("Usage:\n", "FILENAME or FILELIST", "spring", "summer", "fall", "date=", "date_range=", "target_type=", "target_max=",
              "target_min=", "first_year=", "last_year=", "month=", "months=", "state=", "states=",
              "required_range=", "text=", "USHCN")
        exit()
    if ("spring" in arg) :
        spring = True
        MONTHS_UNDER_TEST_LIST.append(3)
        MONTHS_UNDER_TEST_LIST.append(4)
        MONTHS_UNDER_TEST_LIST.append(5)
        print(arg)

    if ("summer" in arg) :
        summer = True
        MONTHS_UNDER_TEST_LIST.append(6)
        MONTHS_UNDER_TEST_LIST.append(7)
        MONTHS_UNDER_TEST_LIST.append(8)
        print(arg)

    if ("fall" in arg) :
        fall = True
        MONTHS_UNDER_TEST_LIST.append(9)
        MONTHS_UNDER_TEST_LIST.append(10)
        MONTHS_UNDER_TEST_LIST.append(11)
        print(arg)

    if (arg == "odd") :
        use_odd_numbered_stations = True
        print("Using odd numbered stations")
    elif (arg == "even") :
        use_even_numbered_stations = True
        print("Using even numbered stations")
    elif (arg == "random") :
        use_random_temperature_records = True
        print("Using random temperature records")

    if ("date=" in arg) :
        target_date = arg.split("date=")[1]
        target_month = int(target_date[0:2])
        target_day = int(target_date[2:4])
        print(monthName(target_month), target_day)
        if (len(target_date) == 8) :
            target_year = int(target_date[4:8])

    if ("date_range=" in arg) :
        begin_date = arg.split("date_range=")[1].split(":")[0]
        end_date = arg.split("date_range=")[1].split(":")[1]
        begin_month = int(begin_date[0:2])
        begin_day = int(begin_date[2:4])
        end_month = int(end_date[0:2])
        end_day = int(end_date[2:4])
        if (len(begin_date) == 8) :
            FIRST_YEAR = int(begin_date[4:8])
        if (len(end_date) == 8) :
            LAST_YEAR = int(end_date[4:8])
        print("Date range", monthName(begin_month), begin_day, FIRST_YEAR, "to", monthName(end_month), end_day, LAST_YEAR)

    if ("target_type=" in arg) :
        target_type = arg.split("target_type=")[1]

    if ("target_max=" in arg) :
        TEMPERATURE_TARGET_MAX = float(arg.split("target_max=")[1])
        print("Maximum target", TEMPERATURE_TARGET_MAX, "F")

    if ("mean=" in arg) :
        MEAN_WIDTH = int(arg.split("mean=")[1])
        print("Mean width", MEAN_WIDTH)

    if (arg == "no_trend" or arg == "notrend") :
        PLOT_TREND = False
        print("No trend line")

    if ("target_min=" in arg) :
        TEMPERATURE_TARGET_MIN = float(arg.split("target_min=")[1])

    if ("first_year=" in arg) :
        FIRST_YEAR = int(arg.split("first_year=")[1])
        print("First year ", FIRST_YEAR)

    if ("last_year=" in arg) :
        LAST_YEAR = int(arg.split("last_year=")[1])
        print("Last year ", LAST_YEAR)

    if ("month=" in arg) :
        MONTH_UNDER_TEST = int(arg.split("month=")[1])
        MONTHS_UNDER_TEST_LIST.append(MONTH_UNDER_TEST)

    if ("months=" in arg) :
        months = arg.split("months=")[1]
        number_of_months = int(len(months) / 2)
        months_string = ""
        index = 0
        for month in range(0, number_of_months) :
            month_name = months[index:index+2]
            month_number = int(month_name)
            MONTHS_UNDER_TEST_LIST.append(month_number)
            index += 2
        print("Months", MONTHS_UNDER_TEST_LIST)

    if ("state=" in arg) :
        STATE_UNDER_TEST = arg.split("state=")[1]
        state_arg = STATE_UNDER_TEST
        STATES_UNDER_TEST_LIST.append(STATE_UNDER_TEST)
        print(state_map[STATE_UNDER_TEST])

    if ("states=" in arg) :
        states = arg.split("states=")[1]
        state_arg = states
        number_of_states = int(len(states) / 2)
        index = 0
        states_string = ""
        for state in range(0, number_of_states) :
            state_name = states[index:index+2]
            states_string += state_map[state_name] + ", "
            STATES_UNDER_TEST_LIST.append(state_name)
            index += 2
        print(states_string[0:len(states_string)-2])

    if ("required_range=" in arg) :
        REQUIRED_FIRST_YEAR = int(arg.split("required_range=")[1].split(":")[0])
        REQUIRED_LAST_YEAR = int(arg.split("required_range=")[1].split(":")[1])
        print("Stations must include", REQUIRED_FIRST_YEAR, "and", REQUIRED_LAST_YEAR)

    if ("text=" in arg or arg == "USHCN") :
        if (arg != "USHCN") :
            USER_PROVIDED_STRING = arg.split("text=")[1]
        if (USER_PROVIDED_STRING == "USHCN" or arg == "USHCN") :
            USER_PROVIDED_STRING = ALL_USHCN_STATIONS_STRING

    if (arg == "dump_daily") :
        DUMP_DAILY_TEMPERATURES_TO_CSV_FILE = True;

    if (arg == "dont_plot") :
        DONT_PLOT= True;



filename = sys.argv[1]
#print(filename, "\n")

Toto = image.imread('Toto.png')
print("Toto is firing up. It takes some time to process the entire temperature record. Please be patient")

station_map = {}
#US1NMRA0009  36.2217 -106.2380 1815.1 NM ALCALDE 14 NW
fd = open("ghcnd-stations.txt")
for line in fd :
    COUNTRY = line[0:2]
    ID = line[0:11]
    LATITUDE = float(line[12:20])
    LONGITUDE = float(line[21:30])
    ELEVATION = float(line[31:37])
    STATE = line[38:40]
    NAME = line[41:71]

    station = Station(COUNTRY, ID, LATITUDE, LONGITUDE, ELEVATION, STATE, NAME)
    station_map[ID] = station
fd.close()

#ACW00011604  17.1167  -61.7833 TMAX 1949 1949
fd = open("ghcnd-inventory.txt")
for line in fd :
    tokens = line.split()
    record_type = tokens[3]

    if (record_type == "TMAX") :
        station_id = tokens[0]

        if (station_id in station_map) :
            station = station_map[station_id]
            first_year = tokens[4]
            last_year = tokens[5]
            station.first_year = int(first_year)
            station.last_year = int(last_year)
            station.record_length = station.last_year - station.first_year
fd.close()

YEAR = "Year"
MAXIMUM_YEAR = "Maximum Year"
MINIMUM_YEAR = "Mimimum Year"
CO2 = "CO2"
AVERAGE_MAXIMUM_TEMPERATURE = "Average Maximum Temperature"
AVERAGE_MINIMUM_TEMPERATURE = "Average Minimum Temperature"
AVERAGE_MEAN_TEMPERATURE = "Average Mean Temperature"
AVERAGE_DAILY_TEMPERATURE_RANGE = "Average Daily Temperature Range"
AVERAGE_STATION_LATITUDE = "Average Station Latitude"
AVERAGE_STATION_LONGITUDE = "Average Station Longitude"
AVERAGE_STATION_ELEVATION = "Average Station Elevation"
AVERAGE_STATION_RECORD_LENGTH = "Average Station Record Length"
NUMBER_OF_STATIONS = "Number Of Stations"
NUMBER_OF_MONTHLY_MAXIMUM_READINGS = "Number Of Monthly Maximum Readings"
NUMBER_OF_MONTHLY_MINIMUM_READINGS = "Number Of Monthly Minimum Readings"
RATIO_OF_MONTHLY_MAXIMUM_TO_MINIMUM_READINGS = "Monthly Max/Min Readings Ratio"
NUMBER_OF_DAILY_READINGS = "Number Of Daily Readings"
NUMBER_OF_VALID_DAYS_PER_MONTH = "Number Of Valid Days/Month"
PERCENT_MEAN_ABOVE_MAX_TARGET = "Percent Of Days Mean Above " + str(TEMPERATURE_TARGET_MAX) + "F"
PERCENT_TO_REACH_MAX_TARGET = "Percent Of Stations Reaching " + str(TEMPERATURE_TARGET_MAX ) + "F"
PERCENT_ABOVE_MAX_TARGET = "Percent Of Days Above " + str(TEMPERATURE_TARGET_MAX) + "F"
PERCENT_ABOVE_MAX_TARGET = "Percent Of Days Above " + str(TEMPERATURE_TARGET_MAX) + "F"
PERCENT_ABOVE_MAX_TARGET_PLUS_5 = "Percent Of Days Above " + str(TEMPERATURE_TARGET_MAX + 5.0) + "F"
PERCENT_ABOVE_MAX_TARGET_PLUS_10 = "Percent Of Days Above " + str(TEMPERATURE_TARGET_MAX + 10.0) + "F"
PERCENT_ABOVE_MAX_TARGET_PLUS_15 = "Percent Of Days Above " + str(TEMPERATURE_TARGET_MAX + 15.0) + "F"
PERCENT_ABOVE_MAX_TARGET_PLUS_20 = "Percent Of Days Above " + str(TEMPERATURE_TARGET_MAX + 20.0) + "F"
PERCENT_TO_REACH_MIN_TARGET = "Percent Of Stations Reaching " + str(TEMPERATURE_TARGET_MIN ) + "F"
PERCENT_BELOW_MIN_TARGET = "Percent Of Nights Below " + str(TEMPERATURE_TARGET_MIN) + "F"
PERCENT_BELOW_MIN_TARGET_PLUS_5 = "Percent Of Nights Below " + str(TEMPERATURE_TARGET_MIN + 5.0) + "F"
PERCENT_BELOW_MIN_TARGET_PLUS_10 = "Percent Of Nights Below " + str(TEMPERATURE_TARGET_MIN + 10.0) + "F"
PERCENT_BELOW_MIN_TARGET_PLUS_15 = "Percent Of Nights Below " + str(TEMPERATURE_TARGET_MIN + 15.0) + "F"
PERCENT_BELOW_MIN_TARGET_PLUS_20 = "Percent Of Nights Below " + str(TEMPERATURE_TARGET_MIN + 20.0) + "F"
USHCN_RAW_TMAX = "USHCN RAW TMAX"
USHCN_FINAL_TMAX = "USHCN FINAL TMAX"
USHCN_FINAL_MINUS_RAW_TMAX = "USHCN FINAL MINUS RAW TMAX"
USHCN_FINAL_FAKE_TMAX = "USHCN FINAL FAKE TMAX"
USHCN_FINAL_REAL_TMAX = "USHCN FINAL REAL TMAX"
USHCN_FINAL_FAKE_MINUS_REAL_TMAX = "USHCN FINAL FAKE MINUS REAL TMAX"
USHCN_FINAL_PERCENT_FAKE_TMAX = "USHCN FINAL PERCENT FAKE TMAX"
USHCN_FINAL_PERCENT_IGNORED_TMAX = "USHCN FINAL PERCENT IGNORED TMAX"
USHCN_FINAL_COUNT_IGNORED_TMAX = "USHCN FINAL COUNT IGNORED TMAX"
USHCN_RAW_TAVG = "USHCN RAW TAVG"
USHCN_FINAL_TAVG = "USHCN FINAL TAVG"
USHCN_FINAL_MINUS_RAW_TAVG = "USHCN FINAL MINUS RAW TAVG"
USHCN_FINAL_FAKE_TAVG = "USHCN FINAL FAKE TAVG"
USHCN_FINAL_REAL_TAVG = "USHCN FINAL REAL TAVG"
USHCN_FINAL_FAKE_MINUS_REAL_TAVG = "USHCN FINAL FAKE MINUS REAL TAVG"
USHCN_FINAL_PERCENT_FAKE_TAVG = "USHCN FINAL PERCENT FAKE TAVG"
USHCN_FINAL_PERCENT_IGNORED_TAVG = "USHCN FINAL PERCENT IGNORED TAVG"
USHCN_FINAL_COUNT_IGNORED_TAVG = "USHCN FINAL COUNT IGNORED TAVG"
AVERAGE_FIRST_DAY_ABOVE_MAX_THRESHOLD = "Average First Day Above " + str(TEMPERATURE_TARGET_MAX)
AVERAGE_LAST_DAY_ABOVE_MAX_THRESHOLD = "Average Last Day Above " + str(TEMPERATURE_TARGET_MAX)
AVERAGE_LAST_DAY_BELOW_MIN_THRESHOLD = "Average Last Spring Day Below " + str(TEMPERATURE_TARGET_MIN)
AVERAGE_FIRST_DAY_BELOW_MIN_THRESHOLD = "Average First Autumn Day Below " + str(TEMPERATURE_TARGET_MIN)

plot_types_list = [
    YEAR,
    #MAXIMUM_YEAR,
    #MINIMUM_YEAR,
    CO2,
    AVERAGE_MAXIMUM_TEMPERATURE,
    AVERAGE_MINIMUM_TEMPERATURE,
    AVERAGE_MEAN_TEMPERATURE,
    AVERAGE_DAILY_TEMPERATURE_RANGE,
    AVERAGE_FIRST_DAY_ABOVE_MAX_THRESHOLD,
    AVERAGE_LAST_DAY_ABOVE_MAX_THRESHOLD,
    AVERAGE_LAST_DAY_BELOW_MIN_THRESHOLD,
    AVERAGE_FIRST_DAY_BELOW_MIN_THRESHOLD,
    AVERAGE_STATION_LATITUDE,
    AVERAGE_STATION_LONGITUDE,
    AVERAGE_STATION_ELEVATION,
    AVERAGE_STATION_RECORD_LENGTH,
    NUMBER_OF_STATIONS,
    NUMBER_OF_MONTHLY_MAXIMUM_READINGS,
    NUMBER_OF_MONTHLY_MINIMUM_READINGS,
    RATIO_OF_MONTHLY_MAXIMUM_TO_MINIMUM_READINGS,
    NUMBER_OF_DAILY_READINGS,
    NUMBER_OF_VALID_DAYS_PER_MONTH,
#    PERCENT_MEAN_ABOVE_MAX_TARGET,
    PERCENT_TO_REACH_MAX_TARGET,
    PERCENT_ABOVE_MAX_TARGET,
    PERCENT_ABOVE_MAX_TARGET_PLUS_5,
    PERCENT_ABOVE_MAX_TARGET_PLUS_10,
    PERCENT_ABOVE_MAX_TARGET_PLUS_15,
    PERCENT_ABOVE_MAX_TARGET_PLUS_20,
    PERCENT_TO_REACH_MIN_TARGET,
    PERCENT_BELOW_MIN_TARGET,
    PERCENT_BELOW_MIN_TARGET_PLUS_5,
    PERCENT_BELOW_MIN_TARGET_PLUS_10,
    PERCENT_BELOW_MIN_TARGET_PLUS_15,
    PERCENT_BELOW_MIN_TARGET_PLUS_20
    ,USHCN_RAW_TMAX
    ,USHCN_FINAL_TMAX
    ,USHCN_FINAL_MINUS_RAW_TMAX
    ,USHCN_FINAL_REAL_TMAX
    ,USHCN_FINAL_FAKE_TMAX
    ,USHCN_FINAL_FAKE_MINUS_REAL_TMAX
    ,USHCN_FINAL_PERCENT_FAKE_TMAX
    ,USHCN_FINAL_PERCENT_IGNORED_TMAX
    ,USHCN_FINAL_COUNT_IGNORED_TMAX
    ,USHCN_RAW_TAVG
    ,USHCN_FINAL_TAVG
    ,USHCN_FINAL_MINUS_RAW_TAVG
    ,USHCN_FINAL_REAL_TAVG
    ,USHCN_FINAL_FAKE_TAVG
    ,USHCN_FINAL_FAKE_MINUS_REAL_TAVG
    ,USHCN_FINAL_PERCENT_FAKE_TAVG
    ,USHCN_FINAL_PERCENT_IGNORED_TAVG
    ,USHCN_FINAL_COUNT_IGNORED_TAVG
    ,
    ]


def cToF(temperature) :
    return((temperature * 1.8) + 32.0)

def metersToFeet(meters) :
    return(meters * 3.28084)

def printToFile(*args) :
    for arg in args :
        if (type(arg) == str) :
            csv_fd.write(arg)
        else :
            csv_fd.write(str(arg))
    csv_fd.write("\n")

station_list = []
Y_AXIS = ""
X_AXIS = ""

def callingFunctionName(class_name = "") :
    frame =  sys._getframe(2)
    return_string = class_name + ":" + frame.f_code.co_name
    return_string += ":" + frame.f_code.co_filename
    return_string += ":" + str(frame.f_lineno)
    return return_string

def currentFunctionName(class_name = "") :
    frame =  sys._getframe(1)
    #return_string = sys._getframe(2).__class__.__name__
    return_string = class_name + ":" + frame.f_code.co_name
    return_string += ":" + frame.f_code.co_filename
    return_string += ":" + str(frame.f_lineno)
    return return_string

def printException() :
    print(currentFunctionName(), callingFunctionName(), "exception caught", sys.exc_info()[0], sys.exc_info()[1])


def calculateLinearRegression(x, y) :
    xAvg = 0.0
    yAvg = 0.0

    if (len(x) == 0 or len(y) ==0) :
        return (0,0)
    for i in range(0, len(x)) :
        xAvg += x[i]
        yAvg += y[i]

    xAvg = xAvg / len(x)
    yAvg = yAvg / len(y)

    v1 = 0.0
    v2 = 0.0

    for i in range(0, len(x)) :
        v1 += (x[i] - xAvg) * (y[i] - yAvg)
        v2 += pow(x[i] - xAvg, 2)

    if (v2 == 0) :
        return 0,0

    a = v1 / v2
    b = yAvg - (a * xAvg)
    return (a, b)

def calculateLinearRegressionFromMap(temperature_map, regression_type = "") :
    year_list = []
    temperature_list = []
    for year in range(FIRST_YEAR, LAST_YEAR) :
        if (year in temperature_map) :
            year_list.append(year)
            if (regression_type == "generic") :
                temperature_list.append(float(temperature_map[year]))
            elif (regression_type == "") :
                temperature_list.append(temperature_map[year].annual_average)
            elif (regression_type == "fake") :
                temperature_list.append(temperature_map[year].fake_annual_average)
            elif (regression_type == "real") :
                temperature_list.append(temperature_map[year].real_annual_average)
    return calculateLinearRegression(year_list, temperature_list)

def createTitleString() :
    x_axis_string = copy.deepcopy(X_AXIS)
    y_axis_string = copy.deepcopy(Y_AXIS)
    #print(currentFunctionName(), x_axis_string, y_axis_string)
    title_string = ""
    if (len(station_list) == 1) :
        station = station_map[station_list[0].ID]
        title_string += station.NAME.rstrip() + ", " + station.STATE + "  "
    elif (STATE_UNDER_TEST != "" and len(STATES_UNDER_TEST_LIST) < 2) :
        state = state_map[STATE_UNDER_TEST]
        title_string += state + " "
    if (spring == True) :
        title_string += "Spring "
    elif (summer == True) :
        title_string += "Summer "
    elif (fall == True) :
        title_string += "Autumn "
    elif (winter == True) :
        title_string += "Winter "
    elif(len(MONTHS_UNDER_TEST_LIST) != 0) :
        for month in MONTHS_UNDER_TEST_LIST :
            title_string += monthName(month) + " "
    elif (MONTH_UNDER_TEST != 0) :
        if (len(MONTHS_UNDER_TEST_LIST) == 0) :
            title_string += monthName(MONTH_UNDER_TEST) + " "
        else :
            last_month = MONTH_UNDER_TEST + MONTHS_UNDER_TEST - 1
            #print("last_month =", last_month, "MONTH_UNDER_TEST =", MONTH_UNDER_TEST)
            if (MONTH_UNDER_TEST == last_month) :
                title_string += monthName(MONTH_UNDER_TEST) + " "
            else :
                title_string += monthName(MONTH_UNDER_TEST) + "-" + monthName(last_month) + " "
#             print("title_string =", title_string)

    #USHCN temperatures are monthly only
    if (target_day != 0 and "USHCN" not in x_axis_string and "USHCN" not in y_axis_string) :
        title_string += monthName(target_month) + " " + str(target_day) + " "
        if ("Percent Of Days" in x_axis_string) :
            print(currentFunctionName(), "Replacing x_axis_string")
            x_axis_string = x_axis_string.replace("Percent Of Days", "Percent Of Stations")
        if ("Percent Of Days" in y_axis_string) :
            print(currentFunctionName(), "Replacing y_axis_string")
            y_axis_string = y_axis_string.replace("Percent Of Days", "Percent Of Stations")
    elif (target_month != 0 and ("USHCN" in x_axis_string or "USHCN" in y_axis_string)) :
        title_string += monthName(target_month) + " "
    if (begin_month != 1 or begin_day != 1 or end_month != 12 or end_day != 31) :
        if ("USHCN" not in x_axis_string and "USHCN" not in y_axis_string) :
            title_string += monthName(begin_month) + " " + str(begin_day) + " To "
            title_string += monthName(end_month) + " " + str(end_day) + " "
        else :
            title_string += monthName(begin_month) + " To " + monthName(end_month) + " "
    if (x_axis_string != "") :
        title_string += y_axis_string + " Vs. " + x_axis_string
    title_string += " " + str(FIRST_YEAR) + "-" + str(LAST_YEAR)
    if (USER_PROVIDED_STRING != "") :
        title_string += "\n" + USER_PROVIDED_STRING + " "
    elif (len(STATES_UNDER_TEST_LIST) != 0) :
        title_string += "\nAt All "
        for state in STATES_UNDER_TEST_LIST :
            title_string += state + " "
        title_string += "USHCN Stations"
    elif (len(STATES_USED_LIST) != 0 and len(STATES_USED_LIST) != len(state_map)) :
        title_string += "\nAt All "
        for state in STATES_USED_LIST :
            title_string += state + " "
        title_string += "USHCN Stations"
    elif ("USHCN" not in title_string) :
        if (".txt" in filename) :
            title_string += " GHCN " + filename.split(".txt")[0].replace("dly","")
        else :
            title_string += " " + filename
    if (REQUIRED_FIRST_YEAR != 0) :
        title_string += "\nActive In Both " + str(REQUIRED_FIRST_YEAR) + " And " + str(REQUIRED_LAST_YEAR) + " "
    if (use_odd_numbered_stations == True) :
        title_string += "\n" + "Using Only Odd Numbered Stations"
    elif (use_even_numbered_stations == True) :
        title_string += "\n" + "Using Only Even Numbered Stations"
    elif (use_random_temperature_records == True) :
        title_string += "\n" + "Using Randomly Chosen Temperature Records"
        #title_string += "_" + str(TEMPERATURE_TARGET_MAX) + "F"
    #title_string += "\n At All United States Historical Climatology Network Stations"
    title_string += "\n" +  "Red Line Is " + str(MEAN_WIDTH) + " Year Mean "
    print(currentFunctionName(), title_string)
    return title_string

def validMonth(month) :
    if (month == target_month) :
        return True

    if (len(MONTHS_UNDER_TEST_LIST) == 0) :
        if (MONTH_UNDER_TEST == month or MONTH_UNDER_TEST == 0) :
            return True
        else :
            return False
    elif month in MONTHS_UNDER_TEST_LIST :
        return True
    else :
        return False

def makeKMLFileForAboveMaximumThreshold() :
    kml_filename = "above_maximum_threshold_" + str(TEMPERATURE_TARGET_MAX) + "_" + str(target_month) + str(target_day) + str(target_year) + ".kml"
    kml_file = open(kml_filename, "w")
    kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    kml_file.write("<kml xmlns=\"http://earth.google.com/kml/2.2\">\n")
    kml_file.write("\n")
    kml_file.write("<Document>\n")

    kml_file.write("<Style id=\"whiteIcon\">\n")
    kml_file.write(" <IconStyle>\n")
    kml_file.write("  <scale>0.8</scale>\n")
    kml_file.write("  <Icon>\n")
    kml_file.write("   <href>https://realclimatescience.com/wp-content/uploads/2017/08/white-circle-1.png</href>\n")
    kml_file.write("  </Icon>\n")
    kml_file.write(" </IconStyle>\n")
    kml_file.write(" <LabelStyle>\n")
    kml_file.write("   <color>ffccffff</color>\n")
    kml_file.write("   <scale>1.0</scale>\n")
    kml_file.write(" </LabelStyle>\n")
    kml_file.write("</Style>\n")

    kml_file.write("<Style id=\"yellowIcon\">\n")
    kml_file.write(" <IconStyle>\n")
    kml_file.write("  <scale>0.8</scale>\n")
    kml_file.write("  <Icon>\n")
    kml_file.write("   <href>https://realclimatescience.com/wp-content/uploads/2017/08/yellow-circle.png</href>\n")
    kml_file.write("  </Icon>\n")
    kml_file.write(" </IconStyle>\n")
    kml_file.write(" <LabelStyle>\n")
    kml_file.write("   <color>ffccffff</color>\n")
    kml_file.write("   <scale>1.0</scale>\n")
    kml_file.write(" </LabelStyle>\n")
    kml_file.write("</Style>\n")

    kml_file.write("<Style id=\"redIcon\">\n")
    kml_file.write(" <IconStyle>\n")
    kml_file.write("  <scale>1.0</scale>\n")
    kml_file.write("  <Icon>\n")
    kml_file.write("   <href>https://realclimatescience.com/wp-content/uploads/2017/08/red-circle.png</href>\n")
    kml_file.write("  </Icon>\n")
    kml_file.write(" </IconStyle>\n")
    kml_file.write(" <LabelStyle>\n")
    kml_file.write("   <color>ffccccff</color>\n")
    kml_file.write("   <scale>1.2</scale>\n")
    kml_file.write(" </LabelStyle>\n")
    kml_file.write("</Style>\n")

    kml_file.write("<Style id=\"greenIcon\">\n")
    kml_file.write(" <IconStyle>\n")
    kml_file.write("  <scale>0.5</scale>\n")
    kml_file.write("  <Icon>\n")
    kml_file.write("   <href>https://realclimatescience.com/wp-content/uploads/2017/09/green-circle.png</href>\n")
    kml_file.write("  </Icon>\n")
    kml_file.write(" </IconStyle>\n")
    kml_file.write(" <LabelStyle>\n")
    kml_file.write("   <color>ffccccff</color>\n")
    kml_file.write("   <scale>1.2</scale>\n")
    kml_file.write(" </LabelStyle>\n")
    kml_file.write("</Style>\n")

    kml_file.write("<Style id=\"blueIcon\">\n")
    kml_file.write(" <IconStyle>\n")
    kml_file.write("  <scale>0.5</scale>\n")
    kml_file.write("  <Icon>\n")
    kml_file.write("   <href>https://realclimatescience.com/wp-content/uploads/2017/09/blue-circle.png</href>\n")
    kml_file.write("  </Icon>\n")
    kml_file.write(" </IconStyle>\n")
    kml_file.write(" <LabelStyle>\n")
    kml_file.write("   <color>ffccccff</color>\n")
    kml_file.write("   <scale>1.2</scale>\n")
    kml_file.write(" </LabelStyle>\n")
    kml_file.write("</Style>\n")

    kml_file.write("<Style id=\"pinkIcon\">\n")
    kml_file.write(" <IconStyle>\n")
    kml_file.write("  <scale>2.0</scale>\n")
    kml_file.write("  <Icon>\n")
    kml_file.write("   <href>https://realclimatescience.com/wp-content/uploads/2017/08/pink-circle-1.png</href>\n")
    kml_file.write("  </Icon>\n")
    kml_file.write(" </IconStyle>\n")
    kml_file.write(" <LabelStyle>\n")
    kml_file.write("   <color>ffccccff</color>\n")
    kml_file.write("   <scale>1.2</scale>\n")
    kml_file.write(" </LabelStyle>\n")
    kml_file.write("</Style>\n")

    kml_file.write("<Style id=\"orangeIcon\">\n")
    kml_file.write(" <IconStyle>\n")
    kml_file.write("  <scale>0.8</scale>\n")
    kml_file.write("  <Icon>\n")
    kml_file.write("   <href>https://realclimatescience.com/wp-content/uploads/2017/08/orange-circle-1.png</href>\n")
    kml_file.write("  </Icon>\n")
    kml_file.write(" </IconStyle>\n")
    kml_file.write(" <LabelStyle>\n")
    kml_file.write("   <color>ffccccff</color>\n")
    kml_file.write("   <scale>1.2</scale>\n")
    kml_file.write(" </LabelStyle>\n")
    kml_file.write("</Style>\n")

    kml_file.write("<Style id=\"brownIcon\">\n")
    kml_file.write(" <IconStyle>\n")
    kml_file.write("  <scale>1.3</scale>\n")
    kml_file.write("  <Icon>\n")
    kml_file.write("   <href>https://realclimatescience.com/wp-content/uploads/2017/08/brown-circle-1.png</href>\n")
    kml_file.write("  </Icon>\n")
    kml_file.write(" </IconStyle>\n")
    kml_file.write(" <LabelStyle>\n")
    kml_file.write("   <color>ffccccff</color>\n")
    kml_file.write("   <scale>1.2</scale>\n")
    kml_file.write(" </LabelStyle>\n")
    kml_file.write("</Style>\n")

    for station in stations_below_target_minus_20_list :
        station_name = station.NAME[0:20].replace("&", "and")
        kml_file.write("<Placemark id=\""  + station_name + "\">\n")
        kml_file.write("    <name>\n")
        kml_file.write("       " + str(int(round(station.target_date_max_temperature))) + "\n")
        kml_file.write("    </name>\n")
        kml_file.write("<styleUrl>blueIcon</styleUrl>\n")
        kml_file.write("<Point>"+ "\n")
        kml_file.write("    <coordinates>"+ "\n")
        kml_file.write("        " +  str(station.LONGITUDE) + ", " + str(station.LATITUDE) + "\n")
        kml_file.write("    </coordinates>"+ "\n")
        kml_file.write("</Point>"+ "\n")
        kml_file.write("</Placemark>"+ "\n")
        kml_file.write("\n")

    for station in stations_below_target_minus_15_list :
        station_name = station.NAME[0:20].replace("&", "and")
        kml_file.write("<Placemark id=\""  + station_name + "\">\n")
        kml_file.write("    <name>\n")
        kml_file.write("       " + str(int(round(station.target_date_max_temperature))) + "\n")
        kml_file.write("    </name>\n")
        kml_file.write("<styleUrl>blueIcon</styleUrl>\n")
        kml_file.write("<Point>"+ "\n")
        kml_file.write("    <coordinates>"+ "\n")
        kml_file.write("        " +  str(station.LONGITUDE) + ", " + str(station.LATITUDE) + "\n")
        kml_file.write("    </coordinates>"+ "\n")
        kml_file.write("</Point>"+ "\n")
        kml_file.write("</Placemark>"+ "\n")
        kml_file.write("\n")

    for station in stations_below_target_minus_10_list :
        station_name = station.NAME[0:20].replace("&", "and")
        kml_file.write("<Placemark id=\""  + station_name + "\">\n")
        kml_file.write("    <name>\n")
        kml_file.write("       " + str(int(round(station.target_date_max_temperature))) + "\n")
        kml_file.write("    </name>\n")
        kml_file.write("<styleUrl>greenIcon</styleUrl>\n")
        kml_file.write("<Point>"+ "\n")
        kml_file.write("    <coordinates>"+ "\n")
        kml_file.write("        " +  str(station.LONGITUDE) + ", " + str(station.LATITUDE) + "\n")
        kml_file.write("    </coordinates>"+ "\n")
        kml_file.write("</Point>"+ "\n")
        kml_file.write("</Placemark>"+ "\n")
        kml_file.write("\n")

    for station in stations_below_target_minus_5_list :
        station_name = station.NAME[0:20].replace("&", "and")
        kml_file.write("<Placemark id=\""  + station_name + "\">\n")
        kml_file.write("    <name>\n")
        kml_file.write("       " + str(int(round(station.target_date_max_temperature))) + "\n")
        kml_file.write("    </name>\n")
        kml_file.write("<styleUrl>greenIcon</styleUrl>\n")
        kml_file.write("<Point>"+ "\n")
        kml_file.write("    <coordinates>"+ "\n")
        kml_file.write("        " +  str(station.LONGITUDE) + ", " + str(station.LATITUDE) + "\n")
        kml_file.write("    </coordinates>"+ "\n")
        kml_file.write("</Point>"+ "\n")
        kml_file.write("</Placemark>"+ "\n")
        kml_file.write("\n")

    for station in stations_above_target_list :
        station_name = station.NAME[0:20].replace("&", "and")
        kml_file.write("<Placemark id=\""  + station_name + "\">\n")
        kml_file.write("    <name>\n")
        kml_file.write("       " + station_name + " : " + str(int(round(station.target_date_max_temperature))) + "\n")
        kml_file.write("    </name>\n")
        kml_file.write("<styleUrl>yellowIcon</styleUrl>\n")
        kml_file.write("<Point>"+ "\n")
        kml_file.write("    <coordinates>"+ "\n")
        kml_file.write("        " +  str(station.LONGITUDE) + ", " + str(station.LATITUDE) + "\n")
        kml_file.write("    </coordinates>"+ "\n")
        kml_file.write("</Point>"+ "\n")
        kml_file.write("</Placemark>"+ "\n")
        kml_file.write("\n")

    for station in stations_above_target_plus_5_list :
        station_name = station.NAME[0:20].replace("&", "and")
        kml_file.write("<Placemark id=\""  + station_name + "\">\n")
        kml_file.write("    <name>\n")
        kml_file.write("       " + station_name + " : " + str(int(round(station.target_date_max_temperature))) + "\n")
        kml_file.write("    </name>\n")
        kml_file.write("<styleUrl>#yellowIcon</styleUrl>\n")
        kml_file.write("<Point>"+ "\n")
        kml_file.write("    <coordinates>"+ "\n")
        kml_file.write("        " +  str(station.LONGITUDE) + ", " + str(station.LATITUDE) + "\n")
        kml_file.write("    </coordinates>"+ "\n")
        kml_file.write("</Point>"+ "\n")
        kml_file.write("</Placemark>"+ "\n")
        kml_file.write("\n")

    for station in stations_above_target_plus_10_list :
        station_name = station.NAME[0:20].replace("&", "and")
        kml_file.write("<Placemark id=\""  + station_name + "\">\n")
        kml_file.write("    <name>\n")
        kml_file.write("       " + station_name + " : " + str(int(round(station.target_date_max_temperature))) + "\n")
        kml_file.write("    </name>\n")
        kml_file.write("<styleUrl>#redIcon</styleUrl>\n")
        kml_file.write("<Point>"+ "\n")
        kml_file.write("    <coordinates>"+ "\n")
        kml_file.write("        " +  str(station.LONGITUDE) + ", " + str(station.LATITUDE) + "\n")
        kml_file.write("    </coordinates>"+ "\n")
        kml_file.write("</Point>"+ "\n")
        kml_file.write("</Placemark>"+ "\n")
        kml_file.write("\n")

    for station in stations_above_target_plus_15_list :
        station_name = station.NAME[0:20].replace("&", "and")
        kml_file.write("<Placemark id=\""  + station_name + "\">\n")
        kml_file.write("    <name>\n")
        kml_file.write("       " + station_name + " : " + str(int(round(station.target_date_max_temperature))) + "\n")
        kml_file.write("    </name>\n")
        kml_file.write("<styleUrl>#redIcon</styleUrl>\n")
        kml_file.write("<Point>"+ "\n")
        kml_file.write("    <coordinates>"+ "\n")
        kml_file.write("        " +  str(station.LONGITUDE) + ", " + str(station.LATITUDE) + "\n")
        kml_file.write("    </coordinates>"+ "\n")
        kml_file.write("</Point>"+ "\n")
        kml_file.write("</Placemark>"+ "\n")
        kml_file.write("\n")

    for station in stations_above_target_plus_20_list :
        station_name = station.NAME[0:20].replace("&", "and")
        kml_file.write("<Placemark id=\""  + station_name + "\">\n")
        kml_file.write("    <name>\n")
        kml_file.write("       " + station_name + " : " + str(int(round(station.target_date_max_temperature))) + "\n")
        kml_file.write("    </name>\n")
        kml_file.write("<styleUrl>#pinkIcon</styleUrl>\n")
        kml_file.write("<Point>"+ "\n")
        kml_file.write("    <coordinates>"+ "\n")
        kml_file.write("        " +  str(station.LONGITUDE) + ", " + str(station.LATITUDE) + "\n")
        kml_file.write("    </coordinates>"+ "\n")
        kml_file.write("</Point>"+ "\n")
        kml_file.write("</Placemark>"+ "\n")
        kml_file.write("\n")

    kml_file.write("</Document>\n")
    kml_file.write("</kml>\n")
    kml_file.close()
    os.chmod(kml_filename, 0o777)

def makeKMLFileForStationsUsed() :
    kml_filename = "stations_used_" + str(target_month) + str(target_day) + str(target_year) + ".kml"
    kml_file = open(kml_filename, "w")
    kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    kml_file.write("<kml xmlns=\"http://earth.google.com/kml/2.2\">\n")
    kml_file.write("\n")
    kml_file.write("<Document>\n")

    kml_file.write("<Style id=\"greenIcon\">\n")
    kml_file.write(" <IconStyle>\n")
    kml_file.write("  <scale>0.5</scale>\n")
    kml_file.write("  <Icon>\n")
    kml_file.write("   <href>https://realclimatescience.com/wp-content/uploads/2017/09/green-circle.png</href>\n")
    kml_file.write("  </Icon>\n")
    kml_file.write(" </IconStyle>\n")
    kml_file.write(" <LabelStyle>\n")
    kml_file.write("   <color>ffccccff</color>\n")
    kml_file.write("   <scale>1.2</scale>\n")
    kml_file.write(" </LabelStyle>\n")
    kml_file.write("</Style>\n")

    for station in station_list :
        station_name = station.NAME[0:20].replace("&", "and")
        kml_file.write("<Placemark id=\""  + station_name + "\">\n")
        kml_file.write("    <name>\n")
        kml_file.write("       " + station_name + "\n")
        kml_file.write("    </name>\n")
        kml_file.write("<styleUrl>greenIcon</styleUrl>\n")
        kml_file.write("<Point>"+ "\n")
        kml_file.write("    <coordinates>"+ "\n")
        kml_file.write("        " +  str(station.LONGITUDE) + ", " + str(station.LATITUDE) + "\n")
        kml_file.write("    </coordinates>"+ "\n")
        kml_file.write("</Point>"+ "\n")
        kml_file.write("</Placemark>"+ "\n")
        kml_file.write("\n")

    kml_file.write("</Document>\n")
    kml_file.write("</kml>\n")
    kml_file.close()
    os.chmod(kml_filename, 0o777)

title_string = createTitleString()
file_name_string = title_string.strip().replace(" ", "-").replace(".", "").replace(",", "").replace("\n", "-").replace("/", "-")
if (target_year != 0 and target_month != 0 and target_day != 0) :
    file_name_string += "_" + str(target_year) + str(target_month) + str(target_day)

csv_filename = file_name_string + ".csv"
try :
    csv_fd = open(csv_filename, "w")
except :
    csv_filename = file_name_string + str(current_time).split()[0] + ".csv"
    csv_fd = open(file_name_string, "w")
printToFile(sys.argv)


data_dict = {}
data_dict[YEAR] = []
data_dict[MAXIMUM_YEAR] = []
data_dict[MINIMUM_YEAR] = []
data_dict[CO2] = []
data_dict[AVERAGE_MAXIMUM_TEMPERATURE] = []
data_dict[AVERAGE_MINIMUM_TEMPERATURE] = []
data_dict[AVERAGE_DAILY_TEMPERATURE_RANGE] = []
data_dict[AVERAGE_FIRST_DAY_ABOVE_MAX_THRESHOLD] = []
data_dict[AVERAGE_LAST_DAY_ABOVE_MAX_THRESHOLD] = []
data_dict[AVERAGE_LAST_DAY_BELOW_MIN_THRESHOLD] = []
data_dict[AVERAGE_FIRST_DAY_BELOW_MIN_THRESHOLD] = []
data_dict[AVERAGE_MEAN_TEMPERATURE] = []
data_dict[AVERAGE_STATION_LATITUDE] = []
data_dict[AVERAGE_STATION_LONGITUDE] = []
data_dict[AVERAGE_STATION_ELEVATION] = []
data_dict[AVERAGE_STATION_RECORD_LENGTH] = []
data_dict[NUMBER_OF_STATIONS] = []
data_dict[NUMBER_OF_MONTHLY_MAXIMUM_READINGS] = []
data_dict[NUMBER_OF_MONTHLY_MINIMUM_READINGS] = []
data_dict[RATIO_OF_MONTHLY_MAXIMUM_TO_MINIMUM_READINGS] = []
data_dict[NUMBER_OF_DAILY_READINGS] = []
data_dict[NUMBER_OF_VALID_DAYS_PER_MONTH] = []
data_dict[PERCENT_MEAN_ABOVE_MAX_TARGET] = []
data_dict[PERCENT_TO_REACH_MAX_TARGET] = []
data_dict[PERCENT_ABOVE_MAX_TARGET] = []
data_dict[PERCENT_ABOVE_MAX_TARGET_PLUS_5] = []
data_dict[PERCENT_ABOVE_MAX_TARGET_PLUS_10] = []
data_dict[PERCENT_ABOVE_MAX_TARGET_PLUS_15] = []
data_dict[PERCENT_ABOVE_MAX_TARGET_PLUS_20] = []
data_dict[PERCENT_TO_REACH_MIN_TARGET] = []
data_dict[PERCENT_BELOW_MIN_TARGET] = []
data_dict[PERCENT_BELOW_MIN_TARGET_PLUS_5] = []
data_dict[PERCENT_BELOW_MIN_TARGET_PLUS_10] = []
data_dict[PERCENT_BELOW_MIN_TARGET_PLUS_15] = []
data_dict[PERCENT_BELOW_MIN_TARGET_PLUS_20] = []
data_dict[USHCN_RAW_TMAX] = []
data_dict[USHCN_FINAL_TMAX] = []
data_dict[USHCN_FINAL_MINUS_RAW_TMAX] = []
data_dict[USHCN_FINAL_FAKE_TMAX] = []
data_dict[USHCN_FINAL_REAL_TMAX] = []
data_dict[USHCN_FINAL_FAKE_MINUS_REAL_TMAX] = []
data_dict[USHCN_FINAL_PERCENT_FAKE_TMAX] = []
data_dict[USHCN_FINAL_PERCENT_IGNORED_TMAX] = []
data_dict[USHCN_FINAL_COUNT_IGNORED_TMAX] = []
data_dict[USHCN_RAW_TAVG] = []
data_dict[USHCN_FINAL_TAVG] = []
data_dict[USHCN_FINAL_MINUS_RAW_TAVG] = []
data_dict[USHCN_FINAL_FAKE_TAVG] = []
data_dict[USHCN_FINAL_REAL_TAVG] = []
data_dict[USHCN_FINAL_FAKE_MINUS_REAL_TAVG] = []
data_dict[USHCN_FINAL_PERCENT_FAKE_TAVG] = []
data_dict[USHCN_FINAL_PERCENT_IGNORED_TAVG] = []
data_dict[USHCN_FINAL_COUNT_IGNORED_TAVG] = []

stations_used_map = {}
stations_used_name_map = {}

for year in range(FIRST_YEAR, LAST_YEAR + 1) :
    data_dict[USHCN_RAW_TMAX].append(0.0)
    data_dict[USHCN_FINAL_TMAX].append(0.0)
    data_dict[USHCN_FINAL_MINUS_RAW_TMAX].append(0.0)
    data_dict[USHCN_FINAL_REAL_TMAX].append(0.0)
    data_dict[USHCN_FINAL_FAKE_TMAX].append(0.0)
    data_dict[USHCN_FINAL_FAKE_MINUS_REAL_TMAX].append(0.0)
    data_dict[USHCN_FINAL_PERCENT_FAKE_TMAX].append(0.0)
    data_dict[USHCN_FINAL_PERCENT_IGNORED_TMAX].append(0.0)
    data_dict[USHCN_FINAL_COUNT_IGNORED_TMAX].append(0.0)
    data_dict[USHCN_RAW_TAVG].append(0.0)
    data_dict[USHCN_FINAL_TAVG].append(0.0)
    data_dict[USHCN_FINAL_MINUS_RAW_TAVG].append(0.0)
    data_dict[USHCN_FINAL_REAL_TAVG].append(0.0)
    data_dict[USHCN_FINAL_FAKE_TAVG].append(0.0)
    data_dict[USHCN_FINAL_FAKE_MINUS_REAL_TAVG].append(0.0)
    data_dict[USHCN_FINAL_PERCENT_FAKE_TAVG].append(0.0)
    data_dict[USHCN_FINAL_PERCENT_IGNORED_TAVG].append(0.0)
    data_dict[USHCN_FINAL_COUNT_IGNORED_TAVG].append(0.0)

if (target_type == "TMAX" or target_type == "TMIN") :
    target_list = [target_type]
else :
    target_list = ["TMAX", "TMIN"]

if (DUMP_DAILY_TEMPERATURES_TO_CSV_FILE) :
    daily_temperature_tmax_fd = open(stripString(createTitleString()) + "_daily_tmax" + ".csv", "w")
    daily_temperature_tmin_fd = open(stripString(createTitleString()) + "_daily_tmin" + ".csv", "w")

for target_type_under_test in target_list :
    print(currentFunctionName(), "Target =", target_type)
    printToFile(target_type_under_test)

    if (target_type_under_test == "TMAX") :
        TEMPERATURE_TARGET = TEMPERATURE_TARGET_MAX
    elif (target_type_under_test == "TMIN") :
        TEMPERATURE_TARGET = TEMPERATURE_TARGET_MIN

    if (target_month != 0) :
        printToFile("Date =", target_month, "/", target_day)

    monthly_station_average_temperature_total_dict = {}
    monthly_station_count_array = {}
    daily_station_count_array = {}
    #monthly_temperature_total = {}
    monthly_days_above_target_year_dict = {}
    station_dict = {}
    station_list = []
    maximum_target_list = []
    target = TEMPERATURE_TARGET
    while (target <= TEMPERATURE_TARGET + TEMPERATURE_TARGET_RANGE) :
        maximum_target_list.append(target)
        target += TEMPERATURE_TARGET_STEP

    month_zero_list = []
    for month in range(0, NUMBER_OF_MONTHS) :
        month_zero_list.append(0.0)

    stations_not_above_target_list = []
    stations_below_target_minus_20_list = []
    stations_below_target_minus_15_list = []
    stations_below_target_minus_10_list = []
    stations_below_target_minus_5_list = []
    stations_above_target_list = []
    stations_above_target_plus_5_list = []
    stations_above_target_plus_10_list = []
    stations_above_target_plus_15_list = []
    stations_above_target_plus_20_list = []

    monthly_mean_days_above_target = {}
    monthly_days_above_target = {}
    monthly_days_above_target_plus_5F = {}
    monthly_days_above_target_plus_10F = {}
    monthly_days_above_target_plus_15F = {}
    monthly_days_above_target_plus_20F = {}


    #Initializations
    for year in range(FIRST_YEAR, LAST_YEAR+1) :
        monthly_station_average_temperature_total_dict[year] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        monthly_station_count_array[year] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        daily_station_count_array[year] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        #monthly_temperature_total[year] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        #monthly_days_above_target_dict = {}
        #target = TEMPERATURE_TARGET
        #for target_index in range(0, TEMPERATURE_TARGET_STEP_COUNT) :
        #    monthly_days_above_target = []
        #    monthly_days_above_target = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        #    monthly_days_above_target_dict[target] = monthly_days_above_target
        #    target += TEMPERATURE_TARGET_STEP
        #monthly_days_above_target_year_dict[year] = monthly_days_above_target_dict
        monthly_mean_days_above_target[year] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        monthly_days_above_target[year] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        monthly_days_above_target_plus_5F[year] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        monthly_days_above_target_plus_10F[year] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        monthly_days_above_target_plus_15F[year] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        monthly_days_above_target_plus_20F[year] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0]
        station_dict[year] = {}

    current_station = 0
    year = 0
    previous_year = 0

    station_file_list = []
    try :
        fd = open(filename)
    except :
        print("Failed to open file:", "\"", filename, "\"", "did you provide the correct filename?")
        exit()
    line = fd.readline().rstrip()
    if (".dly" in line) :
        if (line[0] != "#") :
            print(currentFunctionName(), line.rstrip())
            station_file_list.append(line[0:15].rstrip())
        for line in fd :
            if (line[0] != "#") :
                print(currentFunctionName(), line.rstrip())
                station_file_list.append(line[0:15].rstrip())
    else :
        station_file_list.append(filename)
    fd.close()

    #print(station_file_list)
    for station_file in station_file_list :
        try :
            print(currentFunctionName(), target_type_under_test, station_file)
            fd = open(station_file)
        except :
            print(currentFunctionName(), "bad station_file =", station_file)
            continue
            #exit()

        dont_use_this_station = False
        for line in fd :
            if (dont_use_this_station) :
                break

            if (target_type_under_test in line) :
                #Each line in the file represents one monthly record
                record_parts = line.split(target_type_under_test)[0:17]
                station_info = record_parts[0]
                station_id = station_info[0:11]
                country = station_info[0:2]
                year = int(station_info[11:15])
                month = int(station_info[15:17])

                try :
                    if (current_station != station_map[station_id]) :
                        # Found a new station
                        # Assumes all records from the same station are contiguous in the file being read
                        current_station = station_map[station_id]
                        station_list.append(current_station)

                        if (DUMP_DAILY_TEMPERATURES_TO_CSV_FILE):
                            if (len(STATES_UNDER_TEST_LIST) == 0 or current_station.STATE in STATES_UNDER_TEST_LIST):
                                write_string = target_type_under_test + "," + current_station.NAME + ","
                                write_string += current_station.STATE + "," + current_station.ID + "\n"

                                if (target_type_under_test == "TMAX") :
                                    daily_temperature_tmax_fd.write(write_string)
                                elif (target_type_under_test == "TMIN"):
                                     daily_temperature_tmin_fd.write(write_string)
                    elif (current_station == 0) :
                        current_station = station_map[station_id]
                        station_list.append(current_station)
                    dont_use_this_station = False
                except :
                    dont_use_this_station = True
                    print(currentFunctionName(), "Skipping", station_id, "because it wasn't in the map")
                    continue

                try :
                    last_digit = int(station_id[10])
                    if (last_digit % 2 == 0 and use_odd_numbered_stations == True) :
                        print(currentFunctionName(), "Rejecting", station_id, "because it is even numbered")
                        dont_use_this_station = True
                    elif (last_digit % 2 == 1 and use_even_numbered_stations == True) :
                        print(currentFunctionName(), "Rejecting", station_id, "because it is odd numbered")
                        dont_use_this_station = True
                    elif (use_random_temperature_records and random() % 2 == 1) :
                        print(currentFunctionName(), "Rejecting", station_id, "randomly")
                except :
                    dont_use_this_station = True
                    print(currentFunctionName(), "Skipping", station_id, "because of unrecognized naming convention")
                    continue

                if (year < FIRST_YEAR or year > LAST_YEAR) :
                    continue
                if (spring == True and (month < 3 or month > 5)) :
                    continue
                if (summer == True and (month < 6 or month > 8)) :
                    continue
                if (fall == True and (month < 9 or month > 11)) :
                    continue
                if (target_month != 0 and target_month != month) :
                    continue
                if (MONTH_UNDER_TEST != 0) :
                    if (len(MONTHS_UNDER_TEST_LIST) == 0) :
                        if (MONTH_UNDER_TEST != month) :
                            continue
                    else :
                        month_found = False
                        for month_to_include in MONTHS_UNDER_TEST_LIST :
                            if (month == month_to_include) :
                                month_found = True
                        if (month_found == False) :
                            continue

                if (validMonth(month) == False) :
                    continue

                if (len(STATES_UNDER_TEST_LIST) != 0 and current_station.STATE not in STATES_UNDER_TEST_LIST) :
                    dont_use_this_station = True
                else :
                    if (current_station.STATE not in STATES_USED_LIST) :
                        STATES_USED_LIST.append(current_station.STATE);

                    stations_used_map[current_station.ID] = current_station
                    stations_used_name_map[current_station.ID] = True

                if (REQUIRED_FIRST_YEAR != 0 and current_station.first_year > REQUIRED_FIRST_YEAR) :
                    dont_use_this_station = True
                if (REQUIRED_LAST_YEAR != 0 and current_station.last_year < REQUIRED_LAST_YEAR) :
                    dont_use_this_station = True

                if (dont_use_this_station == True) :
                    if (current_station in station_list) :
                        station_list.remove(current_station)
                        print(currentFunctionName(), "Removing", current_station.NAME, current_station.STATE, current_station.first_year, current_station.last_year)
                    continue

                try :
                    year_index = years.index(year)
                except :
                    do_nothing = 0
                else :
                    years.append(year)

                previous_year = year


                #print(station_map[station_id].NAME, station_map[station_id].STATE)
                station_dict[year][station_id] = station_id
                daily_data_string = record_parts[1].rstrip()
                #print(daily_data_string)
                daily_data_list = []
                index = 0
                while (index < len(daily_data_string)) :
                    temperature_string = daily_data_string[index:index+5]
                    #print(temperature_string)
                    daily_data_list.append(temperature_string)
                    index += 8
                #print("")
                daily_temperatures = []
                station_monthly_total = 0.0
                station_monthly_day_count = 0
                #print(data_info)

                # Sum up the temperatures at that station for the month
                day = 0

                for index in range(0, len(daily_data_list)) :
                    day += 1
                    #print(currentFunctionName(), "Day of year", day_of_year)
                    if (target_day != 0 and target_day != day) :
                        continue
                    if (month < begin_month or month > end_month) :
                        continue
                    elif (month == begin_month and day < begin_day) :
                        continue
                    elif (month == end_month and day > end_day) :
                        continue

                    day_of_year = dayOfYear(day, month, year)

                    temperature = daily_data_list[index]
                    if (temperature != MISSING) :
                        #print(temperature)
                        try :
                            float_temperature = float(temperature) / 10.0
                        except :
                            do_nothing = 0
                        else :
                            if (float_temperature > UNREASONABLE_LOW_TEMPERATURE and float_temperature < UNREASONABLE_HIGH_TEMPERATURE ) :
                                #daily_temperatures.append(float_temperature)
                                if (DUMP_DAILY_TEMPERATURES_TO_CSV_FILE) :
                                    date = year + ((day_of_year - 1) / daysInYear(year))
                                    # write_string = monthName(month) + "," \
                                    #                + str(day) + "," + str(year) + "," + str(day_of_year) + "," \
                                    #                + str(round(date, 3)) + "," + str(round(float_temperature, 2)) + "," + str(round(cToF(float_temperature), 2)) \
                                    #                + "\n"
                                    write_string = str(round(date, 3)) + "," + str(round(cToF(float_temperature), 2)) + "\n"
                                    #write_string = str(day_number) + "," + str(float_temperature) + "\n"
                                    if (target_type_under_test == "TMAX") :
                                        daily_temperature_tmax_fd.write(write_string)
                                    elif (target_type_under_test == "TMIN") :
                                        daily_temperature_tmin_fd.write(write_string)

                                station_monthly_total += float_temperature
                                station_monthly_day_count += 1
                                #monthly_temperature_total[year][month-1] += float_temperature
                                temperature_f = cToF(float_temperature)

                                if (target_type_under_test == "TMAX") :
                                    if (temperature_f >= TEMPERATURE_TARGET) :
                                        if (year not in current_station.first_day_above_max_threshold_map) :
                                            current_station.first_day_above_max_threshold_map[year] = day_of_year
                                        current_station.last_day_above_max_threshold_map[year] = day_of_year
                                        current_station.number_of_days_above_max_threshold_map[year] += 1
                                elif (target_type_under_test == "TMIN") :
                                    if (temperature_f <= TEMPERATURE_TARGET_MIN) :
                                        if (day_of_year < DAYS_PER_YEAR / 2) :
                                                current_station.last_day_below_min_threshold_map[year] = day_of_year
                                        else :
                                            if (current_station.first_day_below_min_threshold_map[year] == DAYS_PER_YEAR + 1) :
                                                current_station.first_day_below_min_threshold_map[year] = day_of_year
                                        current_station.number_of_days_below_min_threshold_map[year] += 1
                                        #print(currentFunctionName(), current_station.NAME, "last day above", TEMPERATURE_TARGET, year, current_station.last_day_above_max_threshold_map[year])
                                if (target_year == year and target_month == month and target_day == day) :
                                    if (target_type_under_test == "TMAX") :
                                        current_station.target_date_max_temperature = temperature_f
                                    elif (target_type_under_test == "TMIN") :
                                        current_station.target_date_min_temperature = temperature_f

                                    if (round(temperature_f) >= TEMPERATURE_TARGET + 20.0) :
                                        stations_above_target_plus_20_list.append(current_station)
                                    elif (round(temperature_f) >= TEMPERATURE_TARGET + 15.0) :
                                        stations_above_target_plus_15_list.append(current_station)
                                    elif (round(temperature_f) >= TEMPERATURE_TARGET + 10.0) :
                                        stations_above_target_plus_10_list.append(current_station)
                                    elif (round(temperature_f) >= TEMPERATURE_TARGET + 5.0) :
                                        stations_above_target_plus_5_list.append(current_station)
                                    elif (round(temperature_f) >= TEMPERATURE_TARGET) :
                                        stations_above_target_list.append(current_station)
                                    elif (round(temperature_f) >= TEMPERATURE_TARGET - 5.0) :
                                        stations_below_target_minus_5_list.append(current_station)
                                    elif (round(temperature_f) >= TEMPERATURE_TARGET - 10.0) :
                                        stations_below_target_minus_10_list.append(current_station)
                                    elif (round(temperature_f) >= TEMPERATURE_TARGET - 15.0) :
                                        stations_below_target_minus_15_list.append(current_station)
                                    else :
                                        stations_below_target_minus_20_list.append(current_station)

                                #for index in range(0, len(maximum_target_list)) :
                                #    target = maximum_target_list[index]
                                #    if (temperature_f >= target) :
                                #        monthly_days_above_target_year_dict[year][target][month-1] += 1.0
                                #        print(year, month, target, monthly_days_above_target_year_dict[year][target])

                                if (temperature_f >= TEMPERATURE_TARGET) :
                                    monthly_days_above_target[year][month-1] += 1.0
                                if (temperature_f >= TEMPERATURE_TARGET + 5.0) :
                                    monthly_days_above_target_plus_5F[year][month-1] += 1.0
                                if (temperature_f >= TEMPERATURE_TARGET + 10.0) :
                                    monthly_days_above_target_plus_10F[year][month-1] += 1.0
                                if (temperature_f >= TEMPERATURE_TARGET + 15.0) :
                                    monthly_days_above_target_plus_15F[year][month-1] += 1.0
                                if (temperature_f >= TEMPERATURE_TARGET + 20.0) :
                                    monthly_days_above_target_plus_20F[year][month-1] += 1.0

                    day_of_year += 1


                if (station_monthly_day_count > 0) :
                    # Calculate the average temperature at that station for the month
                    station_monthly_average = station_monthly_total / float(station_monthly_day_count)
                    if (target_type_under_test == TMAX) :
                        temperature_record = current_station.max_monthly_temperature_record
                    else :
                        temperature_record = current_station.min_monthly_temperature_record
                    if (year not in temperature_record) :
                        temperature_record[year] = AnnualTemperatureList()
                    temperature_record[year].monthly_temperature_list[month-1] = cToF(station_monthly_average)

                    # Add the average temperature at that station for the year/month to the total for all stations for that year/month
                    monthly_station_average_temperature_total_dict[year][month-1] += station_monthly_average
                    # Increment the station count for that year/month
                    monthly_station_count_array[year][month-1] += 1.0
                    daily_station_count_array[year][month-1] += station_monthly_day_count
                    #print(year, month, monthly_average)
        fd.close()

    if (target_type_under_test == "TMAX" and target_year != 0 and target_month != 0 and target_day != 0) :
        makeKMLFileForAboveMaximumThreshold()

    makeKMLFileForStationsUsed()

    print_string =  "Year"
    print_string += ",Atmospheric CO2"
    if (target_type_under_test == "TMAX") :
        print_string += ",Average Maximum Temperature"
    elif (target_type_under_test == "TMIN") :
        print_string += ",Average Minimum Temperature"
    print_string += ",Average Latitude"
    print_string += ",Average Longitude"
    print_string += ",Average Elevation"
    print_string += ",Average Record Length"
    print_string += ",Number of stations"
    print_string += ",Number of monthly readings"
    print_string += ",Number of daily readings"
    print_string += ",Average number of valid days per month"
    if (target_type_under_test == "TMAX") :
        above_below = " above "
    elif (target_type_under_test == "TMIN") :
        above_below = " below "

    print_string += ",Percent" + above_below + str(int(TEMPERATURE_TARGET)) + "F"
    print_string += ",Percent" + above_below + str(int(TEMPERATURE_TARGET + 5.0)) + "F"
    print_string += ",Percent" + above_below + str(int(TEMPERATURE_TARGET + 10.0)) + "F"
    print_string += ",Percent" + above_below + str(int(TEMPERATURE_TARGET + 15.0)) + "F"
    print_string += ",Percent" + above_below + str(int(TEMPERATURE_TARGET + 20.0)) + "F"


    printToFile(print_string)
    year_index = 0
    for year in range(FIRST_YEAR, LAST_YEAR+1) :
        yearly_station_monthly_average_temperature_total = 0.0
        yearly_monthly_station_count = 0.0
        yearly_valid_day_count = 0.0
        #yearly_temperature_total = 0.0
        yearly_mean_above_target_count = 0.0
        yearly_above_target_count = 0.0
        yearly_above_target_plus_5F_count = 0.0
        yearly_above_target_plus_10F_count = 0.0
        yearly_above_target_plus_15F_count = 0.0
        yearly_above_target_plus_20F_count = 0.0

        for month in range(0, NUMBER_OF_MONTHS) :
            if (monthly_station_count_array[year][month] > 0.0) :
                # Add the total monthly station average to the total yearly station average
                yearly_station_monthly_average_temperature_total += monthly_station_average_temperature_total_dict[year][month]
                # Add the total monthly station count to the total yearly station count
                yearly_monthly_station_count += monthly_station_count_array[year][month]
                yearly_valid_day_count += daily_station_count_array[year][month]
                #yearly_temperature_total += monthly_temperature_total[year][month]
                yearly_above_target_count += monthly_days_above_target[year][month]
                yearly_above_target_plus_5F_count += monthly_days_above_target_plus_5F[year][month]
                yearly_above_target_plus_10F_count += monthly_days_above_target_plus_10F[year][month]
                yearly_above_target_plus_15F_count += monthly_days_above_target_plus_15F[year][month]
                yearly_above_target_plus_20F_count += monthly_days_above_target_plus_20F[year][month]


        #Calculate the yearly station average
        if (yearly_monthly_station_count == 0) :
            continue

        yearly_station_average = yearly_station_monthly_average_temperature_total / yearly_monthly_station_count
        #yearly_average_day_count_per_month = yearly_valid_day_count / yearly_monthly_station_count
        number_of_months = MONTHS_PER_YEAR
        if (len(MONTHS_UNDER_TEST_LIST) > 0) :
            number_of_months = len(MONTHS_UNDER_TEST_LIST)
        yearly_average_day_count_per_month = yearly_valid_day_count / (len(station_list) * number_of_months)
        percent_above_target = (yearly_above_target_count / yearly_valid_day_count) * 100.0
        percent_above_target_plus_5F = (yearly_above_target_plus_5F_count / yearly_valid_day_count) * 100.0
        percent_above_target_plus_10F = (yearly_above_target_plus_10F_count / yearly_valid_day_count) * 100.0
        percent_above_target_plus_15F = (yearly_above_target_plus_15F_count / yearly_valid_day_count) * 100.0
        percent_above_target_plus_20F = (yearly_above_target_plus_20F_count / yearly_valid_day_count) * 100.0
        percent_below_target = 100.0 - percent_above_target
        percent_below_target_plus_5F = 100.0 - percent_above_target_plus_5F
        percent_below_target_plus_10F = 100.0 - percent_above_target_plus_10F
        percent_below_target_plus_15F = 100.0 - percent_above_target_plus_15F
        percent_below_target_plus_20F = 100.0 - percent_above_target_plus_20F

        total_latitude = 0.0
        total_longitude = 0.0
        total_elevation = 0.0
        total_record_length = 0.0
        for station in station_dict[year] :
            latitude = station_map[station].LATITUDE
            total_latitude += latitude
            longitude = station_map[station].LONGITUDE
            total_longitude += longitude
            elevation = station_map[station].ELEVATION
            total_elevation += elevation
            total_record_length += station_map[station].record_length
        average_latitude = total_latitude / float(len(station_dict[year]))
        average_longitude = total_longitude / float(len(station_dict[year]))
        average_elevation = total_elevation / float(len(station_dict[year]))
        average_record_length = total_record_length / float(len(station_dict[year]))

        if (year not in data_dict[YEAR]) :
            data_dict[YEAR].append(year)
            try :
                data_dict[CO2].append(CO2_map[year])
            except :
                print(currentFunctionName(), "Attempting to append the CO2 map for year", year)


        if (target_type_under_test == "TMAX") :
            printToFile(       year,
                    ",", CO2_map[year],
                    ",", cToF(yearly_station_average),
                    ",", average_latitude,
                    ",", average_longitude,
                    ",", metersToFeet(average_elevation),
                    ",", average_record_length,
                    ",", len(station_dict[year]),
                    ",", yearly_monthly_station_count,
                    ",", yearly_valid_day_count,
                    ",", yearly_average_day_count_per_month,
                    ",", percent_above_target,
                    ",", percent_above_target_plus_5F,
                    ",", percent_above_target_plus_10F,
                    ",", percent_above_target_plus_15F,
                    ",", percent_above_target_plus_20F)

            data_dict[MAXIMUM_YEAR].append(year)
            data_dict[AVERAGE_MAXIMUM_TEMPERATURE].append(cToF(yearly_station_average))
            data_dict[AVERAGE_STATION_LATITUDE].append(average_latitude)
            data_dict[AVERAGE_STATION_LONGITUDE].append(average_longitude)
            data_dict[AVERAGE_STATION_ELEVATION].append(metersToFeet(average_elevation))
            data_dict[AVERAGE_STATION_RECORD_LENGTH].append(average_record_length)
            data_dict[NUMBER_OF_STATIONS].append(len(station_dict[year]))
            data_dict[NUMBER_OF_MONTHLY_MAXIMUM_READINGS].append(yearly_monthly_station_count)
            data_dict[NUMBER_OF_DAILY_READINGS].append(yearly_valid_day_count)
            data_dict[NUMBER_OF_VALID_DAYS_PER_MONTH].append(yearly_average_day_count_per_month)
            data_dict[PERCENT_ABOVE_MAX_TARGET].append(percent_above_target)
            data_dict[PERCENT_ABOVE_MAX_TARGET_PLUS_5].append(percent_above_target_plus_5F)
            data_dict[PERCENT_ABOVE_MAX_TARGET_PLUS_10].append(percent_above_target_plus_10F)
            data_dict[PERCENT_ABOVE_MAX_TARGET_PLUS_15].append(percent_above_target_plus_15F)
            data_dict[PERCENT_ABOVE_MAX_TARGET_PLUS_20].append(percent_above_target_plus_20F)
        elif (target_type_under_test == "TMIN") :
            printToFile(       year,
                    ",", CO2_map[year],
                    ",", cToF(yearly_station_average),
                    ",", average_latitude,
                    ",", average_longitude,
                    ",", metersToFeet(average_elevation),
                    ",", average_record_length,
                    ",", len(station_dict[year]),
                    ",", yearly_monthly_station_count,
                    ",", yearly_valid_day_count,
                    ",", yearly_average_day_count_per_month,
                    ",", percent_below_target,
                    ",", percent_below_target_plus_5F,
                    ",", percent_below_target_plus_10F,
                    ",", percent_below_target_plus_15F,
                    ",", percent_below_target_plus_20F)

            if (len(data_dict[MAXIMUM_YEAR]) > 0) :
                #print(year, data_dict[MAXIMUM_YEAR])
                if (year not in data_dict[MAXIMUM_YEAR]) :
                    continue
            data_dict[MINIMUM_YEAR].append(year)
            data_dict[NUMBER_OF_MONTHLY_MINIMUM_READINGS].append(yearly_monthly_station_count)
            data_dict[AVERAGE_MINIMUM_TEMPERATURE].append(cToF(yearly_station_average))
            # Check to see if the minimum and maximum years align
            if (len(data_dict[MAXIMUM_YEAR]) >= year_index and data_dict[MAXIMUM_YEAR][year_index] == year) :
                average_mean = (data_dict[AVERAGE_MAXIMUM_TEMPERATURE][year_index] + data_dict[AVERAGE_MINIMUM_TEMPERATURE][year_index]) / 2.0
                data_dict[AVERAGE_MEAN_TEMPERATURE].append(average_mean)
                average_range = data_dict[AVERAGE_MAXIMUM_TEMPERATURE][year_index] - data_dict[AVERAGE_MINIMUM_TEMPERATURE][year_index]
                data_dict[AVERAGE_DAILY_TEMPERATURE_RANGE].append(average_range)
                ratio = data_dict[NUMBER_OF_MONTHLY_MAXIMUM_READINGS][year_index] / data_dict[NUMBER_OF_MONTHLY_MINIMUM_READINGS][year_index]
                data_dict[RATIO_OF_MONTHLY_MAXIMUM_TO_MINIMUM_READINGS].append(ratio)
            else :
                data_dict[RATIO_OF_MONTHLY_MAXIMUM_TO_MINIMUM_READINGS].append(0)
                print(currentFunctionName(), "Mismatch between MIN year and MAX year", year, data_dict[MAXIMUM_YEAR][year_index])
            if (len(data_dict[AVERAGE_MAXIMUM_TEMPERATURE]) == 0) :
                data_dict[AVERAGE_STATION_LATITUDE].append(average_latitude)
                data_dict[AVERAGE_STATION_LONGITUDE].append(average_longitude)
                data_dict[AVERAGE_STATION_ELEVATION].append(metersToFeet(average_elevation))
                data_dict[AVERAGE_STATION_RECORD_LENGTH].append(average_record_length)
                data_dict[NUMBER_OF_STATIONS].append(len(station_dict[year]))
                data_dict[NUMBER_OF_DAILY_READINGS].append(yearly_valid_day_count)
                data_dict[NUMBER_OF_VALID_DAYS_PER_MONTH].append(yearly_average_day_count_per_month)
            data_dict[PERCENT_BELOW_MIN_TARGET].append(percent_below_target)
            data_dict[PERCENT_BELOW_MIN_TARGET_PLUS_5].append(percent_below_target_plus_5F)
            data_dict[PERCENT_BELOW_MIN_TARGET_PLUS_10].append(percent_below_target_plus_10F)
            data_dict[PERCENT_BELOW_MIN_TARGET_PLUS_15].append(percent_below_target_plus_15F)
            data_dict[PERCENT_BELOW_MIN_TARGET_PLUS_20].append(percent_below_target_plus_20F)
        year_index += 1


if (DUMP_DAILY_TEMPERATURES_TO_CSV_FILE):
    daily_temperature_tmax_fd.close()
    daily_temperature_tmin_fd.close()

#USH0001108411912  1374E    1590E    2049E    2623E    3110E    3089E    3278E    3313E    3153E    2659E    2088E    1741E
#USH0001281312006  1999     1818     2338     2782     2951     3397     3356     3385     3067     2647     2128     1877
#USH00012813 2006  1985     1801     2321     2769     2939     3389     3353     3385     3072     2653     2128     1869
#USH00029359 2011   849a     691b    1300a    1629c    1949f    2685     2842a    2990     2518     1964     1098      618
#USH00029359 2012 -9999      873     1329    -9999    -9999     2919     2767d    2724e    2440d    2010c    1520      619
#USC00012813201707TMAX
if os.path.isfile("US_raw.tmax.txt") :
    raw_fd = open("US_raw.tmax.txt")
    for line in raw_fd :
        tokens = line.split()
        station_info = tokens[0]
        year = int(tokens[1])
        if (station_info in ghcn_ushcn_map) :
            station_id = ghcn_ushcn_map[station_info]
        else :
            station_id = station_info[0:11].replace("USH", "USC")
        if (station_id in station_map) :
            station = station_map[station_id]
            temperature_record = station.ushcn_raw_max_monthly_temperature_record
            if year not in temperature_record :
                temperature_record[year] = AnnualTemperatureList()
            index = 17
            month_count = 0
            for month in range(0, NUMBER_OF_MONTHS) :
                temperature_string = line[index:index+5]
                if (temperature_string == MISSING) :
                    temperature = UNREASONABLE_LOW_TEMPERATURE
                else :
                    temperature = cToF(float(temperature_string) / 100.0)
                    month_count += 1
                temperature_record[year].monthly_temperature_list[month] = temperature
                #print(currentFunctionName(), station_map[station_id].NAME, year, temperature)
                index += 9
            temperature_record[year].raw_data_count = month_count

if os.path.isfile("US_final.tmax.txt") :
    raw_fd = open("US_final.tmax.txt")
    for line in raw_fd :
        tokens = line.split()
        station_info = tokens[0]
        year = int(tokens[0][12:16])
        station_id = station_info[0:11].replace("USH", "USC")
        if (station_info in ghcn_ushcn_map) :
            station_id = ghcn_ushcn_map[station_info]
        else :
            station_id = station_info[0:11].replace("USH", "USC")
        if (station_id in station_map) :
            station = station_map[station_id]
            temperature_record = station.ushcn_final_max_monthly_temperature_record
            if year not in temperature_record :
                temperature_record[year] = AnnualTemperatureList()
            index = 17
            for month in range(0, NUMBER_OF_MONTHS) :
                temperature_string = line[index:index+5]
                if (temperature_string == MISSING) :
                    temperature = UNREASONABLE_LOW_TEMPERATURE
                else :
                    temperature = cToF(float(temperature_string) / 100.0)
                    flag = line[index+5]
                    if (flag == "E") :
                        temperature_record[year].fake_data_count += 1
                        temperature_record[year].fake_data_total += temperature
                    else :
                        temperature_record[year].real_data_count += 1
                        temperature_record[year].real_data_total += temperature
                temperature_record[year].monthly_temperature_list[month] = temperature
                #print(currentFunctionName(), station_map[station_id].NAME, year, temperature)
                index += 9
if os.path.isfile("US_raw.tavg.txt") :
    raw_fd = open("US_raw.tavg.txt")
    for line in raw_fd :
        tokens = line.split()
        station_info = tokens[0]
        year = int(tokens[1])
        if (station_info in ghcn_ushcn_map) :
            station_id = ghcn_ushcn_map[station_info]
        else :
            station_id = station_info[0:11].replace("USH", "USC")
        if (station_id in station_map) :
            station = station_map[station_id]
            temperature_record = station.ushcn_raw_average_monthly_temperature_record
            if year not in temperature_record :
                temperature_record[year] = AnnualTemperatureList()
            index = 17
            month_count = 0
            for month in range(0, NUMBER_OF_MONTHS) :
                temperature_string = line[index:index+5]
                if (temperature_string == MISSING) :
                    temperature = UNREASONABLE_LOW_TEMPERATURE
                else :
                    temperature = cToF(float(temperature_string) / 100.0)
                    month_count += 1
                temperature_record[year].monthly_temperature_list[month] = temperature
                #print(currentFunctionName(), station_map[station_id].NAME, year, temperature)
                index += 9
            temperature_record[year].raw_data_count = month_count

if os.path.isfile("US_final.tavg.txt") :
    raw_fd = open("US_final.tavg.txt")
    for line in raw_fd :
        tokens = line.split()
        station_info = tokens[0]
        year = int(tokens[1])
        station_id = station_info[0:11].replace("USH", "USC")
        if (station_info in ghcn_ushcn_map) :
            station_id = ghcn_ushcn_map[station_info]
        else :
            station_id = station_info[0:11].replace("USH", "USC")
        if (station_id in station_map) :
            station = station_map[station_id]
            temperature_record = station.ushcn_final_average_monthly_temperature_record
            if year not in temperature_record :
                temperature_record[year] = AnnualTemperatureList()
            index = 17
            for month in range(0, NUMBER_OF_MONTHS) :
                temperature_string = line[index:index+5]
                if (temperature_string == MISSING) :
                    temperature = UNREASONABLE_LOW_TEMPERATURE
                else :
                    temperature = cToF(float(temperature_string) / 100.0)
                    flag = line[index+5]
                    if (flag == "E") :
                        temperature_record[year].fake_data_count += 1
                        temperature_record[year].fake_data_total += temperature
                    else :
                        temperature_record[year].real_data_count += 1
                        temperature_record[year].real_data_total += temperature
                temperature_record[year].monthly_temperature_list[month] = temperature
                #print(currentFunctionName(), station_map[station_id].NAME, year, temperature)
                index += 9

printToFile("Station Data,,,,,,Maximum Temperatures,,,,,,,,,,,,,,,,,,,,,,Minimum Temperatures")
months_string = ","
for month in month_list :
    months_string += month + ","
printToFile("Name,State,Country,ID,Year,", months_string ,"Number Of Months With Maximum Data" ,",Average Monthly Maximum"
            ,",First Day Above Maximum Threshold"
            ,",Last Day Above Maximum Threshold"
            ,",Number Of Days Above Maximum Threshold"
            ,",Last Soring Day Below Minimum Threshold"
            ,",First Autumn Day Below Minimum Threshold"
            ,",Number Of Days Below Minimum Threshold"
            ,",USHCN RAW Monthly Maximum"
            ,",USHCN FINAL Monthly Maximum"
            ,",Difference Between USHCN FINAL And USHCN RAW Maximum"
            ,",Difference Between USHCN FINAL And Daily Maximum"
            ,",Difference Between USHCN RAW And Daily Maximum"
            ,",Fake USHCN FINAL Maximum Data Percent"
            ,",FINAL Percent Of RAW Maximum Data Which Was Ignored"
            ,",USHCN RAW Monthly Average"
            ,",USHCN FINAL Monthly Average"
            ,",Difference Between USHCN FINAL And USHCN RAW Average"
            ,",Fake USHCN FINAL Average Data Percent"
            ,",FINAL Percent Of RAW Average Data Which Was Ignored"
            ,",", months_string, "Number Of Months With Minmimum Daily Data" ,",Average Monthly Daily Minimum"
            )

yearly_raw_max_total_map = {}
yearly_raw_max_station_count_map = {}

yearly_final_max_total_map = {}
yearly_final_max_station_count_map = {}
yearly_final_fake_max_total_map = {}
yearly_final_fake_max_station_count_map = {}
yearly_final_fake_max_data_count_map = {}
yearly_final_real_max_total_map = {}
yearly_final_real_max_station_count_map = {}
yearly_final_real_max_data_count_map = {}
yearly_final_raw_max_data_which_was_ignored_count_map = {}

yearly_raw_average_total_map = {}
yearly_raw_average_station_count_map = {}

yearly_final_average_total_map = {}
yearly_final_average_station_count_map = {}
yearly_final_fake_average_total_map = {}
yearly_final_fake_average_station_count_map = {}
yearly_final_fake_average_data_count_map = {}
yearly_final_real_average_total_map = {}
yearly_final_real_average_station_count_map = {}
yearly_final_real_average_data_count_map = {}
yearly_final_raw_average_data_which_was_ignored_count_map = {}

for year in range(FIRST_YEAR, LAST_YEAR+1) :
    yearly_raw_max_total_map[year] = 0.0
    yearly_raw_max_station_count_map[year] = 0.0
    yearly_raw_max_total_map[year] = 0.0
    yearly_raw_max_station_count_map[year] = 0.0

    yearly_final_max_total_map[year] = 0.0
    yearly_final_max_station_count_map[year] = 0.0
    yearly_final_fake_max_total_map[year] = 0.0
    yearly_final_fake_max_station_count_map[year] = 0.0
    yearly_final_fake_max_data_count_map[year] = 0.0
    yearly_final_real_max_total_map[year] = 0.0
    yearly_final_real_max_station_count_map[year] = 0.0
    yearly_final_real_max_data_count_map[year] = 0.0
    yearly_final_raw_max_data_which_was_ignored_count_map[year] = 0.0

    yearly_raw_average_total_map[year] = 0.0
    yearly_raw_average_station_count_map[year] = 0.0
    yearly_raw_average_total_map[year] = 0.0
    yearly_raw_average_station_count_map[year] = 0.0

    yearly_final_average_total_map[year] = 0.0
    yearly_final_average_station_count_map[year] = 0.0
    yearly_final_fake_average_total_map[year] = 0.0
    yearly_final_fake_average_station_count_map[year] = 0.0
    yearly_final_fake_average_data_count_map[year] = 0.0
    yearly_final_real_average_total_map[year] = 0.0
    yearly_final_real_average_station_count_map[year] = 0.0
    yearly_final_real_average_data_count_map[year] = 0.0
    yearly_final_raw_average_data_which_was_ignored_count_map[year] = 0.0

total_average_first_day_above_max_threshold = 0.0
total_average_last_day_above_max_threshold = 0.0
number_of_stations_reporting_days_above_max_threshold = 0.0
total_average_first_day_below_min_threshold = 0.0
total_average_last_day_below_min_threshold = 0.0
number_of_stations_reporting_days_below_min_threshold = 0.0

for station in station_list:
    last_day_above_max_threshold_total = 0.0
    first_day_above_max_threshold_total = 0.0
    number_of_days_above_max_threshold = 0.0
    last_day_below_min_threshold_total = 0.0
    first_day_below_min_threshold_total = 0.0
    number_of_days_below_min_threshold = 0.0

    for year in range(FIRST_YEAR, LAST_YEAR+1) :
        daily_max_monthly_data_string = ""
        daily_max_total = 0.0
        daily_max_month_count = 0
        max_average = 0.0

        raw_max_average = 0.0
        raw_max_total = 0.0
        raw_max_month_count = 0
        raw_max_monthly_temperature_string = ""
        raw_max_average_string = ""
        raw_max_minus_daily = 0.0

        final_max_average = 0.0
        final_fake_max_data_percentage = 0.0
        final_real_max_data_percentage = 0.0
        final_percent_of_raw_max_data_which_was_ignored = 0.0
        final_max_total = 0.0
        final_max_month_count = 0
        final_max_minus_raw = 0.0
        final_max_minus_daily = 0.0
        final_max_monthly_temperature_string = ""
        final_max_average_string = ""

        raw_average_average = 0.0
        raw_average_total = 0.0
        raw_average_month_count = 0
        raw_average_monthly_temperature_string = ""
        raw_average_average_string = ""
        raw_average_minus_daily = 0.0

        final_average_average = 0.0
        final_fake_average_data_percentage = 0.0
        final_real_average_data_percentage = 0.0
        final_percent_of_raw_average_data_which_was_ignored = 0.0
        final_average_total = 0.0
        final_average_month_count = 0
        final_average_minus_raw = 0.0
        final_average_minus_daily = 0.0
        final_average_monthly_temperature_string = ""
        final_average_average_string = ""

        daily_min_monthly_data_string = ""
        min_total = 0.0
        min_count = 0

        # MAXIMUM
        if year in station.max_monthly_temperature_record :
            month = 1
            for temperature in station.max_monthly_temperature_record[year].monthly_temperature_list :
                if (dontUseThisMonth(year, month)) :
                    month += 1
                    daily_max_monthly_data_string += ","
                    continue
                if (temperature == UNREASONABLE_LOW_TEMPERATURE) :
                     daily_max_monthly_data_string += ","
                else :
                    daily_max_monthly_data_string += "," + str(temperature)
                    daily_max_total += temperature
                    daily_max_month_count += 1
                month += 1
        else :
            for month in range(0, NUMBER_OF_MONTHS) :
                daily_max_monthly_data_string += ","

        if (daily_max_month_count > 0) :
            daily_max_average = daily_max_total / float(daily_max_month_count)
            station.max_yearly_temperature_record[year] = AnnualTemperatureList()
            station.max_yearly_temperature_record[year].annual_average = daily_max_average
            daily_max_monthly_data_string += "," + str(daily_max_month_count) + "," + str(daily_max_average)
        else :
            daily_max_monthly_data_string += ",,"

        # USHCN RAW MAXIMUM
        if year in station.ushcn_raw_max_monthly_temperature_record :
            month = 1
            for temperature in station.ushcn_raw_max_monthly_temperature_record[year].monthly_temperature_list :
                if (dontUseThisMonth(year, month)) :
                    month += 1
                    raw_max_monthly_temperature_string += ","
                    continue
                if (temperature == UNREASONABLE_LOW_TEMPERATURE) :
                     raw_max_monthly_temperature_string += ","
                else :
                    raw_max_monthly_temperature_string += "," + str(temperature)
                    if (validMonth(month) == True) :
                        raw_max_total += temperature
                        raw_max_month_count += 1
                month += 1
        else :
            for month in range(0, NUMBER_OF_MONTHS) :
                raw_max_monthly_temperature_string += ","

        if (raw_max_month_count > 0) :
            raw_max_average = raw_max_total / float(raw_max_month_count)
            yearly_raw_max_total_map[year] += raw_max_average
            yearly_raw_max_station_count_map[year] += 1.0
            station.ushcn_raw_max_yearly_temperature_record[year] = AnnualTemperatureList()
            station.ushcn_raw_max_yearly_temperature_record[year].annual_average = raw_max_average
            station.ushcn_raw_max_yearly_temperature_record[year].raw_data_count = raw_max_month_count
            raw_max_monthly_temperature_string += "," + str(raw_max_month_count) + "," + str(raw_max_average)
            raw_max_average_string = str(raw_max_average)
        else :
            raw_max_monthly_temperature_string += ","

        # USHCN FINAL MAXIMUM
        if year in station.ushcn_final_max_monthly_temperature_record :
            month = 1
            for temperature in station.ushcn_final_max_monthly_temperature_record[year].monthly_temperature_list :
                if (dontUseThisMonth(year, month)) :
                    #print(currentFunctionName(), "Rejecting month", month)
                    month += 1
                    final_max_monthly_temperature_string += ","
                    continue
                if (temperature == UNREASONABLE_LOW_TEMPERATURE) :
                    final_max_monthly_temperature_string += ","
                else :
                    final_max_monthly_temperature_string += "," + str(temperature)
                    if (validMonth(month) == True) :
                        final_max_total += temperature
                        final_max_month_count += 1
                month += 1
        else :
            for month in range(0, NUMBER_OF_MONTHS) :
                final_max_monthly_temperature_string += ","

        if (final_max_month_count > 0) :
            final_max_average = final_max_total / float(final_max_month_count)
            record = station.ushcn_final_max_monthly_temperature_record[year]

            if (record.fake_data_count > 0 and record.real_data_count > 0) :
                final_fake_max_data_percentage = float(record.fake_data_count) / float(record.fake_data_count + record.real_data_count) * 100.0
                final_real_max_data_percentage = float(record.real_data_count) / float(record.fake_data_count + record.real_data_count) * 100.0
            elif (record.fake_data_count > 0) :
                final_fake_max_data_percentage = 100.0
            elif (record.real_data_count > 0) :
                final_real_max_data_percentage = 100.0
            else :
                final_fake_max_data_percentage = 0.0
                final_real_max_data_percentage = 0.0

            if (year in station.ushcn_raw_max_yearly_temperature_record) :
                raw_record = station.ushcn_raw_max_monthly_temperature_record[year]
                if (raw_record.raw_data_count > 0 and record.real_data_count > 0) :
                    final_percent_of_raw_max_data_which_was_ignored = float(raw_record.raw_data_count - record.real_data_count) / float(raw_record.raw_data_count) * 100.0
                    yearly_final_raw_max_data_which_was_ignored_count_map[year] += raw_record.raw_data_count - record.real_data_count
                    #if (final_percent_of_raw_max_data_which_was_ignored > 0.0) :
                        #print(currentFunctionName(), "ignored", year, yearly_final_raw_max_data_which_was_ignored_count_map[year], raw_record.raw_data_count, record.real_data_count)
                elif (raw_record.raw_data_count > 0) :
                    final_percent_of_raw_max_data_which_was_ignored = 100.0
                else :
                    final_percent_of_raw_max_data_which_was_ignored = 0.0
            else :
                final_percent_of_raw_max_data_which_was_ignored = 0.0

            station.ushcn_final_max_yearly_temperature_record[year] = AnnualTemperatureList()

            if (record.fake_data_count > 0) :
                fake_annual_average = record.fake_data_total / float(record.fake_data_count)
                yearly_final_fake_max_total_map[year] += fake_annual_average
                yearly_final_fake_max_station_count_map[year] += 1.0
                yearly_final_fake_max_data_count_map[year] += record.fake_data_count
                station.ushcn_final_max_yearly_temperature_record[year].fake_annual_average = fake_annual_average
            if (record.real_data_count > 0) :
                real_annual_average = record.real_data_total / float(record.real_data_count)
                yearly_final_real_max_total_map[year] += real_annual_average
                yearly_final_real_max_station_count_map[year] += 1.0
                yearly_final_real_max_data_count_map[year] += record.real_data_count
                station.ushcn_final_max_yearly_temperature_record[year].real_annual_average = real_annual_average

            yearly_final_max_total_map[year] += final_max_average
            yearly_final_max_station_count_map[year] += 1.0
            station.ushcn_final_max_yearly_temperature_record[year].annual_average = final_max_average
            final_max_monthly_temperature_string += "," + str(final_max_month_count) + "," + str(final_max_average)
            final_max_average_string = str(final_max_average)
        else :
            final_max_monthly_temperature_string += ","

        # USHCN RAW AVERAGE
        if year in station.ushcn_raw_average_monthly_temperature_record :
            month = 1
            for temperature in station.ushcn_raw_average_monthly_temperature_record[year].monthly_temperature_list :
                if (dontUseThisMonth(year, month)) :
                    month += 1
                    raw_average_monthly_temperature_string += ","
                    continue
                if (temperature == UNREASONABLE_LOW_TEMPERATURE) :
                     raw_average_monthly_temperature_string += ","
                else :
                    raw_average_monthly_temperature_string += "," + str(temperature)
                    if (validMonth(month) == True) :
                        raw_average_total += temperature
                        raw_average_month_count += 1
                month += 1
        else :
            for month in range(0, NUMBER_OF_MONTHS) :
                raw_average_monthly_temperature_string += ","

        if (raw_average_month_count > 0) :
            raw_average_average = raw_average_total / float(raw_average_month_count)
            yearly_raw_average_total_map[year] += raw_average_average
            yearly_raw_average_station_count_map[year] += 1.0
            station.ushcn_raw_average_yearly_temperature_record[year] = AnnualTemperatureList()
            station.ushcn_raw_average_yearly_temperature_record[year].annual_average = raw_average_average
            station.ushcn_raw_average_yearly_temperature_record[year].raw_data_count = raw_average_month_count
            raw_average_monthly_temperature_string += "," + str(raw_average_month_count) + "," + str(raw_average_average)
            raw_average_average_string = str(raw_average_average)
        else :
            raw_average_monthly_temperature_string += ","

        # USHCN FINAL AVERAGE
        if year in station.ushcn_final_average_monthly_temperature_record :
            month = 1
            for temperature in station.ushcn_final_average_monthly_temperature_record[year].monthly_temperature_list :
                if (dontUseThisMonth(year, month)) :
                    #print(currentFunctionName(), "Rejecting month", month)
                    month += 1
                    final_average_monthly_temperature_string += ","
                    continue
                if (temperature == UNREASONABLE_LOW_TEMPERATURE) :
                    final_average_monthly_temperature_string += ","
                else :
                    final_average_monthly_temperature_string += "," + str(temperature)
                    if (validMonth(month) == True) :
                        final_average_total += temperature
                        final_average_month_count += 1
                month += 1
        else :
            for month in range(0, NUMBER_OF_MONTHS) :
                final_average_monthly_temperature_string += ","

        if (final_average_month_count > 0) :
            final_average_average = final_average_total / float(final_average_month_count)
            record = station.ushcn_final_average_monthly_temperature_record[year]

            if (record.fake_data_count > 0 and record.real_data_count > 0) :
                final_fake_average_data_percentage = float(record.fake_data_count) / float(record.fake_data_count + record.real_data_count) * 100.0
                final_real_average_data_percentage = float(record.real_data_count) / float(record.fake_data_count + record.real_data_count) * 100.0
            elif (record.fake_data_count > 0) :
                final_fake_average_data_percentage = 100.0
            elif (record.real_data_count > 0) :
                final_real_average_data_percentage = 100.0
            else :
                final_fake_average_data_percentage = 0.0
                final_real_average_data_percentage = 0.0

            if (year in station.ushcn_raw_average_yearly_temperature_record) :
                raw_record = station.ushcn_raw_average_monthly_temperature_record[year]
                if (raw_record.raw_data_count > 0 and record.real_data_count > 0) :
                    final_percent_of_raw_average_data_which_was_ignored = float(raw_record.raw_data_count - record.real_data_count) / float(raw_record.raw_data_count) * 100.0
                    yearly_final_raw_average_data_which_was_ignored_count_map[year] += raw_record.raw_data_count - record.real_data_count
                    #if (final_percent_of_raw_average_data_which_was_ignored > 0.0) :
                        #print(currentFunctionName(), "ignored", year, yearly_final_raw_average_data_which_was_ignored_count_map[year], raw_record.raw_data_count, record.real_data_count)
                elif (raw_record.raw_data_count > 0) :
                    final_percent_of_raw_average_data_which_was_ignored = 100.0
                else :
                    final_percent_of_raw_average_data_which_was_ignored = 0.0
            else :
                final_percent_of_raw_average_data_which_was_ignored = 0.0

            station.ushcn_final_average_yearly_temperature_record[year] = AnnualTemperatureList()

            if (record.fake_data_count > 0) :
                fake_annual_average = record.fake_data_total / float(record.fake_data_count)
                yearly_final_fake_average_total_map[year] += fake_annual_average
                yearly_final_fake_average_station_count_map[year] += 1.0
                yearly_final_fake_average_data_count_map[year] += record.fake_data_count
                station.ushcn_final_average_yearly_temperature_record[year].fake_annual_average = fake_annual_average
            if (record.real_data_count > 0) :
                real_annual_average = record.real_data_total / float(record.real_data_count)
                yearly_final_real_average_total_map[year] += real_annual_average
                yearly_final_real_average_station_count_map[year] += 1.0
                yearly_final_real_average_data_count_map[year] += record.real_data_count
                station.ushcn_final_average_yearly_temperature_record[year].real_annual_average = real_annual_average

            yearly_final_average_total_map[year] += final_average_average
            yearly_final_average_station_count_map[year] += 1.0
            station.ushcn_final_average_yearly_temperature_record[year].annual_average = final_average_average
            final_average_monthly_temperature_string += "," + str(final_average_month_count) + "," + str(final_average_average)
            final_average_average_string = str(final_average_average)
        else :
            final_average_monthly_temperature_string += ","

        # MINIMUM
        if year in station.min_monthly_temperature_record :
            month = 1
            for temperature in station.min_monthly_temperature_record[year].monthly_temperature_list :
                if (dontUseThisMonth(year, month)) :
                    month += 1
                    daily_min_monthly_data_string += ","
                    continue
                if (temperature == UNREASONABLE_LOW_TEMPERATURE) :
                    daily_min_monthly_data_string += ","
                else :
                    daily_min_monthly_data_string += "," + str(temperature)
                    min_total += temperature
                    min_count += 1
                month += 1
        else :
            for month in range(0, NUMBER_OF_MONTHS) :
                daily_min_monthly_data_string += ","

        if (min_count > 0) :
            min_average = min_total / float(min_count)
            daily_min_monthly_data_string += "," + str(min_count) + "," + str(min_average)
        else :
            daily_min_monthly_data_string += ",,"

        first_day_above_max_threshold = 0
        last_day_above_max_threshold = 0
        number_of_days_above_max_threshold = 0
        if (year in station.first_day_above_max_threshold_map) :
            first_day_above_max_threshold = station.first_day_above_max_threshold_map[year]
            #print(currentFunctionName(), station.NAME, "first_day_above_max_threshold", first_day_above_max_threshold)
            first_day_above_max_threshold_total += float(first_day_above_max_threshold)
        if (year in station.last_day_above_max_threshold_map) :
            last_day_above_max_threshold = station.last_day_above_max_threshold_map[year]
            last_day_above_max_threshold_total += float(last_day_above_max_threshold)
        if (year in station.number_of_days_above_max_threshold_map) :
            number_of_days_above_max_threshold = station.number_of_days_above_max_threshold_map[year]

        first_day_below_min_threshold = 0
        last_day_below_min_threshold = 0
        number_of_days_below_min_threshold = 0
        if (year in station.last_day_below_min_threshold_map) :
            last_day_below_min_threshold = station.last_day_below_min_threshold_map[year]
            last_day_below_min_threshold_total += float(last_day_below_min_threshold)
        if (year in station.first_day_below_min_threshold_map) :
            first_day_below_min_threshold = station.first_day_below_min_threshold_map[year]
            if (first_day_below_min_threshold < DAYS_PER_YEAR + 1) :
                first_day_below_min_threshold_total += float(first_day_below_min_threshold)
        if (year in station.number_of_days_below_min_threshold_map) :
            number_of_days_below_min_threshold = station.number_of_days_below_min_threshold_map[year]

            #print(currentFunctionName(), station.NAME, "last day above", TEMPERATURE_TARGET, year, last_day_above_max_threshold)

        # Print out the results
        printToFile(station.NAME, ",", station.STATE, ",", station.COUNTRY, ",", station.ID , ",", year , ",", daily_max_monthly_data_string
                , ",", first_day_above_max_threshold
                , ",", last_day_above_max_threshold
                , ",", number_of_days_above_max_threshold
                , ",", last_day_below_min_threshold
                , ",", first_day_below_min_threshold
                , ",", number_of_days_below_min_threshold
                , ",", raw_max_average_string
                , ",", final_max_average_string
                , ",", final_max_average - raw_max_average
                , ",", final_max_average - max_average
                , ",", raw_max_average - max_average
                , ",", final_fake_max_data_percentage
                , ",", final_percent_of_raw_max_data_which_was_ignored
                , ",", raw_average_average_string
                , ",", final_average_average_string
                , ",", final_average_average - raw_average_average
                , ",", final_fake_average_data_percentage
                , ",", final_percent_of_raw_average_data_which_was_ignored
                , ",", daily_min_monthly_data_string
                )

    a,b = calculateLinearRegressionFromMap(station.max_yearly_temperature_record)
    station.max_yearly_temperature_trend = (a,b)
    a,b = calculateLinearRegressionFromMap(station.first_day_above_max_threshold_map, "generic")
    station.first_day_above_max_threshold_trend = (a,b)
    a,b = calculateLinearRegressionFromMap(station.last_day_above_max_threshold_map, "generic")
    station.last_day_above_max_threshold_trend = (a,b)

    a,b = calculateLinearRegressionFromMap(station.min_yearly_temperature_record)
    station.min_yearly_temperature_trend = (a,b)
    a,b = calculateLinearRegressionFromMap(station.first_day_below_min_threshold_map, "generic")
    station.first_day_below_min_threshold_trend = (a,b)
    a,b = calculateLinearRegressionFromMap(station.last_day_below_min_threshold_map, "generic")
    station.last_day_below_min_threshold_trend = (a,b)

    a,b = calculateLinearRegressionFromMap(station.ushcn_raw_max_yearly_temperature_record)
    station.raw_max_yearly_temperature_trend = (a,b)
    a,b = calculateLinearRegressionFromMap(station.ushcn_final_max_yearly_temperature_record)
    station.final_max_yearly_temperature_trend = (a,b)
    a,b = calculateLinearRegressionFromMap(station.ushcn_final_max_yearly_temperature_record, "fake")
    station.final_fake_max_yearly_temperature_trend = (a,b)
    a,b = calculateLinearRegressionFromMap(station.ushcn_final_max_yearly_temperature_record, "real")
    station.final_real_max_yearly_temperature_trend = (a,b)

    a,b = calculateLinearRegressionFromMap(station.ushcn_raw_average_yearly_temperature_record)
    station.raw_average_yearly_temperature_trend = (a,b)
    a,b = calculateLinearRegressionFromMap(station.ushcn_final_average_yearly_temperature_record)
    station.final_average_yearly_temperature_trend = (a,b)
    a,b = calculateLinearRegressionFromMap(station.ushcn_final_average_yearly_temperature_record, "fake")
    station.final_fake_average_yearly_temperature_trend = (a,b)
    a,b = calculateLinearRegressionFromMap(station.ushcn_final_average_yearly_temperature_record, "real")
    station.final_real_average_yearly_temperature_trend = (a,b)

    if (number_of_days_above_max_threshold > 0.0) :
        station.average_first_day_above_max_threshold = first_day_above_max_threshold_total / len(station.first_day_above_max_threshold_map)
        station.average_last_day_above_max_threshold = last_day_above_max_threshold_total / len(station.first_day_above_max_threshold_map)

    #print(currentFunctionName(), station.NAME, "Average last day above max threshold", station.average_last_day_above_max_threshold)
    if (station.average_first_day_above_max_threshold > 0.0) :
        total_average_first_day_above_max_threshold += station.average_first_day_above_max_threshold
        total_average_last_day_above_max_threshold += station.average_last_day_above_max_threshold
        number_of_stations_reporting_days_above_max_threshold += 1.0

    if (number_of_days_below_min_threshold > 0.0) :
        station.average_first_day_below_min_threshold = first_day_below_min_threshold_total / len(station.first_day_below_min_threshold_map)
        station.average_last_day_below_min_threshold = last_day_below_min_threshold_total / len(station.first_day_below_min_threshold_map)

    #print(currentFunctionName(), station.NAME, "Average last day above max threshold", station.average_last_day_below_min_threshold)
    if (station.average_first_day_below_min_threshold > 0.0) :
        total_average_first_day_below_min_threshold += station.average_first_day_below_min_threshold
        total_average_last_day_below_min_threshold += station.average_last_day_below_min_threshold
        number_of_stations_reporting_days_below_min_threshold += 1.0

average_first_day_above_max_threshold = 0.0
average_last_day_above_max_threshold = 0.0
if (number_of_stations_reporting_days_above_max_threshold > 0.0) :
    average_first_day_above_max_threshold = total_average_first_day_above_max_threshold / number_of_stations_reporting_days_above_max_threshold
    average_last_day_above_max_threshold = total_average_last_day_above_max_threshold / number_of_stations_reporting_days_above_max_threshold
print(currentFunctionName(), "Average first day above max threshold", average_first_day_above_max_threshold)
print(currentFunctionName(), "Average last day above max threshold", average_last_day_above_max_threshold)
average_first_day_below_min_threshold = 0.0
average_last_day_below_min_threshold = 0.0
if (number_of_stations_reporting_days_below_min_threshold > 0.0) :
    average_last_day_below_min_threshold = total_average_last_day_below_min_threshold / number_of_stations_reporting_days_below_min_threshold
    average_first_day_below_min_threshold = total_average_first_day_below_min_threshold / number_of_stations_reporting_days_below_min_threshold
print(currentFunctionName(), "Average last day below min threshold", average_last_day_below_min_threshold)
print(currentFunctionName(), "Average first day below min threshold", average_first_day_below_min_threshold)


for year in range(FIRST_YEAR, LAST_YEAR+1) :
    yearly_raw_max_average = 0.0
    yearly_final_max_average = 0.0
    yearly_final_real_max_average = 0.0
    yearly_final_fake_max_average = 0.0
    yearly_final_fake_max_percent = 0.0
    yearly_final_fake_max_station_count = yearly_final_fake_max_station_count_map[year]
    yearly_final_fake_max_data_count = yearly_final_fake_max_data_count_map[year]
    yearly_final_real_max_station_count = yearly_final_real_max_station_count_map[year]
    yearly_final_real_max_data_count = yearly_final_real_max_data_count_map[year]
    yearly_final_max_ignored_data_count = yearly_final_raw_max_data_which_was_ignored_count_map[year]
    index = year - FIRST_YEAR
    if (yearly_raw_max_station_count_map[year] > 0.0) :
        yearly_raw_max_average = yearly_raw_max_total_map[year] / yearly_raw_max_station_count_map[year]
        data_dict[USHCN_RAW_TMAX][index] = yearly_raw_max_average
    if (yearly_final_max_station_count_map[year] > 0.0) :
        yearly_final_max_average = yearly_final_max_total_map[year] / yearly_final_max_station_count_map[year]
        data_dict[USHCN_FINAL_TMAX][index] = yearly_final_max_average
    if (yearly_final_max_station_count_map[year] > 0.0 and yearly_raw_max_station_count_map[year] > 0.0) :
        yearly_final_max_adjustment = yearly_final_max_average - yearly_raw_max_average
        data_dict[USHCN_FINAL_MINUS_RAW_TMAX][index] = yearly_final_max_adjustment
    if (yearly_final_real_max_station_count_map[year] > 0.0) :
        yearly_final_real_max_average = yearly_final_real_max_total_map[year] / yearly_final_real_max_station_count_map[year]
        data_dict[USHCN_FINAL_REAL_TMAX][index] = yearly_final_real_max_average
    if (yearly_final_fake_max_station_count_map[year] > 0.0) :
        yearly_final_fake_max_average = yearly_final_fake_max_total_map[year] / yearly_final_fake_max_station_count_map[year]
        data_dict[USHCN_FINAL_FAKE_TMAX][index] = yearly_final_fake_max_average
    if (yearly_final_fake_max_station_count_map[year] > 0.0 and yearly_final_real_max_station_count_map[year] > 0.0) :
        yearly_final_fake_minus_real = yearly_final_fake_max_average - yearly_final_real_max_average
        data_dict[USHCN_FINAL_FAKE_MINUS_REAL_TMAX][index] = yearly_final_fake_minus_real
        yearly_final_fake_max_percent = yearly_final_fake_max_data_count / (yearly_final_fake_max_data_count + yearly_final_real_max_data_count) * 100.0
        data_dict[USHCN_FINAL_PERCENT_FAKE_TMAX][index] = yearly_final_fake_max_percent
        yearly_final_real_max_ignored_percent = yearly_final_max_ignored_data_count / yearly_final_fake_max_data_count * 100.0
        data_dict[USHCN_FINAL_PERCENT_IGNORED_TMAX][index] = yearly_final_real_max_ignored_percent
        data_dict[USHCN_FINAL_COUNT_IGNORED_TMAX][index] = yearly_final_max_ignored_data_count

    yearly_raw_average_average = 0.0
    yearly_final_average_average = 0.0
    yearly_final_real_average_average = 0.0
    yearly_final_fake_average_average = 0.0
    yearly_final_fake_average_percent = 0.0
    yearly_final_fake_average_station_count = yearly_final_fake_average_station_count_map[year]
    yearly_final_fake_average_data_count = yearly_final_fake_average_data_count_map[year]
    yearly_final_real_average_station_count = yearly_final_real_average_station_count_map[year]
    yearly_final_real_average_data_count = yearly_final_real_average_data_count_map[year]
    yearly_final_average_ignored_data_count = yearly_final_raw_average_data_which_was_ignored_count_map[year]
    index = year - FIRST_YEAR
    if (yearly_raw_average_station_count_map[year] > 0.0) :
        yearly_raw_average_average = yearly_raw_average_total_map[year] / yearly_raw_average_station_count_map[year]
        data_dict[USHCN_RAW_TAVG][index] = yearly_raw_average_average
    if (yearly_final_average_station_count_map[year] > 0.0) :
        yearly_final_average_average = yearly_final_average_total_map[year] / yearly_final_average_station_count_map[year]
        data_dict[USHCN_FINAL_TAVG][index] = yearly_final_average_average
    if (yearly_final_average_station_count_map[year] > 0.0 and yearly_raw_average_station_count_map[year] > 0.0) :
        yearly_final_average_adjustment = yearly_final_average_average - yearly_raw_average_average
        data_dict[USHCN_FINAL_MINUS_RAW_TAVG][index] = yearly_final_average_adjustment
    if (yearly_final_real_average_station_count_map[year] > 0.0) :
        yearly_final_real_average_average = yearly_final_real_average_total_map[year] / yearly_final_real_average_station_count_map[year]
        data_dict[USHCN_FINAL_REAL_TAVG][index] = yearly_final_real_average_average
    if (yearly_final_fake_average_station_count_map[year] > 0.0) :
        yearly_final_fake_average_average = yearly_final_fake_average_total_map[year] / yearly_final_fake_average_station_count_map[year]
        data_dict[USHCN_FINAL_FAKE_TAVG][index] = yearly_final_fake_average_average
    if (yearly_final_fake_average_station_count_map[year] > 0.0 and yearly_final_real_average_station_count_map[year] > 0.0) :
        yearly_final_fake_minus_real = yearly_final_fake_average_average - yearly_final_real_average_average
        data_dict[USHCN_FINAL_FAKE_MINUS_REAL_TAVG][index] = yearly_final_fake_minus_real
        yearly_final_fake_average_percent = yearly_final_fake_average_data_count / (yearly_final_fake_average_data_count + yearly_final_real_average_data_count) * 100.0
        data_dict[USHCN_FINAL_PERCENT_FAKE_TAVG][index] = yearly_final_fake_average_percent
        yearly_final_real_average_ignored_percent = yearly_final_average_ignored_data_count / yearly_final_fake_average_data_count * 100.0
        data_dict[USHCN_FINAL_PERCENT_IGNORED_TAVG][index] = yearly_final_real_average_ignored_percent
        data_dict[USHCN_FINAL_COUNT_IGNORED_TAVG][index] = yearly_final_average_ignored_data_count


ushcn_raw_max_trend_total = 0.0
ushcn_raw_max_trend_count = 0.0
ushcn_final_max_trend_total = 0.0
ushcn_final_max_trend_count = 0.0
ushcn_max_positive_adjustment_total = 0.0
ushcn_max_positive_adjustment_count = 0.0
ushcn_max_negative_adjustment_total = 0.0
ushcn_max_negative_adjustment_count = 0.0

printToFile("Stations used in this analysis")
printToFile("Name,State,Country,ID,Latitude,Longitude,elevation,First Year,Last Year,First Day Above Max Threshold,Last Day Above Max Threshold,Last Spring Day Below Min Threshold,First Autumn Day Below Min Threshold,First Day Above Max Target Century Trend,Last Day Above Max Target Century Trend,Max Trend,Last Day Below Min Target Century Trend,First Day Below Min Target Century Trend,Min Trend,Raw Max Trend,Final Max Trend,Difference Between Final Max Trend And Raw Max Trend,Final Measured Max Trend,Final Estmated Max Trend,Difference Between Final Estmated Max Trend And Final Measured Max Trend,Max Temperature On Target Date,Min Temperature On Target Date")
for station in station_list:
    trend_effect = station.final_max_yearly_temperature_trend[0] - station.raw_max_yearly_temperature_trend[0]
    if ("USC" in station.ID or station.ID in ghcn_ushcn_map.values()) :
        ushcn_raw_max_trend_count += 1.0
        ushcn_raw_max_trend_total += station.raw_max_yearly_temperature_trend[0]
        ushcn_final_max_trend_count += 1.0
        ushcn_final_max_trend_total += station.final_max_yearly_temperature_trend[0]
        if (trend_effect > 0.0) :
            ushcn_max_positive_adjustment_total += trend_effect
            ushcn_max_positive_adjustment_count += 1.0
        else :
            ushcn_max_negative_adjustment_total += trend_effect
            ushcn_max_negative_adjustment_count += 1.0

    printToFile(station.NAME
          ,",", station.STATE
          ,",", station.COUNTRY
          ,",", station.ID
          ,",", station.LATITUDE
          ,",", station.LONGITUDE
          ,",", station.ELEVATION
          ,",", station.first_year
          ,",", station.last_year
          ,",", station.average_first_day_above_max_threshold
          ,",", station.average_last_day_above_max_threshold
          ,",", station.average_last_day_below_min_threshold
          ,",", station.average_first_day_below_min_threshold
          ,",", station.first_day_above_max_threshold_trend[0] * 100.0
          ,",", station.last_day_above_max_threshold_trend[0] * 100.0
          ,",", station.max_yearly_temperature_trend[0] * 100.0
          ,",", station.last_day_below_min_threshold_trend[0] * 100.0
          ,",", station.first_day_below_min_threshold_trend[0] * 100.0
          ,",", station.min_yearly_temperature_trend[0] * 100.0
          ,",", station.raw_max_yearly_temperature_trend[0]
          ,",", station.final_max_yearly_temperature_trend[0]
          ,",", station.final_max_yearly_temperature_trend[0] - station.raw_max_yearly_temperature_trend[0]
          ,",", station.final_real_max_yearly_temperature_trend[0]
          ,",", station.final_fake_max_yearly_temperature_trend[0]
          ,",", station.final_fake_max_yearly_temperature_trend[0] - station.final_real_max_yearly_temperature_trend[0]
          ,",", station.target_date_max_temperature
          ,",", station.target_date_min_temperature
          )

if (ushcn_raw_max_trend_count > 0) :
    average_raw_max_trend = ushcn_raw_max_trend_total / ushcn_raw_max_trend_count
else :
    average_raw_max_trend = 0.0

if (ushcn_final_max_trend_count > 0) :
    average_final_max_trend = ushcn_final_max_trend_total / ushcn_final_max_trend_count
else :
    average_final_max_trend = 0.0

if ((ushcn_max_positive_adjustment_count > 0 or ushcn_max_negative_adjustment_count) > 0) :
    percent_of_max_stations_adjusted_upwards = ushcn_max_positive_adjustment_count / (ushcn_max_positive_adjustment_count + ushcn_max_negative_adjustment_count) * 100.0
else :
    percent_of_max_stations_adjusted_upwards = 0.0

if (ushcn_max_positive_adjustment_count > 0) :
    average_positive_max_adjustment = ushcn_max_positive_adjustment_total / ushcn_max_positive_adjustment_count
else :
    average_positive_max_adjustment = 0.0
if (ushcn_max_negative_adjustment_count > 0) :
    average_negative_max_adjustment = ushcn_max_negative_adjustment_total / ushcn_max_negative_adjustment_count
else :
    average_negative_max_adjustment = 0.0

printToFile("Station Count,Average Raw Trend,Average Final Trend,Average Final Minus Raw Trend,Number Of Stations Adjusted Upwards,Number Of Stations Adjusted Downwards,Percent Of Stations Adjusted Upwards,Average Positive Adjustment,Average Negative Adjustment")
printToFile(ushcn_final_max_trend_count
        ,",", average_raw_max_trend
        ,",", average_final_max_trend
        ,",", average_final_max_trend - average_raw_max_trend
        ,",", ushcn_max_positive_adjustment_count
        ,",", ushcn_max_negative_adjustment_count
        ,",", percent_of_max_stations_adjusted_upwards
        ,",", average_positive_max_adjustment
        ,",", average_negative_max_adjustment
        )

total_first_day_above_max_threshold_map = {}
total_last_day_above_max_threshold_map = {}
number_of_stations_above_max_threshold_map = {}
total_first_day_below_min_threshold_map = {}
total_last_day_below_min_threshold_map = {}
number_of_stations_below_min_threshold_map = {}
spring_number_of_stations_below_min_threshold_map = {}
autumn_number_of_stations_below_min_threshold_map = {}

for year in range(FIRST_YEAR, LAST_YEAR+1) :
    total_first_day_above_max_threshold_map[year] = 0.0
    total_last_day_above_max_threshold_map[year] = 0.0
    number_of_stations_above_max_threshold_map[year] = 0.0
    spring_number_of_stations_below_min_threshold_map[year] = 0.0
    autumn_number_of_stations_below_min_threshold_map[year] = 0.0
    total_first_day_below_min_threshold_map[year] = 0.0
    total_last_day_below_min_threshold_map[year] = 0.0
    number_of_stations_below_min_threshold_map[year] = 0.0

for station in station_list:
    for year in range(FIRST_YEAR, LAST_YEAR+1) :
        if (year in station.first_day_above_max_threshold_map) :
            total_first_day_above_max_threshold_map[year] += station.first_day_above_max_threshold_map[year]
            total_last_day_above_max_threshold_map[year] += station.last_day_above_max_threshold_map[year]
            number_of_stations_above_max_threshold_map[year] += 1.0
        if (year in station.last_day_below_min_threshold_map) :
            total_last_day_below_min_threshold_map[year] += station.last_day_below_min_threshold_map[year]
            spring_number_of_stations_below_min_threshold_map[year] += 1.0
        if (station.first_day_below_min_threshold_map[year] < DAYS_PER_YEAR + 1) :
            total_first_day_below_min_threshold_map[year] += station.first_day_below_min_threshold_map[year]
            autumn_number_of_stations_below_min_threshold_map[year] += 1.0
        if ( year in station.last_day_below_min_threshold_map or (station.first_day_below_min_threshold_map[year] < DAYS_PER_YEAR + 1) ) :
            number_of_stations_below_min_threshold_map[year] += 1.0

for year in range(FIRST_YEAR, LAST_YEAR+1) :
    if (number_of_stations_above_max_threshold_map[year] > 0.0) :
        percent_of_stations_above_max_threshold = number_of_stations_above_max_threshold_map[year] / len(station_dict[year]) * 100.0
        data_dict[PERCENT_TO_REACH_MAX_TARGET].append(percent_of_stations_above_max_threshold)
        average_first_day_above_max_threshold = total_first_day_above_max_threshold_map[year] / number_of_stations_above_max_threshold_map[year]
        data_dict[AVERAGE_FIRST_DAY_ABOVE_MAX_THRESHOLD].append(average_first_day_above_max_threshold)
        average_last_day_above_max_threshold = total_last_day_above_max_threshold_map[year] / number_of_stations_above_max_threshold_map[year]
        data_dict[AVERAGE_LAST_DAY_ABOVE_MAX_THRESHOLD].append(average_last_day_above_max_threshold)
    else :
        data_dict[PERCENT_TO_REACH_MAX_TARGET].append(0.0)
        data_dict[AVERAGE_FIRST_DAY_ABOVE_MAX_THRESHOLD].append(0.0)
        data_dict[AVERAGE_LAST_DAY_ABOVE_MAX_THRESHOLD].append(0.0)

    if (number_of_stations_below_min_threshold_map[year] > 0.0 and len(station_dict[year]) > 0) :
        percent_of_stations_below_min_threshold = number_of_stations_below_min_threshold_map[year] / len(station_dict[year]) * 100.0
        data_dict[PERCENT_TO_REACH_MIN_TARGET].append(percent_of_stations_below_min_threshold)
    else :
        data_dict[PERCENT_TO_REACH_MIN_TARGET].append(0.0)

    if (autumn_number_of_stations_below_min_threshold_map[year] > 0.0) :
        average_first_day_below_min_threshold = total_first_day_below_min_threshold_map[year] / autumn_number_of_stations_below_min_threshold_map[year]
        data_dict[AVERAGE_FIRST_DAY_BELOW_MIN_THRESHOLD].append(average_first_day_below_min_threshold)
    else :
        data_dict[AVERAGE_FIRST_DAY_BELOW_MIN_THRESHOLD].append(0.0)

    if (spring_number_of_stations_below_min_threshold_map[year] > 0.0) :
        average_last_day_below_min_threshold = total_last_day_below_min_threshold_map[year] / spring_number_of_stations_below_min_threshold_map[year]
        data_dict[AVERAGE_LAST_DAY_BELOW_MIN_THRESHOLD].append(average_last_day_below_min_threshold)
    else :
        data_dict[AVERAGE_LAST_DAY_BELOW_MIN_THRESHOLD].append(0.0)

X_AXIS = YEAR
Y_AXIS = AVERAGE_MAXIMUM_TEMPERATURE
X_AXIS_TYPE = "x axis type"
Y_AXIS_TYPE = "y axis type"

class MyButton :
    def __init__(self, axis_type, axes, name) :
        self.axis_type = axis_type
        self.button = Button(axes, name)
        self.button.on_clicked(self.onClicked)
        self.name = name

    def onClicked(self, event) :
        global X_AXIS
        global Y_AXIS
        global current_x_list_button
        global current_y_list_button


        if (self in x_button_list) :
            current_x_list_button.button.color = "lightgrey"
            self.button.color = "Turquoise"
            current_x_list_button = self
        elif (self in y_button_list) :
            current_y_list_button.button.color = "lightgrey"
            self.button.color = "Turquoise"
            current_y_list_button = self

        if (self.axis_type == X_AXIS_TYPE) :
            X_AXIS = self.name
        elif (self.axis_type == Y_AXIS_TYPE) :
            Y_AXIS = self.name

        plot_1.clear()
        title_string = createTitleString()
        print("title_string =", title_string)
        plot_1.set_title(title_string, fontsize=14, fontweight='bold', y=1.04)
        x_label = X_AXIS
        y_label = Y_AXIS
        if (target_month != 0 and target_day != 0) :
            if ("Percent Of Days" in x_label) :
                x_label = x_label.replace("Percent Of Days", "Percent Of Stations")
            if ("Percent Of Days" in y_label) :
                y_label = y_label.replace("Percent Of Days", "Percent Of Stations")
        if ("Temperature" in x_label) :
            x_label += " (F)"
        if ("Temperature" in y_label) :
            y_label += " (F)"
        if ("CO2" in x_label) :
            x_label += " (PPM)"
        if ("CO2" in y_label) :
            y_label += " (PPM)"
        plot_1.set_xlabel(x_label)
        plot_1.set_ylabel(y_label)
        x_list = copy.deepcopy(data_dict[X_AXIS])
        y_list = copy.deepcopy(data_dict[Y_AXIS])
        #print("X Axis list size = ", len(x_list), "Y Axis list size = ", len(y_list))

        # Remove the first year and current year from absolute count plots
#        if (("Number Of" in X_AXIS or "Number Of" in Y_AXIS) and (LAST_YEAR == current_time.year)) :
#            del x_list[-1]
#            del y_list[-1]
#            del x_list[0]
#            del y_list[0]
#
        #if (len(x_list) != len(y_list)) :
            #return

        # Make the list sizes the same
        while (len(x_list) > len(y_list)) :
            del x_list[-1]
        while (len(y_list) > len(x_list)) :
            del y_list[-1]

        if (len(y_list) < 1 or len(x_list) < 1) :
            print(currentFunctionName(), "Can't plot empty list")
            return

        maximum = -10000.0
        minimum = 10000.0
        maximum_x = 0
        minimum_x = 0
        average = 0.0
        total = 0.0
        for index in range(0, len(x_list)) :
            total += y_list[index]
            if (y_list[index] > maximum) :
                maximum = y_list[index]
                maximum_x = x_list[index]
            if (y_list[index] < minimum) :
                minimum = y_list[index]
                minimum_x = x_list[index]
        maximum_round = round(maximum)
        minimum_round = round(minimum)
        maximum_x_round = round(maximum_x)
        minimum_x_round = round(minimum_x)
        average = total / len(y_list)
        label_text = "(" + str(maximum_x_round) + ", " + str(maximum_round) + ")"
        plot_1.text(maximum_x + (maximum_x * 0.00) , maximum, label_text, fontsize=12)
        label_text = "(" + str(minimum_x_round) + ", " + str(minimum_round) + ")"
        plot_1.text(minimum_x + (minimum_x * 0.00) , minimum, label_text, fontsize=12)

        if (X_AXIS == YEAR) :
            try :
                plot_1.plot(x_list, y_list)
                #plotFiveYearMean(plot_1, x_list, y_list)
                plotMean(plot_1, MEAN_WIDTH, x_list, y_list)
            except :
                printException()
                do_nothing = True
        else :
            try :
                plot_1.scatter(x_list, y_list)
            except :
                do_nothing = True
        try :
            if ("USHCN" not in X_AXIS and "USHCN" not in Y_AXIS and PLOT_TREND) :
                # USHCN monthly plots may have a different number of years than daily
                # so don't try to do a linear regression
                plotLinearRegression(plot_1, data_dict[X_AXIS], data_dict[Y_AXIS])
        except :
            do_nothing = True
        #plot_1.imshow(Toto, aspect='auto', extent=(minimum_x, minimum, 2.0, 2.0), zorder=-1)
        #fig.canvas.toolbar.setVisible(True)
        plt.show()


def plotMean(subplot, number_of_years, x_list, y_list) :
    data_size = len(x_list)
    mean_x = []
    mean_y = []
    half_range = int(number_of_years / 2)

    for index in range(half_range, data_size-half_range) :
        mean_x.append(x_list[index])
        y_sum = 0.0
        for offset in range(0, number_of_years) :
            y_sum += y_list[index-half_range+offset]
        mean_y.append(y_sum / float(number_of_years))
    subplot.plot(mean_x, mean_y, "r-", linewidth=4.0)

def plotFiveYearMean(subplot, x_list, y_list) :
    data_size = len(x_list)
    five_year_mean_x = []
    five_year_mean_y = []

    for index in range(2, data_size-2) :
        five_year_mean_x.append(x_list[index])
        y_sum = 0.0
        for offset in range(0, 5) :
            y_sum += y_list[index-2+offset]
        five_year_mean_y.append(y_sum / 5.0)
    subplot.plot(five_year_mean_x, five_year_mean_y, "r-", linewidth=4.0)


def plotLinearRegression(subplot, x, y) :
    a, b = calculateLinearRegression(x, y)
    lr = []
    for i in range(0, len(x)) :
        lr.append( (a * x[i]) + b)
    subplot.plot(x, lr, "r--", linewidth=2.0)


def saveImage(event) :
    title_string = createTitleString()
    file_name_string = stripString(title_string)
    filename = file_name_string + ".png"
    print(filename)
    extent = plot_1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, bbox_inches=extent.expanded(1.2, 1.30))
    os.chmod(filename, 0o777)
    #fig.canvas.toolbar.setVisible(True)
    #plt.show()


def visitToto(event) :
    webbrowser.open('http://realclimatescience.com')

fig = plt.figure(figsize=(18, 10))
plt.subplots_adjust(left=0.4)
plot_1 = fig.add_subplot(111)
number_of_buttons = len(plot_types_list)
button_height = 1.0 / float(number_of_buttons) * 0.7
button_width = 0.17
button__spacing = 0.002
x_button_list = []
y_button_list = []
current_x_list_button = 0
current_y_list_button = 0

toto_button = Button(plt.axes([0.1, 0.84, 0.11, 0.11]), "", image=Toto)
toto_button.on_clicked(visitToto)
save_image_button = Button(plt.axes([0.27, 0.87, 0.06, 0.05]), "Save\n Image", color="Turquoise", hovercolor="Green")
save_image_button.on_clicked(saveImage)


title_button = Button(plt.axes([0.085, 0.96, 0.15, 0.03]), "UNHIDING THE DECLINE", color="lightblue", hovercolor="yellow")
#title_button.on_clicked(visitToto)
title_button.label.set_fontsize(14)
title_button.label.set_fontweight("bold")

x_position = button__spacing
y_position = 0.02
for plot_type in plot_types_list :
    button = MyButton(X_AXIS_TYPE, plt.axes([x_position, y_position, button_width, button_height]), plot_type)
    x_button_list.append(button)
    y_position += button_height + button__spacing
    if (plot_type == YEAR) :
        current_x_list_button = button
        current_x_list_button.button.color = "Turquoise"
x_axis_button = Button(plt.axes([x_position, y_position, button_width, button_height]), "X AXIS", color="Green", hovercolor="Green")

x_position += button_width + button__spacing
y_position = 0.02
for plot_type in plot_types_list :
    button = MyButton(Y_AXIS_TYPE, plt.axes([x_position, y_position, button_width, button_height]), plot_type)
    y_button_list.append(button)
    y_position += button_height + button__spacing
    if (plot_type == AVERAGE_MAXIMUM_TEMPERATURE) :
        current_y_list_button = button
        current_y_list_button.button.color = "Turquoise"
y_axis_button = Button(plt.axes([x_position, y_position, button_width, button_height]), "Y AXIS", color="Green", hovercolor="Green")


csv_fd.close()
#os.chmod(csv_filename, 0o777)


if (state_arg != "") :
    out_filename = state_arg + ".list"
    fd = open(out_filename, "w")
    for station in stations_used_name_map :
        fd.write(station + ".dly\n")
    fd.close()
    os.chmod(out_filename, 0o777)
else :
    out_filename = "last_run.list"
    fd = open(out_filename, "w")
    for station in station_list :
        fd.write(station.ID + ".dly" + " : " + station.NAME.rstrip() + " " + station.STATE + " " + str(station.LATITUDE) + " " + str(station.LONGITUDE) + "\n")
    fd.close()
    os.chmod(out_filename, 0o777)

if (DONT_PLOT == False) :
    plot_1.set_title(title_string, fontsize=14, fontweight='bold', y=1.04)
    plot_1.set_xlabel('Year', fontsize=14)
    plot_1.set_ylabel('Temperature (F)', fontsize=14)
    current_x_list_button.onClicked(0)
    current_y_list_button.onClicked(0)
    #plot_1.plot(data_dict[YEAR], data_dict[AVERAGE_MAXIMUM_TEMPERATURE])
    #plotFiveYearMean(plot_1, data_dict[YEAR], data_dict[AVERAGE_MAXIMUM_TEMPERATURE])
    #plotLinearRegression(plot_1, data_dict[X_AXIS], data_dict[Y_AXIS])
    plt.show()
    #Sfig.canvas.toolbar.setVisible(True)




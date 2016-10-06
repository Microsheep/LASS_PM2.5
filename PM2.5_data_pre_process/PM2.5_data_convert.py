# Import libraries
from datetime import datetime

# Select data
FULL_DATA = False

# Generate DATA_RANGE constants and set RESULT_CSV_NAME
if FULL_DATA:
    DATA_RANGE = []
    for i in range(1,32):
        DATA_RANGE.append('8'+str(i).zfill(2))
    for i in range(1,26):
        DATA_RANGE.append('9'+str(i).zfill(2))
    RESULT_CSV_NAME = "20160801_to_20160925.csv"
else:
    DATA_RANGE = [918, 919, 920, 921, 922, 923, 924, 925]
    RESULT_CSV_NAME = "20160918_to_20160925.csv"

# Define CORRUPTED_LIST which are attibutes that we don't want
COR_LIST = ["s_h00", "s_h0_d1", "s_h0d1", "s_h0s_d1", "s_s_d1", "s_"]

# Define all data_types (Run a search against all the data from 8/01~9/25 using another code)
all_types = [
    'app','co','county','date','device','device_id','fake_gps','fmt_opt','fpmi',
    'gps_alt','gps_fix','gps_lat','gps_lon','gps_num','h','majorpollutant','name',
    'no','no2','nox','o3','pm10','pm2_5','psi','publishtime','s0','s1','s2','s_0',
    's_1','s_2','s_3','s_4','s_d0','s_d1','s_d2','s_g8','s_h0','s_h2','s_t0','s_t2',
    'siteengname','siteid','sitename','sitetype','so2','status','t','tick','time',
    'ver_app','ver_format','winddirec','windspeed'
]

t_int = [
    'fake_gps','fmt_opt',
    'gps_fix','gps_num',
    't','h','pm2_5','pm10',
    'fpmi','psi',
    's_0','s_1','s_2','s_4',
    's_d2','s_g8',
    'tick','ver_format'
]

t_float = [
    's0','s1','s2',
    's_3',
    's_d0','s_d1',
    's_t0','s_t2','s_h0','s_h2',
    'co','o3','so2','no','no2','nox',
    'gps_alt','gps_lat','gps_lon',
    'winddirec','windspeed'
]

t_datetime = [
    'date','time','publishtime'
]

t_char = [
    'app','county','name','ver_app',
    'device','device_id',
    'majorpollutant','status',
    'siteengname','siteid','sitename','sitetype'
]

# Check if we missed anything
assert(all_types == sorted(t_int+t_float+t_datetime+t_char))

# Function to get rid of unwanted values
def find_special_value(Key, Value):
    if  Value in ["-", "_", "na", "NA", "nan", "NaN", "NaN.00", "undefined", "undefined.00"]:
        return ""
    else:
        return Value.strip().replace('\x00', '')

def full_zero_string(s):
    for i in s:
        if i != '0':
            return False
    return True

def check_float_int(s):
    if s == "":
        return True
    if s[0] in ('-', '+'):
        cs = s[1:].split(".")
    else:
        cs = s.split(".")
    if len(cs) == 1:
        return cs[0].isdigit()
    elif len(cs) == 2:
        return cs[0].isdigit() and full_zero_string(cs[1])
    else:
        return False

def check_float(s):
    if s == "":
        return True
    if s[0] in ('-', '+'):
        cs = s[1:].split(".")
    else:
        cs = s.split(".")
    if len(cs) == 1:
        return cs[0].isdigit()
    elif len(cs) == 2:
        return cs[0].isdigit() and cs[1].isdigit()
    else:
        return False

# Change data into csv for database import
f_csv = open(RESULT_CSV_NAME, "w+", encoding="utf-8")

# Write the first line
a_l = ""
for at in all_types:
    a_l = a_l+at+","
f_csv.write(a_l[:-1]+"\n")

# Import each data log and translate it to
for i in DATA_RANGE:
    f_name = "data.log-20160"+str(i)
    print("Importing(type): "+f_name)
    f_data = open(f_name, "r", encoding="utf-8").readlines()
    for l in f_data:
        # Split data using "|"
        l_split = l[:-1].split('|')
        l_split = list(filter(None, l_split))
        data_template = {}
        # Remove list with no "|"
        if len(l_split) <= 1:
            continue
        else:
            data_template['name'] = l_split[0][:-1]
        # Parse data and see if data is corrupted
        # See if there is a strange parameter with 0 or more than 1 "="
        corrupt = False
        type_corrupt = ""
        for d in l_split[1:]:
            h_d = d.split("=")
            if len(h_d) == 2:
                Key = h_d[0].lower()
                sv = find_special_value(Key, h_d[1])
                if Key in COR_LIST or Key in data_template.keys():
                    corrupt = True
                    break
                else:
                    if Key in t_int:
                        if not check_float_int(sv):
                            type_corrupt = "int: " + Key + " |" + sv + "|"
                            corrupt = True
                            break
                        else:
                            sv = sv.split(".")[0]
                    elif Key in t_float:
                        if sv != "":
                            if sv[0] == '.':
                                sv = '0' + sv
                            elif (sv[0] == '+' or sv[0] == '-') and sv[1] == '.':
                                sv = sv[0] + '0' + sv[1:]
                            elif sv[-1] == ".":
                                sv = sv + '0'
                            else:
                                pass
                        if not check_float(sv):
                            type_corrupt = "float: " + Key + " |" + sv + "|"
                            corrupt = True
                            break
                    elif Key in t_datetime:
                        if Key == 'date':
                            # 2016-07-31
                            try:
                                datetime.strptime(sv, "%Y-%m-%d")
                            except:
                                type_corrupt = "date: " + Key + " |" + sv + "|"
                                corrupt = True
                                break
                        elif Key == 'time':
                            # 06:23:16
                            try:
                                datetime.strptime(sv, "%H:%M:%S")
                            except:
                                type_corrupt = "time: " + Key + " |" + sv + "|"
                                corrupt = True
                                break
                        elif Key == 'publishtime':
                            # 2016-09-18 08:00
                            try:
                                datetime.strptime(sv, "%Y-%m-%d %H:%M")
                            except:
                                type_corrupt = "publishtime: " + Key + " |" + sv + "|"
                                corrupt = True
                                break
                        else:
                            type_corrupt = "NONE_DATETIME: " + Key + " |" + sv + "|"
                            corrupt = True
                            break
                    else:
                        pass
                    data_template[Key] = sv
            else:
                corrupt = True
                break
        # If not corrupt write it to csv else print out the corrupted data
        if not corrupt and data_template != {}:
            d_l = ""
            for at in all_types:
                d_l = d_l + data_template.get(at, "") + ","
            f_csv.write(d_l[:-1]+"\n")
        else:
            if type_corrupt != "":
                print("### "+type_corrupt)
                print(l)

f_csv.close()

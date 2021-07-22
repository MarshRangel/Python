import xml.etree.ElementTree as ET
import random
import pandas as pd
import numpy as np
import operator
from itertools import product

def vectorize_values(name, x_, y_):
    # print(name, x_, y_)
    # list_name = [name]
    # list_x = [x_]
    # list_y = [y_]
    pre_data = np.array([x_, y_])
    data = [name, pre_data]
    print(data)
    # pre_data = [[list_name, list_x, list_y]]
    # for data in pre_data:
    #     data.append(data)
    #     print(data)

    result = {}
    for d in data:
        print(d)
        maxi = max(d[1])
        print(maxi)
        arr = np.zeros(maxi + 2)
        aft = 0
        for n in range(len(arr)):
            if n - 1 in d[1]:
                i = d[1].index(n - 1)
                aft = d[2][i]
                arr[n] = aft
            else:
                arr[n] = aft
        result[d[0]] = arr
        break

    print(result)

def extract_signals(signals_df):
    num_signals = len(signals_df)
    names_list = [name for name in signals_df['Name'].unique()]
    # print(names_list)

    for pos, name in enumerate(names_list):
        # print(pos, name)
        # get data
        data = signals_df[signals_df["Name"] == name]["Value"]
        x_ = np.hstack([-1, data.index.values, len(signals_df) - 1])
        y_ = np.hstack([0, data.values, data.iloc[-1]])
        # Data to vectorize
        vectorize_values(name, x_, y_)

file_xml = ET.parse('example_a_child4.xml')
rootXML = file_xml.getroot()

data_XML = [
    {"Name": signal.attrib["Name"],
     "Value": int(signal.attrib["Value"].split(' ')[0])
     } for signal in file_xml.findall(".//Signal")
]
signals_df = pd.DataFrame(data_XML)

extract_signals(signals_df)

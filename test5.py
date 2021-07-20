import xml.etree.ElementTree as ET
import random
import pandas as pd
import numpy as np
import operator
from itertools import product

file_xml = ET.parse('example_a_child4.xml')
rootXML = file_xml.getroot()

def vectorize_values(num_signals, name, x_, y_):
    print(num_signals, name, x_, y_)

    # for item in product(*zip(x_, y_)):
    #     print(item)

    # combined_dict = {}
    # for i, j in zip(x_, y_):
    #     combined_dict[i] = j
    # print(combined_dict)

    zipped = zip(name, x_, y_)
    # print(zipped)

    for i, (pos, val) in enumerate(zip(x_, y_)):
        pass
        # print(i, pos, val)

    for pos, val in zip(x_, y_):
        pass
        # print(pos, val)

    for i in y_:
        pass
        # print(i)
        for j in x_:
            pass
            # print(i)

    # for i in x_:
    #     print(i)
    # for j in y_:
    #     print(j)
    # if i > 0 & i != 1:
    #     zeros = np.zeros(i, dtype=int)
    #     print(zeros)

def extract_signals(signals_df):
    num_signals = len(signals_df)
    names_list = [name for name in signals_df['Name'].unique()]
    # print(names_list)

    for pos, name in enumerate(names_list):
        # print(pos, name)
        # get data
        data = signals_df[signals_df["Name"] == name]["Value"]
        x_ = np.hstack([data.index.values, len(signals_df) - 1])
        y_ = np.hstack([0, data.values, data.iloc[-1]])
        # Data to vectorize
        vectorize_values(num_signals, name, x_, y_)

data_XML = [
    {"Name": signal.attrib["Name"],
     "Value": int(signal.attrib["Value"].split(' ')[0])
     } for signal in file_xml.findall(".//Signal")
]
signals_df = pd.DataFrame(data_XML)

extract_signals(signals_df)

import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd

list_fin = []
attributes1 = []
attributes2 = []
attributes3 = []

def testcase(rootXML):
    file_xml = ET.parse(rootXML)
    root = file_xml.getroot() #Project

    for child in root:  # Testspec
        for child2 in child:  # FunctionArea
            for child3 in child2:  # Usecase
                for child4 in child3:  # Testcase
                    if child4.attrib["Id"] == '150860':
                        for child5 in child4:  # Flowchart
                            for child6 in child5:  # Flowchart.Precons_Events
                                for child7 in child6:  # Act_CANOut, Paralell, Act_DiagnosticIn, Act_SequenceNote, Act_HapticIn, etc.
                                    levelChild7(child7)

def levelChild7(child7):
    global attributes1, list_fin
    if child7.tag == 'Parallel':
        for child8 in child7:
            for child9 in child8:
                levelChild9(child9)
    elif child7.tag == 'TimeRequirement':
        for child8 in child7:
            for child9 in child8:
                levelChild9(child9)
    else:  # Act_CANOut, Act_CANIn
        for child8 in child7:
            attributes1 = [
                {
                    "Name": child8.attrib['Name'],
                    "Value": int(child8.attrib['Value'].split(' ')[0])
                }
            ]
            list_fin += attributes1
            return list_fin

def levelChild9(child9):
    global attributes2, attributes3, list_fin
    if child9.tag == 'TimeRequirement':
        for child10 in child9:
            for child11 in child10:
                attributes2 = [
                    {
                        "Name": child11.attrib['Name'],
                        "Value": int(child11.attrib['Value'].split(' ')[0])
                    }
                ]
                list_fin += attributes2
                return list_fin

    else:  # Act_CANOut, Act_CANIn
        for child10 in child9:
            attributes3 = [
                {
                    "Name": child10.attrib['Name'],
                    "Value": int(child10.attrib['Value'].split(' ')[0])
                }
            ]
            list_fin += attributes3
            return list_fin

def conver_dataframe(rootXML):
    testcase(rootXML)
    signals_df = pd.DataFrame(list_fin)
    print(signals_df)

            
rootXML = 'Audio_Setting_[SyncG3].pxml'
# testcase(rootXML)
conver_dataframe(rootXML)

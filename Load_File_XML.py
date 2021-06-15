#Import Python Modules
from tkinter import *
import os, shutil, easygui
import xml.etree.ElementTree as ET
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import time
from datetime import timedelta

# Code efficiency - start
start = time.monotonic()

# Root configuration
root = Tk()
root.title("Graphical Analysis of Signals of a XML")
root.geometry("1024x820")
root.pack_propagate(False)
root.config(bd=15)

# Function to copy the file in the path
def copyfile(sourcexml):
    global source
    source=os.path.realpath(sourcexml)
    dest = shutil.copy(source,os.getcwd())
    return dest

# Functions to open xml file
def open_file():
    try:
        global temxml, xml_Name
        xml_Name = str(easygui.fileopenbox(title='Select xml file', default='*.xml'))
        if str(os.path.abspath(xml_Name)) != os.path.join(os.path.abspath(os.getcwd()), os.path.basename(xml_Name)):
            menssage.set("Opened xml file: ", xml_Name)
            tempxml = copyfile(xml_Name)
            # buttons(os.path.basename(str(tempxml)))
            transfor_data_atri(os.path.basename(str(tempxml)))
        else:
            # buttons(os.path.basename(str(xml_Name)))
            transfor_data_atri(os.path.basename(str(xml_Name)))
    except FileNotFoundError:
        print('XML file was not loaded.')

# Function to delete the file xml
def delete_file():
    os.remove(xml_Name)

# Function to close window
def exit_win():
    try:
        root.quit()
        root.destroy()
        delete_file()
        print('XML file removed')
    except NameError:
        print('XML file was not loaded..')
    except FileNotFoundError:
        print('XML file was not loaded...')

# Function to download graph image file
def downloadImage():
    pass
    #plot.savefig('graph_lines.png')

# Function to display buttons and choose the TestCase to be plotted
def buttons(xml_Name):
    print("File: ", xml_Name)
    file_xml = ET.parse(xml_Name)
    data_xml = [
        {"Name": signal.attrib["Name"],
         } for signal in file_xml.findall(".//Child_4")
    ]

    for i in data_xml:
        dict_tc = str(i.values()).replace('dict_values([\'', '')
        name_tc = dict_tc.replace('\'])', '')
        Button(root, text=f"TC> {name_tc}", command=downloadImage).pack()
        # Button(root, text=f"TC> {name_tc}", command=downloadImage).grid(column=0, row=0)

    # transfor_data_atri(xml_Name)

# Function to transform xml file to DataFrame
def transfor_data_atri(rootXML):
    print("File: ", rootXML)
    file_xml = ET.parse(rootXML)
    data_xml = [
        {"Name": signal.attrib["Name"],
         # "Value": signal.attrib["Value"]
         "Value": int(signal.attrib["Value"].split(' ')[0])
         } for signal in file_xml.findall(".//Signal")
    ]
    # print(data_xml)

    signals_df = pd.DataFrame(data_xml)
    # print(signals_df)
    # count_signal = signals_df.groupby('Name')['Value'].count()
    # print(count_signal)

    extract_name_value(signals_df)

# Function to extract the Name and Value attributes
def extract_name_value(signals_df):
    # print(_signals)

    # for i in _signals.Name:
    #     signal = _signals[_signals.Name.isin([i])]
    #     row_values = signal.T
    #     vector = row_values.iloc[[1]]
    #     print(vector)

    names_list = [
        'Status', 'SetDSP', 'HMI', 'Delay', 'AutoConfigO_Rear',
        'AutoConfigO_Front', 'AutoConfigO_Drvr','AutoConfigO_Allst',
        'RUResReqstStat', 'RUReqstrSystem', 'RUSource', 'DSP'
    ]
    # print(names_list)

    # for i in signals_df.Name:
    #     names_list = i
    #     signals = signals_df[signals_df["Name"] == names_list]
    #     print(signals)
    #     matplotcanvas(signals)


    signals = signals_df[signals_df["Name"].isin(names_list)]
    # print(signals)
    matplotcanvas(signals)

# Function to graph the values of the DataFrame
def matplotcanvas(signals):
    print(signals)

    graphic = plt.Figure(figsize=(30, 25), dpi=80)

    lines = graphic.add_subplot(111)
    line1 = FigureCanvasTkAgg(graphic, framegraphic)
    line1.get_tk_widget().pack(side=LEFT, fill=BOTH)

    # signals.plot(kind='line', rot=110, ax=lines, marker='o', x="Name", legend=True)
    signals.plot(kind='bar', rot=90, ax=lines, x="Name", legend=True)

    #lines.set_ylim(0, 8)
    lines.set_title(' Signal changes every occur', fontsize=24)
    lines.set_xlabel(' Signal Name', fontsize=18)
    lines.set_ylabel(' Signal Value', fontsize=18)

# Initial buttons
#Button(root, text="Back", command=back).pack(side='left')
Button(root, text="Download Chart", command=downloadImage).pack(side='bottom')
# Button(root, text="Download Chart", command=downloadImage).grid(row=0, column=2, sticky=SE)

# Frame for the chart
framegraphic = Frame(width='800', height='600')
framegraphic.pack(side='bottom', padx=1, pady=1)

# Top Menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open File", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_win)
menubar.add_cascade(menu=filemenu, label="File xml")

# Lower Monitor
menssage = StringVar()
menssage.set("Open xml file to produce a graph based on  signals and repetitions of these signals")
monitor = Label(root, textvar=menssage, justify='left')
monitor.pack(side="top")

# See the menu
root.config(menu=menubar)

# App loop
root.mainloop()

# Code efficiency - end
end = time.monotonic()
print('Duration: ', timedelta(seconds=end - start))

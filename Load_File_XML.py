#Import Python Modules
from re import split
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
            # child_4_separate(os.path.basename(str(tempxml)))
            transfor_data_atri(os.path.basename(str(tempxml)))
        else:
            # child_4_separate(os.path.basename(str(xml_Name)))
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

# Function to display buttons and choose the Child_4 to be plotted
def child_4_separate(xml_Name):
    # print("File: ", xml_Name)
    file_xml = ET.parse(xml_Name)
    data_xml = [
        {
            "Name": signal.attrib["Name"],
            "Id": signal.attrib["Id"],
         } for signal in file_xml.findall(".//Child_4")
    ]
    # print(data_xml)

    for i in data_xml:
        id_tc = i.get('Id')
        dict_tc = str(i.values()).replace('dict_values([\'', '')
        name_tc = dict_tc.replace('\'])', '')
        Button(root, text=f"TC> {name_tc}", command=lambda x=xml_Name, y=id_tc: transfor_data_atri_child_4(x, y)).pack()


# Function to transform xml file to DataFrame
def transfor_data_atri_child_4(rootXML, id_tc):
    print("File: ", rootXML)
    print("id_tc: ", id_tc)
    file_xml = ET.parse(rootXML)
    # data_tc = [
    #     signal for signal in file_xml.findall(".//Child_4/")
    # ]
    data_tc = [
        signal for signal in file_xml.findall(".//Child_4[@Id='150860']/")
    ]
    # print(data_tc)

    data_tc_df = pd.DataFrame(data_tc)
    print("data_tc_df", data_tc_df)

    data_out = [
        signal for signal in file_xml.findall(".//Child_7_d")
    ]
    # print(data_out)

    data_can_in = [
        signal for signal in file_xml.findall(".//Child_7_da")
    ]
    # print(data_in)

    data_signals = [
        {"Name": signal.attrib["Name"],
         # "Value": signal.attrib["Value"]
         "Value": int(signal.attrib["Value"].split(' ')[0])
         } for signal in file_xml.findall(".//Signal")
    ]
    # print(data_signals)


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
    # print(signals_df.groupby(['Name']).size())
    # print(signals_df)
    # count_signal = signals_df.groupby('Name')['Value'].count()
    # print(count_signal)

    extract_name_value(signals_df)

# Function to extract the Name and Value attributes
def extract_name_value(signals_df):
    # print(signals_df)
    names_list = [name for name in signals_df['Name'].unique()]
    num_names_list = len(names_list)

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    # Creation Graphic
    fig = plt.figure(figsize=(18, 20))
    plt.suptitle(f'File PXML: {rootXML}', fontsize=20, fontweight='bold', color='SteelBlue', position=(0.75, 0.90))
    fig.tight_layout()
    i = 1
    for name in names_list:
        # get data
        data = signals_df[signals_df["Name"] == name]["Value"]
        datax = signals_df["Name"]
        # x = [n for n in range(len(data))]
        x = [n for n in range(len(datax))]
        print(x)
        # get color
        j = random.randint(0, len(colors) - 1)
        # add subplots
        ax = plt.subplot(num_names_list, 1, i)
        ax.plot(x, data, drawstyle='steps', marker='o', color=colors[j], linewidth=3)
        # plt.xticks(None)
        # ax.step(x, data, marker='o')
        ax.set_ylabel(name, fontsize=12, fontweight='bold', color='SteelBlue', rotation=50, labelpad=45)
        ax.grid(alpha=0.4)
        i += 1

    plt.show()

    # for i in can_signals.Name:
    #     signal = can_signals[can_signals.Name.isin([i])]
    #     row_values = signal.T
    #     vector = row_values.iloc[[1]]
    #     print(vector)

    # signals = signals_df[signals_df["Name"].isin(names_list)]
    # print(signals)
    # matplotcanvas(signals)

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

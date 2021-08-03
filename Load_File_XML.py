# Import Python Modules
import tkinter as tk
from tkinter import ttk
import os, shutil, easygui
import random
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import time
from datetime import timedelta

# Code efficiency - start
start = time.monotonic()

# Root configuration
root = tk.Tk()
root.title("Graphical Analysis of Signals of a XML")
root.geometry("1280x1024")
root.pack_propagate(False)
root.config(bd=15)


# Function to copy the file in the path
def copyfile(sourcexml):
    global source
    source = os.path.realpath(sourcexml)
    dest = shutil.copy(source, os.getcwd())
    return dest


# Functions to open xml file
def open_file():
    try:
        global temxml, xml_Name
        xml_Name = str(easygui.fileopenbox(title='Select xml file', default='*.xml'))
        if str(os.path.abspath(xml_Name)) != os.path.join(os.path.abspath(os.getcwd()), os.path.basename(xml_Name)):
            menssage.set("Opened xml file: ", xml_Name)
            tempxml = copyfile(xml_Name)
            display_buttons(os.path.basename(str(tempxml)))
        else:
            display_buttons(os.path.basename(str(xml_Name)))
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
    # plot.savefig('graph_lines.png')


# Function to display buttons and choose the Child_4 to be plotted
def display_buttons(xml_Name):
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
        tk.Button(root, text=f"TC> {name_tc}", command=lambda x=xml_Name, y=id_tc: extract_values_xml(x, y)).pack()


def extract_values_xml(pxml_name, id_tc):
    data_can_signals = []
    data_p_can_signals = []
    file_xml = ET.parse(pxml_name)
    root = file_xml.getroot()  # root
    for child in root:  # Child_1
        for child2 in child:  # Child_2
            for child3 in child2:  # Child_3
                for child4 in child3:  # Child_4
                    if child4.attrib["Id"] == id_tc:
                        for child5 in child4:  # Child_5
                            for child6 in child5:  # Child_6.a_Cons, Child_6.b_Events
                                for child7 in child6:  # Child_7_a,b,c,d,e,f...
                                    if child7.tag in ['Child_7_d']:
                                        for child8 in child7:
                                            attributes1 = [
                                                {"Name": child8.attrib["Name"],
                                                 "Value": int(child8.attrib["Value"].split(' ')[0])
                                                 }
                                            ]
                                            data_can_signals += attributes1
                                    elif child7.tag in ['Child_7_p']:
                                        # p = child7.attrib["Id"]
                                        # print(p)
                                        for child8 in child7:
                                            for child9 in child8:
                                                if child9.tag in ['Child_9_t']:
                                                    for child10 in child9:
                                                        for child11 in child10:
                                                            attributes3 = [
                                                                {"Name": child11.attrib["Name"],
                                                                 "Value": int(child11.attrib["Value"].split(' ')[0])
                                                                 }
                                                            ]
                                                            data_can_signals += attributes3
                                                            data_p_can_signals += attributes3
                                                else:
                                                    for child10 in child9:
                                                        attributes2 = [
                                                            {"Name": child10.attrib["Name"],
                                                             "Value": int(child10.attrib["Value"].split(' ')[0])
                                                             }
                                                        ]
                                                        data_can_signals += attributes2
                                                        data_p_can_signals += attributes2
    p_signals_df = pd.DataFrame(data_p_can_signals)
    signals_df = pd.DataFrame(data_can_signals)
    # print(signals_df)
    plot_signals(signals_df, p_signals_df, pxml_name, id_tc)


# Function to extract the Name and Value attributes
def plot_signals(signals_df, p_signals_df, rootXML, id_tc):
    print(p_signals_df)
    names_list = [name for name in signals_df['Name'].unique()]
    num_names_list = len(names_list)
    num_axisx = len(signals_df["Name"])

    colors = ['b', 'g', 'r', 'c', 'm', 'y']

    # Creation Graphics
    fig, ax = plt.subplots(nrows=num_names_list, figsize=(20, 30), sharex=True)
    plt.suptitle('File PXML: {0}, TestCase:{1}'.format(rootXML, id_tc), fontsize=16, fontweight='bold',
                 color='SteelBlue', position=(0.60, 0.99))
    plt.xticks(np.arange(0, num_axisx), color='SteelBlue', fontweight='bold')
    i = 1
    for pos, (a_, name) in enumerate(zip(ax, names_list)):
        # get name axis-y
        if len(name.split('_')) == 2:
            names = name.split('_')[0] + "\n" + name.split('_')[1]
        elif len(name.split('_')) == 3:
            names = name.split('_')[0] + "\n" + name.split('_')[1] + "\n" + name.split('_')[2]
        else:
            names = name
        # get data
        data = signals_df[signals_df["Name"] == name]["Value"]
        # get color
        j = random.randint(0, len(colors) - 1)
        # get values axis-x and axis-y
        x_ = np.hstack([-1, data.index.values, len(signals_df) - 1])
        y_ = np.hstack([0, data.values, data.iloc[-1]])
        # plotting the data by index = pos
        ax[pos].plot(x_, y_, drawstyle='steps-post', marker='o', color=colors[j], linewidth=3)
        ax[pos].set_ylabel(names, fontsize=8, fontweight='bold', color='SteelBlue', rotation=30, labelpad=35)
        ax[pos].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        ax[pos].yaxis.set_tick_params(labelsize=6)
        ax[pos].grid(alpha=0.4)
        i += 1
        # Code to label the markers with the values
        for i in range(len(y_)):
            if i == 0:
                xy = [x_[0], y_[0]]
            else:
                xy = [x_[i - 1], y_[i - 1]]
            ax[pos].text(x=xy[0], y=xy[1], s=str(xy[1]), color='k', fontsize=10, rotation=345)

    # plt.show()
    # Embedded chart in Tkinter window
    canvas = FigureCanvasTkAgg(fig, frame_graphic)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
    # Navigation bar for the chart
    toolbar_frame = tk.Frame(master=root)
    toolbar_frame.grid(row=22, column=4)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()

# Frame for the chart
frame_graphic = tk.Frame(width='1024', height='768')
frame_graphic.pack(side='bottom', padx=1, pady=1)

# Top Menu
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open File", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_win)
menubar.add_cascade(menu=filemenu, label="File XML")

# Lower Monitor
menssage = tk.StringVar()
menssage.set("Open PXML file to produce a graph based on CAN signals and repetitions of these signals")
monitor = tk.Label(root, textvar=menssage, justify='left')
monitor.pack(side="top")

# See the menu
root.config(menu=menubar)

# Code efficiency - end
end = time.monotonic()
print('Duration: ', timedelta(seconds=end - start))

# App loop
root.mainloop()

import tkinter as tk
import os, easygui
import xml.etree.ElementTree as ET
import random
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Root configuration
root = tk.Tk()
root.title("Graphical Analysis of Signals of a XML")
root.geometry("1024x820")
root.pack_propagate(False)
root.config(bd=15)
# Functions to open xml file
def open_file():
    try:
        global temxml, xml_Name
        xml_Name = str(easygui.fileopenbox(title='Select xml file', default='*.xml'))
        if str(os.path.abspath(xml_Name)) != os.path.join(os.path.abspath(os.getcwd()), os.path.basename(xml_Name)):
            # child_4_separate(os.path.basename(str(tempxml)))
            transfor_data_atri(os.path.basename(str(xml_Name)))
        else:
            # child_4_separate(os.path.basename(str(xml_Name)))
            transfor_data_atri(os.path.basename(str(xml_Name)))
    except FileNotFoundError:
        print('XML file was not loaded.')

# Function to close window
def exit_win():
    try:
        root.quit()
        root.destroy()
        print('XML file removed')
    except NameError:
        print('XML file was not loaded..')
    except FileNotFoundError:
        print('XML file was not loaded...')

def transfor_data_atri(rootXML):
    file_xml = ET.parse(rootXML)
    data_XML = [
        {"Name": signal.attrib["Name"],
         "Value": int(signal.attrib["Value"].split(' ')[0])
         } for signal in file_xml.findall(".//Signal")
    ]

    signals_df = pd.DataFrame(data_XML)
    extract_name_value(signals_df, rootXML)

# Function to extract the Name and Value attributes
def extract_name_value(signals_df, rootXML):
    # print(signals_df)
    # Initial part is same as yours
    names_list = [name for name in signals_df['Name'].unique()]
    num_names_list = len(names_list)
    num_axisx = len(signals_df["Name"])

    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    # start new figure
    # fig = plt.figure(figsize=[20, 30], dpi=200)
    fig, ax = plt.subplots(nrows=num_names_list, figsize=(20, 30), sharex=True)
    plt.suptitle(f'File PXML: {rootXML}', fontsize=16, fontweight='bold', color='SteelBlue', position=(0.70, 0.99))
    # plt.xticks(np.arange(0, num_axisx), color='SteelBlue', fontweight='bold')
    # start a loop with the subplots
    for i in range(len(names_list)):
        plt.subplot(num_names_list, 1, i + 1)
        # choose color
        col = np.random.randint(0, len(colors) - 1)
        # get the locations of the values with the similar name in your list
        locs = signals_df['Name'] == names_list[i]
        # get the values in those locations
        data = signals_df['Value'][locs]
        # arrange the x and y coordinates
        x = np.hstack([-1, data.index.values, len(signals_df) - 1])
        y = np.hstack([0, data.values, data.iloc[-1]])
        # plot the values as usual
        plt.plot(x, y, drawstyle='steps-post', marker='o', color=colors[col], linewidth=3)
        plt.ylabel(names_list[i], fontsize=8, fontweight='bold', color='SteelBlue', rotation=30, labelpad=35)
        plt.grid(alpha=0.4)
        # Annotating the values
        for j in range(len(x)):
            if j % 2 == 0:
                plt.annotate(round((y[j])), (x[j], y[j]), xycoords='data',
                             xytext=(-10, 10), textcoords='offset points', color="k", fontsize=8)
            else:
                plt.annotate(round((y[j])), (x[j], y[j]), xycoords='data',
                             xytext=(-10, -10), textcoords='offset points', color="k", fontsize=8)

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
frame_graphic = tk.Frame(width='1024', height='896')
frame_graphic.pack(side='bottom', padx=1, pady=1)

# Top Menu
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open File", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_win)
menubar.add_cascade(menu=filemenu, label="File PXML")

# See the menu
root.config(menu=menubar)

# App loop
root.mainloop()

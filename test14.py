import os, easygui
import random
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
import matplotlib.ticker as matTicker
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")
# fig = plt.figure()

def popupmsg(msg):
    popup = tk.Tk()

    def leavemini():
        popup.destroy()

    popup.wm_title("!!!")
    label = ttk.Label(popup, text=msg, font=NORMAL_FONT)
    label.pack(side="top", fill="x", padx=10, pady=10)
    button1 = ttk.Button(popup, text="Okay", command=leavemini)
    button1.pack()
    popup.mainloop()


class AppCVD(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Graphical Analysis of a XML")
        # tk.Tk.geometry(self, "1280x1024")

        container = tk.Frame(self)
        container.pack(side="top", fill="both")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # container.config(cursor="heart", relief="sunken")

        self.frames = {}

        for F in (StartWindow, WindowOne, WindowTwo, WindowThree):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartWindow)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Press the button to open the XML file:", font=LARGE_FONT)
        label.place(relx=.01, rely=.01)

        # Function to display buttons and choose the TestCase to be plotted
        def separate_tc(xml_name):
            # print("File: ", XML_Name)
            file_xml = ET.parse(xml_name)
            tc_xml = [
                {"Name": signal.attrib["Name"],
                 "Id": signal.attrib["Id"],
                 } for signal in file_xml.findall(".//Child_4")
            ]
            # print(len(tc_xml))
            controller.show_frame(WindowOne.select_tc(self, tc_xml))

        # Functions to open xml file
        def open_file():
            global xml_name
            # if xml_name == '':
            try:
                xml_name = str(easygui.fileopenbox(title='Select XML file', default='*.xml'))
                if str(os.path.abspath(xml_name)) != os.path.join(os.path.abspath(os.getcwd()),
                                                                   os.path.basename(xml_name)):
                    separate_tc(os.path.basename(str(xml_name)))
                else:
                    separate_tc(os.path.basename(str(xml_name)))
            except FileNotFoundError:
                print('XML file was not loaded.')

        button_open = ttk.Button(self, text="Open File XML", command=open_file)
        # button_open = ttk.Button(self, text="Open File XML", command=lambda: popupmsg("Not supported just yet!!"))
        button_open.place(relx=.01, rely=.35)


class WindowOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Select the TestCase you want to plot:", font=LARGE_FONT)
        label.pack(pady=5, padx=5)

        button_back = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartWindow))
        button_back.pack()

    def select_tc(self, tc_xml):
        for i in tc_xml:
            id_tc = i.get('Id')
            dict_tc = str(i.values()).replace('dict_values([\'', '')
            with_apo = dict_tc.replace('\'])', '')
            name_tc = with_apo.replace("'", "")
            buttons_tc = tk.Button(self, text=f"TC> {name_tc}",
                                command=lambda x=xml_name, y=id_tc:
                                WindowTwo.extract_values_xml(self, x, y))
            buttons_tc.pack(pady=3)


class WindowTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="TestCase Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

    # Function to extract the Name, Value, Id_Act and Id_Par attributes
    def extract_values_xml(self, xml_name, id_tc):
        global signals_df
        data_signals = []
        file_xml = ET.parse(xml_name)
        root = file_xml.getroot()
        for child in root:
            for child2 in child:
                for child3 in child2:
                    for child4 in child3:
                        if child4.attrib["Id"] == id_tc:
                            for child5 in child4:
                                for child6 in child5:
                                    for child7 in child6:
                                        if child7.tag in ['Child_7_d', 'Child_7_di']:
                                            for child8 in child7:  # CANSignal
                                                attributes1 = [
                                                    {"Name": child8.attrib["Name"],
                                                     "Value": int(child8.attrib["Value"].split(' ')[0]),
                                                     "Id_Act": int(child7.attrib["Id"]),
                                                     "Id_Par": 0
                                                     }
                                                ]
                                                data_signals += attributes1
                                        elif child7.tag in ['Child_9_t', 'Child_9_l']:
                                            for child8 in child7:
                                                for child9 in child8:
                                                    attributes2 = [
                                                        {"Name": child9.attrib["Name"],
                                                         "Value": int(child9.attrib["Value"].split(' ')[0]),
                                                         "Id_Act": int(child8.attrib["Id"]),
                                                         "Id_Par": 0
                                                         }
                                                    ]
                                                    data_signals += attributes2
                                        elif child7.tag in ['Child_7_p']:
                                            for child8 in child7:
                                                for child9 in child8:
                                                    if child9.tag in ['Child_9_t']:
                                                        for child10 in child9:
                                                            for child11 in child10:
                                                                attributes3 = [
                                                                    {"Name": child11.attrib["Name"],
                                                                     "Value": int(
                                                                         child11.attrib["Value"].split(' ')[0]),
                                                                     "Id_Act": int(child10.attrib["Id"]),
                                                                     "Id_Par": int(child7.attrib["Id"])
                                                                     }
                                                                ]
                                                                data_signals += attributes3
                                                    else:
                                                        for child10 in child9:
                                                            attributes4 = [
                                                                {"Name": child10.attrib["Name"],
                                                                 "Value": int(child10.attrib["Value"].split(' ')[0]),
                                                                 "Id_Act": int(child9.attrib["Id"]),
                                                                 "Id_Par": int(child7.attrib["Id"])
                                                                 }
                                                            ]
                                                            data_signals += attributes4
                                        elif child7.tag in ['Child_9_d']:
                                            for child8 in child7:
                                                for child9 in child8:
                                                    for child10 in child9:
                                                        attributes5 = [
                                                            {"Name": child10.attrib["Name"],
                                                             "Value": int(child10.attrib["Value"].split(' ')[0]),
                                                             "Id_Act": int(child9.attrib["Id"]),
                                                             "Id_Par": int(child9.attrib["Id"])
                                                             }
                                                        ]
                                                        data_signals += attributes5

        signals_df = pd.DataFrame(data_signals)
        print(signals_df, id_tc)
        WindowThree.plot_signals(self, signals_df, xml_name, id_tc)


class WindowThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button_back = ttk.Button(self, text="Select Another TestCase",
                             command=lambda: controller.show_frame(WindowTwo))
        button_back.pack()

    def plot_signals(self, signals, rootXML, id_tc):
        # Count can signals by parallel
        signals['Count'] = signals.groupby('Id_Par').cumcount().add(1).mask(signals['Id_Par'].eq(0), 0)
        # Subtract Parallel values from the index column
        signals['Sub'] = signals.index - signals['Count']
        id_par_prev = signals['Id_Par'].unique()
        id_par = np.delete(id_par_prev, 0)
        signals['Prev'] = [1 if x in id_par else 0 for x in signals['Id_Par']]
        signals['Final'] = signals['Prev'] + signals['Sub']
        # Convert and set Subtract to index
        signals.set_index('Final', inplace=True)

        # Get individual variables names for the chart
        names_list = [name for name in signals['Name'].unique()]
        num_names_list = len(names_list)
        colors = ['b', 'g', 'r', 'c', 'm', 'y']

        # Matplotlib's categorical feature and to convert x-axis values to string
        x_values = [-1, ]
        x_values += (list(set(signals.index)))
        x_values = [str(i) for i in sorted(x_values)]

        # Creation Graphics
        f, ax = plt.subplots(nrows=num_names_list, figsize=(15, 20), sharex=True)
        # ax = plt.subplots(nrows=num_names_list, sharex=True)
        plt.suptitle('File XML: {0}, TestCase:{1}'.format(rootXML, id_tc), fontsize=14, fontweight='bold',
                     color='SteelBlue', position=(0.60, 0.99))
        plt.xticks(color='SteelBlue', fontweight='bold')
        for pos, (a_, name) in enumerate(zip(ax, names_list)):
            # Creating a dummy plot and then remove it with Matplotlib's categorical variables
            dummy, = ax[pos].plot(x_values, np.zeros_like(x_values))
            dummy.remove()
            # Get name axis-y
            if len(name.split('_')) == 2:
                names = name.split('_')[0] + "\n" + name.split('_')[1]
            elif len(name.split('_')) == 3:
                names = name.split('_')[0] + "\n" + name.split('_')[1] + "\n" + name.split('_')[2]
            else:
                names = name
            # Get data
            data = signals[signals["Name"] == name]["Value"]
            # Get color
            # j = random.randint(0, len(colors) - 1)
            # Get values axis-x and axis-y
            x_ = np.hstack([-1, data.index.values, len(signals) - 1])
            y_ = np.hstack([0, data.values, data.iloc[-1]])
            # Plotting the data by position
            ax[pos].plot(x_.astype('str'), y_, drawstyle='steps-post', marker='*', markersize=8,
                         linewidth=2)  # color=colors[j],
            ax[pos].set_ylabel(names, fontsize=8, fontweight='bold', color='SteelBlue', rotation=30, labelpad=35)
            ax[pos].yaxis.set_major_formatter(matTicker.FormatStrFormatter('%0.1f'))
            ax[pos].yaxis.set_tick_params(labelsize=6)
            ax[pos].grid(alpha=0.4, color='SteelBlue')
            # Labeling the markers with CAN-Values
            for i in range(len(y_)):
                if i == 0:
                    xy = [x_[0].astype('str'), y_[0]]
                else:
                    xy = [x_[i - 1].astype('str'), y_[i - 1]]
                ax[pos].text(x=xy[0], y=xy[1], s=str(xy[1]), color='k', fontweight='bold', fontsize=12)

        # plt.show()
        # Embedded chart in Tkinter window
        canvas = FigureCanvasTkAgg(f)
        canvas.get_tk_widget().pack()
        # Navigation bar for the chart
        # toolbar = tk.Frame(master=self)
        # toolbar.place(relx=1270, rely=5)  # 1280x1024
        # toolbar = NavigationToolbar2Tk(canvas, toolbar)
        # toolbar.update()
        # canvas.tkcanvas.pack()


app = AppCVD()
app.geometry("1280x720")
app.mainloop()

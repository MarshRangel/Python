import os, easygui
import xml.etree.ElementTree as ET
import pandas as pd

import tkinter as tk
from tkinter import *  # ttk, Button, Message

LARGE_FONT = ("Verdana", 12)


class AppMain(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Graphical XML file analysis")
        tk.Tk.geometry(self, "1280x1024")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # container.config(cursor="heart", relief="sunken")

        self.frames = {}

        for F in (StartWindow, WindowOne, WindowTwo):
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

        def separate_tc(xml_name):
            file_xml = ET.parse(xml_name)
            tc_xml = [
                {"Name": signal.attrib["Name"],
                 "Id": signal.attrib["Id"],
                 } for signal in file_xml.findall(".//Child_4")
            ]
            print(len(tc_xml))
            WindowOne.select_tc(self, tc_xml)
            # PageOne.__init__(self, parent, controller).select_tc(self, tc_xml)

        # Functions to open pxml file
        def open_file():
            global xml_name
            # if pxml_name == '':
            try:
                xml_name = str(easygui.fileopenbox(title='Select XML file', default='*.xml'))
                if str(os.path.abspath(xml_name)) != os.path.join(os.path.abspath(os.getcwd()),
                                                                   os.path.basename(xml_name)):
                    separate_tc(os.path.basename(str(xml_name)))
                else:
                    separate_tc(os.path.basename(str(xml_name)))
            except FileNotFoundError:
                print('XML file was not loaded.')

        button_open = Button(self, text="Open File XML", command=open_file)
        button_open.place(relx=.01, rely=.04)


class WindowOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Select the TestCase:", font=LARGE_FONT)
        label.pack(pady=5, padx=5)

        button_back = Button(self, text="Back to Home", command=lambda: controller.show_frame(StartWindow))
        button_back.pack()

    def select_tc(self, tc_xml):
        for i in tc_xml:
            id_tc = i.get('Id')
            dict_tc = str(i.values()).replace('dict_values([\'', '')
            with_apo = dict_tc.replace('\'])', '')
            name_tc = with_apo.replace("'", "")
            buttons_tc = Button(self, text=f"TC> {name_tc}",
                                command=lambda x=xml_name, y=id_tc:
                                WindowTwo.extract_can_values_xml(x, y))
            buttons_tc.pack(pady=3)
            # print(range(len(tc_xml)))
            # buttons_tc.place(relx=0.05, rely=0.05)


class WindowTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Child4 Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Select Another Child4",
                         command=lambda: controller.show_frame(WindowOne))
        button1.pack()
        # Message(self,extract_can_values_xml(xml_name, id_tc))

    # Function to extract the Name, Value, Id_Act and Id_Par attributes
    def extract_can_values_xml(xml_name, id_tc):
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
                                            for child8 in child7:
                                                attributes1 = [
                                                    {"Name": child8.attrib["Name"],
                                                     "Value": int(child8.attrib["Value"].split(' ')[0]),
                                                     "Id_Act": int(child7.attrib["Id"]),
                                                     "Id_Par": 0
                                                     }
                                                ]
                                                data_signals += attributes1
                                        elif child7.tag in ['Child_7_p']:
                                            for child8 in child7:
                                                for child9 in child8:
                                                    if child9.tag in ['Child_7_t']:
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
                                                            attributes2 = [
                                                                {"Name": child10.attrib["Name"],
                                                                 "Value": int(
                                                                     child10.attrib["Value"].split(' ')[0]),
                                                                 "Id_Act": int(child9.attrib["Id"]),
                                                                 "Id_Par": int(child7.attrib["Id"])
                                                                 }
                                                            ]
                                                            data_signals += attributes2

        signals_df = pd.DataFrame(data_signals)
        print(signals_df)
        # return signals_df
        Message(text=signals_df).place(relx=.2, rely=.2)


if __name__ == "__main__":
    app = AppMain()
    app.mainloop()

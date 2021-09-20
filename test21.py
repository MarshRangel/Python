import os, easygui
import xml.etree.ElementTree as ET

import tkinter as tk
from tkinter import *

import pandas as pd

LARGE_FONT = ("Verdana", 12)

xml_name = ''
tc_xml = []

class AppMain(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Analysis of a XML')

        self.shared_xml = tk.StringVar()  ###### ***

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.shared_df = {'TC': tk.StringVar()}
        self.frames = {}

        for F in (Home, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(Home)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text='File Upload: Press the button to open the XML file.', font=LARGE_FONT)
        label.place(relx=.01, rely=.01)

        # Function to display buttons and choose the TestCase to be plotted
        def separate_tc(xml_name):
            global tc_xml
            file_xml = ET.parse(xml_name)
            tc_xml = [
                {"Name": signal.attrib["Name"],
                 "Id": signal.attrib["Id"],
                 } for signal in file_xml.findall(".//Child_4")
            ]
            controller.shared_xml.set(tc_xml)   ###### *** Assignment of values to variable shared_xml
            print(controller.shared_xml.get())
            controller.show_frame(PageOne)

        # Functions to open xml file
        def open_file():
            global xml_name
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
        button_open.place(relx=.01, rely=.03)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text='Select the TestCase you want to plot:', font=LARGE_FONT)
        label.place(relx=.01, rely=.01)

        controller.shared_xml.get()  ###### *** How do I get the variable tc_xml from the Home class? ***
        print(controller.shared_xml.get())

        for i in tc_xml:
            id_tc = i.get('Id')
            dict_tc = str(i.values()).replace('dict_values([\'', '')
            with_apo = dict_tc.replace('\'])', '')
            name_tc = with_apo.replace("'", "")
            buttons_tc = Button(self, text=f"TC> {name_tc}", command=PageTwo)
            buttons_tc.pack(pady=3)

        button_back = Button(self, text='Back to Home', command=lambda: controller.show_frame(Home))
        button_back.place(relx=.01, rely=.03)



class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page One!!!', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        print("File to graph" + xml_name)
        # self.shared_df = pd.DataFrame(xml_name)

        button_one = Button(self, text='Back to Page One', command=lambda: controller.show_frame(PageOne))
        button_one.pack()
        button_back =Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button_back.pack()


if __name__ == "__main__":
    app = AppMain(None)
    app.geometry("1280x1024")
    app.mainloop()

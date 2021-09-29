import os, easygui
import xml.etree.ElementTree as ET
import tkinter as tk

LARGE_FONT = ("Verdana", 12)

xml_name = ''
tc_xml = []


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text='Select the TestCase you want to plot:', font=LARGE_FONT)
        label.place(relx=.01, rely=.01)

        print("Second TC:", self.controller.shared_data['tc'])

        # for i in self.controller.shared_data['tc']:
        #     print("****: ", i)
        #     print("Name:", i['Name'], "Id:", i['Id'])
        
        ##### For loop to display buttons (combobox) from tc_xml #####
        # for i in tc_xml:
        #     id_tc = i.get('Id')
        #     dict_tc = str(i.values()).replace('dict_values([\'', '')
        #     with_apo = dict_tc.replace('\'])', '')
        #     name_tc = with_apo.replace("'", "")
        #     buttons_tc = Button(self, text=f"TC> {name_tc}", command=PageTwo)
        #     buttons_tc.pack(pady=3)

        def startpage():
            controller.show_frame("StartPage")

        button_back = tk.Button(self, text='Back to Home', command=startpage, relief='raised')
        button_back.place(relx=.01, rely=.05)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text='File Upload: Press the button to open the XML file.', font=LARGE_FONT)
        label.place(relx=.01, rely=.01)

        # Function to separate the tc "Child_4" inside the xml file
        def separate_tc(xml_name):
            global tc_xml
            file_xml = ET.parse(xml_name)
            tc_xml = [
                {"Name": signal.attrib["Name"],
                 "Id": signal.attrib["Id"],
                 } for signal in file_xml.findall(".//Child_4")
            ]
            self.controller.shared_data['tc'] = tc_xml
            print('First TC:', tc_xml)
            controller.show_frame("PageOne")


        # Function to open xml file
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

        button_open = tk.Button(self, text="Open File XML", command=open_file)
        # File test xml: https://github.com/MarshRangel/Python/blob/develop/TestCase.xml
        button_open.place(relx=.01, rely=.05)


class AppMain(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Analysis of a XML')

        self.shared_data = {'tc': []}

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = AppMain(None)
    app.title('Analysis of XML')
    app.geometry("1024x920")
    app.mainloop()

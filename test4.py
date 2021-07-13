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


# function that places the label give the desired position
def place_label(label, xy, position, ax, rend, pad=0.01):
    # annotate in the initial position, xy is the top right corner of the bounding box
    t_ = ax.text(x=xy[0], y=xy[1], s=label, fontsize=16)

    # find useful values
    tbb = t_.get_window_extent(renderer=rend)
    abb = ax.get_window_extent(renderer=rend)
    a_xlim, a_ylim = ax.get_xlim(), ax.get_ylim()

    # now adjust the position if needed
    new_xy = [xy[0], xy[1]]

    relative_width = tbb.width / abb.width * (a_xlim[1] - a_xlim[0])
    pad_x = pad * (a_xlim[1] - a_xlim[0])
    assert (position[0] in ['l', 'c', 'r'])
    if position[0] == 'c':
        new_xy[0] -= relative_width / 2
    elif position[0] == 'l':
        new_xy[0] -= relative_width + pad_x
    else:
        new_xy[0] += pad_x

    relative_height = tbb.height / abb.height * (a_ylim[1] - a_ylim[0])
    pad_y = pad * (a_ylim[1] - a_ylim[0])
    assert (position[1] in ['b', 'c', 't'])
    if position[1] == 'c':
        new_xy[1] -= relative_height / 2
    elif position[1] == 'b':
        new_xy[1] -= relative_height + pad_y
    else:
        new_xy[1] += pad_y

    t_.set_position(new_xy)

    return t_

# Function to extract the Name and Value attributes
def extract_name_value(signals_df, rootXML):
    # print(signals_df)
    names_list = [name for name in signals_df['Name'].unique()]
    num_names_list = len(names_list)
    num_axisx = len(signals_df["Name"])

    colors = ['b', 'g', 'r', 'c', 'm', 'y']

    axes_qty = 9
    axes_gap = 0.035

    fig = plt.figure(figsize=(10, 8))
    ax = [plt.axes([axes_gap, axes_gap / 2 + i * (1 / axes_qty), 1 - 2 * axes_gap, 1 / axes_qty - axes_gap]) for i in
          range(axes_qty)]
    plt.suptitle(f'File XML: {rootXML}', fontsize=16, fontweight='bold', color='SteelBlue', position=(0.75, 0.95))
    plt.xticks(np.arange(-1, num_axisx), color='SteelBlue', fontweight='bold')
    rend = fig.canvas.get_renderer()

    for a_, pos, name in ax, enumerate(names_list):
        # x_ = [random.randint(0, 10) for _ in range(5)]
        # x_ = np.unique(x_)
        # y_ = [random.randint(0, 12) for _ in x_]
        data = signals_df[signals_df["Name"] == name]["Value"]
        # get color
        j = random.randint(0, len(colors) - 1)
        # get plots by index = pos
        x_ = np.hstack([-1, data.index.values, len(signals_df) - 1])
        y_ = np.hstack([0, data.values, data.iloc[-1]])
        # as x is shared, we set the limits in advance, otherwise the adjustments won't be accurate
        a_.set_xlim([-0.5, 10.5])

        # plotting the data
        data_ = [[x_[0], y_[0]]]
        for i in range(1, len(x_)):
            data_ += [[x_[i - 1], y_[i]], [x_[i], y_[i]]]
        a_.plot([d[0] for d in data_], [d[1] for d in data_])

        mid_y = 0.5 * (a_.get_ylim()[0] + a_.get_ylim()[1])

        # now let's label it
        for i in range(len(x_)):
            # decide what point we annotate
            if i == 0:
                xy = [x_[0], y_[0]]
            else:
                xy = [x_[i - 1], y_[i]]

            # decide its position
            position_0 = 'l' if i == 0 else 'r'
            position_1 = 'b' if xy[1] > mid_y else 't'

            place_label(label=str(xy[1]), xy=xy, position=position_0 + position_1, ax=a_, rend=rend)

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
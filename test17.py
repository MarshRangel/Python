import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

data = {'Name': ['immoControlCmd', 'BrkTerrMde', 'GlblClkYr', 'HsaStat', 'TesterPhysicalResGWM', 'FapLc',
                 'FirstRowBuckleDriver', 'GlblClkDay'],
        'Value': [0, 5, 0, 4, 0, 1, 1, 1],
        'Id_Par': [0, 0, 3, 3, 3, 3, 0, 0]
        }

signals_df = pd.DataFrame(data)


def plot_signals(signals_df):
    # Count signals by par
    signals_df['Count'] = signals_df.groupby('Id_Par').cumcount().add(1).mask(signals_df['Id_Par'].eq(0), 0)
    # Subtract Par values from the index column
    signals_df['Sub'] = signals_df.index - signals_df['Count']
    id_par_prev = signals_df['Id_Par'].unique()
    id_par = np.delete(id_par_prev, 0)
    signals_df['Prev'] = [1 if x in id_par else 0 for x in signals_df['Id_Par']]
    signals_df['Final'] = signals_df['Prev'] + signals_df['Sub']
    # signals_df['Finall'] = signals_df['Final'].unique()
    # print(signals_df['Finall'])
    # Convert and set Subtract to index
    signals_df.set_index('Final', inplace=True)
    # pos_x = len(signals_df.index.unique()) - 1
    # print(pos_x)

    # Get individual names and variables for the chart
    names_list = [name for name in signals_df['Name'].unique()]
    num_names_list = len(names_list)
    num_axis_x = len(signals_df["Name"])

    # Creation Graphics
    fig, ax = plt.subplots(nrows=num_names_list, figsize=(10, 10), sharex=True)

    # No longer any need to define where the ticks go, but still set the colour and weight here
    plt.xticks(color='SteelBlue', fontweight='bold')

    # First make a list of all the xticks we want
    xvals = [-1, ]
    for name in names_list:
        xvals.append(signals_df[signals_df["Name"] == name]["Value"].index.values[0])
    xvals.append(len(signals_df) - 1)

    # Reduce to only unique values, sorted, and then convert to strings
    xvals = [str(i) for i in sorted(set(xvals))]

    # To get the ticks in the right order on all subplots, we need to make
    # a dummy plot here and then remove it
    dummy, = ax[0].plot(xvals, np.zeros_like(xvals))
    dummy.remove()

    for pos, (a_, name) in enumerate(zip(ax, names_list)):
        # Get data
        data = signals_df[signals_df["Name"] == name]["Value"]
        # Get values axis-x and axis-y
        x_ = np.hstack([-1, data.index.values, len(signals_df) - 1])
        y_ = np.hstack([0, data.values, data.iloc[-1]])
        # Plotting the data by position
        # NOTE: here we convert x_ to strings as we plot, to make sure they are plotted as catagorical values
        ax[pos].plot(x_.astype('str'), y_, drawstyle='steps-post', marker='*', markersize=8, color='k', linewidth=2)
        ax[pos].set_ylabel(name, fontsize=8, fontweight='bold', color='SteelBlue', rotation=30, labelpad=35)
        ax[pos].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        ax[pos].yaxis.set_tick_params(labelsize=6)
        ax[pos].grid(alpha=0.4, color='SteelBlue')

    plt.show()


plot_signals(signals_df)
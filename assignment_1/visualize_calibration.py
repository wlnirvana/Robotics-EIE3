import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
import os

def draw_graph(logfile_path, logfile_name):
    data = pd.read_csv(logfile_path, sep="\t", header=None)
    fig = plt.figure(1)

    # set figure title
    plt.suptitle(logfile_name)

    ax1 = plt.subplot(211)
    ax1_line1 = plt.plot(data[0],data[2], "g")
    ax1_line2 = plt.plot(data[0],data[1], "b")
    ax1.set_title('Left motor', fontsize=12)
    plt.xlabel('Time [s]', fontsize=12)
    plt.ylabel('Angle [Radians]', fontsize=12)

    # create legends
    green_patch = mpatches.Patch(color='green', label='Actual angle')
    blue_patch = mpatches.Patch(color='blue', label='Reference angle')

    # place legends on the bottom right
    plt.legend(handles=[green_patch, blue_patch], loc=4)
 
    ax2 = plt.subplot(212)
    ax2_line1 = plt.plot(data[0],data[4], "g")
    ax2_line2 = plt.plot(data[0],data[3], "b")
    ax2.set_title('Right motor', fontsize=12)
    plt.xlabel('Time [s]', fontsize=12)
    plt.ylabel('Angle [Radians]', fontsize=12)

    # place legends on the bottom right
    plt.legend(handles=[green_patch, blue_patch], loc=4)

    # prevent overlapping
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # save as png
    graph_path = './graphs/' + logfile_name + '.png'
    plt.savefig(graph_path, dpi=140)

    # do not show the plot, save instead
    # plt.show()

    # close figure to prevent adding different axes on the same plot
    plt.close()

def main():
    """ generate calibration graphs using log files """
    logfile_root = './logs/'

    # travese log file directory
    for dir_path, dir_names, file_names in os.walk(logfile_root):
        for logfile_name in file_names:
            logfile_path = logfile_root + logfile_name
            draw_graph(logfile_path, logfile_name)
            print("graph generated for", logfile_path)

if __name__ == '__main__':
    main()


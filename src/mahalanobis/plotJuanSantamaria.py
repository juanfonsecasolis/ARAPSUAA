# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
import matplotlib.pylab as plt
import csv
import numpy as np
from pylab import figure
import ConfigParser
import os


def run(outImgPath=None):
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    fig = figure()
    fig.add_subplot(111)

    # read points stored in the csv file
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    filename = configParser.get('output', 'airportDataPath')

    data = []
    with open(filename, 'rb') as csvfile:
        x = csv.reader(csvfile, delimiter=',')
        next(x)  # ignore headers
        for row in x:
            data.append([float(row[1])])  # wind
            data.append([float(row[2])])  # rain
    N = len(data) / 2
    data = np.reshape(data, (N, 2))

    # plot points and the mean point
    plt.scatter(data[:, 0], data[:, 1])
    plt.scatter([np.mean(data[:, 0])], [np.mean(data[:, 1])], marker='x')
    plt.xlabel('Viento (km/h)')
    plt.ylabel('Precipitacion anual acumulada (ml)')
    plt.title('Aeropuerto Juan Santamaria 1990-2016')
    plt.grid()

    if outImgPath is None:
        plt.show()
    else:
        plt.savefig(outImgPath)

    os.chdir(cwd)  # restore directory


if __name__ == '__main__':
    run()

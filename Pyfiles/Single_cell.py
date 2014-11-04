import os
import json
import csv
import pandas as pd
import pylab
import matplotlib.pyplot as plt
import matplotlib as mpl
import operator
from pylab import *
import numpy as np
from random import shuffle
from bokeh.plotting import *
import scipy
import plotly.plotly as py
from plotly.graph_objs import *

#Change working directory
os.chdir('/Users/kleppem/Documents/Python/single_cell')

#import file as pandas table and transpose
df = pd.read_csv('JAK2VF_CD452.csv')

#calculate threshold (from zero cell chambers)
def cal_threshold(df):
    zero_cell = df[df.number == 0]
    mean = zero_cell.mean()
    std = zero_cell.std()
    cnames = list(df.columns.values)
    zipped = zip(mean[0:12], std[0:12])
    th = []
    for entry in zipped:
        temp = entry[0] + (2*entry[1])
        th.append(temp)
        TH = zip(cnames, th)
    return TH, th

#substract threshold from raw values and log transform
def minus_threshold(df):
    one_cell = df[df.number == 1]
    d = one_cell.to_dict()
    KC = []
    for item in d['KC'].values():
        temp = item - th[0]
        KC.append(temp)
    TNF = []
    for item in d['TNFa'].values():
        temp = item - th[1]
        TNF.append(temp)
    IL1b = []
    for item in d['IL1b'].values():
        temp = item - th[2]
        IL1b.append(temp)
    IL6 = []
    for item in d['IL6'].values():
        temp = item - th[3]
        IL6.append(temp)
    IL10 = []
    for item in d['IL10'].values():
        temp = item - th[4]
        IL10.append(temp)
    IL12 = []   
    for item in d['IL12'].values():
        temp = item - th[5]
        IL12.append(temp)
    MCP1 = []
    for item in d['MCP1'].values():
        temp = item - th[6]
        MCP1.append(temp)
    MIP1a = []
    for item in d['MIP1a'].values():
        temp = item - th[7]
        MIP1a.append(temp)
    MIP1b = []
    for item in d['MIP1b'].values():
        temp = item - th[8]
        MIP1b.append(temp)
    MIG = []
    for item in d['MIG'].values():
        temp = item - th[9]
        MIG.append(temp)
    RANTES = []
    for item in d['RANTES'].values():
        temp = item - th[10]
        RANTES.append(temp)
    GMCSF = []
    for item in d['GMCSF'].values():
        temp = item - th[10]
        GMCSF.append(temp)
    minus_th = zip(KC, TNF, IL1b, IL6, IL10, IL12, MCP1, MIP1a, MIP1b, MIG, RANTES, GMCSF) 
    minus_th_df = pd.DataFrame(minus_th, columns = ['KC', 'TNF', 'IL1b', 'IL6', 'IL10', 'IL12', 'MCP1', 'MIP1a', 'MIP1b', 'MIG', 'RANTES', 'GMCSF'])
    minus_th_df[minus_th_df < 0] = 0
    c = 1
    minus_log = minus_th_df[minus_th_df > 0].apply(lambda x: log2(x+c))
    minus_log.fillna(0, inplace=True)
    return minus_th_df, minus_log, minus_th

#histogram -- check data density of cytokine secretion
def data_density(v):
    py.sign_in("kleppem", "3q6fzriaag")
    data = Data([Histogram(x=v)])
    layout = Layout(yaxis=YAxis(title='Fluorescent Intensity (log-transformed)'))
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(data, filename='basic-histogram')

#heatmap plotly no clustering
def heatmap(df):
    py.sign_in("kleppem", "3q6fzriaag")
    KC = df.KC
    TNF = df.TNF
    IL1b = df.IL1b
    IL6 = df.IL6
    IL10 = df.IL10
    IL12 = df.IL12
    MCP1 = df.MCP1
    MIP1a = df.MIP1a
    MIP1b = df.MIP1b
    MIG = df.MIG
    RANTES = df.RANTES
    GMCSF = df.GMCSF
    data = Data([Heatmap(z=[KC , TNF , IL1b , IL6 , IL10, IL12, MCP1, MIP1a, MIP1b, MIG, RANTES, GMCSF], 
                 y=['KC', 'TNFa', 'IL1b', 'IL6', 'IL10', 'IL12', 'MCP1', 'MIP1a', 'MIP1b', 'MIG', 'RANTES', 'GMCSF'])])
    plot_url = py.plot(data, filename='basic-heatmap')

#calculate percentage of cytokine secreting cells (polyfunctionality)
def get_poly(minus_th):
    minus_th_df2 = pd.DataFrame(minus_th, columns = ['KC', 'TNF', 'IL1b', 'IL6', 'IL10', 'IL12', 'MCP1', 'MIP1a', 'MIP1b', 'MIG', 'RANTES', 'GMCSF' ])
    minus_th_df2[minus_th_df2 < 0] = 0
    minus_th_df2[minus_th_df2 > 0] = 1
    count = minus_th_df2.apply(pd.Series.value_counts, axis=1)
    count.fillna(0, inplace=True)    
    count.columns = ['not_expressed', 'expressed']
    count_poly = count['expressed'].value_counts()    
    new = pd.DataFrame(count_poly, columns = ['count'])
    sorted_df = new.sort_index()
    counts = sorted_df['count']
    return counts

#calculate %
def get_percent_poly(counts):
    total = counts.sum()
    c0 = (float(counts[0])/total)*100
    c1 = (float(counts[1])/total)*100
    c2 = (float(counts[2])/total)*100
    c3 = (float(counts[3])/total)*100
    c4 = (float(counts[4])/total)*100
    if len(counts) > 5:
        for item in counts[5:]:
            temp = sum(counts[5:])
    else:
        temp = 0
    c5 = (float(temp)/total)*100
    return [c0, c1, c2, c3, c4, c5]

#pie chart for one data set
def pie_chart(poly_percent):
    labels = ['0', '1', '2', '3', '4', '5']
    cmap = plt.cm.GnBu
    fig = plt.figure(figsize=[10, 10])
    colors = cmap(np.linspace(0., 1., len(poly_percent)))
    mpl.rcParams['font.size'] = 15.0
    plt.pie(poly_percent, autopct='%1.1f%%', labels = labels, startangle = 90, colors = colors, pctdistance=0.6)
    plt.title('Polyfunctionality')
    plt.show()

#stached bar plot of polyfunc. for four populations
def create_plotly(P1, P2, P3, P4, PP1, PP2, PP3, PP4):
    py.sign_in("kleppem", "3q6fzriaag")
    trace1 = Bar(x=[P1, P2, P3, P4],y=[PP1[0], PP2[0], PP3[0], PP4[0]],name='0')
    trace2 = Bar(x=[P1, P2, P3, P4],y=[PP1[1], PP2[1], PP3[1], PP4[1]],name='1')
    trace3 = Bar(x=[P1, P2, P3, P4],y=[PP1[2], PP2[2], PP3[2], PP4[2]],name='2')
    trace4 = Bar(x=[P1, P2, P3, P4],y=[PP1[3], PP2[3], PP3[3], PP4[3]],name='3')
    trace5 = Bar(x=[P1, P2, P3, P4],y=[PP1[4], PP2[4], PP3[4], PP4[4]],name='4')
    trace6 = Bar(x=[P1, P2, P3, P4],y=[PP1[5], PP2[5], PP3[5], PP4[5]],name='5')
    data = Data([trace1, trace2, trace3, trace4, trace5, trace6])
    layout = Layout(barmode='stack', yaxis=YAxis(title='Number of secreted cytokines (%)'))
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='stacked-bar')




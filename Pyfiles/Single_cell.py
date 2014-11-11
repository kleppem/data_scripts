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
from fisher import pvalue
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
import brewer2mpl
import matplotlib.gridspec as gridspec
import scipy.spatial.distance as distance
import scipy.cluster.hierarchy as sch

#Change working directory
os.chdir('/Users/kleppem/Documents/Python/single_cell')

#import file as df
df = pd.read_csv(filename)

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

def subtract_threshold(df, th):
    one_cell = df[df.number == 1]
    cytokines = list(df.columns)[0:11]
    del one_cell['number']
    minus_th_df = one_cell.subtract(th, axis='columns')
    return minus_th_df, cytokines

def convert_to_log(minus_th_df):
    minus_th_df[minus_th_df < 0] = 0
    c = 1
    minus_log = minus_th_df[minus_th_df > 0].apply(lambda x: log2(x+c))
    minus_log.fillna(0, inplace=True)
    return minus_log

def combine_functions1(df):
    TH, th = cal_threshold(df)
    minus_th_df = subtract_threshold(df, th)
    minus_log = convert_to_log(minus_th_df)
    minus_log.to_csv('PCA_input.csv')
    return th, TH, minus_th_df, minus_log

th, TH, minus_th_df, minus_log, cytokines = combine_functions1(df)

#create dataframe for two cytokines
def create_count_table(df, Cyt1, Cyt2):
    df_cont = pd.DataFrame(zip(df[Cyt1], df[Cyt2]), columns = ['A', 'B'])
#create contigency table
    df_cont[df_cont > 0] = 1
#get counts for each condition
    d = df_cont.to_dict()
    A = 0
    B = 0
    AandB = 0
    none = 0
    tup = zip(d['A'].values(), d['B'].values())
    for row in tup:
        if row[0] == 0 and row[1] == 0:
            none = none +1
        if row[0] == 0 and row[1] == 1:
            B = B + 1
        if row[0] == 1 and row[1] == 0:
            A = A +1
        if row[0] ==1 and row[1] == 1:
            AandB = AandB + 1
    # Fishers exact test
    matrix = numpy.matrix([[AandB, B],[A, none]])
    p = pvalue(AandB, B, A, none)
    #output = [Cyt1, Cyt2, p.left_tail, p.right_tail, p.two_tail]
    output = p.two_tail
    return output, Cyt1, Cyt2

def create_pvec(df):
    cytokines = list(minus_th_df.columns)
    output = []
    Cyt1 = []
    Cyt2 = []
    for c in cytokines:
        for i in range(len(cytokines)):
            if c != cytokines[i]:
                temp, C1, C2, matrix = create_count_table(minus_th_df, c, cytokines[i])
                output.append(temp)
                Cyt1.append(C1)
                Cyt2.append(C2)
                #print c, cytokines[i], temp
    return output, Cyt1, Cyt2

def adjust_pvalues(pvalues, method='BH'):
    p_adjust = stats.p_adjust(FloatVector(pvalues), method = method)
    return list(p_adjust)

def create_df_for_heatmap(adjust_pvalues, Cyt1, Cyt2, cytokines):
    ls = zip(Cyt1, Cyt2, adjust_pvalues)
    for row in cytokines:
        temp = (row, row, 'NA')
        ls.append(temp)
#plot adjusted pvalues in heatmap format
    df = pd.DataFrame(ls, columns = ['Cytokine1', 'Cytokine2', 'pvalues'])
    d = {}
    for row in cytokines:
        temp = df[df.Cytokine1 == row].sort('Cytokine2')
        d[row] = list(temp.pvalues)
        index = temp.Cytokine2
#create data frame for heat map
    dfs = pd.DataFrame(d.values(), columns = ['GMCSF', 'IL10', 'IL12', 'IL1b', 'IL6', 'KC', 'MCP1', 'MIG', 'MIP1a', 'MIP1b', 'RANTES', 'TNF'])
    dfs['Index'] = ['KC', 'MCP1', 'IL10', 'IL12', 'MIG', 'IL6', 'TNF', 'MIP1a', 'IL1b', 'RANTES', 'MIP1b', 'GMCSF']
    dfsi = dfs.set_index('Index')
    dfsi[dfsi < 0.05] = 2.0
    dfsi[(dfsi >= 0.05) & (dfsi < 1)] = 0.5
    dfsi[dfsi == 'NA'] = 0.00000
    final_df = dfsi.sort_index()
    final_df_rc = final_df.convert_objects(convert_numeric=True)
    final_df_rc.dtypes
    return final_df_rc

def combine_functions2(df):
    pval, Cyt1, Cyt2 = create_pvec(df)
    adjust_pval = adjust_pvalues(pval, method='BH')
    final_df_rc = create_df_for_heatmap(adjust_pval, Cyt1, Cyt2, cytokines)
    return final_df_rc

final_df_rc = create_df_for_heatmap(adjust_pvalues, Cyt1, Cyt2, cytokines)


#create heat map
# helper for cleaning up axes by removing ticks, tick labels, frame, etc.
def clean_axis(ax):
    """Remove ticks, tick labels, and frame from axis"""
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)


#create heatmap without dendrogram
def create_heatmap(output, data):
    rcParams.update({'font.size': 16})
    rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

    fig = plt.figure(figsize=(12,8))
    heatmapGS = gridspec.GridSpec(2,2,wspace=0.0,hspace=0.0,width_ratios=[0.25,1],height_ratios=[0.25,1])

    heatmapAX = fig.add_subplot(heatmapGS[1,1])
    axi = heatmapAX.imshow(data,interpolation='nearest',aspect='auto',origin='lower',cmap=cm.RdBu_r)
    clean_axis(heatmapAX)
    
    heatmapAX.set_yticks(arange(data.shape[0]))
    heatmapAX.yaxis.set_ticks_position('right')
    heatmapAX.set_yticklabels(data.index)

    heatmapAX.set_xticks(arange(data.shape[1]))
    xlabelsL = heatmapAX.set_xticklabels(data.columns)
    # rotate labels 90 degrees
    for label in xlabelsL:
        label.set_rotation(90)
    # remove the tick lines
    for l in heatmapAX.get_xticklines() + heatmapAX.get_yticklines(): 
        l.set_markersize(0)

    scale_cbGSSS = gridspec.GridSpecFromSubplotSpec(1,2,subplot_spec=heatmapGS[0,0],wspace=0.0,hspace=0.0)
    scale_cbAX = fig.add_subplot(scale_cbGSSS[0,0]) # colorbar for scale in upper left corner
    cb = fig.colorbar(axi,scale_cbAX) # note that we tell colorbar to use the scale_cbAX axis
    cb.set_label('Measurements')
    cb.ax.yaxis.set_ticks_position('left') # move ticks to left side of colorbar to avoid problems with tight_layout
    cb.ax.yaxis.set_label_position('left') # move label to left side of colorbar to avoid problems with tight_layout
    cb.outline.set_linewidth(0)

    fig.tight_layout()
    savefig(output)

create_heatmap('cosecretion.png', final_df_rc)

#calculate ratios for plotting
def calculate_ratios(df1, df2):
    JAK2VF_means = df1.mean()
    Ctrl_means = df2.mean()
    JAK2VF_ratio = list(JAK2VF_means/Ctrl_means)
    Ctrl_ratio = list(Ctrl_means/Ctrl_means)
    cytokines = list(df1.columns)
    return JAK2VF_ratio, Ctrl_ratio, cytokines

#plot average cytokine secretion relative to control
def plot_ratios(cytokines, Ctrl_ratio, JAK2VF_ratio):
    py.sign_in("kleppem", "3q6fzriaag")
    trace1 = Bar(x=cytokines,y=Ctrl_ratio,name='Ctrl CD45.2')
    trace2 = Bar(x=cytokines,y=JAK2VF_ratio,name='JAK2VF CD45.2')
    data = Data([trace1, trace2])
    layout = Layout(barmode='group')
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='grouped-bar')

def combine_functions3(df1, df2):
	JAK2VF_ratio, Ctrl_ratio, cytokines = calculate_ratios(df1, df2)
	plot_ratios(cytokines, Ctrl_ratio, JAK2VF_ratio)

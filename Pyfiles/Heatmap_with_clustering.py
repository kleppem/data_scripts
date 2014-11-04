import os
import brewer2mpl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.spatial.distance as distance
import scipy.cluster.hierarchy as sch

os.chdir(<add your directory>)
df = pd.read_csv(<add your filename>)

# font size for figures
rcParams.update({'font.size': 16})
# Arial font
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

# helper for cleaning up axes by removing ticks, tick labels, frame, etc.
def clean_axis(ax):
    """Remove ticks, tick labels, and frame from axis"""
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

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

# minus threshold values
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
        temp = item - th[11]
        GMCSF.append(temp)
    minus_th = zip(KC, TNF, IL1b, IL6, IL10, IL12, MCP1, MIP1a, MIP1b, MIG, RANTES, GMCSF) 
    minus_th_df = pd.DataFrame(minus_th, columns = ['KC', 'TNF', 'IL1b', 'IL6', 'IL10', 'IL12', 'MCP1', 'MIP1a', 'MIP1b', 'MIG', 'RANTES', 'GMCSF'])
    minus_th_df[minus_th_df < 0] = 0
    c = 1
    minus_log = minus_th_df[minus_th_df > 0].apply(lambda x: log2(x+c))
    minus_log.fillna(0, inplace=True)
    return minus_th_df, minus_log

# look at raw data
def look_at_raw(data):
    axi = imshow(data,interpolation='nearest',cmap=cm.RdBu)
    ax = axi.get_axes()
    clean_axis(ax)

def cluster(data):
    pairwise_dists = distance.squareform(distance.pdist(data))
    # cluster
    sch.set_link_color_palette(['black'])
    row_clusters = sch.linkage(pairwise_dists,method='complete')
    # rename row clusters
    #row_clusters = clusters
    # calculate pairwise distances for columns
    col_pairwise_dists = distance.squareform(distance.pdist(data.T))
    # cluster
    col_clusters = sch.linkage(col_pairwise_dists,method='complete')
    return row_clusters, col_clusters


def create_heatmap(output, data):
    row_clusters, col_clusters = cluster(data)
    
    # heatmap with row names
    fig = plt.figure(figsize=(12,8))
    heatmapGS = gridspec.GridSpec(2,2,wspace=0.0,hspace=0.0,width_ratios=[0.25,1],height_ratios=[0.25,1])
    
    ### col dendrogram ###
    col_denAX = fig.add_subplot(heatmapGS[0,1])
    col_denD = sch.dendrogram(col_clusters,color_threshold=np.inf)
    clean_axis(col_denAX)

    ### row dendrogram ###
    row_denAX = fig.add_subplot(heatmapGS[1,0])
    row_denD = sch.dendrogram(row_clusters,color_threshold=np.inf,orientation='right')
    clean_axis(row_denAX)

    ### heatmap ####
    heatmapAX = fig.add_subplot(heatmapGS[1,1])
    axi = heatmapAX.imshow(data.ix[row_denD['leaves'],col_denD['leaves']],interpolation='nearest',aspect='auto',origin='lower',cmap=cm.RdBu_r)
    clean_axis(heatmapAX)

    ## col labels ##
    heatmapAX.set_xticks(arange(data.shape[1]))
    xlabelsL = heatmapAX.set_xticklabels(data.columns[col_denD['leaves']])
    # rotate labels 90 degrees
    for label in xlabelsL:
        label.set_rotation(90)
    # remove the tick lines
    for l in heatmapAX.get_xticklines() + heatmapAX.get_yticklines(): 
        l.set_markersize(0)

    ### scale colorbar ###
    scale_cbGSSS = gridspec.GridSpecFromSubplotSpec(1,2,subplot_spec=heatmapGS[0,0],wspace=0.0,hspace=0.0)
    scale_cbAX = fig.add_subplot(scale_cbGSSS[0,0]) # colorbar for scale in upper left corner
    cb = fig.colorbar(axi,scale_cbAX) # note that we tell colorbar to use the scale_cbAX axis
    cb.set_label('Measurements')
    cb.ax.yaxis.set_ticks_position('left') # move ticks to left side of colorbar to avoid problems with tight_layout
    cb.ax.yaxis.set_label_position('left') # move label to left side of colorbar to avoid problems with tight_layout
    cb.outline.set_linewidth(0)

    fig.tight_layout()
    savefig(output)

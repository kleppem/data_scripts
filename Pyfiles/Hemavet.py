import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

#set path
os.chdir('/Users/kleppem/Documents/Python')

#open file
file = pd.read_csv('hemavet.csv')

#index file 
file_ix = file.set_index(['Sample ID No'])

#create subdataframe
file_s = file_ix.loc[:,('Analysis Date', 'WBC(K/uL)', 'NEUT#(K/uL)', 'LYMPH#(K/uL)', 'MONO#(K/uL)', 'PLT(K/uL)', 'HCT(%)', 'RBC(M/uL)', 'HGB(g/dL)')]

#export as excel file
file_s.to_excel('hemavet_results.xls')
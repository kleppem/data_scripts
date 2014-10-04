import sys
import pandas as pd
import os
import matplotlib as mpl
import re
import numpy as np
from Bio import Medline
import datetime
import pycountry
from Bio import Entrez
from Bio.Entrez import efetch, read
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

Entrez.email = 'kleppem@mskcc.org'

# count number of publications for keywords
def count_occurence(keyword):
    handle = Entrez.egquery(term=keyword)
    record = Entrez.read(handle)
    for row in record["eGQueryResult"]:
        if row["DbName"]=="pubmed":
            count = (row["Count"])
            return count

#collect medline records
def pubmed_id(keyword, count):
    handle_pubmed = Entrez.esearch(db="pubmed",
                                   term=keyword,
                                   retmax=count)
    record_pubmed = Entrez.read(handle_pubmed)
    handle = Entrez.efetch(db="pubmed",
                           id=record_pubmed["IdList"],
                           rettype="medline",
                           retmode="text")
    records = list(Medline.parse(handle))
    return records

#extract year
def get_date(res):
    date = []
    for rec in res:
        d = rec.get('EDAT')
        y = int(d.split("/")[0])
        date.append(y)
    return date

#extract pmid
def get_pmid(res):
   pmid = []
   for rec in res:
        pmid.append(rec['PMID'])
   return pmid

#extract journal title
def get_journal(res):
    JT = []
    for rec in res:
        d = rec.get('JT')
        JT.append(d)
    return JT

#extract publication type
def get_type(res):
    PT = []
    for rec in res:
        d = rec.get('PT')
        PT.append(d)
    return PT

def remove_brackets(article_type):
    article_type_new = []
    for a in article_type:
        article_type_new.append(','.join(str(item) for item in a))
    return article_type_new

#extract affilitation
def get_aff(res):
    AF = []
    for rec in res:
        d = rec.get('AD')
        AF.append(d)
    return AF

def country_list(t):
    country_list = []
    for country in t:
        country_list.append(country.name)
    return country_list

def get_country(AF):
    t = list(pycountry.countries)
    clist = country_list(t)
    cset = set(clist)
    cset.update(['USA'], ['UK'], ['America'])
    c= []
    for a in AF:
        if not a == None:
            cs = set(a.replace("."," ").replace('America', 'USA').replace('United Kingdom', 'UK').strip().split(" "))
        c.append(cset.intersection(cs))
    return c

#Alternative: comprehension for affs list
#[a.replace(".", " ").strip().split(" ") for a in affs if a != None]

def remove_set(country):
    country_new = []
    for c in country:
        country_new.append(','.join(str(item) for item in c))
    return country_new
    
def create_df(zip_file):
    df_data = pd.DataFrame(zip_file, columns = ['Year', 'PMID', 'Journal','Type', 'Country'])
    data = df_data.replace('','None')  #replace empty country fields with None
    return data
     
def get_pubmed(res):
    year = get_date(res)
    pmid = get_pmid(res)
    journal = get_journal(res)
    article_type = get_type(res)
    article_type_new = remove_brackets(article_type)
    aff = get_aff(res)
    country = get_country(aff)
    country_new = remove_set(country)
    zip_file = zip(year,pmid,journal, article_type_new, country_new)
    return zip_file

###--------------------call your functions
def get_records(keyword):
    count = count_occurence(keyword)
    res = pubmed_id(keyword, count)
    rec = get_pubmed(res)
    df_data = create_df(rec)
    return res, rec, df_data

res, rec, df_data = get_records(keyword)

###--------------------analyze and visualize data stored in the dataframe
### Example 1:
def plot_data_byyear(df_data): 
    df_year = df_data.groupby('Year')
    df_year.size().plot(linewidth=2.0)
    ylabel('Number of publications')
    title('Bargraph: <add keyword>')
    xlabel('Year')
    return plot

plot_data_byyear(df_data)

### Example 2:
def plot_data_bycountry(df_data): 
    df_data.Country.apply(lambda x: pd.value_counts(x.replace(','," ").split(" "))).sum(axis = 0).order().plot(kind='bar')
    ylabel('Number of publications')
    title('Bargraph: Publications per country')
    xlabel('Country')
    
plot_data_byyear(df_data)

### Example 3:
def plot_data_by_journal(df_data):
    df_year_2013 = df_data.groupby(['Year', 'Journal']).size().ix[2013].order()
    df_year_2013[-41:].plot(kind='bar') #in example [-41:] represents journals with >= 5 publications
    ylabel('Number of publications')
    xlabel('Journal Title')
    ttl = 'Year 2013, RNAseq' ##Example, keyword = RNA seq, Year = 2013

plot_data_byyear(df_data)

###-------------------- optional --- export country data for further visualization (see World_map_PubMed_data)
def create_dict(df_data):
    count = df_data.Country.apply(lambda x: pd.value_counts(x.replace(','," ").split(" "))).sum(axis = 0).order()
    count_dict = count.to_dict()
    values = []
    for v in count_dict.values():
        values.append(int(v))
    keys = count_dict.keys()
    dict_country = dict(zip(keys, values))
    return dict_country

def export_file(dict_country):
    output = open('dict_count.txt', 'w')
    json.dump(dict_country, output)
    output.close()

def call_functions(df_data)
	dict_country = create_dict(df_data_country)
	export_file(dict_country)

call_functions(df_data)


# search terms used for side project:
#WGS = pubmed_id('"whole genome sequencing"')
#WES = pubmed_id('"whole exome sequencing"')
#sanger = pubmed_id('"sanger sequencing"')
#CHIPseq = pubmed_id('CHIP seq"')
#RNAseq = pubmed_id('"RNA seq"')
#array = pubmed_id('"SNP array"')

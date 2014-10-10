import sys
import re
import numpy
import mygene
import pandas
mg = mygene.MyGeneInfo()


#set directory to location of your input file (here: Genes.csv)

#open file
def read_file(filename):
	myfile = open(filename, 'r')
	string=myfile.read()
	string_lower = string.lower()
	my_list = []
	for word in string_lower.split():
    	my_list.append(word)
	return my_list

def get_accessions(genes):
    id_list = []
    for word in genes:
         if word not in id_list:
            id_list.append(word)
    out = mg.querymany(id_list, scopes='alias, symbol', fields='entrezgene, accession', species='human')
    return out

def print_data(annotation):
    res = []
    for gene_data in annotation:
        gene_id = gene_data.get('_id')
        gene_name = gene_data['query']
        gene_name_upper = gene_name.upper()
        gene_accession_nm = []
        try:
            for v in gene_data['accession']['rna']:
                if 'NM' in v:
                    gene_accession_nm.append(v)
        except KeyError:
            pass
        x = "Gene Name: %s, ID: %s, Accession number: %s" % (gene_name_upper, gene_id, ' '.join(gene_accession_nm))
        res.append(x)
    return res

def write_to_file(res):
	f = open("gene_accession.txt", "w")
	for i in res:
    	f.write((str(i) + "\n"))
	f.close()

def call_functions(filename):
	genes = read_file(filename)
	annotation = get_accessions(genes)
	res = print_data(annotation)
	write_to_file(res)


call_functions(<add your filename>)

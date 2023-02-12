import math 
from indexing import * 
from query import *

def create_idf(inverted_index):
    numofDocuments = 79923
    idf_values = {}
    for key in inverted_index : 
        if (len(inverted_index[key]) == 0 ):
            idf_values[key] = 0
        else:
            idf_values[key] = math.log2(numofDocuments/ len(inverted_index[key]))
    return idf_values

def calculate_tf_idf(documents, inverted_index, idf_values, max_frequency):
    document_tf_idf={}
    for docNo in documents: 
        document_tf_idf[docNo]={}
        for token in inverted_index: 
            if (inverted_index.get(token,{}).get(docNo, None)) != None: 
                document_tf_idf[docNo][token]= (inverted_index[token][docNo] / max_frequency[docNo]) * idf_values[token]
    return document_tf_idf

def doc_length(doc_tf_idf):
    length_doc={}
    length=0
    for docNo in doc_tf_idf:
        for token in doc_tf_idf[docNo]:
            length= length + doc_tf_idf[docNo][token]**2
        length_doc[docNo]= math.sqrt(length)
    return length_doc
    
# files = get_files("./coll")
# files_names = list(map(lambda x: "./coll/" + x, files))
# inverted_index, documents= produce_index(files_names)
# idf_values= create_idf(inverted_index)
# tf_idf=calculate_tf_idf(documents, inverted_index,idf_values)
# print (tf_idf)

def calc_cosSim(doc_tf_idf, query_tf_idf, doc_length, query_length):
    cosSim={}
    sum=0
    for docNo in doc_tf_idf: 
        for token in doc_tf_idf:
            if token in query_tf_idf.keys():
                sum= sum+ (query_tf_idf[token] * doc_tf_idf[docNo][token])
        cosSim[docNo]= sum/ (doc_length[docNo] * query_length)
        sum=0
    return cosSim

inverted_index, documents, max_frequency = produce_index(["./coll/AP880212"])
idf_values= create_idf(inverted_index)
tf_idf=calculate_tf_idf(documents, inverted_index,idf_values, max_frequency)
# print(doc_length(tf_idf))

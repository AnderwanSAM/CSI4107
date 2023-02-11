# Construct the inverted index 
import re
import string
import os
import operator as op
from map_documents import map_documents
# from preprocessing import process_files, get_files
from preprocessing import process_files, get_files
import math


def read_file(file_name): 
    f = open(file_name,"r")
    text = f.read()
    return text 

def get_tokens():
    files = get_files("./coll")
    files_names = list(map(lambda x: "./coll/" + x, files))
    return process_files(files_names)


# print(process_files(files_names))
def produce_index (files_names): 
    inverted_index = {}
    # get list of unique terms (list of tokens)
    tokens = get_tokens()
    # add tokens as keys for the inverted index 
    for token in tokens:
        inverted_index[token] = {}
    for file in files_names : 
        mapped_documents = map_documents(file)
        for key in mapped_documents : 
            for term in mapped_documents[key]: 
                if term in inverted_index : 
                    inverted_index[term][key] = mapped_documents[key].count(term)
    return inverted_index, mapped_documents

def get_files(folder_path):
    files = os.listdir(folder_path) 
    return files

def create_idf(inverted_index):
    numofDocuments = 79923
    idf_values = {}
    for key in inverted_index : 
        idf_values[key] = math.log2(numofDocuments/ len(inverted_index[key]))
    return idf_values


# files = get_files("./coll")
# files_names = list(map(lambda x: "./coll/" + x, files))
# # print (produce_index(files_names))
# # print(produce_index(["./coll/AP880212"]))

# inverted_index = produce_index(files_names)
# idf_values = create_idf(inverted_index)
# print(idf_values)
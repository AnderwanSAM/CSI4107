# Construct the inverted index 
import re
import string
import os
import operator as op
from map_documents import map_documents
# from preprocessing import process_files, get_files
from preprocessing import process_files, get_files

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
    final_index = {}
    # get list of unique terms (list of tokens)
    tokens = get_tokens()
    # add tokens as keys for the inverted index 
    for token in tokens:
        inverted_index[token] = []
    for file in files_names : 
        mapped_documents = map_documents(file)
        for key in mapped_documents : 
            for term in mapped_documents[key]: 
                if term in inverted_index : 
                    # inverted_index[term].append((key,op.countOf(mapped_documents[key],term)))
                    inverted_index[term].append((  key , mapped_documents[key].count(term)))
    return inverted_index

def get_files(folder_path):
    files = os.listdir(folder_path) 
    return files

files = get_files("./coll")
files_names = list(map(lambda x: "./coll/" + x, files))
print(produce_index(files_names))


# print(produce_index(["./coll/AP880212"]))

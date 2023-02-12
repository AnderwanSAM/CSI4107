import re
import string
from  preprocessing import *
import math
from map_documents import remove_stopwords
from indexing import * 

def extract_query(query):
    pattern = re.compile(r'<title>(.*?)<desc>', re.DOTALL)
    matches = pattern.findall(query)
    first_query=matches[0].split()
    final_query = []
    for x in first_query : 
        final_query.append(x.lower())
    no_stopwords_q= remove_stopwords(final_query)
    return no_stopwords_q

def query_tf_idf(query, idf_values ):
     query_token={}
     for token in query: 
         query_token[token] = idf_values[token]
     return query_token

def query_length(query_tf_idf):
    length=0
    for value in query_tf_idf:
        length= length + query_tf_idf[value]**2
    length= math.sqrt(length)
    return length

query_files = read_file("test_query.txt")
query= extract_query(query_files)
# print(query)
doc_files = get_files("./coll")
doc_files_names = list(map(lambda x: "./coll/" + x, doc_files))


inverted_index, documents, max_frequency = produce_index(doc_files_names)
idf_values= create_idf(inverted_index)
q_tf_idf=(query_tf_idf(query, idf_values))
# print(query_length(q_tf_idf))
import re
import string
from  preprocessing import *
from map_documents import remove_stopwords
from cosSim import * 

def extract_query(query):
    pattern = re.compile(r'<title>(.*?)<desc>', re.DOTALL)
    matches = pattern.findall(query)
    first_query=matches[0].split()
    for x in first_query : 
        first_query.append(x.lower())
    no_stopwords_q= remove_stopwords(first_query)
    return no_stopwords_q

def query_tf_idf(query, idf_values ):
     query_token={}
     for token in query: 
         query_token[token] = idf_values[token]
     return query_token
    
query_files = read_file("test_query.txt")
query= extract_query(query_files)

doc_files = get_files("./coll")
doc_files_names = list(map(lambda x: "./coll/" + x, doc_files))


inverted_index, documents, max_frequency = produce_index(doc_files_names)
idf_values= create_idf(inverted_index)
print(query_tf_idf(query, idf_values))
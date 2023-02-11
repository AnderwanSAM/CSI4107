import math 
from indexing import * 
from map_documents import map_documents

def create_idf(inverted_index):
    numofDocuments = 79923
    idf_values = {}
    for key in inverted_index : 
        if (len(inverted_index[key]) == 0 ):
            idf_values[key] = 0
        else:
            idf_values[key] = math.log2(numofDocuments/ len(inverted_index[key]))
    return idf_values

def calculate_tf_idf(documents, inverted_index, idf_values):
    document_tf_idf={}
    for docNo in documents: 
        document_tf_idf[docNo]={}
        for token in inverted_index: 
            if (inverted_index.get(token,{}).get(docNo, None)) != None: 
                document_tf_idf[docNo][token]= inverted_index[token][docNo] * idf_values[token]
    return document_tf_idf

# files = get_files("./coll")
# files_names = list(map(lambda x: "./coll/" + x, files))
# inverted_index, documents= produce_index(files_names)
# idf_values= create_idf(inverted_index)
# tf_idf=calculate_tf_idf(documents, inverted_index,idf_values)
# print (tf_idf)

inverted_index, documents=produce_index(["./coll/AP880212"])
idf_values= create_idf(inverted_index)
tf_idf=calculate_tf_idf(documents, inverted_index,idf_values)
print (tf_idf)
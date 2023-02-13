import math 
from retrieval import *
from indexing import *

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

def calc_cosSim(doc_tf_idf, q_tf_idf, doc_len, query_len):
    cosSim={}
    sum=0
    for docNo in doc_tf_idf: 
        for token in doc_tf_idf[docNo]:
            if token in q_tf_idf.keys():
                sum= sum+ (q_tf_idf[token] * doc_tf_idf[docNo][token])
        if sum != 0 :
            cosSim[docNo]= sum/ (doc_len[docNo] * query_len)
        sum=0
    return dict(sorted(cosSim.items(), key=lambda x: x[1], reverse=True))


#Step3 : CosSim for 1 query 
def compute_cossim_iq(query_files, idf_values,count,doc_tf_idf, doc_len) : 
    query= extract_query(query_files,count)  #returns a list of words for a given query
    q_tf_idf=query_tf_idf(query, idf_values) #calculates tf_idf of the query
    query_len= query_length(q_tf_idf)        #calculates the length of the query 
    results=calc_cosSim(doc_tf_idf, q_tf_idf, doc_len, query_len)  #calculates cosine Similarity with 1 query and the collection of documents (key: DocNo value: casine similarity)
    return results

# Write to Result file (topic_id Q0 docno rank score tag) 
def write_to_file(topicNo,results):
    # {'AP880212-0062': 0.009771322815600376, 'AP880212-0108': 0.0014723630652527925}
    count = 1
    for docNo in results:   
        to_print = str(topicNo) + " Q0 " + str(docNo) + " " + str(count) + " " + str(results[docNo]) + " " + "testTag"
        with open("Results.txt", "a") as file:
            print(to_print, file=file)
        count += 1 


def main():
    # Retrieves the collection of documents 
    files = get_files("./coll")
    files_path = list(map(lambda x: "./coll/" + x, files))
    
    inverted_index, documents, max_frequency = produce_index(files_path) 
    idf_values= create_idf(inverted_index)
    doc_tf_idf=calculate_tf_idf(documents, inverted_index,idf_values, max_frequency)
    doc_len= doc_length(doc_tf_idf)

    query_files = read_file("test_query.txt")
    
    # print(query_files)
    #CosSim for 50 queries 
    # for i in range (0,50) :
    #     results=compute_cossim_iq(query_files, idf_values, i, doc_tf_idf, doc_len)
    #     write_to_file((i+1),results)
    # results=compute_cossim_iq(query_files, idf_values, 0, doc_tf_idf, doc_len)
    # write_to_file((0+1),results)
    print(documents)


if __name__ == "__main__":
    main()



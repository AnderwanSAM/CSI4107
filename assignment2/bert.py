from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import os
import torch
import re
import nltk
from nltk.stem import PorterStemmer
nltk.download('punkt')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_embedding(text):
    input_ids = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model(input_ids)
    last_hidden_states = outputs[0]
    return last_hidden_states[:, 0, :]

def get_files(folder_path):
    files = os.listdir(folder_path) 
    return files

def get_files_names(folder_path): 
    files = get_files(folder_path)
    files_names = list(map(lambda x: folder_path + "/" + x, files))
    return files_names

def read_file(file_name): 
    f = open(file_name,"r")
    text = f.read()
    return text 

# def extract_docs(file_content):
#     docs = re.findall(r'<DOC>(.+?)</DOC>', file_content, flags=re.DOTALL)           # only keep text between DOC tags
#     doc_text = [re.search(r'<TEXT>(.+?)</TEXT>', doc).group(1) for doc in docs]     # retrieve document number between DOCNO tags
#     # doc_text = re.findall(r'<TEXT>(.+?)</TEXT>', file_content, flags=re.DOTALL)     # only keep text between TEXT tags
#     docnos = [re.search(r'<DOCNO>(.+?)</DOCNO>', doc).group(1) for doc in docs]     # retrieve document number between DOCNO tags
#     doc_text = [' '.join(re.findall(r'\b[a-zA-Z]+\b', t)) for t in doc_text]        # only keep text
#     return doc_text, docnos

def extract_docs(file_content):
    docs = re.findall(r'<DOC>(.+?)</DOC>', file_content, flags=re.DOTALL)
    doc_text = []
    for doc in docs:
        match = re.search(r'<TEXT>\s*(.+?)\s*</TEXT>', doc, flags=re.DOTALL)
        if match:
            doc_text.append(match.group(1))
        else:
            doc_text.append('')
    docnos = [re.search(r'<DOCNO>\s*(.+?)\s*</DOCNO>', doc).group(1) for doc in docs]
    doc_text = [' '.join(re.findall(r'\b[a-zA-Z]+\b', t)) for t in doc_text]
    return doc_text, docnos

def extract_query(query):
    pattern = re.compile(r'<title>(.*?)<narr>', re.DOTALL)
    queries = pattern.findall(query)
    queries = [' '.join(re.findall(r'\b\w+\b', q)) for q in queries]
    return queries

def extract_query_desc_title(query):
    query_pattern = re.compile(r'<title>(.*?)<desc>(.*?)<narr>', re.DOTALL)
    matches = query_pattern.findall(query)
    results = []
    for match in matches:
        result = match[0].strip() + ' ' + match[1].strip()  # combine the two extracted strings with a space separator
        results.append(result)
    return results 

def remove_stopwords(text_list):
    # Read stopwords from file 
    with open('StopWords.txt', 'r') as f:
        stopwords = set(f.read().splitlines())
    result = []
    # Remove stopwords from text
    for text in text_list:
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stopwords]
        result.append(' '.join(filtered_words))
    return result

def stem_text(docs):
    stemmer = PorterStemmer()
    result = []
    for doc in docs:
        words = nltk.word_tokenize(doc)
        stemmed_words = [stemmer.stem(word) for word in words]
        result.append(' '.join(stemmed_words))
    return result

# Read from the files and extract text
queries = read_file("test_query.txt")
file_content = read_file('AP880212')
doc_text, docnos = extract_docs(file_content)
# extracted_queries = extract_query(queries)
extracted_queries= extract_query_desc_title(queries)

# Remove stopwords from the documents and the queries 
doc_text = remove_stopwords(doc_text)
queries = remove_stopwords(extracted_queries)

# Stem documents and queries
doc_text = stem_text(doc_text)
# queries = stem_text(extracted_queries)

# print(doc_text)
# print("\n\n\n\n\n\n\n\n")
print(queries)

# results=[]
# query_embedding = get_embedding(queries[0])
# for docno, doc in tqdm(zip(docnos, doc_text), total=len(doc_text)):
#         doc_embedding = get_embedding(doc)
#         similarity = cosine_similarity(query_embedding, doc_embedding)
#         results.append((docno, similarity[0][0]))
# results.sort(key=lambda x: x[1], reverse=True)
    
# all_results = []

# for i, query in enumerate(queries):
#     query_embedding = get_embedding(query)
#     results = []
#     for docno, doc in tqdm(zip(docnos, doc_text), total=len(doc_text)):
#         doc_embedding = get_embedding(doc)
#         similarity = cosine_similarity(query_embedding, doc_embedding)
#         results.append((docno, similarity[0][0]))
#     results.sort(key=lambda x: x[1], reverse=True)
#     all_results.append(results)

# with open("Results.txt", "w") as f:
#     for i, results in enumerate(results):
#         for rank, (docno, score) in enumerate(results[:1000]):
#             f.write(f"{i+1} Q0 {docno} {rank+1} {score} run_name\n")
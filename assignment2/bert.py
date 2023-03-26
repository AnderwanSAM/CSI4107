from transformers import BertTokenizer, BertModel
import torch.nn.functional as F
from tqdm import tqdm
import os
import torch
import re
import nltk
from nltk.stem import PorterStemmer
# nltk.download('punkt')


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model.to(device)

def merge_files(folder_path: str, output_file: str):
    with open(output_file, 'w') as outfile:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path) as infile:
                    outfile.write(infile.read())

def get_embedding(text):
    input_ids = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    input_ids = input_ids.to(device)
    with torch.no_grad():
        outputs = model(input_ids)
    last_hidden_states = outputs[0]
    last_hidden_states = last_hidden_states.to(device)
    return last_hidden_states[:, 0, :]

def read_file(file_name): 
    f = open(file_name,"r")
    text = f.read()
    return text 

def extract_docs(file_content):
    docs = re.findall(r'<DOC>(.+?)</DOC>', file_content, flags=re.DOTALL)
    doc_text = []
    for doc in tqdm(docs, desc='Extracting docs'):
        match = re.search(r'<TEXT>\s*(.+?)\s*</TEXT>', doc, flags=re.DOTALL)
        if match:
            doc_text.append(match.group(1))
        else:
            doc_text.append('')
    docnos = [re.search(r'<DOCNO>\s*(.+?)\s*</DOCNO>', doc).group(1) for doc in docs]
    doc_text = [' '.join(re.findall(r'\b[a-zA-Z]+\b', t)) for t in doc_text]
    return doc_text, docnos

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
    with open('stopwords', 'r') as f:
        stopwords = set(f.read().splitlines())
    result = []
    # Remove stopwords from text
    for text in tqdm(text_list, desc='Removing stopwords'):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stopwords]
        result.append(' '.join(filtered_words))
    return result

def stem_text(docs):
    stemmer = PorterStemmer()
    result = []
    for doc in tqdm(docs, desc='Stemming documents'):
        words = nltk.word_tokenize(doc)
        stemmed_words = [stemmer.stem(word) for word in words]
        result.append(' '.join(stemmed_words))
    return result

# Read from the files and extract text

merge_files('coll', 'AP_merged')
queries = read_file("queries")
file_content = read_file('AP_merged')
doc_text, docnos = extract_docs(file_content)
extracted_queries = extract_query_desc_title(queries)

# Remove stopwords from the documents and the queries 
doc_text = remove_stopwords(doc_text)
queries = remove_stopwords(extracted_queries)

# Stem documents and queries
doc_text = stem_text(doc_text)
queries = stem_text(extracted_queries)

all_results = []

for i, query in enumerate(queries):
    query_embedding = get_embedding(query)
    results = []
    for docno, doc in tqdm(zip(docnos, doc_text), total=len(doc_text), desc='Calculating cosine similarity'):
        doc_embedding = get_embedding(doc)
        similarity = F.cosine_similarity(query_embedding, doc_embedding, dim=-1)
        results.append((docno, similarity.item()))
    results.sort(key=lambda x: x[1], reverse=True)
    all_results.append(results)

with open("Results_GPU.txt", "w") as f:
    for i, results in enumerate(all_results):
        for rank, (docno, score) in enumerate(results[:1000]):
            f.write(f"{i+1} Q0 {docno} {rank+1} {score} run_name\n")
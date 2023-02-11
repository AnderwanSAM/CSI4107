import re
import string
import os

def extract_text(document):
    pattern = re.compile(r'<TEXT>(.*?)</TEXT>', re.DOTALL)
    matches = pattern.findall(document)
    text = ' '.join(matches)
    translate_table = text.maketrans('', '', string.punctuation)
    no_punct = text.translate(translate_table)
    return no_punct

def tokenize_string(str): 
    return_value = [str.split()]
    return return_value[0]

def read_file(file_name): 
    f = open(file_name,"r")
    text = f.read()
    return text 

def process_files (files):
    extracted_text = ""
    for file_name in files :  
        file_content = read_file(file_name)
        extracted_text += extract_text(file_content)
    # remove numbers
    text_without_numbers = re.sub(r'\d+', '', extracted_text)
    tokenized_text = tokenize_string(text_without_numbers)
    tokenized_text_lower = list(map(lambda x: x.lower(), tokenized_text))  #convert to lower case 
    # remove duplicate words: https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    text_no_duplicate  = list(dict.fromkeys(tokenized_text_lower))
    #remove stop words
    return_value = remove_stopwords(text_no_duplicate)
    return return_value

def remove_stopwords(tokens): 
    with open("StopWords.txt") as f:
        stopwords= f.readlines()
    stopwords = [x.strip() for x in stopwords]
    tokens= set(tokens) - set(stopwords)
    tokens = sorted(list(tokens))
    return tokens

def get_files(folder_path):
    files = os.listdir(folder_path) 
    return files

# files = get_files("./coll")
# files_names = list(map(lambda x: "./coll/" + x, files))
# tokens = []

# print(process_files(files_names))

# def main():
# print("Hello Andie!")

# if __name__ == "__main__":
#     main()

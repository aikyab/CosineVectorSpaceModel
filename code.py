#Name: Aikya Banerjee 
#UIN : 675064035 
#Course : CS494 Information Retrieval and Web Search
#HW2


from os import listdir
from os.path import isfile, join

import os
import math

from pathlib import Path

import re
from collections import defaultdict
from collections import Counter



my_path = os.getcwd()

def stemmerStopEliminator(word_list):
    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    dict_stop_words = Counter(stop_words)
    new_words = []
    
    
    for word in word_list:
        if dict_stop_words[word]==0:
            new_word = word
            if dict_stop_words[new_word]==0:
                new_words.append(new_word)
    return new_words

def tokenize_documents():
    doc_folder = my_path+"/cranfieldDocs"
    os.chdir(doc_folder)
    onlyfiles = [f for f in listdir(doc_folder) if isfile(join(doc_folder, f))]
    text_corpus = {}
    regex_EXP = re.compile(r'[^\W\d]+')
    for path in onlyfiles:
        with open(path,encoding="latin-1") as f:
            text = f.readlines()
            flag = 0
            matcher = re.search("[\d]+",f.name)
            file_name = int(matcher.group())
            string_title = ""
            string_text = ""
            for line in text:
                if "<TITLE>" in line:
                    flag = 1
                    continue
                if "</TITLE>" in line:
                    flag = 0
                if flag == 1:
                    string_title+=line
            flag = 0
            for line in text:
                if "<TEXT>" in line:
                    flag = 1
                    continue
                if "</TEXT>" in line:
                    flag = 0
                if flag == 1:
                    string_text+=line
            
            word_match=regex_EXP.finditer(string_title)
            words = []
            for i in word_match:
                words.append(i.group())
            word_match=regex_EXP.finditer(string_text)
            for i in word_match:
                words.append(i.group())
            trimmed_words = []
            for word in words:
                if len(word)!=1 and len(word)!=2:
                    trimmed_words.append(word.lower())
            new_stemmed_words = stemmerStopEliminator(trimmed_words)
            text_corpus[file_name]=new_stemmed_words
    return text_corpus




def tokenize_queries():
    os.chdir(my_path)
    with open("queries.txt",encoding="latin-1") as f:
        queries = {}
        text = f.readlines()
        counter = 1
        for line in text:
            words = []
            regex_EXP = re.compile(r'[^\W\d]+')
            word_match=regex_EXP.finditer(line)
            
            for i in word_match:
                words.append(i.group())
            trimmed_words = []
            for word in words:
                if len(word)!=1 and len(word)!=2:
                    trimmed_words.append(word.lower())
            new_stemmed_words = stemmerStopEliminator(trimmed_words)
            queries[counter]=new_stemmed_words
            counter+=1
    return queries

doc_collection = tokenize_documents()
query_collection = tokenize_queries()



def df_calc(doc_collection):
    df = defaultdict(list)
    for key,value in doc_collection.items():
        for word in value:
            if key not in df[word]:
                df[word].append(key)
    return df

                
df = df_calc(doc_collection)

def cosine_similarity(top_n):
    doc_length = {}
    for key_i,value_i in doc_collection.items():
        tf = Counter(value_i)
        doc_l = 0
        for key_j,value_j in tf.items():
            div_l = len(doc_collection)/len(df[key_j])
            idf_l = math.log(div_l,2)
            weight = value_j*idf_l
            doc_l += weight*weight
        doc_length[key_i] = math.sqrt(doc_l)
    cosine_sim = {}
    for key_i,value_i in doc_collection.items():
        for key_j,value_j in query_collection.items():
            sumx = 0
            for word in value_j:
                if len(df[word])==0:
                    continue
                div = len(doc_collection)/len(df[word])
                idf = math.log(div,2)
                term_f = value_i.count(word)
                sumx += term_f*idf*idf
            if key_j not in cosine_sim:
                cosine_sim[key_j] = [(key_i,sumx/doc_length[key_i])]
            else:
                cosine_sim[key_j].append((key_i,sumx/doc_length[key_i]))
    def take_second(elem):
        return elem[1]
    for key,value in cosine_sim.items():
        value.sort(key=take_second,reverse=True)
        l1 = []
        for val in value:
            l1.append(val[0])
        if top_n<0:
            value[:] = l1
        else:
            value[:] = l1[:top_n]
    return cosine_sim


def process_rel():
    os.chdir(my_path)
    with open("relevance.txt","r") as f:
        text = f.readlines()
        rel = {}
        for line in text:
            line_x = re.findall("[\d]+",line)
            if int(line_x[0]) not in rel:
                rel[int(line_x[0])] = [int(line_x[1])]
            else:
                rel[int(line_x[0])].append(int(line_x[1]))
    return rel
            

def common_docs(l1,l2):
    counter = Counter(l2)
    final = []
    for i in l1:
        if counter[i]>0:
            final.append(counter)
    return len(final)

queries = process_rel()

def calc_recall(top_n):
    cos_sim = cosine_similarity(top_n)
    recall = {}
    for i in range(1,len(queries)+1):
        l1 = queries[i]
        l2 = cos_sim[i]
        retrieved = common_docs(l1,l2)
        total = len(queries[i])
        recall[i] = retrieved/total
    return recall

def calc_precision(top_n):
    cos_sim = cosine_similarity(top_n)
    precision = {}
    for i in range(1,len(queries)+1):
        l1 = queries[i]
        l2 = cos_sim[i]
        retrieved = common_docs(l1,l2)
        total = top_n
        precision[i] = retrieved/total
    return precision

print("Query Id's and document Id's in pairs (of descending order) :\n")

final_list = []

def list_retrieved():
    for key,value in cosine_similarity(-1).items():
        for doc_id in value:
            final_list.append((key,doc_id))
    
list_retrieved()
        
print(final_list,"\n")
    


def precision_recall_output():
    for i in [10,50,100,500]:
        print("For top",i,"documents, we have :\n")
        print("Queries\t\tPrecision\tRecall\n")
        print("----------------------------------------------\n")
        prec = calc_precision(i)
        recall = calc_recall(i)
        for j in range(1,len(queries)+1):
            print("Query",j,"\t",prec[j],"\t\t",recall[j],"\n")
        print("Average Precision (across all",len(queries),"queries): ",sum(prec.values())/len(prec),"\n")
        print("Average Recall (across all",len(queries),"queries): ",sum(recall.values())/len(recall),"\n\n")
    
precision_recall_output()


                
                
                
                
            

        
        


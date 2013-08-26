# See also tf_idf_linkedin.py for a much simpler example. See the file file for credits on 3 functions on tf-idf.
#Author : Ekta Grover, ekta1007@gmail.com
#tf_idf_linkedin_Jobfeed.py

import re , nltk
from nltk.tokenize import RegexpTokenizer
#import tokenize
from itertools import chain
from nltk import bigrams, trigrams
import math, string
import urllib2, urllib
import csv
import operator 


#Base Query
query="data mining machine learning python NLP NLTK predictive modelling artificial intelligence research scientist auction theory applied science collective intelligence analytics analyst"
query=query.lower()
query_name="query"
doc_names=[]
top_k=10
# list_of_words is a dict which has the summary of top_k words in the doc 
#for docs in doc_list , build doc_names


Y=[5796385, 6052768, 6175979, 6216895, 6222577, 6583427, 6584834, 6626351, 6723434, 6811983, 6836724, 6979495]
url=[]
for k in range(0,len(Y)):
    temp="http://www.linkedin.com/jobs?viewJob=&jobId="+str(Y[k])+"&trk=rj_jshp"
    url.append(temp)
doc_list=[]
#doc_names=raw.split("\n")[0].replace(" - Job | LinkedIn","").strip()

stopwords2=["after","about","jobs", "join","also","across","additional","agreement","area","community","company","companys","cookie","copy","copyright","corporate","corporation","could","create","current","computer","expertise","external","faster","focusedon","half","hired","home","people","new","following","full","fulltime","functions","services","show","sign","similar","skills","solutions","staff","starts","requires","policy","post","presentations","privacy","problems","products"]
for k in range(0,len(url)):
    html = urllib.urlopen(url[k]).read()
    raw = nltk.clean_html(html)
    if (raw.find("The job you&#8217;re looking for is no longer active")>=1 or raw.find("We can&#8217;t find the job you&#8217;re looking for")>=1):
        pass
    elif (raw.find("Bangalore")!=-1 or raw.find("Bengaluru")!=-1):
        doc_names.append(raw.split("\n")[0].replace(" - Job | LinkedIn","").strip())
        index_begin=raw.find("main content starts below")
        if index_begin !=-1 :
            index_begin=index_begin+len("main content starts below")
        elif index_begin ==-1 :
            index_begin==raw.find("Skip to main content")
            if (index_begin!=-1):
                index_begin=index_begin+len("Skip to main content")
        index_end=raw.find("Sign in to view similar jobs")
        if index_end !=-1 and index_begin !=-1:
            raw=raw[index_begin:index_end]
        elif index_end !=-1 or index_begin !=-1:
            pass
    # if we dont find both these contents, then just skip
        special_punct=["/", ":" ,"-","&","(",")","{","}"]
        for i in range(0,len(special_punct)):
            if special_punct[i] in raw:
                raw=raw.replace(special_punct[i]," ")
        for c in string.punctuation:
            raw= raw.replace(c,"")
        raw=raw.lower()
        doc_list.append(raw)  
# string.punctuation  '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

stopwords = nltk.corpus.stopwords.words('english')
stopwords.append(stopwords2)
stopwords=list(chain.from_iterable(stopwords))
 
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')

def freq(word, doc,docs):
    return docs[doc]['tokens'].count(word)
 
def word_count(docs,doc):
    return len(docs[doc]['tokens'])
    
def tf(word, doc,docs):
    return (freq(word, doc,docs) / float(word_count(docs,doc)))
 
 
def num_docs_containing(word, list_of_docs,docs,doc_names):
    count = 0
    for document in doc_names:
        if freq(word,document,docs) > 0:
            count += 1
    return count
 
 
def idf(word, list_of_docs,docs,doc_names):
    if num_docs_containing(word, list_of_docs,docs,doc_names)!=0:
        return math.log(len(list_of_docs) /
            float(num_docs_containing(word, list_of_docs,docs,doc_names)))
    else :
        return 0
 
 
def tf_idf(word, doc, list_of_docs,docs,doc_names):
    return (tf(word, doc,docs) * idf(word, list_of_docs,docs,doc_names))

docs={}
i=0
for doc_no in doc_names:
    docs[doc_no] = {'freq': {}, 'tf': {}, 'idf': {},'tf-idf': {}, 'tokens': []}
    tokens = tokenizer.tokenize(doc_list[i])
    docs[doc_no]['tokens']=tokens
    i=i+1
for doc_no in doc_names:
    for token in docs[doc_no]['tokens']:
        docs[doc_no]['freq'][token]=freq(token, doc_no,docs)
        docs[doc_no]['tf'][token]=tf(token, doc_no,docs)
        docs[doc_no]['idf'][token]=idf(token, doc_list,docs,doc_names)
        docs[doc_no]['tf-idf'][token]=tf_idf(token, doc_no, doc_list,docs,doc_names)

#post this the whole docs (dict of dict of 'freq', 'tf', 'idf','tf-idf', 'tokens', of which we will need only tf-idf list, corresponding to the individual tokens in that doc
#print docs

#Build the global vocab now
global_vocab =[]
for doc_no in doc_names:
    for token in set(docs[doc_no]['tokens']):
        if token not in global_vocab:
            global_vocab.append(token)
        elif token in global_vocab:
            pass
#print global_vocab -> All (global)terms in the corpus
dict_tf_idf={}
for token in global_vocab:
    dict_tf_idf[token] = dict((str(doc_no), '') for doc_no in doc_names)
for token in global_vocab :
    for doc_no in doc_names:
        if token in global_vocab and token in docs[doc_no]['tokens']:
            dict_tf_idf[token][doc_no] = docs[doc_no]['tf-idf'][token]
        elif token in global_vocab and token not in docs[doc_no]['tokens']: 
            dict_tf_idf[token][doc_no] = 0

#print dict_tf_idf
list_of_words={}
# Find what are the top terms by tf-id per doc- ie what terms summarize a doc
for doc_no in doc_names[0:len(doc_names)] :
    x=docs[doc_no]['tf-idf']
    sorted_y = sorted(x.iteritems(), key=operator.itemgetter(1))
    sorted_y.reverse()
    list_of_words[doc_no]=[sorted_y[0:top_k]]
#print list_of_words
		

# Now we need to do two things 1) Find the Sim(query,doc) and find tf-idf for the base against the whole corpus 2) For each doc_name, find the k most significant words
# TD-IDF of query

query_dict={}
docs_entire={}
# z is the merged corpus including the query+ docs
entire_corpus_list=[]
entire_corpus_list=doc_list
entire_corpus_list.append(query)
entire_corpus_names=[]
entire_corpus_names=doc_names
entire_corpus_names.append(query_name)

query_dict[query_name] = {'freq': {}, 'tf': {}, 'idf': {},'tf-idf': {}, 'tokens': []}
tokens = tokenizer.tokenize(query)
query_dict[query_name]['tokens']=tokens

for token in query_dict[query_name]['tokens']:
    query_dict[query_name]['freq'][token]=freq(token, query_name,query_dict)
    query_dict[query_name]['tf'][token]=tf(token, query_name,query_dict)
    
docs_entire = dict(docs.items() + query_dict.items())
for token in query_dict[query_name]['tokens']:
    query_dict[query_name]['idf'][token]=idf(token, entire_corpus_list,docs_entire,entire_corpus_names)#list_of_docs,docs,doc_names
    query_dict[query_name]['tf-idf'][token]=tf_idf(token, query_name, entire_corpus_list,docs_entire,entire_corpus_names) 

#updating global var for tokens only in base query is not required since tf-idf when doing similarity will be 0 anyways.

query_dict_tf_idf={}
for token in global_vocab:
    query_dict_tf_idf[token] = {query_name:{}}
for token in global_vocab :
    if token in global_vocab and token in query_dict[query_name]['tokens']:
        query_dict_tf_idf[token][query_name] = query_dict[query_name]['tf-idf'][token]
    else:
        #if token in global_vocab and token not in query_dict[query_name]['tokens']: 
        query_dict_tf_idf[token][query_name]= 0
#print query_dict_tf_idf

# merging both the doc_tf_idf_dicts and dict_tf_idf
sim={}

for doc_name in doc_names[0:len(doc_names)-1] :
    sim[str(doc_name),query_name] = {'tf-idf': 0}
for doc_name in doc_names[0:len(doc_names)-1] :
    normalize_query=0
    normalize_doc=0
    for token in dict_tf_idf.keys():
        if dict_tf_idf[token][doc_name] !=0 and query_dict_tf_idf[token][query_name] !=0 :
            sim[str(doc_name),query_name]['tf-idf']= sim[str(doc_name),query_name]['tf-idf']+dict_tf_idf[token][doc_name]*query_dict_tf_idf[token][query_name]
            normalize_doc=dict_tf_idf[token][doc_name]*dict_tf_idf[token][doc_name]+normalize_doc
            normalize_query=query_dict_tf_idf[token][query_name]*query_dict_tf_idf[token][query_name]+normalize_query
        else :
            pass
    if (math.sqrt(normalize_query)*math.sqrt(normalize_doc)) !=0:
        sim[str(doc_name),query_name]['tf-idf']=sim[str(doc_name),query_name]['tf-idf']/(math.sqrt(normalize_query)*math.sqrt(normalize_doc))
    else :
        sim[str(doc_name),query_name]['tf-idf']=0.0


# Rank order the sim values across the docs
x={}
for items in sim.keys():
    x[items]=sim[items]['tf-idf']
    sorted_x = sorted(x.iteritems(), key=operator.itemgetter(1))
    sorted_x.reverse()
#sorted_x.reverse() has the list of docs sorted by top tf-idf 
    
#The sim for tf-idf - write everything to csv file
f=open("C:\Users\ekta\Desktop\unittest_tf_idf_Linkedin5.csv", "wb")
mywriter = csv.writer(f,dialect='excel')
#Note I am re-using m on purpose
for doc_no in doc_names[0:len(doc_names)-1]:
    mywriter.writerow([doc_no])
    m=docs[doc_no]['tf'].keys()
    m.insert(0,"keys")
    mywriter.writerow(m)
    m=docs[doc_no]['tf'].values()
    m.insert(0,"tf")
    mywriter.writerow(m)
    m=docs[doc_no]['idf'].values()
    m.insert(0,"idf")
    mywriter.writerow(m)
    m=docs[doc_no]['tf-idf'].values()
    m.insert(0,"tf-idf")
    mywriter.writerow(m)
    mywriter.writerow([""])
mywriter.writerow([query_name])
m=query_dict['query']['tf'].keys()
m.insert(0,"keys")
mywriter.writerow(m)
m=query_dict['query']['tf'].values()
m.insert(0,"tf")
mywriter.writerow(m)
m=query_dict['query']['idf'].values()
m.insert(0,"idf")
mywriter.writerow(m)
m=query_dict['query']['tf-idf'].values()
m.insert(0,"tf-idf")
mywriter.writerow(m)
mywriter.writerow([""])
f.close()

# Write 3 csv files with final results
#writing realtionships
f=open("C:\Users\ekta\Desktop\unittest_tf_idf_Linkedin51.csv", "wb")
mywriter = csv.writer(f,dialect='excel')
mywriter.writerow(["Job description","Tf-Idf value"])
for i in range(0,len(doc_names)-1):
    mywriter.writerow([sorted_x[i][0][0],sorted_x[i][1]])
f.close()

#,list_of_words[sorted_x[i][0][0]]]
f=open("C:\Users\ekta\Desktop\unittest_tf_idf_Linkedin52.csv", "wb")
mywriter = csv.writer(f,dialect='excel')
mywriter.writerow(["Job description"])
mywriter.writerow([""])
#,"list_of_words","Tf-idf values"])
for i in range(0,len(doc_names)-1):
    mywriter.writerow([sorted_x[i][0][0]])
    mywriter.writerow(["list_of_words","Tf-idf values"])
    for m in range(0,top_k):
        mywriter.writerow([list_of_words[sorted_x[i][0][0]][0][m][0], list_of_words[sorted_x[i][0][0]][0][m][1]])
    mywriter.writerow([""])
f.close()

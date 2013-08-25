
# -*- coding: utf-8 -*-
# freq,word_count , tf, num_docs_containing, idf, tf_idf forked(and modified) from from https://gist.github.com/AloneRoad/1605037
# to do extend the base case, lemmatization , dispersion plots & concordance in NLTK and other hacks on  base below
#stop words not correctly parsing, need to fix that

import re , nltk
from nltk.tokenize import RegexpTokenizer
#import tokenize
from itertools import chain
from nltk import bigrams, trigrams
import math, string
import urllib2, urllib
# TD-idf small example

doc_list =["ekta just met a candy girl", "ekta will go to school tomorrow", "ekta could but will not", "oh ekta is coming to work"]
#Base Query
query="ekta just went to school"
#for docs in doc_list , build doc_names
doc_names=[]
for i in range(0,len(doc_list)):
    doc_names.append('doc'+str(i+1))
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
print docs

"""  
# To test & understand the base code use the doc_list input.
# The functions from Marcelo's had some severe flaws, which I rectified, and I hope you will be able to see them now. for one, IDF can NEVER be negative, unless you use the augmented/custom tf-idf , see more at wiki-
http://en.wikipedia.org/wiki/Tf%E2%80%93idf

doc_list =["ekta just met a candy girl", "ekta will go to school tomorrow", "ekta could but will not", "oh ekta is coming to work"]
This will give docs as below, compute for yourself and validate
{'oh ekta is coming to work': {'tf': {'oh': 0.16666666666666666, 'is': 0.16666666666666666, 'work': 0.16666666666666666, 'ekta': 0.16666666666666666, 'to': 0.16666666666666666, 'coming': 0.16666666666666666}, 'idf': {'oh': 1.3862943611198906, 'is': 1.3862943611198906, 'work': 1.3862943611198906, 'ekta': 0.0, 'to': 0.6931471805599453, 'coming': 1.3862943611198906}, 'freq': {'oh': 1, 'is': 1, 'work': 1, 'ekta': 1, 'to': 1, 'coming': 1}, 'tokens': ['oh', 'ekta', 'is', 'coming', 'to', 'work'], 'tf-idf': {'oh': 0.23104906018664842, 'is': 0.23104906018664842, 'work': 0.23104906018664842, 'ekta': 0.0, 'to': 0.11552453009332421, 'coming': 0.23104906018664842}}, 'ekta will go to school tomorrow': {'tf': {'school': 0.16666666666666666, 'ekta': 0.16666666666666666, 'will': 0.16666666666666666, 'to': 0.3333333333333333, 'go': 0.16666666666666666, 'tomorrow': 0.16666666666666666}, 'idf': {'school': 1.3862943611198906, 'ekta': 0.0, 'will': 0.6931471805599453, 'to': 0.6931471805599453, 'go': 1.3862943611198906, 'tomorrow': 1.3862943611198906}, 'freq': {'school': 1, 'ekta': 1, 'will': 1, 'to': 2, 'go': 1, 'tomorrow': 1}, 'tokens': ['ekta', 'will', 'go', 'to', 'school', 'tomorrow'], 'tf-idf': {'school': 0.23104906018664842, 'ekta': 0.0, 'will': 0.11552453009332421, 'to': 0.23104906018664842, 'go': 0.23104906018664842, 'tomorrow': 0.23104906018664842}}, 'ekta could but will not': {'tf': {'will': 0.2, 'not': 0.2, 'could': 0.2, 'ekta': 0.2, 'but': 0.2}, 'idf': {'will': 0.6931471805599453, 'not': 1.3862943611198906, 'could': 1.3862943611198906, 'ekta': 0.0, 'but': 1.3862943611198906}, 'freq': {'will': 1, 'not': 1, 'could': 1, 'ekta': 1, 'but': 1}, 'tokens': ['ekta', 'could', 'but', 'will', 'not'], 'tf-idf': {'will': 0.13862943611198905, 'not': 0.2772588722239781, 'could': 0.2772588722239781, 'ekta': 0.0, 'but': 0.2772588722239781}}, 'ekta just met a candy girl': {'tf': {'a': 0.5, 'just': 0.16666666666666666, 'ekta': 0.16666666666666666, 'candy': 0.16666666666666666, 'met': 0.16666666666666666, 'girl': 0.16666666666666666}, 'idf': {'a': 0.0, 'just': 1.3862943611198906, 'ekta': 0.0, 'candy': 1.3862943611198906, 'met': 1.3862943611198906, 'girl': 1.3862943611198906}, 'freq': {'a': 3, 'just': 1, 'ekta': 1, 'candy': 1, 'met': 1, 'girl': 1}, 'tokens': ['ekta', 'just', 'met', 'a', 'candy', 'girl'], 'tf-idf': {'a': 0.0, 'just': 0.23104906018664842, 'ekta': 0.0, 'candy': 0.23104906018664842, 'met': 0.23104906018664842, 'girl': 0.23104906018664842}}}
"""

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

print dict_tf_idf

# Now we need to do two things 1) Find the Sim(query,doc) and find tf-idf for the base against the whole corpus 2) For each doc_name, find the k most significant words
# TD-IDF of query

query_name="query"
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

query_dict_tf_idf={}
for token in global_vocab:
    query_dict_tf_idf[token] = {query_name:{}}
for token in global_vocab :
    if token in global_vocab and token in query_dict[query_name]['tokens']:
        query_dict_tf_idf[token][query_name] = query_dict[query_name]['tf-idf'][token]
    else:
        #if token in global_vocab and token not in query_dict[query_name]['tokens']: 
        query_dict_tf_idf[token][query_name]= 0
print query_dict_tf_idf

# merging both the doc_tf_idf_dicts and dict_tf_idf
"""sim_tf_idf={}
sim_tf_idf = dict(dict_tf_idf.items() + query_dict_tf_idf.items()) """
sim={}

for doc_name in doc_names[0:len(doc_names)-1] :
    sim[str(doc_name),query_name] = {'tf-idf': 0}
for doc_name in doc_names[0:len(doc_names)-1] :
   # sim[str(doc_name)+query_name]=0
    normalize=0
    for token in dict_tf_idf.keys():
        sim[str(doc_name),query_name]['tf-idf']= sim[str(doc_name),query_name]['tf-idf']+dict_tf_idf[token][doc_name]*int(query_dict_tf_idf[token][query_name])
        normalize=dict_tf_idf[token][doc_name]*dict_tf_idf[token][doc_name]+normalize
    sim[str(doc_name),query_name]['tf-idf']=sim[str(doc_name),query_name]['tf-idf']/math.sqrt(normalize)

# Rank order the sim values across the docs

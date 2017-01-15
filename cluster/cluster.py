import pandas as pd
import numpy as np
import scipy.spatial.distance as dist
import jieba
import re

from cluster.cluster import calc_hot, sort_hot, calc_dict, calc_list, freq2vec, build_doc, build_vec
from cluster.cluster import jaccard, Euclidean, Cosine, Cosine_Cluster, jaccard_Cluster

with open('stopwords.dat','r') as f:
    g=f.readlines()
stopwords=set([x.rstrip('\n').decode('utf8') for x in g])


df = pd.read_csv('news.csv')

document = build_doc(df)
word_dict = calc_dict(document)
word_list = calc_list(document)
#sort df by hot
df = calc_hot(df,word_dict)
df = sort_hot(df)
vec = build_vec(df,word_list)
#Cosine_Cluster(vec,df)
jaccard_Cluster(vec,df)
print len(vec)
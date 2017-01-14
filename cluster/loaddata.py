import pandas as pd
import jieba
import re
df = pd.read_csv('news.csv')

with open('stopwords.dat','r') as f:
    g=f.readlines()
stopwords=set([x.rstrip('\n').decode('utf8') for x in g])

def clac_freq(document):
    pat_num=re.compile(r'\d{2,}');pat_en=re.compile(r'[a-zA-Z]{3,}');pat_ch=re.compile(u"[\u4e00-\u9fa5]+")
    sentences=pat_ch.findall(document);ch_text=u''.join(sentences);word_dict={};word_dict['numOfNumbers']=0;word_dict['numOfNumbers']+=len(pat_num.findall(document))
    word_list=[];word_list=jieba.lcut(ch_text);word_list+=pat_en.findall(document);word_list=[x for x in word_list if x not in stopwords]
    for word in word_list:
        word_dict.setdefault(word,0);word_dict[word]+=1
    return word_dict,word_list

def freq2vec(word_dict,word_list):
    length=len(word_list)
    word2index=dict([(word_list[i],i) for i in range(length)])
    new_vec=[0]*length
    for word,freq in word_dict.iteritems():
        t=word2index.get(word,None)
        if t==None:
            continue
        else:
            new_vec[t]=freq
    return new_vec

def build_doc(df):
    document = ''
    for d in df['title']:
        document += d.decode('utf-8')
        document += ','
    for d in df['body']:
        document += d.decode('utf-8')
        document += ','
    return document

document = build_doc(df)
word_dict,word_list = clac_freq(document)

for d in df['title']:
    document = d.decode('utf-8')
    word_dict, x = clac_freq(document)
    new_vec = freq2vec(word_dict,word_list)
    print new_vec,len(new_vec)

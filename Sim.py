#encoding=utf-8
import codecs
import copy
import math
import requests
import json
import wordSim
from bosonnlp import BosonNLP

def Denoising(tagdict , uTag = None):
    """去除噪声

    tagList : 分词过后得到的列表
    uTag : 需要去噪的词性标记列表，默认为('w','o','y','u')
    """
    if(uTag):
        uselessTag = uTag
    else:
        uselessTag = ('w','o','y','u')
    ls = tagdict
    ls2=[]
    for index,it in enumerate(ls['tag']):
        if it[0] not in uselessTag:
            ls2.append(ls['word'][index])

    return ls2

def getTFdict(wordlist):
    """计算词频 
    返回 词-词频 的字典

    wordlist: 需要计算词频的分词列表
    """
    d={}
    for item in wordlist:
        if item in d:
            d[item]+=1.0
        else:
            d[item]=1.0

    lenofd=len(d)
    for key in d:
        d[key]/=lenofd

    return d

def getSimilar_by_cos(TFdict1,TFdict2):
    """获取两个句子的相似性

    Sdict1: 计算好的词频字典1
    Sdict1: 计算好的词频字典1
    """
    TFD1=copy.deepcopy(TFdict1)
    TFD2=copy.deepcopy(TFdict2)

    wordlist1=TFD1.keys()
    wordlist2=TFD2.keys()

    #将两个集合补齐，
    difflist1=set(wordlist1).difference(wordlist2)
    difflist2=set(wordlist2).difference(wordlist1)
    difflist=set(difflist1).union(difflist2)
    for keys in difflist:
        if keys not in wordlist1:
            TFD1[keys]=0.0
        if keys not in wordlist2:
            TFD2[keys]=0.0

    a=0.0
    b=0.0
    c=0.0

    #计算两个n维向量TFD1、TFD2的余弦值
    for key in TFD1:
        a+=(TFD1[key]*TFD2[key])
        b+=(TFD1[key]**2)
        c+=(TFD2[key]**2)
    
    similarVlue=a/(math.sqrt(b)*math.sqrt(c))

    return similarVlue

def ScentenceSimilar(str1,str2):
    """得到str1和str2的相似度，使用余弦相似性计算。
    采用bosonnlp分词；联网使用。

    """
    
    nlp = BosonNLP('wx3Ua05Y.21658.Ch876jBfuqIH')
    
    #获取分词结果
    tags1=nlp.tag(str1.lower())
    tags2=nlp.tag(str2.lower())

    tfdict1=getTFdict(Denoising(tags1[0]))
    tfdict2=getTFdict(Denoising(tags2[0]))

    return getSimilar_by_cos(tfdict1,tfdict2)

def readFFile(path):
    sentences=[]
    file_obj = codecs.open(path, 'r', 'utf-8')
    while True:
        line = file_obj.readline()
        line = line.strip('\r\n')
        if not line:
            break
        sentences.append(line)
    file_obj.close()
    return sentences

def getSimbyMarix(wordList1,wordList2,weightDitc={}):

    marix=[]
    for word1 in wordList1:
        lenArray=[]
        for word2 in wordList2:
            wordpairS=hownet_word_sim(word1,word2)
            if wordpairS==None:
                lenArray.append(0)
            else:
                lenArray.append(wordpairS)
        marix.append(lenArray)

    a=0.0
    b=0.0

    for i,arra in enumerate(marix):
        lenmax=max(arra)
        weight=1
        if weightDitc.has_key(wordList1[i]):
            weight=weightDitc[wordList1[i]]
        a+=weight*lenmax
        b+=weight
    similar=a/b
    return similar

def hownet_word_sim(word1,word2):
    data = {'apiKey':"vpze450m",'word1':word1,'word2':word2}
    url = 'http://yuzhinlp.com/api/call_similarity.do'
    html = requests.post(url,data).text
    s=requests.session()
    s.keep_alive = False
    html=json.loads(html,encoding='utf-8')
    if html.has_key('error'):
        return 0
    return float(html['similarity'])


def hownet_sentence_sim(s1,s2):
    data = {'apiKey':"vpze450m",'text1':s1,'text2':s2}
    url = 'http://yuzhinlp.com/api/getShortSimilarityApi.do'
    html = requests.post(url,data).text
    s=requests.session()
    s.keep_alive = False
    html=json.loads(html,encoding='utf-8')
    if html.has_key('error'):
        return 0
    return float(html['success'])

if __name__=="__main__":
    scentences1=readFFile(r"testSet/trainSet.txt")
    scentences2=readFFile(r"testSet/testSet1.txt")

    nlp = BosonNLP('wx3Ua05Y.21658.Ch876jBfuqIH')

    # 获取分词结果
    tags1 = nlp.tag(scentences1[16])
    tags2 = nlp.tag(scentences2)
    wordA = Denoising(tags1[16])
    wordB = Denoising(tags2[16])



    print hownet_sentence_sim(scentences1[16],scentences2[16])





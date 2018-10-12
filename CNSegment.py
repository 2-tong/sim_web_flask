#encoding=utf-8

from bosonnlp import BosonNLP
import json

bosonkey='wx3Ua05Y.21658.Ch876jBfuqIH'
class CNSegment:
    """
    封装分词工具。
    使用bosonnlp提供API
    """

    #停用词表
    stopwords = []

    def __init__(self):
        self.nlp=BosonNLP(bosonkey)

    def get_tags(self,sentences):
        """
        获取分词
        :param sentences:分词的句子或者句子list
        :return: 分词结果list
        """
        result= self.nlp.tag(sentences)
        return result

    def denoisingOne(self,tagdict , uTag = None,useStopWord = False):
        """通过词性和停用词去除噪声

            :param  tagList : 分词过后得到的列表
            :param  uTag : 需要去噪的词性标记列表，默认为('w','o','y','u')
            :return: 分词结果list
            """
        if (uTag):
            uselessTag = uTag
        else:
            uselessTag = ('w', 'o', 'y', 'u')
        tagdict
        word_list = []
        for index, it in enumerate(tagdict['tag']):
            if it[0] not in uselessTag:
                if not useStopWord:
                    word_list.append(tagdict['word'][index])
                elif tagdict['word'][index] not in self.stopwords:
                    word_list.append(tagdict['word'][index])
        return word_list

    def cut(self,sentences):
        """
        分词
        :param sentences:需要分词的语料集
        :return: 去噪后的单词list
        """
        tags=self.get_tags(sentences)
        cutedSentences=[]
        for sentence in tags:
            cutedSentences.append(self.denoisingOne(sentence))
        return cutedSentences

    def depenPars(self,sentences):
        return self.nlp.depparser(sentences)


if __name__=="__main__":
    from fileObject import FileObj
    Fobj=FileObj(r"testSet/trainSet.txt")

    scentences1 = Fobj.read_lines()
    cutTool=CNSegment()
    lst=cutTool.depenPars(scentences1[0])
    print json.dumps(lst,encoding="UTF-8", ensure_ascii=False)
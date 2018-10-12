#encoding=utf-8

import urllib
import json
from aip import AipNlp
from bosonnlp import BosonNLP
#LTP密钥和url
API_key = "c1Q8e8M1c5wlOQpR0lkFNQPhVaXY8C8SrepkKykz"
API_url = "https://api.ltp-cloud.com/analysis/"

#百度自然语言处理所需密钥等
Bai_appid = '11337761'
Bai_apikey = '68nandCD7AAnLAUfjhPF9aL9'
Bai_Skey = 'GLiuqH5AaiaxGdOM2eTs0zDiQcQEQwWR'

bosonkey='wx3Ua05Y.21658.Ch876jBfuqIH'
class DepTree:
    """
    依存关系类，用于获取、分析依存关系
    args:ltp平台参数表
    nlp_baidu:百度nlp实例
    """

    args = {
        'api_key' : API_key,
        'text' : '',
        'pattern' : '',
        'format' : 'json'
    }

    nlp_baidu = AipNlp(Bai_appid, Bai_apikey, Bai_Skey)
    def get_LtpDepT(self,sentences,pattern='dp'):
        """
        从LTP平台获取语句分析信息
        :param sentences: 需要分析的句子
        :param pattern: 分析类型，默认sdp,参考ltp平台文档
        :return: 转换后的list
        """
        self.args['text']=sentences
        self.args['pattern'] = pattern
        return json.loads(self.urlget())[0][0]

    def urlget(self):
        """
        urllib访问平台
        根据本对象设定好的args
        :return: json字符串
        """
        result = urllib.urlopen(API_url, urllib.urlencode(self.args))
        str = result.read()
        return str

    def get_BaiDepT(self,text):
        """
        从百度平台获取语句分析信息
        :param text: 需要分析的句子
        :return: 依照平台文档的list-dict集合
        """
        options = {}
        options["mode"] = 1
        result=self.nlp_baidu.depParser(text,options)
        return result

    def get_BosDepT(self,text):
        bos=BosonNLP(bosonkey)
        return bos.depparser(text)

    def list_tree(self,resultList,type=None):
        """
        同一转换格式
        :param resultList:在线工具返回结果
        :param type:在线工具类型
        :return:list所构成的tree
        """
        treeArray = resultList['head']

        #找出根节点
        rootTree=[]
        for index,head in enumerate(treeArray):
            if head== -1:
                rootTree.append(index)
                break

        #数组tree到列表Tree转换
        self.treeTrans(rootTree,treeArray)

        return rootTree

    def treeTrans(self,tmproot,treeAraay):
        """
        将列表数组转换成按层次顺序的listTREE
        便于之后的树遍历。
        使用递归算法  O(n*n)
        :param tmproot:当前根节点
        :param treeAraay: 数组Tree
        :return: None，结果放在最开始传入的tmproot中
        """

        tmp = []
        flag = True

        #找出当前跟节点的所有子节点
        for index, head in enumerate(treeAraay):
            if head == tmproot[0]:
                flag = False
                tmp.append([index])

        #当前根节点没有子节点，list[1]=-2
        if flag:
            tmproot.append(-2)

        #有子节点就依次递归
        else:
            tmproot.append(tmp)
            for root in tmp:
                self.treeTrans(root,treeAraay)

    def treeSim(self,treeA,treeB):
        pass

def wordPair_sim(pairA,pairB):
    pass

if __name__ == "__main__":
    str="百度是一家高科技公司"
    str2="耶利米对我说，他的任务是准备当地自治。"
    dtreetool = DepTree()

    # #ltp测试
    # Tresult=dtreetool.get_LtpDepT(str)
    # lst=[]
    # for len in Tresult:
    #     lst.append((len['cont'],len['relate'],len['parent']))
    # print json.dumps(lst, encoding="UTF-8", ensure_ascii=False)
    #
    # #百度测试
    # Bresult=dtreetool.get_BaiDepT(str)
    # lst = []
    # for len in Bresult['items']:
    #     lst.append((len['word'], len['deprel'],len['head']))
    # print json.dumps(lst, encoding="UTF-8", ensure_ascii=False)
    #
    # Bosresult=dtreetool.get_BosDepT(str)[0]
    # print(Bosresult)
    # lst = []
    # for index,word in enumerate(Bosresult['word']):
    #     lst.append([word, Bosresult['role'][index], Bosresult['head'][index]])
    # print json.dumps(lst, encoding="UTF-8", ensure_ascii=False)
    #
    # Bosresult = dtreetool.get_BosDepT(str2)[0]
    # print(Bosresult)
    # lst = []
    # for index, word in enumerate(Bosresult['word']):
    #     lst.append([word, Bosresult['role'][index], Bosresult['head'][index]])
    # print json.dumps(lst, encoding="UTF-8", ensure_ascii=False)

    result=dtreetool.get_BosDepT(str)[0]

    tree=dtreetool.list_tree(result)

    print tree
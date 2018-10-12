#encoding=utf-8

from sqlConnecter import myDB
import Sim
from CNSegment import CNSegment
from aip import AipNlp
import thread


#百度自然语言处理所需密钥等
Bai_appid = '11337761'
Bai_apikey = '68nandCD7AAnLAUfjhPF9aL9'
Bai_Skey = 'GLiuqH5AaiaxGdOM2eTs0zDiQcQEQwWR'

def put_stu_answer(quesid,answertext):
    stu_List = []
    for line in answertext.splitlines():
        lineList = line.split()
        try:
            lineList[0] = int(lineList[0])
        except:
            return "格式错误"
        student = {"ID": lineList[0], "answer": lineList[1]}
        stu_List.append(student)
    thread.start_new_thread(createThread2Sim,(quesid,stu_List,True))
    return "成功！正在计算中"

def createThread2Sim(quesid,stu_List,weight=False,treeW=0.3,mriax=0.7):
    simTOOl=wordSimTool()
    db=myDB()
    stand_answer=db.getstandAndwerbyQusid(quesid)[0]
    weightDict={}
    if weight:
        weightDict=db.get_weightDict(quesid)
    ctool=CNSegment()
    cut_tand_answer=ctool.cut(stand_answer)[0]

    for student in stu_List:
        cut_stu_answer=ctool.cut(student['answer'])[0]
        score1 = 0
        if mriax!=0:
            score1=Sim.getSimbyMarix(cut_tand_answer,cut_stu_answer,weightDict)
        score=simTOOl.getsentenceSim(stand_answer,student['answer'])
        student['score']=treeW*score['score']+mriax*score1
    res=db.addstu_answers(stu_List,quesid)
    if not res:
        print 'wrong'
    else:
        print 'marking ok!'

class wordSimTool:
    client=AipNlp(Bai_appid,Bai_apikey,Bai_Skey)

    def getwordsim_api(self,wordA,wordB):
        """
        测量词汇的相似度，词林、百度NLP
        :param wordA: 测量词1
        :param wordB: 测量词2
        :return: 文档dict。
                 包含相似度值（float） （0，1]
        """
        result=self.client.wordSimEmbedding(wordA,wordB)
        return result

    def getsentenceSim(self,s1,s2):
        es1=s1.encode('utf-8')
        es2=s2.encode('utf-8')
        return self.client.simnet(es1,es2)


if __name__=="__main__":
    student=[{'ID':112,'answer':u"订一张从北京起飞的机票"}]
    createThread2Sim(20,student,weight=True)


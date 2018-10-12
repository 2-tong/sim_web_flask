# -*- coding: utf-8 -*- #
import MySQLdb
class myDB:
    dbuser='sim_web'
    dbpsw = '123456'
    dbname = 'simsys'

    def __init__(self):
        self.db = MySQLdb.connect('localhost',self.dbuser,self.dbpsw,self.dbname,charset='utf8')
        self.cursor = self.db.cursor()

    def checkpsw(self,username ,psw):
        SQLstr="""
            SELECT
            sim_user.`password`,sim_user.`user_id`
            FROM
            sim_user
            WHERE
            sim_user.username='%s'
        """%(username)
        self.cursor.execute(SQLstr)
        result=self.cursor.fetchone()
        id=-1;
        if(result and result[0] == psw):
            id=result[1]
        return id

    def get_lastid(self):
        sql="""select last_insert_id()"""
        self.cursor.execute(sql)
        id=self.cursor.fetchone()[0]
        return id

    def addQuestion(self,standAns,quesname,uId):
        sql="""
            INSERT INTO question
            (question.ques_name,question.ques_answer,question.user_id)
            VALUES('%s','%s',%d)
        """%(quesname,standAns,uId)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            return -1
        return self.get_lastid()

    def addWeight(self,ww_list,qid):
        try:
            for wd_we in ww_list:
                sql = """
                    INSERT INTO ques_word_weight 
                    (ques_word_weight.ques_id,ques_word_weight.word,ques_word_weight.weght)
                    VALUES( %d, '%s', %f)
                """ % (qid, wd_we["word"], wd_we["weight"])
                self.cursor.execute(sql)
            self.db.commit()
        except Exception ,e:
            print e
            self.db.rollback()
            return False
        return True

    def getquesbyuid(self,userid):
        sql="""
            SELECT
            question.ques_id,
            question.ques_name
            FROM
            question
            WHERE
            question.user_id = %d
        """%(userid)

        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        return res

    def getstandAndwerbyQusid(self,quesid):
        sql="""
            SELECT
            question.ques_answer
            FROM
            question
            WHERE
            question.ques_id = %d
        """%(quesid)

        self.cursor.execute(sql)
        res=self.cursor.fetchone()
        return res

    def addstu_answers(self,stu_list,quesid):
        try:
            for student in stu_list:
                sql="""
                    INSERT INTO stu_score
                    VALUES
                    (%d,%d,'%s',%f)
                """%(student['ID'],quesid,student['answer'],student['score'])
                self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            return False
        return True

    def get_all_teacherScore(self,userid):
        sql="""
            SELECT
                stu_score.student_id,
                stu_score.ques_id,
                stu_score.score,
                stu_score.answer 
            FROM
                stu_score 
            WHERE
                stu_score.ques_id IN ( SELECT question.ques_id FROM question WHERE question.user_id =%d )
        """%(userid)

        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        return result

    def get_weightDict(self,quesid):
        """
        返回权重列表
        :param quesid:
        :return: 词-权重的字典
        """
        sql="""
            SELECT
            ques_word_weight.word,
            ques_word_weight.weght
            FROM
            ques_word_weight
            WHERE
            ques_word_weight.ques_id=%d
        """%(quesid)
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        if result:
            dic = {}
            for line in result:
                dic[line[0]] = line[1]
            return dic
        else:
            return {}

    def __del__(self):
        self.cursor.close()
        self.db.close()
        print "DB  disconnectted!"



if __name__=="__main__":
    db=myDB()
    res=db.get_weightList(16)
    dic={}
    for line in res:
        dic[line[0]]=line[1]
    print dic
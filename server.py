#! /usr/bin/env python
# -*- coding: utf-8 -*-

import jieba
import jieba.analyse
import jieba.posseg as pseg
import os
import codecs
import math
import json
import re
import string
import httplib,urllib,urllib2
import random
from trim import sentence,construct_tree

f = open('text.txt')
s = f.readlines()
# k is ：
k = s[0].replace('\n','')
# l is ！
l = s[1].replace('\n','')
# l1 is ,
l1 = s[2].replace('\n','')
# l2 is 图
l2 = s[3].replace('\n','')
# l3 is 。
l3 = s[4].replace('\n','')
# l4 is [图]
l4 = s[5].replace('\n','')
# l5 is [组图]
l5 = s[6].replace('\n','')
l6 = s[7].replace('\n','')
l7 = s[8].replace('\n','')
# l8 is ？
l8 = s[9].replace('\n','')
# l9 is 上引号
l9 = s[10].replace('\n','')
# l10 is 下引号
l10 = s[11].replace('\n','')
f.close()
def delete(old):
    
    temp = string.replace(old,l2.decode('utf-8'),"")
    temp = temp.lstrip()
    temp = string.replace(temp,l4.decode('utf-8'),"")
    temp = string.replace(temp,l5.decode('utf-8'),"")
    temp = string.replace(temp,l6.decode('utf-8'),"")
    temp = string.replace(temp,l7.decode('utf-8'),"")
    #去掉数据库中的关联词
    # for term in mon_db1[col_name1].find():
    #     for word in term['words']:
    #         if term['type'] == 1:
    #             temp = string.replace(temp,word,"")
    #去掉引号
    temp = string.replace(temp,l9.decode('utf-8'),"")
    temp = string.replace(temp,l10.decode('utf-8'),"")
    
    temp = string.replace(temp,'-',"")
    zuoyin = "】"
    youyin = "【"
    temp = string.replace(temp,zuoyin.decode('utf-8'),"")
    temp = string.replace(temp,youyin.decode('utf-8'),"")
    
    
    zifu = '·'
    temp = string.replace(temp,zifu.decode('utf-8'),"")
    
    sheng = "..."
    temp = string.replace(temp,sheng.decode('utf-8'),"")
    tu = "/图"
    temp = string.replace(temp,tu.decode('utf-8'),"")
    daoyu = "导语："
    temp = string.replace(temp,daoyu.decode('utf-8'),"")
    #去掉非汉字
    temp = string.replace(temp,"+","")
    temp = string.replace(temp,"Iwatchfootballmatchwithmyfriends.","")
    
    temp = string.replace(temp,">>","")
    ad = "丶"
    temp = string.replace(temp,ad.decode('utf-8'),"")
   
    #去掉顿点之前的数字
    dund = '、'
    a3 = re.compile('\d{1}'+dund.decode('utf-8'))
    temp = a3.sub('',temp)


    #去掉日期4-2-2
    aa = re.compile('\d{4}'+'-'+'\d{2}'+'-'+'\d{2}')
    temp = aa.sub('',temp)

    #去掉7位或者8位连续数字
    aa = re.compile('\d{7,8}')
    temp = aa.sub('',temp)
    
    xiaoyu = "＜"
    temp = string.replace(temp,xiaoyu.decode('utf-8'),"")
    dayu = ">"
    temp = string.replace(temp,dayu.decode('utf-8'),"")
    wu = "5、"
    temp = string.replace(temp,wu.decode('utf-8'),"")

    #去掉括号中间的内容
    hao1 = "（"
    hao2 = "）"
    a3 = re.compile(hao1.decode('utf-8')+'.*?'+hao2.decode('utf-8') )
    temp = a3.sub('',temp)
    a1 = re.compile('\(.*?\)' )
    temp = a1.sub('',temp)
    a1 = re.compile('\[.*?\]' )
    temp = a1.sub('',temp)
    
    tupian = "图片来源："
    temp = string.replace(temp,tupian.decode('utf-8'),"")
    tupian = "图片说明："
    temp = string.replace(temp,tupian.decode('utf-8'),"")
    #去掉日期和时间
    '''
    yue = "月"
    ri = "日"
    a2 = re.compile('\d{1,2}'+yue.decode('utf-8')+'\d{1,2}'+ri.decode('utf-8'))
    temp = a2.sub('',temp)
    '''
    a3 = re.compile('\d{1,2}:\d{1,2}')
    temp = a3.sub('',temp)
    a3 = re.compile('\d{1,2}/\d{1,2}')
    temp = a3.sub('',temp)
    
    #去掉第一词是连词的
    words = pseg.cut(temp)
    for w in words:
        if w.flag == 'c':
            temp = string.replace(temp,w.word,"",1)
        break
    #去掉第一词是连词的
    words = pseg.cut(temp)
    for w in words:
        if w.flag == 'c':
            temp = string.replace(temp,w.word,"",1)
        break
    
    return temp

def cixing(old):
    org = old
    words = pseg.cut(org)
    qingli = "清理"
    try:
        while 1:
            w = words.next()
            k = words.next()
            #去掉形容词
            if (w.flag == 'a' or w.flag == 'ad' or w.flag == 'an' or w.flag == 'ag' or w.flag == 'al') and w.word != qingli.decode('utf-8'):
                old = string.replace(old,w.word,"")
                if k.flag == 'uj':
                    old = string.replace(old,w.word,"")
    except StopIteration:
        print 'old'
    words = pseg.cut(org)

    try:
        w = words.next()
        while 1:
            w = words.next()
            k = words.next()
            #去掉形容词
            if (w.flag == 'a' or w.flag == 'ad' or w.flag == 'an' or w.flag == 'ag' or w.flag == 'al') and w.word != qingli.decode('utf-8'):
                old = string.replace(old,w.word,"")
                if k.flag == 'uj':
                    old = string.replace(old,w.word,"")
    except StopIteration:
        print 'old'
    return old


#计算标题字数
def countnum(temp):
    shu1 = "《"
    shu2 = "》"
    dunhao = "、"
    maohao = "："
    temp = string.replace(temp,shu1.decode('utf-8'),"")
    temp = string.replace(temp,shu2.decode('utf-8'),"")
    temp = string.replace(temp,maohao.decode('utf-8'),"")
    temp = string.replace(temp,dunhao.decode('utf-8'),"")
    temp = string.replace(temp,'-',"")
    doudian = "·"
    temp = string.replace(temp,doudian.decode('utf-8'),"")
    temp = string.replace(temp,' ',"")
    shang = "～"
    temp = string.replace(temp,shang.decode('utf-8'),"")
    length = len(temp)
    return length

#x is word, y is sentence
def frequency(x,y):
    temp = list(jieba.cut(y))
    i = 0
    for item in temp:
        if x==item:
            i+=1
    return i

#计算相似度
def similarity(a,b):
    atags = jieba.analyse.extract_tags(a,10)
    #print ",".join(atags)
    btags = jieba.analyse.extract_tags(b,10)
    #print ",".join(btags)
    alist = list(atags)
    blist = list(btags)
    aset = set(alist)
    bset = set(blist)
    uset = aset.union(bset)
    ulist = list(uset)
    a_array = []
    b_array = []
    for item in ulist:
        #print item
        af = frequency(item,a)
        #print 'af=',af
        bf = frequency(item,b)
        #print 'bf=',bf
        a_array.append(af)
        b_array.append(bf)
    result1=0.0;
    result2=0.0;
    result3=0.0;
    for i in range(len(a_array)):
        result1+=a_array[i]*b_array[i]   #sum(X*Y)
        result2+=a_array[i]**2     #sum(X*X)
        result3+=b_array[i]**2     #sum(Y*Y)
    if ((result2**0.5)*(result3**0.5)) !=0:
        result = result1/((result2**0.5)*(result3**0.5))
    else:
        result = 0
    return result


def zhaiyao(content,first, title):
    #content = string.replace(content,'\n',"")
    #取第一段内容
    print content
    #keywords
    KK = []
    KY = {}
    NM = []
    tags = jieba.analyse.extract_tags(content, 10, True)
    for tag in tags:
        tmp = tag[0].encode('UTF-8')
        KK.append(tag[0].encode('UTF-8'))
        #print tag[0].encode('UTF-8')
        KY[tmp] = string.atof(tag[1])
        NM.append(string.atof(tag[1]))
    max0 = max(NM)
    #取原标题的关键词，动词和名词；之前去掉原标题无关词
    words = pseg.cut(title)
    for w in words:
        if w.flag == 'v' or w.flag == 'n' or w.flag == 'nr' or w.flag == 'nz' or w.flag == 'ns' or w.flag == 'nt':
            tmp = w.word
            if tmp.encode('utf-8') not in KK:
                KK.append(tmp.encode('utf-8'))
                KY[tmp.encode('utf-8')] = max0
            else:
                KY[tmp.encode('utf-8')] = max0
    '''
    for k in KK:
        print k,KY[k]
    '''
    #content = delete(content)
    content = first.decode('utf-8')
    #中文句号分隔和段落分隔
    ju = "。"
    pp = []
    kongge = ' 　　'
    gantan = '！'
    wenhao = '？'
    fenhao = '；'
    sheng = '    '
    fan2 = []

    ju_array = content.split(ju.decode('utf-8'))
    for i in ju_array:
        kong = i.split('\n')
        for j in kong:
            fan = j.split(kongge.decode('utf-8'))
            for k in fan:
                fan = k.split(gantan.decode('utf-8'))
                for k in fan:
                    fan = k.split(wenhao.decode('utf-8'))
                    for k in fan:
                        fan = k.split(fenhao.decode('utf-8'))
                        for k in fan:
                            yuan = "原标题："
                            yuan1 = "原标题:"
                            if k.count(yuan.decode('utf-8'))<=0 and k.count(yuan1.decode('utf-8'))<=0:
                                fan2.append(k)
                            for k in fan2:
                                '''
                                shu1 = "《"
                                shu2 = "》"
                                teep = k
                                a3 = re.compile(shu1.decode('utf-8')+'.*?'+shu2.decode('utf-8') )
                                wu = a3.sub('',teep)
                                print wu
                                #空格在书名号里
                                if k.count(' ')>0 and wu.count(' ')<=0:
                                    print k
                                    fan.append(k)
                                else:
                                '''
                                fan = k.split(' ')
                                for k in fan:
                                    fan = k.split(sheng.decode('utf-8'))
                                    for k in fan:
                                        fan = k.split('?')
                                        for k in fan:
                                            kkk = '　　'
                                            k = string.replace(k,kkk.decode('utf-8'),'')
                                            pp.append(k)

    #中文逗号分隔，优先选择选择2句以下的分句的句子，然后再看三个分句的句子，没有符合要求的就用原来的标题
    aa = []
    for i in pp:
        #print i
        dou_array = i.split(l1.decode('utf-8'))
        for j in dou_array:
            aa.append(j)
    LL = {}
    #广告词汇
    xinmin = "新民网"
    weixin = "微信"
    zhuangxiu = "装修户主"
    bianji = "编辑："
    ganrenshi = "感人事、烦心事"
    tufa = "突发事、新鲜事"
    guanjianci = "关键词："
    xinwen = "新闻网"
    for term in aa:
        #print term
        
        #关键词的重要程度
        
        total = 0
        ss = []
        for k in KK:
            #tmp = string.atof(KY[k])
            rank = math.pow( 2, KY[k] )
            #关键词出现多于两次就过滤掉且不含广告新民网，微信，http
            if term.count(k.decode('utf-8')) == 1 and term.count(xinmin.decode('utf-8')) <= 0 and term.count(weixin.decode('utf-8')) <= 0 and term.count('http') <= 0 and term.count(zhuangxiu.decode('utf-8')) <= 0 and term.count(bianji.decode('utf-8')) <= 0 and term.count(ganrenshi.decode('utf-8')) <= 0 and term.count(guanjianci.decode('utf-8')) <= 0 and term.count(xinwen.decode('utf-8')) <= 0 and term.count(tufa.decode('utf-8')) <= 0:
                
                total = total + rank
        #先按照关键词重要程度排序，再按照长度排序

        ss.append(total)
        ss.append(len(term))
        #print ss
        LL[term] = ss

    LL = sorted(LL.iteritems(), key = lambda asd:asd[1], reverse=True)
    
    #print LL[0][0]
    temp_f = ""
    douhao = "，"
    #如果包含关键词，且字数大于7个字
    for l in LL:
        #print l
        if l[1][0] > 0:
            if (l[0].count(douhao.decode('utf-8'))<=0 and countnum(l[0]) > 7) or (l[0].count(douhao.decode('utf-8'))>0 and countnum(l[0]) > 10):
                temp = l[0]
                break
    '''选择好的句子删减'''
    temp = delete(temp)
    #temp = cixing(temp)
    return temp
# title = "日本男子跳入海中救落水中国男性溺水遇难"
# first = "[环球网报道 记者 余鹏飞] 据日本NHK新闻6月12日报道，一名在千叶县市川市东浜海边采挖海贝的中国男子11日不慎落水，正在岸边的一名日本男子听到呼救声后跳入海中前往救助，不幸溺水遇难。"
# content = "[环球网报道 记者 余鹏飞] 据日本NHK新闻6月12日报道，一名在千叶县市川市东浜海边采挖海贝的中国男子11日不慎落水，正在岸边的一名日本男子听到呼救声后跳入海中前往救助，不幸溺水遇难。  　　报道援引日本千叶县警方的消息称，获救的中国籍男性（40岁左右）与友人共4人来到海边采挖海贝，因为水位上涨未能及时逃离。据悉，事发海滩属于不能采挖海贝的区域。  　　报道称，呼救的中国男子最后在友人的帮助下爬上岸边，不过跳入海中救助他的日本人却不幸遇难。  　　遇难的日本人名叫佐佐木淳（殁年34岁），是当地渔业协会委托监视偷捞海贝的一家管理公司的职员，事发时，他正在现场担任监视员。听到呼救后佐佐木淳立即跳入海中前往救助，但是遭海浪席卷而后不见身影，1个小时后，被当地的消防队员在离防波堤10米左右的海水中发现，但已宣告死亡。"

# title = "IS宣称对美国奥兰多夜总会枪击案负责"
# first = "【环球网报道 记者 赵衍龙】美国当地时间12日凌晨，佛州“脉动奥兰多”夜总会发生美国30年以来最惨烈的大规模枪击案，目前已经造成50人死亡，53人受伤。据英国天空新闻网6月13日消息，极端组织“伊斯兰国”宣称对发生在美国奥兰多夜总会的大规模枪击案负责，据悉，这一消息来源于IS的通讯社“Amaq News Agency”，其在声明中称，“IS的战士发动了此次袭击”。"
# content = "【环球网报道 记者 赵衍龙】美国当地时间12日凌晨，佛州“脉动奥兰多”夜总会发生美国30年以来最惨烈的大规模枪击案，目前已经造成50人死亡，53人受伤。据英国天空新闻网6月13日消息，极端组织“伊斯兰国”宣称对发生在美国奥兰多夜总会的大规模枪击案负责，据悉，这一消息来源于IS的通讯社“Amaq News Agency”，其在声明中称，“IS的战士发动了此次袭击”。  　　美国总统奥巴马就此次袭击事件发表讲话并谴责称“这是一场残忍的谋杀和一场可怕的大屠杀”，“是一种恐怖和充满仇恨的行为”。  　　奥巴马称，“这标志着美国历史上最严重的枪击事件”，同时奥巴马还表示，“官方目前对于枪手的动机还没有明确的判断”，“美国不会畏缩和恐惧，将会团结一致的保护美国人民，以应对威胁美国的人”。  　　奥巴马称同时也表示，“今天对于同性恋社群(LGBT)来说是令人悲伤的一天”，“对于同性恋社群的袭击就是对我们所有人的袭击”。"



#temp = zhaiyao(content,first, title)
#print sentence(temp,content)



import BaseHTTPServer
import urllib
import json



class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        self.process(1)
    
    def do_GET(self):
        self.process(2)
    
    def do_OPTIONS(self):
        self.process(3)
    
    def process(self, type):
        
        print 'received a request......'

        if type==1:
            datas = self.rfile.read(int(self.headers['content-length']))
            datas = urllib.unquote(datas).decode("utf-8", 'ignore')
            datas = eval(datas)
                
            title = datas['title']
            print title
            content = datas['content']
            print content
            first = datas['first']
            print first
                
            if datas != "":
                data = {}
                temp = zhaiyao(content,first, title)
                result_final = sentence(temp,content)
                # result = similarity(title,result_final[1])
                # #print result,result_final[1]
                # #相似度太高或者字数大于30字
                # if result>0.95 or countnum(result_final[1]) > 30:
                #     #flags=1说明相似度大于95%
                #     result_final = zhaiyao(content,title,1)
            print result_final
            data['newtitle'] = result_final
            jdata = json.dumps(data, ensure_ascii=False)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(jdata)
        else:
            self.send_response(404)
            self.end_headers()



server = BaseHTTPServer.HTTPServer(('0.0.0.0', 8020), WebRequestHandler)
server.serve_forever()

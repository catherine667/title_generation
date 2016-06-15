#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liqun'

#构建树
import json                     # pretty print nested hash
import httplib,urllib2
import string
import jieba

def construct_tree(edges):
    """Given a list of edges [child, parent], return a tree."""

    parentDB = {} # key is a node. value is its parent
    childrenDB = {} # key is a node. value is its children as hash
    for edg in edges:
        c, p = edg[0], edg[1]
        parentDB[c] = p
        if p in childrenDB:
            childrenDB[p][c] = None
        else:
            childrenDB[p] = {c:None}

    root = None
    for v in childrenDB.viewkeys():
        if v not in parentDB:
            root = v
            break

    leaf_set = (set(parentDB.keys()) - set(childrenDB.keys()))

    # construct the tree, bottom up
    tree = {}
    for node in leaf_set:
        tree[node] = {}

    while len(parentDB) != 0:
        for head, tail in tree.items():
            if head != root:
                if head not in childrenDB:     # not parent of somebody
                    if parentDB[head] in tree: # add sibling
                        tree[parentDB[head]][head] = tail
                    else:           # add parent
                        tree[parentDB[head]] = {head: tail}
                    del tree[head]
                    del childrenDB[parentDB[head]][head]
                    if len(childrenDB[parentDB[head]]) == 0:
                        del childrenDB[parentDB[head]]
                    del parentDB[head]
    return tree

# if __name__ == '__main__':
#     edges = [[0, 2], [3, 0], [1, 4], [2, 4]]
#     print(json.dumps(construct_tree(edges), indent=1))
#     print construct_tree(edges)

import httplib,urllib2

def keywords(content):
    #keywords
    KK = []
    KY = {}
    NM = []
    #jieba.analyse.set_idf_path("./jieba/extra_dict/idf.txt.big")
    tags = jieba.analyse.extract_tags(content, 10, True)
    for tag in tags:
        tmp = tag[0].encode('UTF-8')
        KK.append(tag[0].encode('UTF-8'))
        KY[tmp] = string.atof(tag[1])
        NM.append(string.atof(tag[1]))
    max0 = max(NM)
    return KK

def sentence(text,content):
    text = text.encode('utf-8')
    url_get_base = "http://ltpapi.voicecloud.cn/analysis/?"
    api_key = 'A352m9y8DFlIDLQe5xuUIsnBqM8w5CvKIjBzjVKY'
    format1 = 'json'
    pattern = 'all'
    result = urllib2.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,text,format1,pattern))

    analysis = result.read().strip()
    analysis = eval(analysis)
    edges = []

    #只有一句话
    number = 0
    result_text = ""
    cut_final = []
    for j in analysis[0][0]:
        #print j['cont'],j
        #不去掉数词,不去掉副词和动词,人名，地名
        if (j['pos'] != 'm' and j['pos'] != 'q' and j['pos'] != 'p' and j['relate'] != 'SBV' and j['relate'] != 'VOB' and j['relate'] != 'POB' and j['relate'] != 'HED' and j['relate']!='WP'):
            #print j['cont'],j['relate'],j['pos']
            #含否定词不删去
            if j['cont'].count("不")==0 and j['cont'].count("别")==0:
                ff = 0
                for k in keywords(content):
                    if j['cont'] == k:
                        #print k
                        ff = 1
                if ff == 0:
                    cut_final.append(j['id'])
    for k in analysis[0][0]:
        flag = 0
        for q in cut_final:
            if k['id'] == q:
                flag = 1
        if flag == 0:
            result_text = result_text + k['cont']
    #print(json.dumps(construct_tree(edges), indent=1))
    return result_text


def fenju(text):
    douhao = "，"
    array = text.split(douhao)
    result = ""
    for i in array:
        #分句大于4个字才进行删词
        if len(i)>12:
            result = result + sentence(i) + "，"
        else:
            result = result + i + "，"
    #result = string.replace(result,"。，","。")
    return result

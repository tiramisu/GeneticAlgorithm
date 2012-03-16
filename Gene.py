#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random
#遺伝子クラス
class Gene:
    def aaa(self,y):
        for i in y:
            self.bits[i]=1
    #遺伝子初期化、bitsが指定されていなければランダムで生成
    def __init__(self,gene_len,bits=[],parents=[-1,-1],crosspoint=-1):
        #遺伝子情報
        if bits==[]:
            self.bits=[random.randint(0,1) for i in range(gene_len)]
            #self.bits=[0 for i in range(gene_len)]
            #self.aaa([8,15,16,19,24,25,29,30,32,33,35,36,37,38,40,41,42,43,44,47,48])
        else:
            self.bits=bits
        self.fitness=0.0	        #適合度
        self.parents=parents	    #親情報
        self.crosspoint=crosspoint	#交叉点
        self.gene_len=gene_len	    #遺伝子長
    #遺伝子（0,1のリスト）を文字列に
    def __str__(self):
        return "".join(map(str,self.bits))
    #親の情報を文字列に
    def pareInfo(self):
        return "( %d, %d) %d"%(self.parents[0],self.parents[1],self.crosspoint)

    #遺伝子情報書式表示
    def printInfoFormat(self):
        space=(0 if self.gene_len<=5 else self.gene_len-5)+8
        sys.stdout.write("\t#gene%s#fitness        #parents\n"%(" "*space))
    #遺伝子の情報を表示
    def printInfo(self,i):
        space=(0 if self.gene_len>5 else 5-self.gene_len)+8
        sys.stdout.write("%d)\t%s%s%f        %s\n"%(i,self.__str__()," "*space,self.fitness,self.pareInfo()))
    def onecross(self,point):
        return [self.bits[:point],self.bits[point:]]
    def mutation(self,mutarr):
        for i in range(self.gene_len):
            if mutarr[i]==1:
                self.bits[i]=self.bits[i]^1

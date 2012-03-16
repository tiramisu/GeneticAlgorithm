#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Gene
import sys
import math
import random
import numpy
import Gnuplot
#遺伝的アルゴリズムクラス
class GeneList:
    def __init__(self,gene_len,generation,popul,crossR,MutatR,EliteR):
        self.gene_len=gene_len	    #遺伝子長
        self.generation=generation	#最大世代数
        self.popul=popul	        #1世代あたりの集団サイズ
        self.crossR=crossR	        #交叉率
        self.mutatR=MutatR	        #突然変率
        self.eliteR=EliteR	        #エリートをそのまま残す確率
        self.initList()             #遺伝子管理リストの初期化
        self.current_gene=0	        #現在の世代数
        self.rouletteTable=[0.0 for i in range(self.popul+1)]	#ルーレットテーブル
        self.scoreMax=[0 for i in range(generation+1)]
        self.scoreAve=[0 for i in range(generation+1)]
        self.scoreAllMax=[0 for i in range(generation+1)]
        
    #遺伝子集団生成
    def initList(self):
        self.list=[None for i in range(self.popul)]
        for i in range(self.popul):
            self.list[i]=Gene.Gene(self.gene_len)

    #遺伝的アルゴリズム実行
    def main(self):
        self.fitnessCul()       #すべての遺伝子の適合度を計算
        while True:
            self.printResult()      #適合度の高い順に遺伝子を表示
            if self.current_gene<self.generation:
                self.reproduction()     #選択、交叉
                self.mutation()         #突然変異
                self.current_gene+=1	#世代をひとつ進める
                self.fitnessCul()       #すべての遺伝子の適合度を計算
            else:
                break
        print self.scoreAve
        print self.scoreMax
        gp=Gnuplot.Gnuplot()
        gp("set style data lines")
        gp.plot(self.scoreMax)
    def printResult(self):
        sys.stdout.write(" %d Generation\n"%self.current_gene)
        self.list[0].printInfoFormat()
        for i in range(self.popul):
            self.list[i].printInfo(i)
        sys.stdout.write("%f\n"%self.average)
    #集団の適合度の計算
    def fitnessCul(self):
        for i in range(self.popul):
            self.list[i].fitness=self.evaluation(self.list[i])
        self.list.sort(cmp=lambda x,y:-1 if x.fitness<y.fitness else 1)
        self.makeRouletteTable()
        self.average=sum(map(lambda x:x.fitness,self.list))/self.popul
        self.scoreAve[self.current_gene]=self.average
        self.max=self.list[0].fitness
        self.min=self.list[self.popul-1].fitness
        self.scoreMax[self.current_gene]=self.max
    def makeRouletteTable(self):
        table=map(lambda x:1.0/x.fitness*10,self.list)
        self.rouletteMax=sum(table)
        for i in range(len(table)):
            self.rouletteTable[i+1]=self.rouletteTable[i]+table[i]

    #遺伝子の評価関数
    def evaluation(self,gene):
        A=0
        B=0
        for i in range(self.gene_len):
            if gene.bits[i]==0:
                A+=math.sqrt(i+1)
            else:
                B+=math.sqrt(i+1)
        return math.fabs(A-B)

    #選択、生殖
    def reproduction(self):
        #エリート選択
        elite_sel=int((self.eliteR/100)*self.popul)
        select=elite_sel
        #選択、交叉
        while select<=self.popul-1:
            point=random.randint(1,self.gene_len-2)
            parents=[self.roulette(),self.roulette()]
            pareA=self.list[parents[0]].onecross(point)
            pareB=self.list[parents[1]].onecross(point)
            self.list[select]=Gene.Gene(self.gene_len,pareA[0]+pareB[1],parents,point)
            select+=1
            if select>self.popul-1:
                break
            self.list[select]=Gene.Gene(self.gene_len,pareA[1]+pareB[0],parents[::-1],point)
            select+=1
    def roulette(self):
        ball=random.uniform(0.0,self.rouletteMax)
        for i in range(self.popul):
            if self.rouletteTable[i]<ball<=self.rouletteTable[i+1]:
                return i

    #突然変異
    def mutation(self):
        for i in range(self.popul):
            mutafunc=(lambda:0 if self.mutatR*(self.gene_len/100.0)<=random.uniform(0.0,100.0) else 1)
            mutarr=[mutafunc() for j in range(self.gene_len)]
            self.list[i].mutation(mutarr)

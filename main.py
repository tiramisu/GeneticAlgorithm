#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import GeneList

def main():
    sys.stdout.write("len for gene:")
    gene_len=int(sys.stdin.readline())
    sys.stdout.write("Generation:")
    generation=int(sys.stdin.readline())
    sys.stdout.write("Population:")
    popul=int(sys.stdin.readline())
    sys.stdout.write("Crossover Rate:") 
    crossR=float(sys.stdin.readline())
    sys.stdout.write("Mutation Rate:")
    mutatR=float(sys.stdin.readline())
    sys.stdout.write("Elite Rate:")
    eliteR=float(sys.stdin.readline())
    gl=GeneList.GeneList(gene_len,generation,popul,crossR,mutatR,eliteR)
    gl.main()

if __name__=="__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 08:55:24 2020

@author: tjian
"""
import pandas as pd
import argparse
import sys
import random

def betweenDataGen(sheet, index):  
    temp = sheet.dataRange[index] 
    numStr = temp.split('~',1)
    sheet.testData[index] = random.randint(int(numStr[0], 16), int(numStr[1], 16))

def multiDataGen(sheet, index):  
    temp = sheet.dataRange[index] 
    numStr1 = temp.split(';',10)
    sheet.testData[index] = int(random.choice(numStr1), 16)

def multiAndBetweenDataGen(sheet, index):  
    temp = sheet.dataRange[index] 
    
    
    numStr1 = temp.split(';',10)               
    numStr2 = numStr1[0].split('~',1)                
    numStr3 = numStr1[1:]              
    i = 0
    for tempStr in numStr3:
        numStr3[i] = int(numStr3[i], 16)
        i += 1

    numStr4 = random.randint(int(numStr2[0], 16), int(numStr2[1], 16))
    numStr3.append(numStr4)
    sheet.testData[index] = int(random.choice(numStr3))


def formalDataGen(sheet, index):
    if sheet.dataType[index] == 'B':
        betweenDataGen(sheet, index)
        pass
    elif sheet.dataType[index] == 'M':
        multiDataGen(sheet, index)
        pass
    elif sheet.dataType[index] == 'MB':
        multiAndBetweenDataGen(sheet, index)
        pass
    

def dataGenerator(sheet, flag):
        for index in range(len(sheet)):
            if sheet.layer1Test[index] == 'Y':
                if flag == 'any':
                    sheet.testData[index] = random.randint(-65535, 65536)
                elif flag == 'formal':
                    formalDataGen(sheet, index)
    
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--xls', help='test data sheet file pathname')
    parser.add_argument('-o','--output', help='save encode/decode data to a file')
    parser.add_argument('-f','--flag', help='generator data rule, [formal] according to dataRange or [any] not caring dataRange')
    args = parser.parse_args()
    
 
    if args.flag == None:
        print('please use -f or --flag [any][formal]')
        exit(0)
    elif args.flag not in ['any','formal']:
        print('please use -f [any] or [formal]')
        exit(0)
        

    if args.xls == None:
        print('please use -s or --xls to input data sheet excel file pathname')
        exit(0)
    else:
        xls_file = args.xls
        data_sheet = pd.read_excel(io=xls_file)
        data_sheet.columns = ['index', 'testRef', 'abstract', 'varName', 'layer1Test', 'layer2Test','dataType', 'dataRange', 'testData', 'testResult', 'remarks']
    
    dataGenerator(data_sheet, args.flag)
    data_sheet_to_save = data_sheet.copy()
    data_sheet_to_save.columns = ['序号', '测试参考', '说明', '变量名参考', '级别一测试','级别二测试', '数据类型','数据范围', '测试数据', '测试结果', '备注']
    data_sheet_to_save.to_excel(args.output)
     
 

    
if __name__ == '__main__':
    main(sys.argv[1:])

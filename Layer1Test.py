#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:38:14 2020

@author: tjian

python Layer1Test.py -s test_sheet.xlsx -t all
python Layer1Test.py -s test_sheet.xlsx -t SS
python Layer1Test.py -s test_sheet.xlsx -t B
python Layer1Test.py -s test_sheet.xlsx -t MB
python Layer1Test.py -s test_sheet.xlsx -t M

python Layer1Test.py -s test_sheet_layer2.xlsx -t SS,MB,M
"""

import pandas as pd
import argparse
import sys

totalTestResult = []

def getVarRow(varName, sheet):
    for i in range(len(sheet)):
        if varName == sheet.varName[i]:
            return i


def assertBetween(x, lo, hi, index):
    if not (lo <= x <= hi):
        print('(%r) Error! %r not between %r and %r' % (index+1, x, lo, hi))
        totalTestResult.append('Error')
    else:
        print('(%r) Pass! %r is between %r and %r' % (index+1, x, lo, hi))
        totalTestResult.append('Pass')

        

def checkBetween(index, varName, sheet):
    if sheet['varName'][index] == varName:
        testNum = sheet['testData'][index]
        if sheet['layer1Test'][index] == 'Y':
            temp = sheet['dataRange'][index] 
            numStr = temp.split('~',1)
            assertBetween(int(testNum), int(numStr[0], 16), int(numStr[1], 16), index)
        return int(testNum)


def checkSpecialSingle(index, varName, sheet):
    if sheet['varName'][index] == varName:
        testNum = sheet['testData'][index]
        if sheet['layer1Test'][index] == 'Y':
                numStr = sheet['dataRange'][index]    
                if  testNum !=  numStr:
                    print('(%d) Error! test data is %s , but must be %s' % (index+1, testNum, numStr))
                    totalTestResult.append('Error')
                else:
                    print('(%d) Pass! test data is %s , and must be %s' % (index+1, testNum, numStr))
                    totalTestResult.append('Pass')
                    
        return testNum 





def assertMultiAndBetween(x, lo, hi, con, index, flag=True):
    if flag:
        if not (lo <= x <= hi or x in con):
            print('(%r) Error! %r not between %r and %r, also not in %r' % (index+1, x, lo, hi, con))
            totalTestResult.append('Error')
        else:
            if x in con:
                print('(%r) Pass! %r is in  %r' % (index+1, x, con))
            else:
                print('(%r) Pass! %r is between %r and %r' % (index+1, x, lo, hi))
                
            totalTestResult.append('Pass')
    else:
        if not (x in con):
            print('(%r) Error! %r not in %r' % (index+1, x, con))
            totalTestResult.append('Error')
        else:
            print('(%r) Pass! %r is in %r' % (index+1, x, con))
            totalTestResult.append('Pass')


            

def checkNulti(index, varName, sheet):
    if sheet['varName'][index] == varName:
        testNum = sheet['testData'][index]
        if sheet['layer1Test'][index] == 'Y':
            temp = sheet['dataRange'][index] 
   #         print(temp)
            import re
            if re.search(r"~",temp) == None:
                numStr1 = temp.split(';',10)
   #             print(numStr1)
                i = 0
                for tempStr in numStr1:
                    numStr1[i] = int(numStr1[i], 16)
                    i += 1
                assertMultiAndBetween(int(testNum), 0, 0, numStr1, index, False)     
            else:
                numStr1 = temp.split(';',10)               
                numStr2 = numStr1[0].split('~',1)                
                numStr3 = numStr1[1:]
                
                i = 0
                for tempStr in numStr3:
                    numStr3[i] = int(numStr3[i], 16)
                    i += 1

#                testNum = 254
                assertMultiAndBetween(int(testNum), int(numStr2[0], 16), int(numStr2[1], 16), numStr3, index+1)            
            return testNum

def checkMultiAndBetween(index, varName, sheet):
    if sheet['varName'][index] == varName:
        testNum = sheet['testData'][index]
        if sheet['layer1Test'][index] == 'Y':
            temp = sheet['dataRange'][index] 
            import re
            if re.search(r"~",temp) == None:
                numStr1 = temp.split(';',10)
                i = 0
                for tempStr in numStr1:
                    numStr1[i] = int(numStr1[i], 16)
                    i += 1
                assertMultiAndBetween(int(testNum), 0, 0, numStr1, index, False)     
            else:
                numStr1 = temp.split(';',10)               
                numStr2 = numStr1[0].split('~',1)                
                numStr3 = numStr1[1:]              
                i = 0
                for tempStr in numStr3:
                    numStr3[i] = int(numStr3[i], 16)
                    i += 1

#                testNum = 254
                assertMultiAndBetween(int(testNum), int(numStr2[0], 16), int(numStr2[1], 16), numStr3, index+1)            
        return int(testNum)



def layer1Test(sheet, typeList):
    print('******** Layer1 Testing Begin ********')
    print('---------------------------')
    for index in range(len(sheet)):
        if sheet.layer1Test[index] == 'Y':
            var = sheet.varName[index]
            if  sheet.dataType[index] in typeList and sheet.dataType[index] == 'B' :
                testDataValue = checkBetween(index, var, sheet)
                print('---------------------------')
            elif  sheet.dataType[index] in typeList and sheet.dataType[index] == 'M' :
                testDataValue = checkNulti(index, var, sheet)
                print('---------------------------')
            elif  sheet.dataType[index] in typeList and sheet.dataType[index] == 'MB' :
                testDataValue = checkMultiAndBetween(index, var, sheet)
                print('---------------------------')
            elif  sheet.dataType[index] in typeList and sheet.dataType[index] == 'SS' :
                testDataValue = checkSpecialSingle(index, var, sheet)
                print('---------------------------')





    

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--xls', help='test data sheet file pathname')
    parser.add_argument('-t','--type', help='testing according to data type , -t [B,M,...] or -t [all] for B,M,MB,SS')
    args = parser.parse_args()
    if args.type == 'all':
        varTypeList = ['B', 'M', 'MB', 'SS']
    else:
        varTypeList = args.type.split(",")
    if args.xls == None:
        print('please use -s or --xls to input data sheet excel file pathname')
        exit(0)
    else:
        xls_file = args.xls
        data_sheet = pd.read_excel(io=xls_file)
        data_sheet.columns = ['index', 'testRef', 'abstract', 'varName', 'layer1Test', 'layer2Test','dataType', 'dataRange', 'testData', 'testResult', 'remarks']
    
    layer1Test(data_sheet, varTypeList)
    passNum = 0
    errorNum = 0
    for testResult in totalTestResult:
        if testResult == 'Pass':
            passNum += 1
        elif testResult == 'Error':
            errorNum += 1
    if passNum + errorNum <= 1:
        print('Tested total %r item'%(passNum+errorNum))
    else:
        print('Tested total %r items'%(passNum+errorNum))
        
    print('Pass %r'%(passNum))
    print('Error %r'%(errorNum))



    
if __name__ == '__main__':
    main(sys.argv[1:])

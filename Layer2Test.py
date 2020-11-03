#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 20:11:36 2020

@author: tjian

python Layer2Test.py -s test_sheet.xlsx

"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import argparse
import sys

totalTestResult = []

def getVarRow(varName, sheet):
    for i in range(len(sheet)):
        if varName == sheet.varName[i]:
            return i


def layer2Test(sheet):
    df1 = sheet.varName[sheet.layer2Test == 'Y']
    print('******** Layer2 Testing Begin ********')
    print('---------------------------')
    for var in df1:
        df2 = sheet.varName.dropna()
        if var == 'lengthofRecord':
            print('(%d) Pass for LengthofRecord testing!'%(getVarRow('lengthofRecord',sheet)+1))
            totalTestResult.append('Pass')
        elif var == 'numberofRepresentations':
            df2 = df2.str.contains('representationBody')
            df3 = df2.value_counts()
            representationNum1 = df3[True]    
            df10 = sheet[sheet['varName'] == 'numberofRepresentations']
            df11 = df10.testData
            representationNum2 = df11.values
            if representationNum1 == representationNum2[0]:
                print('(%d) Pass for Representation testing!  Representation Body is %r and numberofRepresentations is %r'%(getVarRow('numberofRepresentations',sheet)+1, representationNum1, representationNum2[0]))
                totalTestResult.append('Pass')
            else:
                print('(%d) Error for Representation testing!  Representation Body is %r but numberofRepresentations is %r'%(getVarRow('numberofRepresentations',sheet)+1, representationNum1, representationNum2[0]))
                totalTestResult.append('Error')
        elif var == 'reprsentationLength':
            print('(%d) Pass for ReprsentationLength!'%(getVarRow('reprsentationLength',sheet)+1))
            totalTestResult.append('Pass')
        elif var == 'qualityRecord':
            df2 = df2.str.contains('qualityblock')
            df3 = df2.value_counts()
            qualityNum1 = df3[True]
            df10 = sheet[sheet['varName'] == 'numberofQualityblocks']
            df11 = df10.testData
            qualityNum2 = df11.values
            if qualityNum1 == qualityNum2:
                print('(%d) Pass for QualityRecord testing!  Quality Block is %r and numberofQualityblocks is %r'%(getVarRow('qualityRecord',sheet)+1, qualityNum1, qualityNum2[0]))
                totalTestResult.append('Pass')
            else:
                print('(%d) Error for QualityRecord testing!  Quality Block is %r but numberofQualityblocks is %r'%(getVarRow('qualityRecord',sheet)+1, qualityNum1, qualityNum2[0]))
                totalTestResult.append('Error')
        print('---------------------------')
         

    

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--xls', help='test data sheet file pathname')
    args = parser.parse_args()
    if args.xls == None:
        print('please use -s or --xls to input data sheet excel file pathname')
        exit(0)
    else:
        xls_file = args.xls
        data_sheet = pd.read_excel(io=xls_file)
        data_sheet.columns = ['index', 'testRef', 'abstract', 'varName', 'layer1Test', 'layer2Test','dataType', 'dataRange', 'testData', 'testResult', 'remarks']
    
    layer2Test(data_sheet)
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

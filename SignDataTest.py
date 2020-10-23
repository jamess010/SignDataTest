#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sat Oct 17 12:58:26 2020

@author: tjian

for ber test
encode:
./SignDataTest.py -a /home/data/asn1tests/sign_data.asn -s /home/data/asn1tests/test_sheet.xlsx -e ber -o /home/data/asn1tests/testBer.txt
decode 
./SignDataTest.py -a /home/data/asn1tests/sign_data.asn -s /home/data/asn1tests/test_sheet.xlsx -d ber -i /home/data/asn1tests/testBer.txt -o /home/data/asn1tests/testBerResult.xls

for per test
encode:
./SignDataTest.py -a /home/data/asn1tests/sign_data.asn -s /home/data/asn1tests/test_sheet.xlsx -e per -o /home/data/asn1tests/testPer.txt
decode:
./SignDataTest.py -a /home/data/asn1tests/sign_data.asn -s /home/data/asn1tests/test_sheet.xlsx -d per -i /home/data/asn1tests/testPer.txt -o /home/data/asn1tests/testPerResult.xls

for xer test
encode:
./SignDataTest.py -a /home/data/asn1tests/sign_data.asn -s /home/data/asn1tests/test_sheet.xlsx -e xer -o /home/data/asn1tests/testXer.txt
decode:
./SignDataTest.py -a /home/data/asn1tests/sign_data.asn -s /home/data/asn1tests/test_sheet.xlsx -d xer -i /home/data/asn1tests/testXer.txt -o /home/data/asn1tests/testXerResult.xls

"""
from __future__ import print_function
import argparse
import sys
import asn1tools
import pandas as pd
from sys import getsizeof, stderr
from itertools import chain
from collections import deque

try:
    from reprlib import repr
except ImportError:
    pass


varNameDefine = [
    'formatId',
    'standardVersion',
    'lengthofRecord',
    'numberofRepresentations',
    'certificationFlag',
    'reprsentationLength',
    'captureDateTime',
    'captureDeviceTechId',
    'captureDeviceVendId',
    'captureDeviceTypeId',
    'numberofQualityblocks',
    'qualityRecord',
    'certificationRecord',
    'xchannelScaling',
    'ychannelScaling',
    'tchannelScaling',
    'fchannelScaling',
    'numberofDynamicEvents',
    'numberofAveragingSamples',
    'xCoordinate',
    'yCoordinate',
    'fValue',
    'timeValue',
    'typeofEvent',
    'totalTime',
    'meanValues',
    'meanX',
    'meanY',
    'meanF',
    'sdValues',
    'sdX',
    'sdY',
    'sdF',
    'cCoefficient',
    'extendedData'
]

def  signDynamicBlock(varValue):
 

    generalHeader = {
        'formatId': varValue['formatId'],
        'standardVersion': varValue['standardVersion'],
        'lengthofRecord': varValue['lengthofRecord'],
        'numberofRepresentations': varValue['numberofRepresentations'],
        'certificationFlag': varValue['certificationFlag']
    }

    qualityBlockValues = {
            'numberofQualityblocks': varValue['numberofQualityblocks'],
            'qualityblock': varValue['qualityRecord']
    }
     
    representationHeaderValues = {
        'reprsentationLength': varValue['reprsentationLength'], 
        'captureDateTime': varValue['captureDateTime'], 
        'captureDeviceTechId': varValue['captureDeviceTechId'], 
        'captureDeviceVendId': varValue['captureDeviceVendId'], 
        'captureDeviceTypeId': varValue['captureDeviceTypeId'], 
        'qualityRecord': qualityBlockValues,
        'certificationRecord': varValue['certificationRecord'], 
        'xchannelScaling': varValue['xchannelScaling'], 
        'ychannelScaling': varValue['ychannelScaling'], 
        'tchannelScaling': varValue['tchannelScaling'], 
        'fchannelScaling': varValue['fchannelScaling'], 
        'numberofDynamicEvents': varValue['numberofDynamicEvents'], 
        'numberofAveragingSamples': varValue['numberofAveragingSamples']
    }
   

    dynamicEventData = {
        'xCoordinate': varValue['xCoordinate'], 
        'yCoordinate': varValue['yCoordinate'],
        'fValue': varValue['fValue'], 
        'timeValue':varValue ['timeValue'], 
        'typeofEvent': varValue['typeofEvent']  
    }

    featureData = {
        'totalTime': varValue['totalTime'], 
        'meanValues': varValue['meanValues'], 
        'sdValues': varValue['sdValues'], 
        'cCoefficient': varValue['cCoefficient'] 
    }

    extendedData = varValue['extendedData']
    extendedData = extendedData.encode('utf-8')
    representationBodyValues = {
        'dynamicEventData': dynamicEventData,
        'featureData': featureData, 
        'extendedData': extendedData
    }
     
    Body = {
        'representation':  representationHeaderValues,
        'representationBody': representationBodyValues
    }

    signDynamicBlock = {
        'header': generalHeader,
        'body': Body 
    }

    representationHeaderValues['reprsentationLength'] = total_size(representationHeaderValues)
    generalHeader['lengthofRecord'] = total_size(signDynamicBlock)
    
    return signDynamicBlock

def varNameDict(varNameDefine, sheet):
    varNameDict = {}
    for i in range(len(varNameDefine)):
        varName = varNameDefine[i]
        index = getVarRow(varName, sheet)
        if sheet.dataType[index] == 'B': # between value
            testDataValue = checkBetween(index, varName, sheet)
        elif sheet.dataType[index] == 'S':  # string
            testDataValue = checkSingle(index, varName, sheet)
        elif sheet.dataType[index] == 'M': # multi value
            testDataValue = checkNulti(index, varName, sheet)
        elif sheet.dataType[index] == 'MB': # multi value
            testDataValue = checkMultiAndBetween(index, varName, sheet)
        elif sheet.dataType[index] == 'QR': # qualityRecord
             testDataValue = qualityRecord(sheet)
        elif sheet.dataType[index] == 'CS': # channelScaling
            testDataValue = channelScaling(varName, sheet)
        elif sheet.dataType[index] == 'DT': # captureDateTime
            testDataValue = captureDateTime(sheet)

        varNameDict.update({varName:testDataValue})
        
    return varNameDict

def qualityRecord(sheet):
    qualityblock = []
    index = getVarRow('qualityRecord', sheet)
    index += 1
    numberofQualityblocks = sheet.testData[index]
    for i in range(numberofQualityblocks):
        qualityblockDict = {}

        index += 1
        blockName = sheet['varName'][index]

        index += 1
        qualityScore = checkMultiAndBetween(index, 'qualityScore', sheet)
        qualityblockDict.update({'qualityScore':qualityScore})

        index += 1
        qualityalgorithmVendId = checkBetween(index, 'qualityalgorithmVendId', sheet)  
        qualityblockDict.update({"qualityalgorithmVendId":qualityalgorithmVendId})

        index += 1
        qualityalgorithmId = checkBetween(index, 'qualityalgorithmId', sheet)  
        qualityblockDict.update({'qualityalgorithmId':qualityalgorithmId})
        qualityblock.append(qualityblockDict)
    return qualityblock


def assertBetween(x, lo, hi, index):
    if not (lo <= x <= hi):
        raise AssertionError('index=%r, %r not between %r and %r' % (index, x, lo, hi))

def assertMultiAndBetween(x, lo, hi, con, index, flag=True):
    if flag:
        if not (lo <= x <= hi or x in con):
            raise AssertionError('index=%r, %r not between %r and %r, also not in %r' % (index, x, lo, hi, con))
    else:
        if not (x in con):
            raise AssertionError('index=%r, %r not in %r' % (index, x, con))

def checkBetween(index, varName, sheet):
    if sheet['varName'][index] == varName:
        testNum = sheet['testData'][index]
        if sheet['needCheck'][index] == 'Y':
            temp = sheet['dataRange'][index] 
            numStr = temp.split('~',1)
            assertBetween(int(testNum), int(numStr[0], 16), int(numStr[1], 16), index+1)
        return int(testNum)
    else:
        assert False, 'index=%d：%s not correct！'%(index+1, sheet['varName'][index])



def checkSingle(index, varName, sheet):
    if sheet['varName'][index] == varName:
        testNum = sheet['testData'][index]
        if sheet['needCheck'][index] == 'Y':
                numStr = sheet['dataRange'][index]    
                if numStr[1] == 'x':
                    assert testNum ==  int(numStr,16), 'index=%d：test data is %s , but must be %s' % (index+1,  testNum, numStr)
                else:
                    assert testNum ==  numStr, 'index=%d：test data is %s , but must be %s' % (index+1,  testNum, numStr)
        return testNum 
    else:
        assert False, 'index=%d：%s not correct！'%(index+1, sheet['varName'][index])


def checkMultiAndBetween(index, varName, sheet):
    if sheet['varName'][index] == varName:
        testNum = sheet['testData'][index]
        if sheet['needCheck'][index] == 'Y':
            temp = sheet['dataRange'][index] 
            import re
            if re.search(r"~",temp) == None:
                numStr1 = temp.split(';',10)
                i = 0
                for tempStr in numStr1:
                    numStr1[i] = int(numStr1[i], 16)
                    i += 1
                assertMultiAndBetween(int(testNum), 0, 0, numStr1, index+1, False)     
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
    else:
        assert False, 'index=%d：%s not correct！'%(index+1, sheet['varName'][index])

def checkNulti(index, varName, sheet):
    if sheet['varName'][index] == varName:
        testNum = sheet['testData'][index]
        if sheet['needCheck'][index] == 'Y':
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
                assertMultiAndBetween(int(testNum), 0, 0, numStr1, index+1, False)     
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
    else:
        assert False, 'index=%d：%s not correct！'%(index+1, sheet['varName'][index])


 
def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.
    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:
        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}
    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__
 
    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)
 
        if verbose:
            print(s, type(o), repr(o), file=stderr)
 
        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s
 
    return sizeof(o)


def traverse_take_field(data, fields, values={}, currentKey=None):
    if isinstance(data, list):
        for i in data:
            traverse_take_field(i, fields, values, currentKey)
    elif isinstance(data, dict):
        for key, value in data.items():
            #print(key, value)
            if key in fields:                
                data1 = {key:data[key]}
#                print(data1)
                values.update(data1)
            traverse_take_field(value, fields, values, key)
    else:
        pass
    return values

def channelScalingToTestResult(varName, sheet,testResultBlock):
    rowChannelScaling = getVarRow(varName, sheet)
    channelScalingBlock = testResultBlock[varName]
    sheet.testResult[rowChannelScaling + 2] = channelScalingBlock['exponent']
    sheet.testResult[rowChannelScaling + 3] = channelScalingBlock['fraction']


def captureDateTimeToTestResult(varName, sheet, testResultBlock):
    rowcaptureDateTime = getVarRow(varName, sheet)
    captureDateTimeBlock = testResultBlock[varName]
    tempStr = captureDateTimeBlock[:4]
    sheet.testResult[rowcaptureDateTime + 1] = int(tempStr, 16)
    tempStr = captureDateTimeBlock[4:6]
    sheet.testResult[rowcaptureDateTime + 2] = int(tempStr, 16)
    tempStr = captureDateTimeBlock[6:8]
    sheet.testResult[rowcaptureDateTime + 3] = int(tempStr, 16)
    tempStr = captureDateTimeBlock[8:10]
    sheet.testResult[rowcaptureDateTime + 4] = int(tempStr, 16)
    tempStr = captureDateTimeBlock[10:12]
    sheet.testResult[rowcaptureDateTime + 5] = int(tempStr, 16)
    tempStr = captureDateTimeBlock[12:14]
    sheet.testResult[rowcaptureDateTime + 6] = int(tempStr, 16)
    tempStr = captureDateTimeBlock[14:]
    sheet.testResult[rowcaptureDateTime + 7] = int(tempStr, 16)

    
    
def getVarRow(varName, sheet):
    for i in range(len(sheet)):
        if varName == sheet.varName[i]:
            return i

def get_dict_allkeys(dict_a,special_value,random_function):
            if isinstance(dict_a,dict):
                for key, value in dict_a.items():
 #                   print(key, value)
                    if isinstance(value,str) and (value.startswith('$')) and value[1:len(value)] == special_value:
                        dict_a[key] = random_function
                    get_dict_allkeys(value,special_value,random_function)
            elif isinstance(dict_a,list):  
                for k in dict_a:
                    if isinstance(k,dict):
                        for key,value in k.items():
                            if (value.startswith('$')) and value[1:len(value)] == special_value:
                                k[key] = random_function
                            get_dict_allkeys(value, special_value, random_function)                    

def captureDateTime(sheet):

    index = getVarRow('year', sheet)
    year = checkBetween(index, 'year', sheet)

    index = getVarRow('month', sheet)    
    month = checkBetween(index, 'month', sheet)

    index = getVarRow('date', sheet)    
    date = checkBetween(index, 'date', sheet)

    index = getVarRow('hour', sheet)    
    hour = checkBetween(index, 'hour', sheet)

    index = getVarRow('minute', sheet)    
    minute = checkBetween(index, 'minute', sheet)

    index = getVarRow('second', sheet)    
    second = checkBetween(index, 'second', sheet)

    index = getVarRow('millisecond', sheet)    
    millisecond = checkBetween(index, 'millisecond', sheet)

    captureDateTime = '%04x%02x%02x%02x%02x%02x%04x'%(int(year), int(month), int(date), int(hour), int(minute),
                                  int(second), int(millisecond))

    captureDateTime = captureDateTime.encode('utf-8')
    return captureDateTime

def channelScaling(varName, sheet):
    index = getVarRow(varName, sheet)
    numScalling = sheet.testData[index+1]
#    print(index+1, numScalling)
    channelScalingValue = {}
    for i in range(int(numScalling)):
        sheet.varName[index+2+i]
        channelScalingValue.update({sheet.varName[index+2+i]:sheet.testData[index+2+i]})
    return channelScalingValue






def add_1(binary_inpute):#二进制编码加1
    _,out = bin(int(binary_inpute,2)+1).split("b")
    return out

def reverse(binary_inpute):#取反操作
    binary_inpute = list(binary_inpute)
    binary_out = binary_inpute
    for epoch,i in enumerate(binary_out):
        if i == "0":
            binary_out[epoch] = "1"
        else:
            binary_out[epoch] = "0"
    return "".join(binary_out)

"""
a = "00110"
if a[0] == "1":#判断为负数
    a_reverse = reverse(a[1:])  # 取反
    a_add_1 = add_1(a_reverse)  # 二进制加1
    a_int = -int(a_add_1, 2)
else:
    a_int = int(a[1:], 2)
print(a_int)
"""

def int2bin(n, count=24): # int-> 二进制 ，二进制按count取位
    assert -2**(count - 1) <= n < 2**(count - 1), "the %d is not in range [%d,%d)" % (n, -2**(count-1), 2**(count-1))
    return ''.join([str((n >> y) & 1) for y in range(count-1, -1, -1)])






def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--encode',  help='encode data and output to a file')
    parser.add_argument('-d','--decode',  help='decode data from a file and output to a file')
    parser.add_argument('-i','--input', help='read encoded data from a file')
    parser.add_argument('-o','--output', help='save encode/decode data to a file')
    parser.add_argument('-a','--asn', help='asn file pathname')
    parser.add_argument('-s','--xls', help='test data sheet file pathname')
    args = parser.parse_args()
#    print(args)
    if args.asn == None:
        print('please use -a or --asn to input asn file pathname')
        exit(0)
    if args.xls == None:
        print('please use -s or --xls to input data sheet excel file pathname')
        exit(0)
    else:
        xls_file = args.xls
        data_sheet = pd.read_excel(io=xls_file)
        data_sheet.columns = ['index', 'testRef', 'abstract', 'varName', 'needCheck', 'dataType', 'dataRange', 'testData', 'testResult', 'remarks']

    if args.encode:
        if args.encode in ('ber','per','xer'):
            codec = args.encode
        else:
            print('not suport, default is ber')
            codec = 'ber'
        
#        print('codec={0}'.format(codec))
        
        db = asn1tools.compile_files(args.asn, codec)
#        xls_file = '/home/data/asn1tests/test_sheet.xlsx'
        nameDict = varNameDict(varNameDefine, data_sheet)
        signBlock = signDynamicBlock(nameDict)
#        sign_dynamic_block = varCheckAndPack(data_sheet)
        print(signBlock)
        encoded_data = db.encode('SignDynamicBlock', signBlock)
        
         
        if args.output != None:
             with open(args.output, mode='wb') as f:
                 f.seek(0)
                 f.write(encoded_data)
        else:
             print(encoded_data)
     
    elif args.decode:
        if args.decode in ('ber','per','xer'):
            codec = args.decode
        else:
            print('not suport, codec is ber or xer!')
            exit(0)
        
        with open(args.input, mode='rb') as f:
            f.seek(0)
            sign_data_encode_read = f.read()
        
        db = asn1tools.compile_files(args.asn, codec)
        decoded_data = db.decode('SignDynamicBlock', sign_data_encode_read)

        if args.output == None:
            print('no output name, please use -o or --output to input!')
            exit(0)
            
        if args.xls == args.output:
            print('output file is same with -s or --xls name, please select another name!')
            exit(0)
            
            
        if args.xls != None:
            # write unpack data to xls testResult
           # print(decoded_data)
            testResultBlock = traverse_take_field(decoded_data,varNameDefine)
            print(testResultBlock)
           
            for key, value in testResultBlock.items():
                rowNumber = getVarRow(key, data_sheet)
#                print(key, row_i)
                if rowNumber != None and data_sheet.dataType[rowNumber] not in('DT','QR', 'CS') :
                        data_sheet.testResult[rowNumber] = value
            
            # unpack qualityRecord and write to testResult
            qualityBlock = testResultBlock['qualityRecord']
            qualityblock_temp = qualityBlock['qualityblock']
            number_qualityblocks = qualityBlock['numberofQualityblocks']
            row_number_qualityblocks = getVarRow('numberofQualityblocks', data_sheet)
            data_sheet.testResult[row_number_qualityblocks] = number_qualityblocks
            for i in range(number_qualityblocks):
                temp = 'qualityblock%d'%(i+1)
                quality_block = qualityblock_temp[i]
                row_i = getVarRow(temp, data_sheet)
                data_sheet.testResult[row_i+1] = quality_block['qualityScore']
                data_sheet.testResult[row_i+2] = quality_block['qualityalgorithmVendId']
                data_sheet.testResult[row_i+3] = quality_block['qualityalgorithmId']

            # unpack channelScaling an write to testResult
            channelScalingToTestResult('xchannelScaling', data_sheet, testResultBlock)
            channelScalingToTestResult('ychannelScaling', data_sheet, testResultBlock)
            channelScalingToTestResult('tchannelScaling', data_sheet, testResultBlock)
            channelScalingToTestResult('fchannelScaling', data_sheet, testResultBlock)
            
            # unpack captureDateTime
            
            captureDateTimeToTestResult('captureDateTime', data_sheet, testResultBlock)
            
            data_sheet_to_save = data_sheet.copy()
            data_sheet_to_save.columns = ['序号', '测试参考', '说明', '变量名参考', '数据检查', '数据类型','数据范围', '测试数据', '测试结果', '备注']
            data_sheet_to_save.to_excel(args.output)
       
    else:
        print('Error! Missing encode or decode argument')
    
if __name__ == '__main__':
    main(sys.argv[1:])

# Python--递归函数实现：多维嵌套字典数据无限遍历
# https://www.cnblogs.com/wangyanyan/p/11270063.html
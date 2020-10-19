#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 12:58:26 2020

@author: tjian
"""
from __future__ import print_function
import pprint
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
    'extendedData',
]





def traverse_take_field(data, fields, values={}, currentKey=None):
    """遍历嵌套字典列表，取出某些字段的值
    
    :param data: 嵌套字典列表
    :param fields: 列表，某些字段
    :param values: 返回的值
    :param currentKey: 当前的键值
    :return: 列表
    """
    if isinstance(data, list):
        for i in data:
            traverse_take_field(i, fields, values, currentKey)
    elif isinstance(data, dict):
        for key, value in data.items():
            #print(key, value)
            if key in fields:                
                data1 = {key:data[key]}
                print(data1)
                values.update(data1)
            traverse_take_field(value, fields, values, key)
    else:
        pass
    return values





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


def assertBetween(x, lo, hi, index):
    if not (lo <= x <= hi):
        raise AssertionError('index=%r, %r not between %r and %r' % (index, x, lo, hi))

def assertBetwennAndIn(x, lo, hi, con, index, flag=True):
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
        return testNum
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


def checkBetweenAndIn(index, varName, sheet):
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
                assertBetwennAndIn(int(testNum), 0, 0, numStr1, index+1, False)     
            else:
                numStr1 = temp.split(';',10)               
                numStr2 = numStr1[0].split('~',1)                
                numStr3 = numStr1[1:]              
                i = 0
                for tempStr in numStr3:
                    numStr3[i] = int(numStr3[i], 16)
                    i += 1

#                testNum = 254
                assertBetwennAndIn(int(testNum), int(numStr2[0], 16), int(numStr2[1], 16), numStr3, index+1)            
        return testNum
    else:
        assert False, 'index=%d：%s not correct！'%(index+1, sheet['varName'][index])

    
# unpack x,y,t, f channelScaling and write to testResult
def channelScalingToTestResult(varName, sheetName,testResult_block):
    row_channelScaling = getVarRow(varName, sheetName)
    channelScaling_block = testResult_block[varName]
    sheetName.testResult[row_channelScaling + 1] = channelScaling_block['exponent']
    sheetName.testResult[row_channelScaling + 2] = channelScaling_block['fraction']

def getVarRow(name, sheetName):
    for i in range(len(sheetName)):
        if name == sheetName.varName[i]:
            return i




# encode data block 
        
def varCheckAndPack(sheet):
    
# read test data from xlsx
    index = 0

    formatId = checkSingle(index, 'formatId', sheet)

    index += 1
    standardVersion = checkSingle(index, 'standardVersion', sheet)

    index += 1
    lengthofRecord = checkBetween(index, 'lengthofRecord', sheet)

    index += 1
    numberofRepresentations = checkBetween(index, 'numberofRepresentations', sheet)

    index += 1
    certificationFlag = checkBetween(index, 'certificationFlag', sheet)

    index += 1
    reprsentationLength = checkBetween(index, 'reprsentationLength', sheet)


    index += 1
    captureDateTime = checkSingle(index, 'captureDateTime', sheet)

    index += 1
    year = checkBetween(index, 'year', sheet)

    index += 1
    month = checkBetween(index, 'month', sheet)

    index += 1
    date = checkBetween(index, 'date', sheet)

    index += 1
    hour = checkBetween(index, 'hour', sheet)

    index += 1
    minute = checkBetween(index, 'minute', sheet)

    index += 1
    second = checkBetween(index, 'second', sheet)

    index += 1
    millisecond = checkBetween(index, 'millisecond', sheet)

    captureDateTime = '%04x%02x%02x%02x%02x%02x%04x'%(int(year), int(month), int(date), int(hour), int(minute),
                                  int(second), int(millisecond))

    captureDateTime = captureDateTime.encode('utf-8')
    #print(captureDateTime)

    index += 1
    captureDeviceTechId = checkBetweenAndIn(index, 'captureDeviceTechId', sheet)


    index += 1
    captureDeviceVendId = checkBetween(index, 'captureDeviceVendId', sheet)


    index += 1
    captureDeviceTypeId = checkBetween(index, 'captureDeviceTypeId', sheet)


    index += 1
    numberofQualityblocks = checkBetween(index, 'numberofQualityblocks', sheet)
#    print('numberofQualityblocks:%d'%numberofQualityblocks)

    qualityblock = []
    for i in range(numberofQualityblocks):
        qualityblockDict = {}

        index += 1
        blockName = sheet['varName'][index]
      #  print(blockName)

        index += 1
        qualityScore = checkBetweenAndIn(index, 'qualityScore', sheet)
        xx = {'qualityScore':qualityScore}
        qualityblockDict.update(xx)
     #   print(xx)


        index += 1
        qualityalgorithmVendId = checkBetween(index, 'qualityalgorithmVendId', sheet)  
        xx = {"qualityalgorithmVendId":qualityalgorithmVendId}
        qualityblockDict.update(xx)
    #    print(xx)



        index += 1
        qualityalgorithmId = checkBetween(index, 'qualityalgorithmId', sheet)  
        xx = {'qualityalgorithmId':qualityalgorithmId}
        qualityblockDict.update(xx)
        qualityblock.append(qualityblockDict)

    #    print(xx)

    #print(qualityblock)


    index += 1 # 30  # ---> real:31
    certificationRecord = checkSingle(index, 'certificationRecord', sheet)

    index += 1
    indexTemp = index

    index += 1
    exponent = checkBetween(index, 'exponent', sheet)
    index += 1
    fraction = checkBetween(index, 'fraction', sheet)

    xchannelScaling = checkSingle(indexTemp, 'xchannelScaling', sheet)
    xchannelScaling = {'exponent':exponent, 'fraction':fraction}

#    print(xchannelScaling)

    index += 1
    indexTemp = index

    index += 1
    exponent = checkBetween(index, 'exponent', sheet)
    index += 1
    fraction = checkBetween(index, 'fraction', sheet)

    ychannelScaling = checkSingle(indexTemp, 'ychannelScaling', sheet)
    ychannelScaling = {'exponent':exponent, 'fraction':fraction}

#    print(ychannelScaling)

    index += 1
    indexTemp = index

    index += 1
    exponent = checkBetween(index, 'exponent', sheet)
    index += 1
    fraction = checkBetween(index, 'fraction', sheet)

    tchannelScaling = checkSingle(indexTemp, 'tchannelScaling', sheet)
    tchannelScaling = {'exponent':exponent, 'fraction':fraction}

#    print(tchannelScaling)

    index += 1
    indexTemp = index

    index += 1
    exponent = checkBetween(index, 'exponent', sheet)
    index += 1
    fraction = checkBetween(index, 'fraction', sheet)

    fchannelScaling = checkSingle(indexTemp, 'fchannelScaling', sheet)
    fchannelScaling = {'exponent':exponent, 'fraction':fraction}

#    print(fchannelScaling)


    index += 1
    numberofDynamicEvents = checkBetween(index, 'numberofDynamicEvents', sheet)

    numberofDynamicEvents = int(numberofDynamicEvents)
    index += 1
    numberofAveragingSamples = checkBetween(index, 'numberofAveragingSamples', sheet)
    numberofAveragingSamples = int(numberofAveragingSamples)
#    print(numberofDynamicEvents, numberofAveragingSamples)


    index += 1
    xCoordinate = checkBetween(index, 'xCoordinate', sheet)

    index += 1
    yCoordinate = checkBetween(index, 'yCoordinate', sheet)

    index += 1
    fValue = checkBetween(index, 'fValue', sheet)

    index += 1
    timeValue = checkBetween(index, 'timeValue', sheet)

    index += 1
    typeofEvent = checkBetween(index, 'typeofEvent', sheet)

    index += 1
    totalTime  = checkBetween(index, 'totalTime', sheet)

    index += 1
    indexTemp = index


    index += 1
    meanX  = checkBetween(index, 'meanX', sheet)

    index += 1
    meanY  = checkBetween(index, 'meanY', sheet)

    index += 1
    meanF  = checkBetween(index, 'meanF', sheet)

    meanValues  = checkBetween(indexTemp, 'meanValues', sheet)
    meanValues = {'meanX':meanX, 'meanY':meanY, 'meanF':meanF}

    index += 1
    indexTemp = index

    index += 1
    sdX  = checkBetween(index, 'sdX', sheet)

    index += 1
    sdY  = checkBetween(index, 'sdY', sheet)

    index += 1
    sdF  = checkBetween(index, 'sdF', sheet)

    sdValues  = checkBetween(indexTemp, 'sdValues', sheet)
    sdValues = {'sdX':sdX, 'sdY':sdY, 'sdF':sdF}

    index += 1
    cCoefficient  = checkBetween(index, 'cCoefficient', sheet)

    index += 1
    extendedData  = checkSingle(index, 'extendedData', sheet)

    extendedData = extendedData.encode('utf-8')
# pack data
    block_header = {
        'formatId': formatId,
        'standardVersion': standardVersion, 
        'lengthofRecord': lengthofRecord,
        'numberofRepresentations': numberofRepresentations,
        'certificationFlag': certificationFlag
    }

    quality_block_values = {
            'numberofQualityblocks':numberofQualityblocks,
            'qualityblock': qualityblock}
    
    representation_header = {
        'reprsentationLength': reprsentationLength, 
        'captureDateTime': captureDateTime, 
        'captureDeviceTechId': captureDeviceTechId, 
        'captureDeviceVendId': captureDeviceVendId, 
        'captureDeviceTypeId': captureDeviceTypeId, 
        'qualityRecord': quality_block_values, 
        'certificationRecord': certificationRecord, 
        'xchannelScaling': xchannelScaling, 
        'ychannelScaling': ychannelScaling, 
        'tchannelScaling': tchannelScaling, 
        'fchannelScaling': fchannelScaling, 
        'numberofDynamicEvents': numberofDynamicEvents, 
        'numberofAveragingSamples': numberofAveragingSamples 
    }

    dynamic_event_data = {
        'xCoordinate': xCoordinate, 
        'yCoordinate': yCoordinate,
        'fValue': fValue, 
        'timeValue': timeValue, 
        'typeofEvent': typeofEvent  
    }

    overall_meanValues = meanValues
    
    standard_deviation = sdValues

    feature_data = {
        'totalTime': totalTime, 
        'meanValues': overall_meanValues, 
        'sdValues': standard_deviation, 
        'cCoefficient': cCoefficient 
    }

    representation_body = {
        'dynamicEventData': dynamic_event_data,
        'featureData': feature_data, 
        'extendedData': extendedData
    }
    
    block_body = {
        'representation': representation_header,
        'representationBody': representation_body
    }

    sign_dynamic_block = {
        'header':	 block_header,
        'body': block_body
    }

    representation_header['reprsentationLength'] = total_size(representation_header)
    block_header['lengthofRecord'] = total_size(sign_dynamic_block)


    return sign_dynamic_block



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
        data_sheet.columns = ['index', 'testRef', 'abstract', 'varName', 'needCheck', 'dataRange', 'testData', 'testResult', 'remarks']

    if args.encode:
        if args.encode == 'ber':
#            print('codec is ber')
            codec = args.encode
        elif args.encode == 'xer':
#            print('codec is xer')
            codec = args.encode
        else:
            print('not suport, default is ber')
            codec = 'ber'
        
#        print('codec={0}'.format(codec))
        
        db = asn1tools.compile_files(args.asn, codec)
#        xls_file = '/home/data/asn1tests/test_sheet.xlsx'

        sign_dynamic_block = varCheckAndPack(data_sheet)
        print(sign_dynamic_block)
        encoded_data = db.encode('SignDynamicBlock', sign_dynamic_block)
        
         
        if args.output != None:
             with open(args.output, mode='wb') as f:
                 f.seek(0)
                 f.write(encoded_data)
        else:
             print(encoded_data)
     
    elif args.decode:
        if args.decode == 'ber':
 #           print('codec is ber')
            codec = args.decode
        elif args.decode == 'xer':
 #           print('codec is xer!')
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
            testResult_block = traverse_take_field(decoded_data,varNameDefine)
            print(testResult_block)
           
            for key, value in testResult_block.items():
                row_i = getVarRow(key, data_sheet)
#                print(key, row_i)
                if row_i != None:
                    data_sheet.testResult[row_i] = value
            
            # unpack qualityRecord and write to testResult
            qualityBlock = testResult_block['qualityRecord']
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

                channelScalingToTestResult('xchannelScaling', data_sheet, testResult_block)
                channelScalingToTestResult('ychannelScaling', data_sheet, testResult_block)
                channelScalingToTestResult('tchannelScaling', data_sheet, testResult_block)
                channelScalingToTestResult('fchannelScaling', data_sheet, testResult_block)
                
                data_sheet_to_save = data_sheet.copy()
                data_sheet_to_save.columns = ['序号', '测试参考', '说明', '变量名参考', '数据检查', '数据范围', '测试数据', '测试结果', '备注']
                data_sheet_to_save.to_excel(args.output)
           
    else:
        print('Error! Missing encode or decode argument')
    
if __name__ == '__main__':
    main(sys.argv[1:])

# Python--递归函数实现：多维嵌套字典数据无限遍历
# https://www.cnblogs.com/wangyanyan/p/11270063.html
## SignDataTest

#### 本项目是对"ISO/IEC 19794-11"数据格式验证的python实现，目前可以使用BER(Basic Encoding Rules)、PER(Packed Encoding Rules)、XER(Xml Encoding Rules)编码规则对数据进行编码和解码。文件sign_data.asn依据"ISO/IEC 19794-11"编写，并修正了一些错误内容。

##### BER验证
  * 编码命令：./SignDataTest.py -a pathname/sign_data.asn -s pathname/test_sheet.xlsx -e ber -o pathname/testBer.txt </br>
用于读取test_sheet.xlsx的内容，使用BER进行编码，并将编码结果输出到testBer.txt中（因为是二进制文件看不到内容）</br>

  * 解码命令：./SignDataTest.py -a pathname/sign_data.asn -s pathname/test_sheet.xlsx -d ber -i pathname/testBer.txt -o pathname/testBerResult.xls</br>
用于读取testBer.txt中的编码结果，使用BER进行解码，并将解码结果输出到testBerResult.xls中，可以打开此文件比较测试数据和测试结果来验证编解码的正确性。</br>

##### PER验证
  * 编码命令：./SignDataTest.py -a pathname/sign_data.asn -s pathname/test_sheet.xlsx -e per -o pathname/testPer.txt</br>
用于读取test_sheet.xlsx的内容，使用PER进行编码，并将编码结果输出到testPer.txt中（因为是二进制文件看不到内容，但文件Size比BER小）</br>

  * 解码命令：./SignDataTest.py -a pathname/sign_data.asn -s pathname/test_sheet.xlsx -d per -i pathname/testPer.txt -o pathname/testPerResult.xls</br>
用于读取testPer.txt中的编码结果，使用PER进行解码，并将解码结果输出到testPerResult.xls中，可以打开此文件比较测试数据和测试结果来验证编解码的正确性。</br>


##### XER验证
  * 编码命令：./SignDataTest.py -a pathname/sign_data.asn -s pathname/test_sheet.xlsx -e xer -o pathname/testXer.txt</br>
用于读取test_sheet.xlsx的内容，使用XER进行编码，并将编码结果输出到testXer.txt中（文件内容是XML格式，可以看到内容）</br>

  * 解码命令：./SignDataTest.py -a pathname/sign_data.asn -s pathname/test_sheet.xlsx -d xer -i pathname/testXer.txt -o pathname/testXerResult.xls</br>
用于读取testXer.txt中的编码结果，使用XER进行解码，并将解码结果输出到testXerResult.xls中，可以打开此文件比较测试数据和测试结果来验证编解码的正确性。</br>

##### 帮助命令：./SignDataTest.py -h（or --help） </br>
usage: SignDataTest.py [-h] [-e ENCODE] [-d DECODE] [-i INPUT] [-o OUTPUT] [-a ASN] [-s XLS]

optional arguments: </br>
  -h, --help            show this help message and exit </br>
  -e ENCODE, --encode ENCODE     encode data and output to a file </br>
  -d DECODE, --decode DECODE     decode data from a file and output to a file</br>
  -i INPUT,  --input INPUT       read encoded data from a file</br>
  -o OUTPUT, --output OUTPUT     save encode/decode data to a file</br>
  -a ASN, --asn ASN     asn file pathname</br>
  -s XLS, --xls XLS     test data sheet file pathname</br>
 
 ## Layer1Test
 #### 针对test_sheet.xlsx中testdata进行layer 1 测试
 ./Layer1Test.py -s pathname/test_sheet.xlsx -t all
 ##### 帮助命令：./Layer1Test.py -h
 usage: Layer1Test.py [-h] [-s XLS] [-t TYPE]

 optional arguments:</br>
  -h, --help            show this help message and exit</br>
  -s XLS, --xls XLS     test data sheet file pathname</br>
  -t TYPE, --type TYPE  testing according to data type , -t [B,M,...] or -t [all] for B,M,MB,SS

 
 ## Layer2Test
 #### 针对test_sheet.xlsx中testdata进行layer 2 测试
 ./Layer2Test.py -s pathname/test_sheet.xlsx
 ##### 帮助命令：./Layer2Test.py -h
 usage: Layer2Test.py [-h] [-s XLS]

 optional arguments:</br>
  -h, --help         show this help message and exit</br>
  -s XLS, --xls XLS  test data sheet file pathname
 
 
## DataGen
 #### 针对test_sheet.xlsx产生testdata测试数据
 ./DataGen.py -s pathname/test_sheet.xlsx -o pathname/test_temp_data.xls -f formal
 ##### 帮助命令：./DataGen.py -h
 usage: DataGen.py [-h] [-s XLS] [-o OUTPUT] [-f FLAG]

 optional arguments:</br>
  -h, --help            show this help message and exit</br>
  -s XLS, --xls XLS     test data sheet file pathname</br>
  -o OUTPUT, --output OUTPUT
                        save encode/decode data to a file</br>
  -f FLAG, --flag FLAG  generator data rule, [formal] according to dataRange or [any] not caring
                        dataRange

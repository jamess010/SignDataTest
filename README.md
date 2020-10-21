## SignDataTest

#### 本项目用于对19794-11数据格式的验证,目前实现了BER，XER格式的编码和解码。


1）使用命令：./SignDataTest.py -a /home/data/asn1tests/sign_data.asn -s /home/data/asn1tests/test_sheet.xlsx -e ber -o /home/data/asn1tests/testBer.txt </br>
用于读取test_sheet.xlsx的内容，使用BER进行编码，并将编码结果输出到testBer.txt中（因为是二进制文件看不到内容）</br>

2）使用命令：./SignDataTest.py -a /home/data/asn1tests/sign_data.asn -s /home/data/asn1tests/test_sheet.xlsx -d ber -i /home/data/asn1tests/testBer.txt -o /home/data/asn1tests/testBerResult.xls</br>
用于读取testBer.txt中的编码结果，使用BER进行解码，并将解码结果输出到testBerResult.xls中，可以打开此文件比较测试数据和测试结果来验证编解码的正确性。</br>

3）使用命令：./SignDataTest.py -a /home/data/asn1tests/sign_data.asn -s /home/data/asn1tests/test_sheet.xlsx -e xer -o /home/data/asn1tests/testXer.txt</br>
用于读取test_sheet.xlsx的内容，使用XER进行编码，并将编码结果输出到testXer.txt中（文件内容是XML格式，可以看到内容）</br>

4）使用命令：./SignDataTest.py -a /home/data/asn1tests/sign_data.asn -s /home/data/asn1tests/test_sheet.xlsx -d xer -i /home/data/asn1tests/testXer.txt -o /home/data/asn1tests/testXerResult.xls</br>
用于读取testXer.txt中的编码结果，使用XER进行解码，并将解码结果输出到testXerResult.xls中，可以打开此文件比较测试数据和测试结果来验证编解码的正确性。</br>

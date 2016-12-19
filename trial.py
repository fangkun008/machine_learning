#coding:utf-8
#test stock info pulling
#2016-12-19
#Frank FANG


import urllib2
import sys

names = [  
#'详情', 
'名字',  
'代码',  
'当前价格',  
'昨收',  
'今开',  
'成交量（手）',  
'外盘',  
'内盘',  
'买一',  
'买一量（手）',  
'买二',  
'买二量（手）',  
'买三',  
'买三量（手）',  
'买四',  
'买四量（手）',  
'买五',  
'买五量（手）',  
'卖一',  
'卖一量',  
'卖二',  
'卖二量',  
'卖三',  
'卖三量',  
'卖四',  
'卖四量',  
'卖五',  
'卖五量',  
'最近逐笔成交',  
'时间',  
'涨跌',  
'涨跌%',  
'最高',  
'最低',  
'价格/成交量（手）/成交额',  
'成交量（手）',  
'成交额（万）',  
'换手率',  
'市盈率',  
'未知40',  
'最高',  
'最低',  
'振幅',  
'流通市值',  
'总市值',  
'市净率',  
'涨停价',  
'跌停价'  
]  
  
def getStockDetail(num):  
    print "股票代码: " + num  
    f = urllib2.urlopen('http://qt.gtimg.cn/q='+ str(num))  
    text = f.readline()   
    stmp=text[14:-3]  
    slist=stmp.split('~')
    if(len(slist) < len(names)):  
        print("[ERROR]return '%s' is not value"%text)  
        return  
  
    print('*******************************')  
    i = 0  
    for item in names:  
        if i == 28:  
            print item + ":"  
            details=slist[i].split('|')  
            for detail in details:  
                sb = detail.split('/')  
                if sb[3] == 'S':  
                    print sb[0] + " 卖出价 " + sb[1] + " 卖出额 " + sb[2]  
                else:  
                    print sb[0] + " 买入价 " + sb[1] + " 买入额 " + sb[2]  
        elif i == 0:
            type = sys.getfilesystemencoding()
            print item + ":" + slist[i].decode('GBK').encode(type)  
        else:  
            print item + ":" + slist[i]  
        i = i + 1  
    print('*******************************')  
  
if __name__ == '__main__':
    stock_num = sys.argv[1]
    getStockDetail(stock_num)
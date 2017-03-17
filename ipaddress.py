# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import json
import sys
reload(sys) 
sys.setdefaultencoding('gb18030') 
import xml.dom.minidom as Dom
#首先来创建一个xml文件
ip_addressname=[]#创建的存放省内名称的列表
#创建的是存放ip地址的列表
ipurl=[]
storeip=[]
#-------------查询ip地址--------
IpUrl ="http://ips.chacuo.net/"
user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64)'
headers={'User-Agent':user_agent}
try:
      req=urllib2.Request(IpUrl,headers=headers)
      response=urllib2.urlopen(req)
      content=response.read().decode('utf-8')
      my_get=r'<ul class="list">(.*?)</ul>'
      myitem=re.findall(my_get,content,re.S|re.M)
      i=0
      m=0
      for line in myitem:
            my_re=r'<li>(.*?)</li>'
            myitem1=re.findall(my_re,line,re.S|re.M)
            for line1 in myitem1:
                  if "a" in line1:
                        my_re1=r'<a .*?>(.*?)</a>'
                        myitem2=re.findall(my_re1,line1,re.S|re.M)
                        
                        #获取href中的url
                        my_url=r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
                        myitem3=re.findall(my_url,line1,re.I|re.S|re.M)
                        b2=json.dumps(myitem2,encoding="utf-8",ensure_ascii=False) 
                        b1=json.dumps(myitem3,encoding="utf-8",ensure_ascii=False)
                        string=','.join(myitem2)#把列表转换为字符串
                        stringURL=','.join(myitem3)#把列表中的url转换为字符串
                        ip_addressname.append(string)
                        ipurl.append(stringURL)
                        
                        
                  #else:
                        #print line1
      ad=json.dumps(ip_addressname,encoding="utf-8",ensure_ascii=False)
      ul=json.dumps(ipurl,encoding="utf-8",ensure_ascii=False)
      print ad
      print (u"从以上地址当中选择一个地址输入屏幕".decode('gb18030'))
      while True:
            ip_address=raw_input("please input address:").decode('gb18030')
            count=0
            for  i,inputname in enumerate(ip_addressname):
                  if ip_address==inputname:
                        req1=urllib2.Request(ipurl[count],headers=headers)
                        response1=urllib2.urlopen(req1)
                        content1=response1.read().decode('utf-8')
                        my_get1=r'<dd>(.*?)</dd>'
                        myitem4=re.findall(my_get1,content1,re.S|re.M)
                        for line2 in myitem4:
                              if "span" in line2:
                                    my_re2=r'<span .*?>(.*?)</span>'
                                    myitem5=re.findall(my_re2,line2,re.S|re.M)
                                    b=json.dumps(myitem5,encoding="utf-8",ensure_ascii=False)
                                    stringip='-'.join(myitem5)
                                    storeip.append(stringip)
                        n=0
                        length=len(storeip)
                        print  (u"你输入的地址共有%d个IP地址段如下显示并且保存到ip.xml文件中".decode('gb18030') % length)
                        storeip1=','.join(storeip)
                        print storeip1
                        
                        if __name__ == "__main__":
                              doc = Dom.Document()
                              root_node = doc.createElement("ip")#创建一个名为paquip的xml文件
                              doc.appendChild(root_node)
                              for i in range(0,length):            
                                    ip_author_node = doc.createElement("ip_range")
                                    for m in range(n,n+1):
                                          ip_author_value = doc.createTextNode(storeip[m])
                                          ip_author_node.appendChild(ip_author_value)  
                                    root_node.appendChild(ip_author_node)
                                    n+=1
                              f = open("ip.xml", "w")  
                              f.write(doc.toprettyxml(indent = "", newl = "\n", encoding = "utf-8"))  
                              f.close()
                  else:
                        count +=1
except urllib2.URLError,e:
      if hasattr(e,"code"):
            print e.code
      if hasattr(e,"reason"):
            print e.reason
            
      

# telnet-scanner 
telnet服务密码撞库  
本模块主要用于扫描在公网上开启telnet服务的设备(主要是物联网设备)  
并尝试进行密码对登录，将能登录IP和密码对，存入数据库中   

**安装方法**    
安装mysql、python2.7  
Python依赖库： pexpect, MySQLdb, 17monip, scapy  
将mysql数据库表mysql.sql导入数据库中  
 
**使用方法**  
将网卡设置为混杂模式：  
    Linux下命令： ifconfig eth0 promisc  
在ip.xml中配置要扫描的IP段
在scanner.py中的auth_table中配置登录密码对，如:    
("user","password",10)   user是用户名，password是密码，10是优先级 
 
**扫描结果**    
运行时截图:  
![image](https://github.com/scu-igroup/telnet-scanner/raw/master/images/result.png)  
数据库截图：  
![image](https://github.com/scu-igroup/telnet-scanner/raw/master/images/mysql_result.png)  

**启动方式**  
python scanner.py 20 #20为开的线程数  
# 用python 来爬取ip地址段
ipaddress.py是爬取网上的ip地址，并且将爬取的结果放到新创建的xml文件之中
在Python 自带的编辑器IDLE下编写
**使用的库**
程序用到的Python库有**urllib**，**urllib2**

在构造正则表达式的时候用到了**re**，**json** 模块

使用的xml.dom.minidom来创建xml文件

**运行的结果**

在命令行下运行显示：

![image](https://github.com/scu-igroup/telnet-scanner/blob/master/images/run_result.png)

结果保存在xml 文件中的截图：

![image](https://github.com/scu-igroup/telnet-scanner/blob/master/images/result_store.png)

**爬虫用的网址**

[爬虫爬取的网址](http://ips.chacuo.net/)



***
注：目前已在Centos6.5和Ubuntu14.04测试通过


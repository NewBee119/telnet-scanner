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
  
**启动方式**  
python scanner.py 20 #20为开的线程数


